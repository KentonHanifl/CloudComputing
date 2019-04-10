#DiAggStorage
#Distributed Aggregated (Cloud) Storage

#.txt only demo version

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import os
import time #remove when proper download verification is done
import math


setup = input("new accounts? y/n")
        
dbx_access_tokens = []
num_accounts = 0

if setup.lower() == 'y':
    num_accounts = int(input("number accounts: "))
    app_key = open('app_key.txt').read()
    app_secret = open('app_secret.txt').read()

    for i in range(num_accounts):
        flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        url = flow.start()
        print("visit the following url: {0}".format(url))
        code = input('put the code here: ').strip()
        res = flow.finish(code)
        dbx_access_tokens.append(res.access_token)
        print("\nmake sure to sign out of the account you were just signed into\n\n")

    #save accounts
    accounts = open('accounts.txt','w')
    for token in dbx_access_tokens:
        accounts.write(token)
        accounts.write('\n')
    accounts.close()

    num_accounts = len(dbx_access_tokens)

else:
    accounts = open('accounts.txt','r').read().strip('\n').split('\n')
    for acc in accounts:
        dbx_access_tokens.append(acc)
    num_accounts = len(dbx_access_tokens)

print('loaded {0} accounts'.format(num_accounts))
##
##dbx1 = dropbox.Dropbox(dbx_access_tokens[0])
##dbx2 = dropbox.Dropbox(dbx_access_tokens[1])
dbxAccounts = []
for token in dbx_access_tokens:
    dbxAccounts.append(dropbox.Dropbox(token))

    
action = input("\n\nsee files\nupload\ndownload\nquit\n")
while 'upload' in action.lower() or 'download' in action.lower() or 'see files' in action.lower():

    if 'upload' in action.lower():
        filename = input('type upload file with extention (only .txt for now)')

        #read original file
        try:
            f = open(filename,'rb')
        except:
            print('file not found')
            action = input("\n\nsee files\nupload\ndownload\nquit\n")
            continue

        #read the file
        dat = f.read()
        f.close()
        l = len(dat)

        #identify the extention for later
        dot = filename.rfind(".")
        ext = filename[dot:]
        filename=filename[:dot]
        n = num_accounts

        #split the files
        for i in range(n):
            start = math.ceil((l/n)*i)
            end = math.ceil((l/n)*(i+1))
            f = dat[start:end]
            
            dbxAccounts[i].files_upload(f,'/'+filename+str(i)+ext)
##            os.remove(filename+str(i)+ext)
##            with open("out"+str(i),'wb') as out:
##                out.write(f)
##                out.close()
                #upload the split file then remove it
        #remove original file
        os.remove(filename+ext)

    elif 'download' in action.lower():
        filename = input('type download file')
        dot = filename.rfind(".")
        ext = filename[dot:]
        filename=filename[:dot]
        directory = os.getcwd()
        
        try:
            for i in range(num_accounts):
                dbxAccounts[i].files_download_to_file(directory+'/'+filename+str(i)+ext,'/'+filename+str(i)+ext)
        except:
            print('file not found')
            action = input("\n\nsee files\nupload\ndownload\nquit\n")
            continue

        re = bytes()
        n=num_accounts
        for i in range(n):
            with open(filename+str(i)+ext,'rb') as infile:
                re += infile.read()
                infile.close()
                os.remove(filename+str(i)+ext)

        with open(filename+ext,'wb') as outfile:
            outfile.write(re)
            outfile.close()
        
##        o1 = open(filename+'1.txt','rb')
##        o2 = open(filename+'2.txt','rb')
##        datOut = o1.read() + o2.read()
##        o1.close()
##        o2.close()
##        
##        #remove local split files
##        os.remove(filename+'1.txt')
##        os.remove(filename+'2.txt')
##
##        fullOut = open(filename+'.txt','wb')
##        fullOut.write(datOut)
##        fullOut.close()

        #we need to delete the dropbox file too
        for idx,account in enumerate(dbxAccounts):
            account.files_delete('/'+filename+str(idx)+ext)
##        dbx1.files_delete('/'+filename+'1.txt')
##        dbx2.files_delete('/'+filename+'2.txt')

        
    elif 'see files' in action.lower():
        for account in dbxAccounts:
            for entry in account.files_list_folder('').entries:
                print(entry.name)
            
    action = input("\n\nsee files\nupload\ndownload\nquit\n")

        
##      old stuff
##
##        f1 = dat[:l//2]
##        f2 = dat[l//2:]
##        k = open(filename+'1.txt','wb')
##        k.write(f1)
##        k2 = open(filename+'2.txt','wb')
##        k2.write(f2)
##
##        k.close()
##        k2.close()
##
##
##        #upload the split files
##
##        file1 = open(filename+'1.txt','rb').read()
##        file2 = open(filename+'2.txt','rb').read()
##
##        dbx1.files_upload(file1,'/'+filename+'1.txt')
##
##        dbx2.files_upload(file2,'/'+filename+'2.txt')
##
##        #we need to delete the local files too
##        os.remove(filename+'1.txt')
##        os.remove(filename+'2.txt')
##        os.remove(filename+'.txt')

    
##                dbx1.files_download_to_file(directory+'/'+filename+'1.txt','/'+filename+'1.txt')
##                dbx2.files_download_to_file(directory+'/'+filename+'2.txt','/'+filename+'2.txt')
