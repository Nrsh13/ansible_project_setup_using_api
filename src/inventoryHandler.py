import os, sys, json, urllib3, time, requests
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from credentialsHandler import CredentialsHandler

class InventoryHandler(object):

  def __init__ (self, url, inventory_data, headers):
    self.url = url
    self.inventory_data = inventory_data
    self.headers = headers


  ########### Inventory ##########
  # GET
  def get_inventory_id(url, name, headers):
    try:
      response = requests.get(url=url + '/api/v2/inventories/', verify=False,headers=headers)
      if response.ok:
        data = response.json()
        for i in data['results']:
          if ( i['name'] == name ):
            InventoryID = i['id']
            return InventoryID
      else:
        print('ERROR: Get '+ name + ' Inventory Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    except Exception as e:
      print('Exception Occured: ', str(e))
      sys.exit(1)
  
  
  # CREATE
  def create_inventory(self):
    inventory_exists = InventoryHandler.get_inventory_id(self.url, self.inventory_data["name"], self.headers)
    if ( inventory_exists is None ):
      response = requests.post(url=self.url + '/api/v2/inventories/', data = json.dumps(self.inventory_data), verify=False, headers=self.headers)
      if response.ok:
        print ('\nINFO: Create '+ str(self.inventory_data["name"]) + ' Inventory Command Status is ' + str(response.status_code))
        kafkaInventoryID = self.InventoryHandler.get_inventory_id(self.url, self.inventory_data["name"], self.headers)
        print('INFO: Inventory '+ str(self.inventory_data["name"]) + ' ID - '+ str(kafkaInventoryID))
      else:
        print('ERROR: Create '+ str(self.inventory_data["name"]) + ' Inventory Failed - ' + str(response.reason) + '\n')
        sys.exit(1)
    else:
      print('INFO: Inventory '+ str(self.inventory_data["name"]) + ' Already Exists')
      kafkaInventoryID = InventoryHandler.get_inventory_id(self.url, self.inventory_data["name"], self.headers)
      print('INFO: Existing '+ str(self.inventory_data["name"]) + ' Inventory ID is '+ str(kafkaInventoryID) + '\n')


  # UPDATE
  
  
  # DELETE
  def delete_inventory(self):
    kafkaInventoryID = InventoryHandler.get_inventory_id(self.url, self.inventory_data["name"], self.headers)
    if ( kafkaInventoryID is None ):
      print('\nINFO: Inventory ' + self.inventory_data["name"] + ' Does not Exists')
    else:
      print('INFO: Deleting Inventory ID '+ str(kafkaInventoryID))
      response = requests.delete(url=self.url + '/api/v2/inventories/'+ str(kafkaInventoryID) + '/', verify=False, headers=self.headers)
      if response.ok:
        print ('INFO: Deleted '+ self.inventory_data["name"] + ' Inventory Successfully\n')
      else:
        print('ERROR: Delete '+ self.inventory_data["name"] + ' Inventory Failed - ' + str(response.content) + '\n')
        sys.exit(1)  
