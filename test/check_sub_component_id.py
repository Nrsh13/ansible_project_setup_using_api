import os, sys, json, requests, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_sub_component_id(sub_component, name, headers, url):
    response_status_code = 200
    status = 0
    try:
      response = requests.get(url=url + '/api/v2/'+ sub_component + '/', verify=False, headers=headers)
      if response.ok:
        data = response.json()
        for i in data['results']:
          if ( i['name'] == name ):
            sub_componentID = i['id']
            return sub_componentID
      else:
        print('ERROR: Get '+ name + ' ' + sub_component + ' ID Failed - ' + str(response.reason) + '\n')
        sys.exit()
    except Exception as e:
      print('Exception Occured: ', str(e))
      sys.exit()


