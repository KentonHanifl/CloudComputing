#DiAggStorage
#Distributed Aggregated (Cloud) Storage

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import os
import math
from diaggdropbox import *


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

dbxAccounts = []
for token in dbx_access_tokens:
    dbxAccounts.append(dropbox.Dropbox(token))

    
action = input("\n\nsee files\nupload\ndownload\nquit\n")
while 'upload' in action.lower() or 'download' in action.lower() or 'see files' in action.lower():

    if 'upload' in action.lower():
        filename = input('type upload file with extention (only .txt for now)')
        uploadfiledbx(dbxAccounts,filename)

    elif 'download' in action.lower():
        filename = input('type download file')
        
        #get the extention
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
        
        #download all of the split files and combine their binary data
        for i in range(num_accounts):
            with open(filename+str(i)+ext,'rb') as infile:
                re += infile.read()
                infile.close()
                #remove the file when we're done
                os.remove(filename+str(i)+ext)

        #write the full binary data to the output file
        with open(filename+ext,'wb') as outfile:
            outfile.write(re)
            outfile.close()

        #delete the dropbox files too
        for idx,account in enumerate(dbxAccounts):
            account.files_delete('/'+filename+str(idx)+ext)
        
    elif 'see files' in action.lower():

        fileset = set()
        for account in dbxAccounts:
            space = account.users_get_space_usage()
            used = space.used
            allocated = space.allocation.get_individual().allocated
            print("used {0:0.2f}% from account {1}".format((used/allocated)*100, account.users_get_current_account().email))
                  
            for entry in account.files_list_folder('').entries:
                entry = entry.name
                dot = entry.rfind(".")
                ext = entry[dot:]
                filename=entry[:dot-1]
                fileset.add(filename+ext)

        for file in fileset:
            print(file)
            
    action = input("\n\nsee files\nupload\ndownload\nquit\n")
