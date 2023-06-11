import pytest

from .read_conf_property import read_conf_property
from .check_sub_component_id import check_sub_component_id

sub_component = read_conf_property()

@pytest.mark.parametrize("sub_component,name,headers,url",sub_component)
def test_sub_component(sub_component, name, headers, url):
    response_status_code = ''
    sub_component_exists = check_sub_component_id(sub_component, name, headers, url)
    if (sub_component_exists is None):
      print("\nINFO: " + sub_component + " " + name + "Does Not Exist")
      response_status_code = 400
    else:
      print("\nINFO: "  + sub_component + " "  + name + " Exist")
      response_status_code = 200
    assert response_status_code == 200
    print("INFO: " + sub_component + " " + name + " Tested!!")

