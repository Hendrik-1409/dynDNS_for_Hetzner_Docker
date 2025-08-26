import logging.config
import requests
import time
import json
import logging
import yaml

currentIP = '0.0.0.0'
zone = {}
rootRecord = {}
wwwRecord = {}

#load logging config
with open("logging.yaml", "r") as f:
    logging_config = yaml.load(f, Loader=yaml.FullLoader)
logging.config.dictConfig(logging_config)

#create Logger
logger = logging.getLogger("HetznerDynDNS")

def loadConfig():
    configFile = open('config.json')
    config = json.load(configFile)
    global interval, apitoken, domain
    interval = config["interval"]
    apitoken = config["apitoken"]
    domain = config["domain"]

def getIP():
    try:
        response = requests.get('https://api.ipify.org').text
        logging.debug("Public IP: " + response)
    except requests.exceptions.RequestException:
        logger.error("Failed to get public IP")
        return -1
    return response

#uses HetznerAPI to get all Zones, finds the correct one using the name and safes corresponding Zone and values in global Variables
def getZoneID():
    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/zones",
            headers={"Auth-API-Token": apitoken}
        )
        response = response.json()
        for x in response["zones"]:
            if x["name"] == domain:
                global zone
                zone = x
                break
    except requests.exceptions.RequestException:
        logger.error("Failed to get ZoneID")
        return -1
    return 0

def getRecords():
    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/records",
            params={"zone_id": zone["id"]},
            headers={"Auth-API-Token": apitoken}
        )
        #TODO: loopinterrupt after both Records have bin found
        response = response.json()
        for x in response["records"]:
            if x["type"] == "A":
                if x["name"] == "@":
                    global rootRecord
                    rootRecord = x
                if x["name"] == "www":
                    global wwwRecord
                    wwwRecord = x
    except requests.exceptions.RequestException:
        logger.error("Failed to get Records")
        return -1
    return 0

def preparePayload():
    getZoneIDStatus = getZoneID()
    if getZoneIDStatus == -1:
        return -1
    getRecordsStatus = getRecords()
    if getRecordsStatus == -1:
        return -1
    rootRecord["value"] = currentIP
    wwwRecord["value"] = currentIP

def runCheckup():
    global currentIP
    ip = getIP()
    if ip == -1:
        return
    if currentIP != ip:
        logger.info("IP changed from " + currentIP + " to " + ip)
        currentIP = ip
        preparePayloadStatus = preparePayload()
        if preparePayloadStatus == -1:
            return
        updateRecord()

def updateRecord():
    try:
        response = requests.put(
            url="https://dns.hetzner.com/api/v1/records/bulk",
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": apitoken,
            },
            data=json.dumps({
                "records" : [rootRecord, wwwRecord]
            })
        )
        #TODO: Analyze for failedRecords | LOGGER
    except requests.exceptions.RequestException:
        logger.error("Failed to update Record")

def main():
    logging.info("Starting Script...")
    try:
        loadConfig()
    except:
        logging.critical("Config could not be loaded!")
        exit()
    logging.info("Loaded Config...")
    while True:
        runCheckup()
        time.sleep(interval)

if __name__ == "__main__":
    main()
