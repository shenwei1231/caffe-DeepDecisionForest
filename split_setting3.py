import os,random
imgdir = './data/morph/' ## dir for data 

def splitbw(race,gender):
    b_w = [im+' '+im[-7:-5]+'\n' for im in os.listdir(imgdir) if ('.jpg' in im and race in im and gender in im)]
    b_w.sort()
    random.seed(1)
    random.shuffle(b_w)
    return b_w

other = [im+' '+im[-7:-5]+'\n' for im in os.listdir(imgdir) if ('.jpg' in im and 'B' not in im and 'W' not in im)]
s=[]
s2=[]
race = 'B'
gender = 'F'
b_f = splitbw(race, gender)
black_num = len(b_f)
s+=b_f[0:1285]
s2+=b_f[1285:1285*2]
other += b_f[1285*2::]

race = 'W'
gender = 'F'
w_f = splitbw(race, gender)
white_num = len(w_f)
s+=w_f[0:1285]
s2+=w_f[1285:1285*2]
other += w_f[1285*2::]

race = 'B'
gender = 'M'
b_m = splitbw(race, gender)
black_num += len(b_m)
s+=b_m[0:3980]
s2+=b_m[3980:3980*2]
other += b_m[3980*2::]

race = 'W'
gender = 'M'
w_m = splitbw(race, gender)
white_num = len(w_m)
s+=w_m[0:3980]
s2+=w_m[3980:3980*2]
other += w_m[3980*2::]

print black_num
print white_num

##file to write list
stxt = 'train1.txt'
s2txt = 'train2.txt'
other1txt = 'test1.txt'
other2txt = 'test2.txt'
with open(stxt,'w') as f:
    f.writelines(s)
with open(s2txt,'w') as f:
    f.writelines(s2)
with open(other1txt,'w') as f:
    f.writelines(s2+other)
with open(other2txt,'w') as f:
    f.writelines(s+other)
