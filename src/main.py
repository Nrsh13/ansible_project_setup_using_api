import os, sys, json, urllib3, time, requests
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from credentialsHandler import CredentialsHandler
from projectHandler import ProjectHandler
from inventoryHandler import InventoryHandler
from jobTemplateHandler import JobTemplateHandler
from inventorySourceHandler import InventorySourceHandler


########## MAIN ##########

if __name__ == '__main__':

  # Check Arguments
  if len(sys.argv) != 2:
    print ('\nERROR: Need Argument Action (create or delete) - \n')
    print ('\tpython ' + sys.argv[0] + ' create|delete\n')
    sys.exit(1)
  else:
    if sys.argv[1] not in ["create", "delete"]:
      print ('\nERROR: Invalid Action - Use create or delete\n')
      print ('\tpython ' + sys.argv[0] + ' create|delete\n')
      sys.exit(1)

  action = sys.argv[1]

  ## Setting up Different Paths
  src_path = os.path.dirname(os.path.abspath(__file__)) # Your Scripts Parent Path
  project_path = os.path.dirname(src_path)
  conf_path = os.path.join(project_path, 'conf')
  cred_file = os.path.join(conf_path, 'credentials.json')
  property_file = os.path.join(conf_path, 'properties.json')

  # Credentials Setup
  print("\n--- Crednetials Setup\n")

  with open(cred_file, 'r') as c:
    data = json.load(c)
    aap_api_token = data['aap_api_token']
    url = data['ansible_tower_url']
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {aap_api_token}",
    }
    credentials_data = data['credentials']

    for credential in credentials_data:
      credObj = CredentialsHandler(url, credential, headers)
      if action.lower() == 'create':
        credObj.create_credential()
      else:
        credObj.delete_credential()
    c.close()


  # Project, Inventory and Job Tempalte Setup 
  with open(property_file, 'r') as f:
    data = json.load(f)
    components = list(data.keys())  # in properties.json - kafka, informatica, emr etc

    for component in components:
      sub_components = list(data[component].keys()) # Check if project_data, inventory_data etc exists)

      if action.lower() == 'create':

        print ('\n--- ' + component.upper() + ': Creating Project, Inventory and Job Template\n')

        # Project Actions
        #print ('\n## INFO: Project in Progress\n')
        if 'project_data'in sub_components:
          project_data = data[component]['project_data']
          projectObj = ProjectHandler(url, project_data, headers)
          projectObj.create_project()
          #create_project(project_data)
        else:
          print('\nINFO: No Project to Create for ' + component + '\n')

        # Inventory Actions
        #print ('\n## INFO: Inventory in Progress\n')
        if 'inventory_data'in sub_components:
          inventory_data = data[component]['inventory_data']
          inventoryObj = InventoryHandler(url, inventory_data, headers)
          inventoryObj.create_inventory()
        else:
          print('\nINFO: No Inventory  to Create for ' + component + '\n')

        # Inventory Source Actions
        #print ('\n## INFO: Inventory Source in Progress\n')
        if 'inventory_source_data'in sub_components:
          inventory_source_data = data[component]['inventory_source_data']
          inventorySourceObj = InventorySourceHandler(url, inventory_source_data, inventory_data, project_data, headers)
          #inventorySourceObj.create_inventory_source() # Does not have permissions
        else:
          print('\nINFO: No Inventory Source Data  to Create for ' + component + '\n')

        # Job Template Actions
        #print ('\n## INFO: Job Template in Progress\n')
        time.sleep(30) # Wait for Credentials/Project to be ready. Else BAD Request ERROR
        if 'job_template_data'in sub_components:
          job_template_data = data[component]['job_template_data']
          jobTemplateObj = JobTemplateHandler(url, job_template_data, inventory_data, project_data, ["Machine-Secret", "Vault-Secret"], headers)
          jobTemplateObj.create_job_template()
        else:
          print('\nINFO: No Job Template to Create for ' + component + '\n')


      else:
        print ('\n\n--- ' + component.upper() + ': Deleting Project, Inventory and Job Template\n')

        #print ('\n## INFO: Project in Progress\n')
        if 'project_data'in sub_components:
          project_data = data[component]['project_data']
          projectObj = ProjectHandler(url, project_data, headers)
          projectObj.delete_project()

        #print ('\n## INFO: Inventory in Progress\n')
        if 'inventory_data'in sub_components:
          inventory_data = data[component]['inventory_data']
          inventoryObj = InventoryHandler(url, inventory_data, headers)
          #inventoryObj.delete_inventory() # Does not have permissions

        #print ('\n## INFO: Job Template in Progress\n')
        if 'job_template_data'in sub_components:
          job_template_data = data[component]['job_template_data']
          jobTemplateObj = JobTemplateHandler(url, job_template_data, inventory_data, project_data, ["Machine-Secret", "Vault-Secret"], headers)
          jobTemplateObj.delete_job_template()

