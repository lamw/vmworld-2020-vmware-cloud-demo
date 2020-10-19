# import flask dependencies
import datetime
import time
import configparser
from hcxapi import create_mobility_group, migrate_mobility_group
from flask import Flask, request, make_response, jsonify

# initialize the flask app
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

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')

    if action == "create_mobility_group":
        startTime = datetime.datetime.now() + datetime.timedelta(days=1)
        endTime =  startTime + datetime.timedelta(days=1)

        response = create_mobility_group(tagId,mobilityGroupName,
            srcEndpointId,srcComputeResourceId,srcEndpointName,srcResourceId,srcRscName,
            dstEndpointId,dstComputeResourceId,dstEndpointName,dstResourceId,dstRscName,
            placementRpId,placementRpName,placementDcId,placementDcName,placementFolderId,placementFolderName,placementStorageId,placementStorageName,
            srcNetworkName,srcNetworkValue,srcNetworkType,dstNetworkName,dstNetworkValue,dstNetworkType,
            startTime,endTime)

        group = response[0]['name']
        msg = "Successfully created Mobility Group {}".format(group)

    if action == "migrate_mobility_group":
        response = migrate_mobility_group(mobilityGroupName)
        group = response[0]['name']

        msg = "Successfully started migration for Mobility Group {}".format(group)

    if msg == None:
        "Webhook called but no functions were executed"

    # return a fulfillment response
    return jsonify({'fulfillmentText': msg})

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(results())

# run the app
if __name__ == '__main__':
   app.run(debug=True)
