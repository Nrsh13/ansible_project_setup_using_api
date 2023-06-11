import os, sys, json, urllib3, time, requests
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from credentialsHandler import CredentialsHandler
from projectHandler import ProjectHandler
from inventoryHandler import InventoryHandler

class InventorySourceHandler(object):

  def __init__ (self, url, inventory_source_data, inventory_data, project_data, headers):
    self.url = url
    self.inventory_source_data = inventory_source_data
    self.inventory_data = inventory_data
    self.project_data = project_data	
    self.headers = headers


  # GET
  def get_inventory_source_id(url, name, headers):
    try:
      response = requests.get(url=url + '/api/v2/inventory_sources/', verify=False,headers=headers)
      if response.ok:
        data = response.json()
        #print (data)
        for i in data['results']:
          if ( i['name'] == name ):
            InventorySourceID = i['id']
            return InventorySourceID
      else:
        print('ERROR: Get '+ name + ' Inventory Source ID Failed - ' + srt(response.reason) + '\n')
        sys.exit(1)
    except Exception as e:
      print('Exception Occured: ', str(e))
      sys.exit(1)

  
  # CREATE
  def create_inventory_source(self):
    inventory_source_exists = InventorySourceHandler.get_inventory_source_id(self.url, self.inventory_source_data["name"], self.headers)
    if ( inventory_source_exists is None ):
      kafkaProjectID = ProjectHandler.get_project_id(self.url, self.project_data["name"],self.headers)	
      self.inventory_source_data['source_project'] = kafkaProjectID
      kafkaInventoryID = InventoryHandler.get_inventory_id(self.url, self.inventory_data["name"], self.headers)
      self.inventory_source_data['inventory'] = kafkaInventoryID
      response = requests.post(url=self.url + '/api/v2/inventory_sources/', data = json.dumps(self.inventory_source_data), verify=False, headers=self.headers )
      if response.ok:
        print ('INFO: Create '+ str(self.inventory_source_data["name"]) + ' Inventory Source Command Status is ' + str(response.status_code))
      else:
        print('ERROR: Create '+ str(self.inventory_source_data["name"]) + ' Inventory Source Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    else:
      kafkaInventorySourceID = get_inventory_source_id(self.url, self.inventory_source_data["name"], self.headers)
      print('INFO: Inventory '+ str(self.inventory_source_data["name"]) + ' Source Exists with ID '+ str(kafkaInventorySourceID))
      print ('INFO: Trying '+ str(self.inventory_source_data["name"]) + ' Inventory Source Update')
      InventorySourceHandler.update_inventory_source(self, inventory_source_exists)
	  
  
  # UPDATE
  def update_inventory_source(self, inventory_source_exists):
      kafkaProjectID = ProjectHandler.get_project_id(self.url, self.project_data["name"],self.headers)	
      inventory_source_data['source_project'] = kafkaProjectID
      kafkaInventoryID = InventoryHandler.get_inventory_id(self.url, self.inventory_data["name"], self.headers)
      inventory_source_data['inventory'] = kafkaInventoryID
      response = requests.put(url=self.url + '/api/v2/inventory_sources/' + str(inventory_source_exists) + '/', data = json.dumps(self.inventory_source_data), verify=False,headers=self.headers)
      if response.ok:
        print ('INFO: Updated '+ str(self.inventory_source_data["name"]) + ' Inventory Source Successfully\n')
      else:
        print('ERROR: Update '+ str(self.inventory_source_data["name"]) + ' Inventory Source Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
  
