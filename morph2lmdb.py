import sys, argparse, scipy, lmdb, shutil, hashlib
from PIL import Image
from collections import OrderedDict
sys.path.append('caffe-ldl/python')
import caffe
import numpy as np
from random import shuffle
import scipy
import os, re
from os.path import join, splitext, split, abspath, isdir
parser = argparse.ArgumentParser(description='Convert Morph database to LMDB')
parser.add_argument('--data', type=str, help='Morph database directory', required=False, default='./data/morph/')
parser.add_argument('--ratio', type=float, help='Training set ratio', required=False, default=0.5)
parser.add_argument('--imsize', type=int, help='Image size', required=False, default=256)
parser.add_argument('--std', type=float, help='gaussian std', required=False, default=2)
parser.add_argument('--debug', type=bool, help='debug', required=False, default=False)
parser.add_argument('--traintxt', type=str, required=False, default='./train.txt')
parser.add_argument('--testtxt', type=str, required=False, default='./test.txt')
args = parser.parse_args()

if args.debug:
  import matplotlib.pyplot as plt
NUM_IDX_DIGITS = 10
IDX_FMT = '{:0>%d' % NUM_IDX_DIGITS + 'd}'

def is_image(im):
  return ('.jpg' in im) or ('.JPG' in im) or ('.PNG' in im) or ('.png' in im)

max_age = max([int(re.sub("[^0-9]", "", img)[-2::]) for img in os.listdir(args.data) if is_image(img)])
min_age = min([int(re.sub("[^0-9]", "", img)[-2::]) for img in os.listdir(args.data) if is_image(img)])
mean_age = np.mean(np.array([int(re.sub("[^0-9]", "", img)[-2::]) for img in os.listdir(args.data) if is_image('.JPG')], dtype=np.float))
gaussian = scipy.signal.gaussian(max_age - min_age + 1, args.std)
if (args.std == 0):
    gaussian = np.zeros([max_age - min_age + 1])
    gaussian[int(np.ceil((max_age - min_age + 1) / 2) - 1)] = 1

def make_label(label_value):
  label_value = label_value - min_age
  label_distr = np.zeros([(max_age - min_age + 1)])
  mid = int(np.ceil((max_age - min_age + 1) / 2) - 1)
  shift = int(label_value - mid)
  if shift > 0:
    label_distr[shift:] = gaussian[0:-shift]
  elif shift == 0:
    label_distr = gaussian
  else:
    label_distr[:shift] = gaussian[-shift:]
  label_distr = label_distr / np.sum(label_distr)
  if args.debug:
    print "Debug Info: age=%d"%(label_value+min_age)
    plt.plot(label_distr)
    plt.show()
  return label_distr

def make_lmdb(db_path, img_list, data_type='image'):
  if os.path.exists(db_path):
    # remove the old db files, I found the old db-files would cause some error
    shutil.rmtree(db_path)
  os.makedirs(db_path)
  db = lmdb.open(db_path, map_size=int(1e12))
  with db.begin(write=True) as in_txn:
    for idx, im in enumerate(img_list):
      if data_type == 'image':
        im = im.split()[0]
        data = np.array(Image.open(os.path.join(args.data, im)), dtype=np.float)
        data = scipy.misc.imresize(data, [args.imsize]*2)
        # data = data - 112
        data = data[:,:,::-1] # rgb to bgr
        data = data.transpose([2, 0, 1])
      elif data_type == 'age':
          #age = int(re.sub("[^0-9]", "", im)[-2::])
        age = int(im.split()[1])
        data = make_label(age).reshape([max_age - min_age + 1, 1, 1]).astype(np.float)
      data = caffe.io.array_to_datum(data)
      in_txn.put(IDX_FMT.format(idx), data.SerializeToString())
      if (idx+1) % 10 == 0:
        print "Serializing to %s, %d of %d, image size(%s x %s)"%(db_path, idx+1, len(img_list), args.imsize, args.imsize)
  db.close()

if __name__ == '__main__':
  with open(args.traintxt,'r') as f:
      train = f.readlines()
  assert(len(train) != 0)

  NTrain = len(train)
  from random import shuffle
  shuffle(train)
  base_dir = abspath(join('./MorphDB')) ## dir to save lmdb
  # convert training data
  db_path = abspath(join(base_dir, str(args.std), 'train-img'))
  make_lmdb(db_path, train, 'image')
  db_path = abspath(join(base_dir, str(args.std), 'train-age'))
  make_lmdb(db_path, train, 'age')
  ## converting testing data
  with open(args.testtxt,'r') as f:
      test = f.readlines()
  assert(len(test) != 0)
  NTest = len(test)
  shuffle(test)
  db_path = abspath(join(base_dir, str(args.std), 'test-img'))
  make_lmdb(db_path, test, 'image')
  db_path = abspath(join(base_dir, str(args.std), 'test-age'))
  make_lmdb(db_path, test, 'age')
  
  with open(abspath(join(base_dir, str(args.std), 'db.info')), 'w') as db_info:
    db_info.write("Morph dataset LMDB info: TrainSet ratio=%f \n"%(args.ratio))
    db_info.write("nTrain=%d, nTest=%d, minAge=%d, maxAge=%d, meanAge=%f"%(NTrain, NTest, min_age, max_age, mean_age))
  if not isdir("data"):
    os.makedirs("data")
  if not isdir("data/MorphDB_std"):
    os.symlink(base_dir, "data/MorphDB_std")
    print "Make data symbol link at 'data/MorphDB_std'."
  
