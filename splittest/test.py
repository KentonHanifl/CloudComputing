import math

fname = input("file=")
f = open(fname,'rb')
dat = f.read()
f.close()
l = len(dat)

ext = fname[-3:]

n=int(input("n="))

for i in range(n):
    start = math.ceil((l/n)*i)
    end = math.ceil((l/n)*(i+1))
    f = dat[start:end]
    with open("out"+str(i),'wb') as out:
        out.write(f)
        out.close()

re = bytes()
for i in range(n):
    with open("out"+str(i),'rb') as infile:
        re += infile.read()
        infile.close()

with open("fullout."+ext,'wb') as outfile:
    outfile.write(re)
    outfile.close()
