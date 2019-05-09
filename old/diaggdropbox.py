import os
import math

def uploadfiledbx(dbxAccounts, filename):
    num_accounts = len(dbxAccounts)
    
    #read original file
    try:
        with open(filename,'rb') as f:
            dat = f.read()
            f.close()
            l = len(dat)
    except:
        print('file not found')
        return -1

    #identify the extention for later
    dot = filename.rfind(".")
    ext = filename[dot:]
    filename=filename[:dot]

    #split the files
    for i in range(num_accounts):
        start = math.ceil((l/num_accounts)*i)
        end = math.ceil((l/num_accounts)*(i+1))
        f = dat[start:end]
        #upload the split "file"
        dbxAccounts[i].files_upload(f,'/'+filename+str(i)+ext)

    #remove original file
    os.remove(filename+ext)


    return 1
