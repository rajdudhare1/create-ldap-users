
import pandas as pd

class Excel():
    def __init__(self, fullPathToFile='SAMPLE.xlsx',sheet_name ='UserDetails'):
        self.file = fullPathToFile
        self.sheet_name = sheet_name
    
    def read_file(self):
        data = pd.read_excel(self.file,sheet_name=self.sheet_name)
        title = data['Title']
        fnames = data['FirstName']
        lnames = data['LastName']
        emails = data['Email']
        org = data['Organization']
        return title, fnames, lnames, emails, org

class CSV():
    def __init__(self, fullPathToFile='SAMPLE.csv'):
        self.file = fullPathToFile
    
    def read_file(self):
        data = pd.read_csv(self.file)
        title = data['Title']
        fnames = data['FirstName']
        lnames = data['LastName']
        emails = data['Email']
        org = data['Organization']
        return title, fnames, lnames, emails, org

