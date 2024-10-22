# Python Docker Container running a "DynDNS" update client to update Hetzner DNS Records

This Docker Container checks in a configured Intervall if the public IP-Adress of the local Network it is running in has changed. If this is the case multiple HTTP request are used to get the necessery Information on the www and @ record of the configured Domain. The domain configuartion API of the Hetzner Account that is correlated to the Domain needs to be reachable with the configured API Key.

## How to

## Current functionallity

## Planned features

## Dependencies

### Container
- alpine Linux Version 3.20
- python Version 3.13.0

### Python packages
- requests Version 2.32.3

## Know Issues
- Any Failure of an HTTP request to the Hetzner API might result in unpredicatble behavior
- Having more than one DNS Zone has not been test and therefore might result in unpredictable behavior
- No logging of events is present in this Version. Investigation of non expected behavior might be impossible

---
---

Note: This Repository is also personally used to learn advanced GitHub functionallity