import os, sys, json, urllib3, time, requests
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from credentialsHandler import CredentialsHandler
from projectHandler import ProjectHandler
from inventoryHandler import InventoryHandler

class JobTemplateHandler(object):

  def __init__ (self, url, job_template_data, inventory_data, project_data, credentials_list, headers):
    self.url = url
    self.job_template_data = job_template_data
    self.inventory_data = inventory_data
    self.project_data = project_data
    self.credentials_list = credentials_list
    self.headers = headers


  #GET
  def get_job_template_id(url, name, headers):
    try:
      response = requests.get(url=url + '/api/v2/job_templates/', verify=False, headers=headers)
      if response.ok:
        data = response.json()
        for i in data['results']:
          if ( i['name'] == name ):
            jobTemplateID = i['id']
            return jobTemplateID
      else:
        print('ERROR: Get '+ name + ' Job Tempalte ID Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    except Exception as e:
      print('Exception Occured: ', str(e))
      sys.exit(1)
  

  # CREATE
  def create_job_template(self):
    job_template_exists = JobTemplateHandler.get_job_template_id(self.url, self.job_template_data["name"], self.headers)
    if ( job_template_exists is None ):
      kafkaProjectID = ProjectHandler.get_project_id(self.url, self.project_data["name"],self.headers)
      self.job_template_data['project'] = kafkaProjectID
      kafkaInventoryID = InventoryHandler.get_inventory_id(self.url, self.inventory_data["name"], self.headers)
      self.job_template_data['inventory'] = kafkaInventoryID
      bitBucketCredID = CredentialsHandler.get_credential_id(self.url, "BitBucket-Secret", self.headers)
      self.job_template_data["credential"] = bitBucketCredID
      response = requests.post(url=self.url + '/api/v2/job_templates/', data = json.dumps(self.job_template_data), verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Create '+ str(self.job_template_data["name"]) + ' Job Template Command Status is ' + str(response.status_code))
        JobTemplateHandler.attach_credentials(self)
      else:
        print('ERROR: Create '+ str(self.job_template_data["name"]) + ' Job Template Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    else:
      jobTemplateID = JobTemplateHandler.get_job_template_id(self.url, self.job_template_data["name"], self.headers)
      print('INFO: Job '+ str(self.job_template_data["name"]) + ' Template Exists with ID '+ str(jobTemplateID))
      print ('INFO: Trying '+ str(self.job_template_data["name"]) + ' Job Template Update')
      JobTemplateHandler.update_job_template(self, jobTemplateID)
  
  # UPDATE
  def update_job_template(self, jobTemplateID):
      kafkaProjectID = ProjectHandler.get_project_id(self.url, self.project_data["name"],self.headers)
      self.job_template_data['project'] = kafkaProjectID
      kafkaInventoryID = InventoryHandler.get_inventory_id(self.url, self.inventory_data["name"], self.headers)
      self.job_template_data['inventory'] = kafkaInventoryID
      response = requests.put(url=self.url + '/api/v2/job_templates/' + str(jobTemplateID) + '/', data = json.dumps(self.job_template_data), verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Updated '+ str(self.job_template_data["name"]) + ' Job Template Successfully\n')
        JobTemplateHandler.attach_credentials(self)
      else:
        print('ERROR: Update '+ str(self.job_template_data["name"]) + ' Job Tempalte Failed - ' + str(response.content) + '\n')
        sys.exit(1)


  # ATTACH Creds TO JOB Tempalte
  def attach_credentials(self):
    for cred in self.credentials_list:
      data = {"associate": "true"}
      jobTemplateID = JobTemplateHandler.get_job_template_id(self.url, self.job_template_data['name'], self.headers)
      credID = CredentialsHandler.get_credential_id(self.url, cred,self.headers)
      data["id"] = credID
      response = requests.post(url=self.url + '/api/v2/job_templates/' + str(jobTemplateID) + '/credentials/', data = json.dumps(data), verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Credential '+ cred + ' ID ' + str(credID)  + ' Attached')
      else:
        print('INFO: Credential '+ cred + ' ID ' + str(credID)  + ' Already Attached')
    print('\n')
  

  # DELETE
  def delete_job_template(self):
    kafkaJobTemplateID = JobTemplateHandler.get_job_template_id(self.url, self.job_template_data['name'], self.headers)
    if ( kafkaJobTemplateID is None ):
      print('\nINFO: Job Template ' + self.job_template_data["name"] + ' Does not Exists\n')
    else:
      print('\nINFO: Deleting '+ self.job_template_data['name'] + ' Job Template ID - '+ str(kafkaJobTemplateID))
      response = requests.delete(url=self.url + '/api/v2/job_templates/'+ str(kafkaJobTemplateID) + '/', verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Deleted '+ self.job_template_data['name'] + ' Job Template Command Status is ' + str(response.reason) + '\n')
      else:
        print('ERROR: Delete '+ self.job_template_data['name'] + ' Job Template Failed - ' + str(response.content) + '\n')
        sys.exit(1)


