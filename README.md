## Ansible Project Setup using API

### Purpose

- To Set up Ansible Project, Inventory, Creds, Job Template using Ansible Tower API.

### What it does

- Reads the Configuration File conf/properties.json and conf/credentials.json.
- Fire API Call to AAP Tower to create Project, Inventory, Creds, Job Template etc.

### How to Run

- Execute the shell script ansible_project_setup_using_api/bin/trigger_main.sh

```
[~/Repositories/ansible_project_setup_using_api]$ sh bin/trigger_main.sh -h

This Program will read the conf/properties.json and conf/credentials.json, get the required details, use these details to setup Project/Job Tempalte/Credentials in Ansible Tower.

Usage:
cd ansible_project_setup_using_api
sh bin/trigger_main.sh create|delete [-h]

where:
    -h  show this help text

Example:
        sh ansible_project_setup_using_api/bin/trigger_main.sh create
```

OR

```
cd ansible_project_setup_using_api/src
python3.9 ansible_project_setup.py.org # Code is same (without using Classes)
```

### Automated Tests - pytest

```
python3.9 -m pip install pytest pytest-html
cd ansible_project_setup_using_api/test
pytest
```

### Contact
nrsh13@gmail.com
