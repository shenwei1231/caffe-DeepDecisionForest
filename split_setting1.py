import random

imglist='./morph_setting1.list'
with open(imglist,'r') as f:
    imgs = f.readlines()

num_data = len(imgs)

random.seed()
random.shuffle(imgs)
trainlist='./train.txt'
with open(trainlist,'w') as f:
    f.writelines(imgs[0:int(num_data*0.8)])

testlist='./test.txt'
with open(testlist,'w') as f:
    f.writelines(imgs[int(num_data*0.8)::])