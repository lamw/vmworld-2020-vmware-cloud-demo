
$VCServer = "172.17.31.9"
$VCUsername = "administrator@vsphere.local"
$VCPassword = "VMware1!"

$HCXServer = "172.17.31.17"
$HCXUsername = "administrator@vsphere.local"
$HCXPassword = "VMware1!"

$MigrationType = "RAV"
$MobilityGroupName = "VMworld"
$MobilityTagName = "VMC"

$SrcNetworkName = "Test"
$DstNetworkName = "sddc-cgw-network-01"
$DstResourcePoolName = "Compute-ResourcePool"
$DstDatacenterName = "SDDC-Datacenter"
$DstFolderName = "Workloads"
$DstDatastoreName = "WorkloadDatastore"

Write-Host "Generating output ..."

Connect-VIServer -Server $VCServer -User $VCUsername -Password $VCPassword | Out-Null
Connect-HCXServer -Server $HCXServer -User $HCXUsername -Password $HCXPassword | Out-Null

$tagId = (Get-Tag $MobilityTagName).Id

$sourceSite = Get-HCXSite -Source
$targetSite = Get-HCXSite -Destination

$srcEndpointId = $sourceSite.EndpointId
$srcComputeResourceId = $sourceSite.Id
$srcEndpointName = $sourceSite.EndpointName
$srcRscName = $sourceSite.Name

$dstEndpointId = $targetSite.EndpointId
$dstComputeResourceId = $targetSite.Id
$dstEndpointName = $targetSite.EndpointName
$dstRscName = $targetSite.Name

$srcNetwork = (Get-VirtualNetwork $SrcNetworkName)
($srcNetworkType,$srcNetworkId) = $srcNetwork.Id -split ("-dvportgroup")
$dstNetwork = Get-HCXNetwork -Name $DstNetworkName -Site $targetSite

$dstNetworkType = "NsxtSegment"
$DstNetwork = Get-HCXNetwork -Type $dstNetworkType -Name $DstNetworkName -Site $targetSite
$dstNetworkId = $DstNetwork.Id

$dcId = (Get-HCXContainer -Type Datacenter -Site $targetSite -Name $DstDatacenterName).Id
$rpId = (Get-HCXContainer -Site $targetSite -Name $DstResourcePoolName -Type "ResourcePool").Id
$folderId = (Get-HCXContainer -Site $targetSite -Type Folder -Name $DstFolderName).Id
$datastoreId = (Get-HCXDatastore -Site $targetSite -Name $DstDatastoreName).Id

$output = @"
[vcenterConfig]
url = https://${VCServer}/rest
user = ${VCUsername}
password = ${VCPassword}

[hcxConfig]
url = https://${HCXServer}/hybridity/api
user = ${HCXUsername}
password = ${HCXPassword}

[migrationConfig]
mobilityGroupName = ${MobilityGroupName}
tagId = ${tagId}
migrationType = ${MigrationType}

srcEndpointId = ${srcEndpointId}
srcComputeResourceId = ${srcComputeResourceId}
srcEndpointName = ${srcEndpointName}
srcRscName = ${srcRscName}
srcResourceId = ${srcComputeResourceId}

dstEndpointId = ${dstEndpointId}
dstComputeResourceId = ${dstComputeResourceId}
dstEndpointName = ${dstEndpointName}
dstRscName = ${dstRscName}
dstResourceId = ${dstComputeResourceId}

srcNetworkName = ${SrcNetworkName}
srcNetworkValue = dvportgroup${srcNetworkId}
srcNetworkType = ${srcNetworkType}
dstNetworkName = ${DstNetworkName}
dstNetworkValue = ${dstNetworkId}
dstNetworkType =  ${DstNetworkType}

placementRpId = ${rpId}
placementRpName = ${DstResourcePoolName}
placementDcId = ${dcId}
placementDcName = ${DstDatacenterName}
placementFolderId = ${folderId}
placementFolderName = ${DstFolderName}
placementStorageId = ${datastoreId}
placementStorageName = ${DstDatastoreName}

"@

Write-Host "Storing output to config.txt, please copy this to etc directory"
$output | Out-File -FilePath "config.txt"

Disconnect-HCXServer * -Confirm:$false | Out-Null
