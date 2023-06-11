import os, sys, json, urllib3, time, requests
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from credentialsHandler import CredentialsHandler

class ProjectHandler(object):

  def __init__ (self, url, project_data, headers):
    self.url = url
    self.project_data = project_data
    self.headers = headers

  
  # GET
  def get_project_id(url, name, headers):
    try:
      response = requests.get(url=url + '/api/v2/projects/', verify=False, headers=headers)
      #print(response.status_code) #Get status code 200
      if response.ok:
        data = response.json()
        for i in data['results']:
          if ( i['name'] == name ):
            ProjectID = i['id']
            return ProjectID
      else:
        print('ERROR: Get '+ name + ' Project ID Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    except Exception as e:
      print('Exception Occured: ', str(e))
      sys.exit(1)
  
  
  # CREATE
  def create_project(self):
    project_exists = ProjectHandler.get_project_id(self.url, self.project_data["name"], self.headers)
    # Bitbucket
    #project_data["scm_url"]  = "REPOURL"
    bitBucketCredID = CredentialsHandler.get_credential_id(self.url, "BitBucket-Secret", self.headers)
    self.project_data["credential"] = bitBucketCredID
    # Github
    #self.project_data["scm_url"]  = "REPOURL"
    #GitCredID = CredentialsHandler.get_credential_id(self.url, "Github-Secret", self.headers)
    #project_data["credential"] = GitCredID
  
    if ( project_exists is None ):
      response = requests.post(url=self.url + '/api/v2/projects/', data = json.dumps(self.project_data), verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Create '+ str(self.project_data["name"]) + ' Project Command Status ' +  str(response.status_code))
        kafkaProjectID = ProjectHandler.get_project_id(self.url, self.project_data["name"], self.headers)
        print('INFO: Project '+ str(self.project_data["name"]) + ' ID '+ str(kafkaProjectID) + '\n')
      else:
        print('ERROR: Create '+ str(self.project_data["name"]) + ' Project Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    else:
      kafkaProjectID = ProjectHandler.get_project_id(self.url, self.project_data["name"], self.headers)
      print('INFO: Project '+ str(self.project_data["name"]) + ' Already Exists with Project ID '+ str(kafkaProjectID))
      print ('INFO: Trying '+ str(self.project_data["name"]) + ' Project Update')
      ProjectHandler.update_project(self, project_exists)
  
  # UPDATE
  def update_project(self, project_exists):
      # BitBucket
      bitBucketCredID = CredentialsHandler.get_credential_id(self.url, "BitBucket-Secret", self.headers)
      self.project_data["credential"] = bitBucketCredID
      # Github
      #GitCredID = CredentialsHandler.get_credential_id(self.url, "Github-Secret", self.headers)
      #self.project_data["credential"] = GitCredID
      response = requests.put(url=self.url + '/api/v2/projects/' + str(project_exists) + '/', data = json.dumps(self.project_data), verify=False, headers=self.headers)
      #print(project_data)
      if response.ok:
        print ('INFO: Project '+ str(self.project_data["name"]) + ' Updated Successfully\n')
      else:
        print('ERROR: Update '+ str(self.project_data["name"]) + ' Project Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
  
  
  # DELETE
  def delete_project(self):
    kafkaProjectID = ProjectHandler.get_project_id(self.url, self.project_data["name"], self.headers)
    if ( kafkaProjectID is None ):
      print('\nINFO: Project ' + self.project_data["name"] + ' Does not Exists')
    else:
      print('INFO: Deleting '+ self.project_data['name'] + ' Project ID '+ str(kafkaProjectID))
      response = requests.delete(url=self.url + '/api/v2/projects/'+ str(kafkaProjectID) + '/', verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Deleted '+ self.project_data['name'] + ' Project Successfully')
      else:
        print('ERROR: Delete '+ self.project_data['name'] + ' Project Failed - ' + str(response.content) + '\n')
        sys.exit(1)
