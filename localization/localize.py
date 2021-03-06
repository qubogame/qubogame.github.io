import os
import json

from appdirs import user_data_dir

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from translations import Translations
from generator import Generator

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def getLocalDataDirectory ():
    '''Gets the path to the local data directory (i.e. Users/User/AppData/Local/Cronyx/qubo/website on Windows)'''
    return os.path.join(user_data_dir("qubo", "Cronyx"), "website")

def getTokenPath ():
    '''Returns the path to the token.json file for Google auth'''
    return os.path.join(getLocalDataDirectory(), "token.json")

def getSettings ():
    '''Gets the settings object stored in the settings.json file'''
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.json")
    with open(path, "r") as file:
        contents = file.read()
        return json.loads(contents)
    
def authorize ():
    '''Authorizes this application with Google auth and returns the built Google sheets service'''
    creds = None
    tokenPath = getTokenPath()
    if os.path.exists(tokenPath):
        creds = Credentials.from_authorized_user_file(tokenPath, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # No cached tokens, let the user select a credentials file.
            print("No cached credentials token could be found. Please select a credentials.json file.")

            Tk().withdraw()
            clientSecretPath = askopenfilename(initialdir = "/", title = "Select a credentials.json", filetypes = (("Credentials File","*.json"),))
            if not clientSecretPath:
                print ("No client secrets path was specified.")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                clientSecretPath, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Check that the credentials are valid
        if not creds.valid: return None

        # Save the credentials for the next run
        os.makedirs(os.path.dirname(tokenPath), exist_ok=True) # Ensure write directory exists
        with open(tokenPath, 'w+') as token:
            token.write(creds.to_json())
    
    return build('sheets', 'v4', credentials=creds).spreadsheets()

def main():
    settings = getSettings()
    print(settings)

    print("Authorizing application with Google auth...")
    service = authorize()
    if service is None:
        print("Failed to authorize application. Please try again.")
        return
    else: print("Authorized application.")

    translations = Translations(service, settings)
    generator = Generator(translations, settings)

    print ()
    print ()

    generator.generate()

if __name__ == "__main__":
    main()