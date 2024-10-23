# Python Docker Container running a "DynDNS" update client to update Hetzner DNS Records

This Docker Container checks in a configured Intervall if the public IP-Adress of the local Network it is running in has changed. If this is the case multiple HTTP request are used to get the necessery Information on the www and @ record of the configured Domain. The domain configuartion API of the Hetzner Account that is correlated to the Domain needs to be reachable with the configured API Key.

## How to

## Current functionallity

- Requesting current public IP-Adress using https://api.ipify.org and comparing it to a locally stored older Version in order to detect changes. The interval in seconds of the checkups is configurable in the config file.
- If changes are detected the script will get the Zone ID via the Hetzner API of the domain wich DNS records should be updated.
- The script will then modify the records that were requested in JSON format locally and update them via the Hetzner API

## Planned features
- Detailed logging of events to simplify investigation of unexpected behavior.
- Advanced error detection to prevent wrong updates of DNS Records
- Ability to update a flexible amount of records for more than one domain

## Dependencies

### Container
- alpine Linux Version 3.20
- python Version 3.13.0

### Python packages
- requests Version 2.32.3

## Know Issues
- Any Failure of an HTTP request to the Hetzner API might result in unpredicatble behavior
- Having more than one DNS Zone has not been test and therefore might result in unpredictable behavior
- No logging of events is present in this Version. Investigation of unexpected behavior might be impossible

---
---

Note: This Repository is also personally used to learn advanced GitHub functionallity