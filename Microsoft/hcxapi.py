import json
import requests
import configparser
from vsphereapi import get_all_vms,get_vms_from_tag
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable SSL warnings

config = configparser.ConfigParser()
config.read("etc/config.txt")
url = config.get("hcxConfig","url")
user = config.get("hcxConfig","user")
password = config.get("hcxConfig","password")
debug = False

def get_hcx_vms():
    vmUrl = '{}/vc/query?entityType=vm'.format(url)

    sid = auth_hcx(user,password)
    headers = {'x-hm-authorization':sid,'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.get(vmUrl,verify=False,headers=headers)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        print(resp.json())
        return

    vms = resp.json()
    results = {}
    for i in vms:
        if i['guest'].get('net'):
            results[i['entity_id']] = {
                "name": i['name'],
                "net": [
                    i['guest']['net']
                ]
            }

    return results

def create_mobility_group(tagId,mg_name,migrationType,
        srcEpId,srcComputeRscId,srcEpName,srcRscId,srcRscName,
        dstEpId,dstComputeRescId,dstEpName,dstRscId,dstRscName,
        placementRpId,placementRpName,placementDcId,placementDcName,placementFolderId,placementFolderName,placementStorageId,placementStorageName,
        srcNetworkName,srcNetworkValue,srcNetworkType,dstNetworkName,dstNetworkValue,dstNetworkType,
        startTime,endTime):

    item = {
        "name": mg_name,
        "groupDefaults": {
            "source": {
                "endpointId": srcEpId,
                "computeResourceId": srcComputeRscId,
                "endpointType": "VC",
                "endpointName": srcEpName,
                "resourceType": "VC",
                "resourceId": srcRscId,
                "resourceName": srcRscName
            },
            "destination": {
                "endpointId": dstEpId,
                "computeResourceId": dstComputeRescId,
                "endpointType": "VC",
                "endpointName": dstEpName,
                "resourceType": "VC",
                "resourceId": dstRscId,
                "resourceName": dstRscName
            },
            "transferParams": {
                "transferType": "vSphereReplication",
                "schedule": {},
                "transferProfile": [
                    {
                        "option": "removeSnapshots",
                        "value": False
                    },
                    {
                        "option": "removeISOs",
                        "value": False
                    }
                ]
            },
            "switchoverParams": {
                "schedule": {
                    "scheduledFailover": True,
                    "startYear": startTime.year,
                    "startMonth": startTime.month,
                    "startDay": startTime.day,
                    "endYear": endTime.year,
                    "endMonth": endTime.month,
                    "endDay": endTime.day
                },
                "options": {
                    "retainMac": False,
                    "forcePowerOffVm": False,
                    "upgradeHardware": False,
                    "upgradeVMTools": False,
                    "isEvcDisabled": False
                },
                "switchoverProfile": [
                    {
                        "option": "retainMac",
                        "value": True
                    },
                    {
                        "option": "forcePowerOffVm",
                        "value": False
                    },
                    {
                        "option": "upgradeHardware",
                        "value": False
                    },
                    {
                        "option": "upgradeVMTools",
                        "value": False
                    },
                    {
                        "option": "isEvcDisabled",
                        "value": False
                    }
                ]
            },
            "placement": [
                {
                    "id": placementRpId,
                    "name": placementRpName,
                    "type": "resourcePool"
                },
                {
                    "id": placementDcId,
                    "name": placementDcName,
                    "type": "dataCenter"
                },
                {
                    "id": placementFolderId,
                    "name": placementFolderName,
                    "type": "folder"
                }
                ],
            "storage": {
                "defaultStorage": {
                    "id": placementStorageId,
                    "type": "datastore",
                    "name": placementStorageName,
                    "diskProvisionType": "thin",
                    "storageParams": [
                        {
                            "option": "StorageProfile",
                            "value": "default"
                        }
                    ]
                }
            },
            "networkParams": {}
        }
    }

    allvms = get_hcx_vms()
    taggedvms = get_vms_from_tag(tagId)

    migrations = []
    for i in taggedvms:
        m = {
            "migrationType": migrationType,
            "entity": {
                "entityId": i,
                "entityType": "VirtualMachine",
                "entityName": allvms[i]['name'],
            },
            "networkParams": {
                "networkMappings": [
                    {
                        "macAddress": allvms[i]['net'][0][0]['macAddress'],
                        "srcNetworkName": srcNetworkName,
                        "srcNetworkDisplayName": srcNetworkName,
                        "srcNetworkValue": srcNetworkValue,
                        "srcNetworkId":  srcNetworkValue,
                        "srcNetworkType": srcNetworkType,
                        "destNetworkName": dstNetworkName,
                        "destNetworkDisplayName": dstNetworkName,
                        "destNetworkValue": dstNetworkValue,
                        "destNetworkId": dstNetworkValue,
                        "destNetworkType": dstNetworkType
                    }
                ]
            }
        }
        migrations.append(m)

    item["migrations"] = migrations
    data = {
        "items" : [
            item
        ]
    }

    mgUrl = '{}/mobility/groups'.format(url)

    if debug:
        print('POST to {}'.format(mgUrl))
        print('DATA {}'.format(json.dumps(data)))

    sid = auth_hcx(user,password)
    headers = {'x-hm-authorization':sid,'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.post(mgUrl,data=json.dumps(data),verify=False,headers=headers)
    if resp.status_code != 201 and resp.status_code != 202:
        print('Error! API responded with: {}'.format(resp.status_code))
        print(resp.json())
        return
    return resp.json()['items'][0]


def migrate_mobility_group(mobilityGroupName):
    mgQueryUrl = '{}/mobility/groups/query'.format(url)

    data = {
        "filters":  {
            "groups": [
                {
                    "name": mobilityGroupName
                }
            ]
        }
    }

    if debug:
        print('POST to {}'.format(mgQueryUrl))
        print('DATA {}'.format(json.dumps(data)))

    sid = auth_hcx(user,password)
    headers = {'x-hm-authorization':sid,'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.post(mgQueryUrl,data=json.dumps(data),verify=False,headers=headers)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        print(resp.json())
        return

    mgId = resp.json()['items'][0]['migrationGroupId']

    mgStartUrl = '{}/mobility/groups/start'.format(url)
    data = {
        "items" : [
            {
                "migrationGroupId": mgId
            }
        ]
    }

    if debug:
        print('POST to {}'.format(mgStartUrl))
        print('DATA {}'.format(json.dumps(data)))

    resp = requests.post(mgStartUrl,data=json.dumps(data),verify=False,headers=headers)
    if resp.status_code != 201 and resp.status_code != 202:
        print('Error! API responded with: {}'.format(resp.status_code))
        print(resp.json())
        return

    return resp.json()['items']

def auth_hcx(username,password):
    if debug:
        print('Authenticating to HCX Manager, user: {}'.format(username))
    data = {'username':username, 'password':password}
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.post('{}/sessions'.format(url),data=json.dumps(data),headers=headers,verify=False)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp.headers['x-hm-authorization']

def get_api_data(req_url):
    sid = auth_hcx(user,password)
    if debug:
        print('Requesting Page: {}'.format(req_url))
    headers = {'x-hm-authorization':sid,'Accept':'application/json','Content-Type':'application/json'}
    resp = requests.get(req_url,verify=False,headers=headers)
    if resp.status_code != 200:
        print('Error! API responded with: {}'.format(resp.status_code))
        return
    return resp
