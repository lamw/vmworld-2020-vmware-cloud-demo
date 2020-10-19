import json
from flask import Flask, request, Response, jsonify
import datetime
import time
import configparser
from hcxapi import create_mobility_group, migrate_mobility_group

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("etc/config.txt")

mobilityGroupName = config.get("migrationConfig","mobilityGroupName")
tagId = config.get("migrationConfig","tagId")
migrationType = config.get("migrationConfig","migrationType")

srcEndpointId = config.get("migrationConfig","srcEndpointId")
srcComputeResourceId = config.get("migrationConfig","srcComputeResourceId")
srcEndpointName = config.get("migrationConfig","srcEndpointName")
srcRscName = config.get("migrationConfig","srcRscName")
srcResourceId = config.get("migrationConfig","srcResourceId")

dstEndpointId = config.get("migrationConfig","dstEndpointId")
dstComputeResourceId = config.get("migrationConfig","dstComputeResourceId")
dstEndpointName = config.get("migrationConfig","dstEndpointName")
dstRscName = config.get("migrationConfig","dstRscName")
dstResourceId = config.get("migrationConfig","dstResourceId")

srcNetworkName = config.get("migrationConfig","srcNetworkName")
srcNetworkValue = config.get("migrationConfig","srcNetworkValue")
srcNetworkType = config.get("migrationConfig","srcNetworkType")
dstNetworkName = config.get("migrationConfig","dstNetworkName")
dstNetworkValue = config.get("migrationConfig","dstNetworkValue")
dstNetworkType =  config.get("migrationConfig","dstNetworkType")

placementRpId = config.get("migrationConfig","placementRpId")
placementRpName = config.get("migrationConfig","placementRpName")
placementDcId = config.get("migrationConfig","placementDcId")
placementDcName = config.get("migrationConfig","placementDcName")
placementFolderId = config.get("migrationConfig","placementFolderId")
placementFolderName = config.get("migrationConfig","placementFolderName")
placementStorageId = config.get("migrationConfig","placementStorageId")
placementStorageName = config.get("migrationConfig","placementStorageName")

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

@app.route('/createmg', methods=['GET', 'POST'])
def createmg():
    startTime = datetime.datetime.now() + datetime.timedelta(days=1)
    endTime =  startTime + datetime.timedelta(days=1)

    r = create_mobility_group(tagId,mobilityGroupName,migrationType,
        srcEndpointId,srcComputeResourceId,srcEndpointName,srcResourceId,srcRscName,
        dstEndpointId,dstComputeResourceId,dstEndpointName,dstResourceId,dstRscName,
        placementRpId,placementRpName,placementDcId,placementDcName,placementFolderId,placementFolderName,placementStorageId,placementStorageName,
        srcNetworkName,srcNetworkValue,srcNetworkType,dstNetworkName,dstNetworkValue,dstNetworkType,
        startTime,endTime)

    '''
    payload = {
        "message": "Successfully created Mobility Group AVS {}".format(group)
    }
    '''
    payload = {
        "message": "Successfully created Mobility Group AVS"
    }

    return Response(json.dumps(payload), mimetype='application/json')

@app.route('/migratemg', methods=['GET', 'POST'])
def migratemg():
    response = migrate_mobility_group(mobilityGroupName)
    group = response[0]['name']

    payload = {
        "message": "Successfully started migration for Mobility Group {}".format(group)
    }

    return Response(json.dumps(payload), mimetype='application/json')

# run the app
if __name__ == '__main__':
    app.run(debug=True)
