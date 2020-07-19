import os,random
imgdir = './data/morph/'## dir for data 

alldata= [im+' '+im[-6:-4]+'\n' for im in os.listdir(imgdir) if ('.JPG' in im)]

num_data = len(alldata)

random.shuffle(alldata)

##file to write list
traintxt = 'train.txt'
testtxt = 'test.txt'
with open(traintxt,'w') as f:
    f.writelines(alldata[0:int(num_data*0.8)])
with open(testtxt,'w') as f:
    f.writelines(alldata[int(num_data*0.8)::])
