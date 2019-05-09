from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import requests

class GDriveAccount:
    '''
    to create:
    call GDriveAccount(GDriveAccount.getAccount(X))
    where X is the number of whatever google drive account to be loaded
    '''
    
    
    def __init__(self,account,token,folderid):
            self.accountType = "GDrive"
            self.account = account
            self.token = token
            self.folderid = folderid
 
    def download(self,filename):
        res = self.seeFiles(ids=True)
        for item in res:
            if item['name'] == filename:
                fileid = item['id']
        headers = {"Authorization": "Bearer {0}".format(self.token)}
        r = requests.get(
            "https://www.googleapis.com/drive/v3/files/"+fileid+"?alt=media",
            headers=headers
        )
        data = r.content
        with open(filename,'wb') as out:
                out.write(data)
                out.close()

        self.account.files().delete(fileId=fileid).execute()


    def upload(self,filename):

        f = open(filename,"rb")
        lastSlash = filename.rfind('/')
        filename = filename[lastSlash+1:]
        headers = {"Authorization": "Bearer {0}".format(self.token)}
        para = {
            "name": filename,
            "parents": [self.folderid]
        }
        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': f
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )

        f.close()        
        
        os.remove(filename)

##    def delete(self,filename): #this is just called in download()
##        pass

    def seeFiles(self,ids=False):
        query = "'"+self.folderid+"' in parents"

        results = self.account.files().list(q=query,
                                        spaces='drive',
                                        fields='files(id, name, parents)').execute()
        items=results.get('files', [])
        if ids:
            return items
        
        items = [item['name'] for item in items]
        
        
        return items
####        old
##        results = self.account.files().list(
##            pageSize=100, fields="nextPageToken, files(id, name)").execute()
##        items=results.get('files', [])
##        if ids:
##            return items
##        
##        items = [item['name'] for item in items]
##        
##        
##        return items
##
    

    @staticmethod
    def getAccount(num):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        num = str(num)
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('gdrive/token'+num+'.pickle'):
            with open('gdrive/token'+num+'.pickle', 'rb') as token:
                creds = pickle.load(token)
            with open('gdrive/folderid'+num+'.txt','r') as fid:
                folderid = fid.read()
                fid.close()
            account = build('drive','v3',credentials=creds)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'gdrive/credentials.json', SCOPES)
                #creds = flow.run_console()
                creds = flow.run_local_server(host='localhost',
                                              port=8080,
                                              authorization_prompt_message='',
                                              success_message='The auth flow is complete; you may close this window.',
                                              open_browser=True)
                account = build('drive','v3',credentials=creds)
                file_metadata = {
                    'name': 'DiAgg',
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                file = account.files().create(body=file_metadata,
                                                    fields='id').execute()
                folderid = file.get('id')
            # Save the credentials for the next run
            with open('gdrive/token'+num+'.pickle', 'wb') as token:
                pickle.dump(creds, token)
            with open('gdrive/folderid'+num+'.txt','w') as fid:
                fid.write(folderid)
                fid.close()
            

        
        return (account,creds.token,folderid)
