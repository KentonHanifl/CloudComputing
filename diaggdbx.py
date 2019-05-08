import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import os
import math
from diaggdropbox import *

class DropboxAccount:

    def __init__(self,account):
        self.accountType = "Dropbox"
        self.account = account

    def download(self,filename):
        directory = os.getcwd()
        self.account.files_download_to_file(directory+'/'+filename,'/'+filename)
        self.delete(filename)
        
    def upload(self,filename):
        with open(filename,'rb') as fb:
            f = fb.read()
            self.account.files_upload(f,'/'+filename)
            fb.close()
        os.remove(filename)

    def delete(self,filename):
        self.account.files_delete('/'+filename)   

    def seeFiles(self):
        space = self.account.users_get_space_usage()
        used = space.used
        allocated = space.allocation.get_individual().allocated
        #print("used {0:0.2f}% from account {1}".format((used/allocated)*100, self.account.users_get_current_account().email))

        files = []
        for entry in self.account.files_list_folder('').entries:
            files.append(entry.name)

        return files

     

    @staticmethod
    def getAccount(num):
        num = str(num)
        if os.path.exists('dropbox/token'+num+'.txt'):
            token = open('dropbox/token'+num+'.txt','r').read().strip('\n')
            return dropbox.Dropbox(token)
        else:
            app_key = open('dropbox/app_key.txt').read()
            app_secret = open('dropbox/app_secret.txt').read()
            flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
            url = flow.start()
            print("visit the following url: {0}".format(url))
            code = input('put the code here: ').strip()
            res = flow.finish(code)
            token = res.access_token
            print("\nmake sure to sign out of the account you were just signed into\n\n")

            account = open('dropbox/token'+num+'.txt','w')        
            account.write(token)
            account.close()
            return dropbox.Dropbox(token)     
