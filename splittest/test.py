f = open("video.mp4",'rb')
dat = f.read()
f.close()
l = len(dat)
f1 = dat[:l//2]
f2 = dat[l//2:]
k = open("out1",'wb')
k.write(f1)
k2 = open("out2",'wb')
k2.write(f2)

k.close()
k2.close()

o1 = open("out1",'rb')
o2 = open("out2",'rb')
datOut = o1.read() + o2.read()
o1.close()
o2.close()

fullOut = open("test.mp4",'wb')
fullOut.write(datOut)
fullOut.close()
