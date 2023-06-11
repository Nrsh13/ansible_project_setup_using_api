import os, sys, json, urllib3, time, requests
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CredentialsHandler(object):

  def __init__ (self, url, credential, headers):
    self.url = url
    self.credential = credential
    self.headers = headers


  # GET
  def get_credential_id(url, name, headers):
    response = requests.get(url=url + '/api/v2/credentials/', verify=False, headers=headers)
    try:
      #response = requests.get(url=url + '/api/v2/credentials/', auth = HTTPBasicAuth('admin', 'password'), verify=False)
      response = requests.get(url=url + '/api/v2/credentials/', verify=False, headers=headers)
      if response.ok:
        data = response.json()
        for i in data['results']:
          if ( i['name'] == name ):
            credentialID = i['id']
            return credentialID
      else:
        print('ERROR: Get '+ name + ' Credential ID Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    except Exception as e:
      print('Exception Occured: ', str(e))
      sys.exit(1)
  

  # CREATE
  def create_credential(self):
    credential_exists = CredentialsHandler.get_credential_id(self.url, self.credential['name'], self.headers)
    if ( credential_exists is None ):
      response = requests.post(url=self.url + '/api/v2/credentials/', data = json.dumps(self.credential), verify=False, headers=self.headers)
      if response.ok:
        print('\nINFO: Create Credential Command Status is ' + str(response.status_code))
        credentialID = CredentialsHandler.get_credential_id(self.url, self.credential['name'], self.headers)
        print('INFO: Credential '+ str(self.credential["name"]) + ' ID is ' + str(credentialID))
      else:
        print('\nERROR: Create '+ str(self.credential["name"]) + ' Credential Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    else:
      credentialID = CredentialsHandler.get_credential_id(self.url, self.credential['name'], self.headers)
      print('INFO: Credential '+ str(self.credential["name"]) + ' Already Exists with Credential ID '+ str(credentialID))
      print ('INFO: Trying '+ str(self.credential["name"]) + ' Credential Update')
      CredentialsHandler.update_credential(self,credential_exists)
  

  # UPDATE
  def update_credential(self, credential_exists):
      response = requests.put(url=self.url + '/api/v2/credentials/' + str(credential_exists) + '/', data = json.dumps(self.credential), verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Updated '+ str(self.credential["name"]) + ' Credential Successfully\n')
      else:
        print('ERROR: Update '+ str(self.credential["name"]) + ' Credential Failed - ' + str(response.content) + '\n')
        sys.exit(1)
  

  # DELETE
  def delete_credential(self):
    credentialID = CredentialsHandler.get_credential_id(self.url, self.credential['name'], self.headers)
    if ( credentialID is None ):
      print('\nINFO: Credential ' + self.credential["name"] + ' Does not Exists')
    else:
      print('INFO: Deleting '+ self.credential['name'] + ' Credential ID '+ str(credentialID))
      response = requests.delete(url=self.url + '/api/v2/credentials/'+ str(credentialID) + '/', verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Deleted '+ self.credential['name'] + ' Credential Successfully\n')
      else:
        print('ERROR: Delete '+ self.credential['name'] + ' Credentials Failed - ' + str(response.content) + '\n')
        sys.exit(1)
  
