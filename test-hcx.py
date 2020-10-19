#!/usr/bin/python3

import datetime
import time
import configparser
from hcxapi import create_mobility_group, migrate_mobility_group

debug = True

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

epoch = datetime.datetime.utcfromtimestamp(0)

startTime = datetime.datetime.now() + datetime.timedelta(days=1)
endTime =  startTime + datetime.timedelta(days=1)


response = create_mobility_group(tagId,mobilityGroupName,
        srcEndpointId,srcComputeResourceId,srcEndpointName,srcResourceId,srcRscName,
        dstEndpointId,dstComputeResourceId,dstEndpointName,dstResourceId,dstRscName,
        placementRpId,placementRpName,placementDcId,placementDcName,placementFolderId,placementFolderName,placementStorageId,placementStorageName,
        srcNetworkName,srcNetworkValue,srcNetworkType,dstNetworkName,dstNetworkValue,dstNetworkType,
        startTime,endTime)

print(response[0]['name'])

migrate_mobility_group(mobilityGroupName)
