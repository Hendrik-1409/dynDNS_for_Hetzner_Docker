import logging.config
import requests
import time
import json
import logging

currentIP = '0.0.0.0'
zone = {}
rootRecord = {}
wwwRecord = {}

logging.config.fileConfig("logging.conf")

#create Logger
logger = logging.getLogger("HetznerDynDNS")

def loadConfig():
    configFile = open('config.json')
    config = json.load(configFile)
    global interval, apitoken, domain
    interval = config["interval"]
    apitoken = config["apitoken"]
    domain = config["domain"]

#gets Public IP and returns it as string
def getIP():
    try:
        response = requests.get('https://api.ipify.org').text
        print(response)
    except requests.exceptions.RequestException:
        pass #TODO: LOGGER
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
        pass #TODO: LOGGER

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
        pass #TODO: LOGGER

def preparePayload():
    getZoneID()
    getRecords()
    rootRecord["value"] = currentIP
    wwwRecord["value"] = currentIP

def runCheckup():
    global currentIP
    ip = getIP()
    if currentIP != ip:
        currentIP = ip
        preparePayload()
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
        pass #TODO: LOGGER

def main():
    loadConfig()
    while True:
        runCheckup()
        time.sleep(interval)

if __name__ == "__main__":
    main()
