import pytest
import os, sys, json, requests, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_conf_property():
  ## Setting up Different Paths
  src_path = os.path.dirname(os.path.abspath(__file__)) # Your Scripts Parent Path
  project_path = os.path.dirname(src_path)
  conf_path = os.path.join(project_path, 'conf')
  cred_file = os.path.join(conf_path, 'credentials.json')
  property_file = os.path.join(conf_path, 'properties.json')

  sub_component = [] # projects, credentials, job_templates, inventories etc

  # Fetch Headers and Credentials Names from credentials.json
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
      sub_component.append(('credentials',credential['name'], headers, url))

    c.close()


  # Fetch Project, Inventory and Job Tempalte from properties.json
  with open(property_file, 'r') as f:
    data = json.load(f)
    components = list(data.keys())  # in properties.json - kafka, informatica, emr etc

    for component in components:
      sub_components = list(data[component].keys()) # Check if project_data, inventory_data etc exists)

      print ('\n--- ' + component.upper() + ': Testing Project and Job Template\n')

      # Project Actions
      if 'project_data'in sub_components:
          project_data = data[component]['project_data']
          name = project_data['name']
          sub_component.append(('projects',name, headers, url))
      if 'job_template_data'in sub_components:
          job_template_data = data[component]['job_template_data']
          name = job_template_data['name']
          sub_component.append(('job_templates', name, headers, url))
      if 'inventory_data'in sub_components:
          inventory_data = data[component]['inventory_data']
          name = inventory_data['name']
          sub_component.append(('inventories', name, headers, url))

  return  sub_component

