from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import os

#these shouldn't be imported but have to be because of newDropbox()
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from diaggdbx import *

from AccountsHandler import *

class DiaggStorage:
    selected_file = 0
    files_num = 0

    waiting = "waiting..."
    downloading = "downloading..."
    uploading = "uploading..."
    done = "operation complete"
    fetching = "getting files..."

    dbxflow = None
    
    def __init__(self,root):
        #downloader/uploader handler
        self.handler = AccountsHandler()
        self.handler.loadAccounts()
        
        ###window setup
        root.title("DiAgg Storage")
        root.geometry("400x400")

        ###download button
        self.download_button = ttk.Button(root,
                                          text="Download",
                                          command=lambda: self.download())
        self.download_button.grid(row=0,column=1,padx=10,pady=10,sticky=W)

        ###upload button
        self.upload_button = ttk.Button(root,
                                          text="Upload",
                                          command=lambda: self.upload())
        self.upload_button.grid(row=0,column=0,padx=10,pady=10,sticky=W)
        
        ###file list
        #title of list
        file_list_label = Label(root, text="Files uploaded:")
        file_list_label.grid(row=1,column=0,padx=10,pady=10,sticky=W)

        #operation test (downloading... uploading... wating... done...ect)
        self.operation = Label(root,text = self.waiting)
        self.operation.grid(row=1,column=1,padx=10,pady=10,sticky=E)
        
        #actual list
        fileframe = Frame(root)
        fileframe.grid(row=2,column=0,columnspan=8,padx=10,pady=10,sticky=W+E)
        scrollbar = Scrollbar(fileframe,orient="vertical")
        scrollbar.pack(side="right", fill="y")        
        self.file_list = Listbox(fileframe,width=40,height=10,yscrollcommand=scrollbar.set)
        self.file_list.bind('<<ListboxSelect>>',self.select_file)
        self.file_list.pack(expand=True,side="left",fill="y")
        scrollbar.config(command=self.file_list.yview)
        self.get_files()
        self.operation['text'] = self.waiting

        ###menu
        menu = Menu(root)
        accountmenu = Menu(menu,tearoff=0)
        accountmenu.add_command(label="Add Dropbox Account", command=self.addDropbox)
        accountmenu.add_command(label="Add GoogleDrive Account", command=self.addGDrive)
        menu.add_cascade(label="Accounts",menu=accountmenu)
        root.config(menu=menu)
                



##        self.test_button = ttk.Button(root,text="test",command=lambda:self.list_test())
##        self.test_button.grid(row=0,column=2)

##    def list_test(self):
##        for i in range(30):
##            self.file_list.insert(i,"test"+str(i))

    def get_files(self):
        #delete all files in box
        self.operation['text'] = self.fetching
        self.file_list.delete(0,END)
        self.files_num = 0

        #put files in box
        try:
            files = self.handler.seeFiles() #change the function in AccountHandler
            for file in files:
                self.file_list.insert(self.files_num,file)
                self.files_num+=1
            self.operation['text'] = self.done
        except Exception as e:
            self.operation['text']=e
        
    def download(self):
        self.operation['text'] = self.downloading
        try:   
            self.handler.download(self.file_list.get(self.selected_file))
            self.get_files()
            self.operation['text'] = self.done

        except Exception as e:
            self.operation['text']=e

    def upload(self):
        try:
            self.operation['text'] = self.uploading
            initialD = os.getcwd()
            file = tkinter.filedialog.askopenfilename(parent=root,
                                                      initialdir=initialD)
            if file:
                self.handler.upload(file)
                self.operation['text'] = self.done
                self.get_files()
        except Exception as e:
            self.operation['text']=e

    def select_file(self,event=None):
        lb_widget = event.widget
        index = str(lb_widget.curselection()[0])
        self.selected_file = index

    def addDropbox(self):
        self.code_label = Label(root,text="enter dropbox code here:")
        self.code_label.grid(row=3,column=0)

        self.code_entry_val = StringVar(root,value="")
        self.code_entry = ttk.Entry(root,textvariable=self.code_entry_val)
        self.code_entry.grid(row=3,column=1)

        self.code_submit = ttk.Button(root,
                                 text="Submit Code",
                                 command=lambda: self.dropboxSubmit())
        self.code_submit.grid(row=3,column=2)

        self.dbxflow = self.handler.newDropbox()

    def dropboxSubmit(self):
        #this function needs to move to AccountsHandler.
        #it is doing things AccountsHandler should do.
        with open("userAccounts.txt",'r') as accs:
            rl=accs.readlines()
            num_dropboxaccounts = int(rl[0])
            num_gdriveaccounts = int(rl[1])
            accs.close()
            
        code = self.code_entry_val.get()
        self.code_label.grid_forget()
        self.code_entry.grid_forget()
        self.code_submit.grid_forget()
        
        flow = self.dbxflow
        res = flow.finish(code)
        token = res.access_token

        dbxaccount = dropbox.Dropbox(token)
        dbxaccount = DropboxAccount(dbxaccount)
        self.handler.accounts.append(dbxaccount)
        
        
        account = open('dropbox/token'+str(num_dropboxaccounts)+'.txt','w')        
        account.write(token)
        account.close()

        
        num_dropboxaccounts += 1
        with open("userAccounts.txt",'w') as accs:
            accs.write(str(num_dropboxaccounts)+'\n')
            accs.write(str(num_gdriveaccounts)+'\n')
            accs.close()


        self.get_files()
        self.dbxflow = None        

    def addGDrive(self):
        self.handler.newGDrive()
        self.get_files()

root = Tk()
diaggstorage = DiaggStorage(root)
root.mainloop()
