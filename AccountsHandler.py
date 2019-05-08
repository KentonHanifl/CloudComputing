from splitjoin import splitter,joiner
from diaggdbx import *
from diagggdrive import *

class AccountsHandler:
    
    def __init__(self,accounts=[]):
        self.accounts = accounts #list of accounts

    def newAccounts(self):
        num_dropboxaccounts = int(input("number of dropbox accounts: "))
        num_gdriveaccounts = int(input("number of gdrive accounts: "))
        with open("userAccounts.txt",'w') as accs:
            accs.write(str(num_dropboxaccounts)+'\n')
            accs.write(str(num_gdriveaccounts)+'\n')
            accs.close()

    def newDropbox(self):
        with open("userAccounts.txt",'r') as accs:
            rl=accs.readlines()
            num_dropboxaccounts = int(rl[0])
            num_gdriveaccounts = int(rl[1])
            accs.close()
            
        num_dropboxaccounts += 1
        account = DropboxAccount(DropboxAccount.getAccount(num_dropboxaccounts-1))
        self.accounts.append(account)
        
        with open("userAccounts.txt",'w') as accs:
            accs.write(str(num_dropboxaccounts)+'\n')
            accs.write(str(num_gdriveaccounts)+'\n')
            accs.close()

    def newGDrive(self):
        with open("userAccounts.txt",'r') as accs:
            rl=accs.readlines()
            num_dropboxaccounts = int(rl[0])
            num_gdriveaccounts = int(rl[1])
            accs.close()
            
        num_gdriveaccounts += 1
        temp = GDriveAccount.getAccount(num_gdriveaccounts)
        acc = temp[0]
        token = temp[1]
        folderid = temp[2]
        
        account = GDriveAccount(acc,token,folderid)
        self.accounts.append(account)
        
        with open("userAccounts.txt",'w') as accs:
            accs.write(str(num_dropboxaccounts)+'\n')
            accs.write(str(num_gdriveaccounts)+'\n')
            accs.close()

    def loadAccounts(self):
        with open("userAccounts.txt",'r') as accs:
            rl=accs.readlines()
            num_dropboxaccounts = int(rl[0].replace("\n",''))
            num_gdriveaccounts = int(rl[1].replace("\n",''))
            accs.close()

        for i in range(num_dropboxaccounts):
            account = DropboxAccount(DropboxAccount.getAccount(i))
            self.accounts.append(account)

        for i in range(num_gdriveaccounts):
            temp = GDriveAccount.getAccount(i)
            acc = temp[0]
            token = temp[1]
            folderid = temp[2]
            
            account = GDriveAccount(acc,token,folderid)
            self.accounts.append(account)
        

    def upload(self,filename):
        splitfiles = splitter(filename,len(self.accounts))

        for part,account in enumerate(self.accounts):
            account.upload(splitfiles[part])

    def download(self,filename):
        originalfilename = filename
        dot = filename.rfind(".")
        ext = filename[dot:]
        filename=filename[:dot-1]
        
        for account in self.accounts:
            files = account.seeFiles()
            for file in files:
                if filename in file:
                    f = file
            try:
                account.download(f)
                #account.delete(f)
            except Exception as e:
                print("file not found in one account")

        joiner(originalfilename)

    def seeFiles(self):
        fileset = set()
        for account in self.accounts:
            
            files = account.seeFiles()
            for file in files:
                
                dot = file.rfind(".")
                if dot > 0: #don't append directories
                    ext = file[dot:]
                    filename=file[:dot]
                    
                    if filename[-1].isdigit() and ext.replace('.','').isalpha():
                        filename = filename[:-1] #remove part number
                        fileset.add(filename+ext)
                        
                    else:
                        pass
                        #fileset.add("NOT SPLIT "+file)

        for element in fileset:
            print(element)



##num_gdrive = int(input("number of gdrive accounts: "))
##num_dropbox = int(input("number of dropbox accounts: "))
##
##accs = []
##
##for i in range(3):
##    accs.append(DropboxAccount(DropboxAccount.getAccount(i)))
##


handler = AccountsHandler()

handler.loadAccounts()
