import requests
import configparser
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

config = configparser.ConfigParser()
config.read("etc/config.txt")
url = config.get("vcenterConfig","url")
user = config.get("vcenterConfig","user")
password = config.get("vcenterConfig","password")
debug=False

def get_vcenter_health_status():
    health = get_api_data('{}/appliance/health/system'.format(url))
    j = health.json()
    return '{}'.format(j['value'])

def get_all_vms():
    vmarry = {}
    for i in get_api_data('{}/vcenter/vm'.format(url)).json()['value']:
        vmarry[i['vm']]= i['name']
    return vmarry

def get_vms_from_tag(tagId):
    tagUrl = ('{}/com/vmware/cis/tagging/tag-association/id:'+tagId).format(url)+'?~action=list-attached-objects'

    sid = auth_vcenter(user,password)
    if debug:
        print('POST to {}'.format(tagUrl))
    headers = {'vmware-api-session-id':sid}
    resp = requests.post(tagUrl,verify=False,headers=headers)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return

    vmarry = []
    for i in resp.json()['value']:
        vmarry.append(i['id'])

    return vmarry

def auth_vcenter(username,password):
    if debug:
        print('Authenticating to vCenter, user: {}'.format(username))
    resp = requests.post('{}/com/vmware/cis/session'.format(url),auth=(user,password),verify=False)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp.json()['value']

def get_api_data(req_url):
    sid = auth_vcenter(user,password)
    if debug:
        print('Requesting Page: {}'.format(req_url))
    resp = requests.get(req_url,verify=False,headers={'vmware-api-session-id':sid})
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp