# __init__.py - Starting of our application

from flask import Flask
from flask_ask import Ask, statement, question
from vsphereapi import get_all_vms, get_vms_from_tag
from hcxapi import create_mobility_group, migrate_mobility_group
import os
import subprocess
from threading import Thread
from subprocess import check_output
from subprocess import Popen, PIPE
import datetime
import time
import configparser

app = Flask(__name__)
ask = Ask(app, "/vmc_demo")

VMTENV = os.environ.copy()

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

def execute(cmd, ofile=subprocess.PIPE, efile=subprocess.PIPE,
            env=os.environ):
    proc = subprocess.Popen(cmd, stdout=ofile, stderr=efile, env=env)
    out, err = proc.communicate()

    if type(out).__name__ == "bytes":
        out = out.decode()


@app.route('/')
def homepage():
    return "VMware Cloud on AWS 2020 Demo"

@ask.launch
def start_skill():
    welcome_message = 'VMware Cloud on AWS 2020 Demo is online'
    return question(welcome_message)

@ask.intent("CreateMobilityGroupIntent")
def create_hcx_mg():
    startTime = datetime.datetime.now() + datetime.timedelta(days=1)
    endTime =  startTime + datetime.timedelta(days=1)

    response = create_mobility_group(tagId,mobilityGroupName,migrationType,
            srcEndpointId,srcComputeResourceId,srcEndpointName,srcResourceId,srcRscName,
            dstEndpointId,dstComputeResourceId,dstEndpointName,dstResourceId,dstRscName,
            placementRpId,placementRpName,placementDcId,placementDcName,placementFolderId,placementFolderName,placementStorageId,placementStorageName,
            srcNetworkName,srcNetworkValue,srcNetworkType,dstNetworkName,dstNetworkValue,dstNetworkType,
            startTime,endTime)

    group = response[0]['name']

    hcx_msg = "Successfully created Mobility Group {}".format(group)

    return question(hcx_msg)

@ask.intent("MigrateMobilityGroupIntent")
def migrate_hcx_mg():
    response = migrate_mobility_group(mobilityGroupName)
    group = response[0]['name']

    hcx_msg = "Successfully started migration for Mobility Group {}".format(group)

    return question(hcx_msg)

@ask.intent("GoodbyeIntent")
def goodby():
    msg = "Goodbye"

    return question(msg)


if __name__ == '__main__':
    app.run(debug=True)
