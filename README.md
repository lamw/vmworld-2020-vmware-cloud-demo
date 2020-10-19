# VMworld 2020 Demo - Voice activated workload migration to VMware Cloud SDDCs

For more information, please see this blog post [https://www.virtuallyghetto.com/2020/10/vmworld-2020-demo-voice-activated-workload-migration-to-vmware-cloud-sddcs.html](https://www.virtuallyghetto.com/2020/10/vmworld-2020-demo-voice-activated-workload-migration-to-vmware-cloud-sddcs.html)

![](https://i0.wp.com/www.virtuallyghetto.com/wp-content/uploads/2020/09/vmworld-vmware-cloud-demo.png?w=1404&ssl=1)

## Requirements

* Sign up for one of the Public Cloud Voice Assistance Service
    * AWS - https://developer.amazon.com/alexa/console
    * Microsoft - https://azure.microsoft.com/en-us/try/cognitive-services/
    * Google - https://console.cloud.google.com/freetrial
* Access to VMware Cloud SDDC
    * VMware Cloud on AWS - https://cloud.vmware.com/vmc-aws/get-started
    * Azure VMware Solution - https://portal.azure.com/
    * Google Cloud VMware Engine - https://console.cloud.google.com/gve
* VMware HCX deployed and configured
* Photon OS VMware deployed within the SDDC used for Python Flask App (see Setup section below for more details)

## Setup

Each Cloud Provider has its own directory where `__init__.py` is the main Flask Application. Within each directory, there is etc folder which needs `config.txt` that contains the configuration of your SDDC setup including credentials to both on-premises vCenter Server and HCX that has already been paired with your SDDC. Examples of what the data looks like is included in the repo.

```
.
├── AWS
│   ├── __init__.py
│   ├── etc
│   │   └── config.txt
│   ├── hcxapi.py
│   └── vsphereapi.py
├── Google
│   ├── __init__.py
│   ├── etc
│   │   └── config.txt
│   ├── hcxapi.py
│   └── vsphereapi.py
├── Microsoft
│   ├── __init__.py
│   ├── etc
│   │   └── config.txt
│   ├── hcxapi.py
│   └── vsphereapi.py
├── generate-sddc-config.ps1
└── test-hcx.py
```

The `config.txt` can be auto-generated using the `generate-sddc-config.ps1` PowerCLI script. Simply update the variables with your own environment details and run the script. There is also `test-hcx.py` script which can be used to verify HCX Mobility Group creation and migration is successful prior to using voice assistance.

Install the following packages on your Photon OS VM
```
apt update
apt install
apt install -y net-tools
apt install -y python3-pip
snap install powershell --classic
snap install ngrok
pip3 install flask
```

Generate `config.txt` using `generate-sddc-config.ps1` Script:
```
.\generate-sddc-config.ps1
```

Test HCX Mobility Group / Migration using `test-hcx.py` which will read `etc/config.txt`
```
python ./test-hcx.py
```

Once you have verified connectivity and HCX functionality. You can setup the respective voice assistance services. The following resources are helpful to get started. 

* [https://www.virtuallyghetto.com/2017/06/introducing-alexa-to-a-few-more-vmware-apis.html](https://www.virtuallyghetto.com/2017/06/introducing-alexa-to-a-few-more-vmware-apis.html)
* [https://developer.amazon.com/en-US/docs/alexa/custom-skills/steps-to-build-a-custom-skill.html](https://developer.amazon.com/en-US/docs/alexa/custom-skills/steps-to-build-a-custom-skill.html)
* [https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-custom-commands-use-custom-voice](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-custom-commands-use-custom-voice)
* [https://www.pragnakalp.com/dialogflow-fulfillment-webhook-tutorial/](https://www.pragnakalp.com/dialogflow-fulfillment-webhook-tutorial/)

As part of the setup, you will need to provide the generated ngrok HTTPS URL which you will find in the the command below to start.

Start ngrok listening on port 5000 (default Flask port):
```
ngrok http 5000
```

Start Flask app:
```
❯ python __init__.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 122-751-074
```

## Known Issue

* During the development, I noticed with the Azure Cognitive Services that a single voice request would actually trigger duplicated Flask endpoint calls. I was never able to get to the bottom of this issue and had [filed the following bug](74/seeing-duplicate-requests-to-flask-endpoint.html). To workaround the issue, I would only process the first response.