import requests
import time

#---------- config ----------#
# Fully Qualified Domain Name
# Can not neglect the 'dot' in the tail of the fqdn
fqdns = ['your.domain.', '*.your.domain.']
# username and token
username = "your username"
token = "your token"
auth = (username, token)
# domain
domain = "your registered domain"
#---------- end config ------#

new_ip = None
# Get New IP
print("----------Start at {}----------".format(time.strftime('%H:%M:%S',time.localtime())))
print("Step 1. Get New IP")
ip_url = "http://ip-api.com/json"
ip_result = requests.get(ip_url)
if requests.codes.ok == ip_result.status_code:
    ip_json = ip_result.json()
    new_ip = ip_json["query"]
    if new_ip != None and new_ip != "":
        print("New IP is {}".format(new_ip))
    else:
        print("Get new IP is failed!")

if new_ip != None and new_ip != "":
    # Get records
    print("Step 2. Get All Records")
    records_url = "https://api.name.com/v4/domains/{}/records".format(domain)
    records_result = requests.get(records_url, auth = auth)
    if records_result.status_code == requests.codes.ok:
        records_json = records_result.json()
        print(records_json)

        print("Step 3. Handle Records")
        for i in range(len(records_json["records"])):
            id     = records_json["records"][i]["id"]
            fqdn   = records_json["records"][i]["fqdn"]
            src_ip = records_json["records"][i]["answer"]
            type   = records_json["records"][i]["type"]
            print("---Handle fqdn:{}---".format(fqdn))
            if fqdn in fqdns and type == 'A':
                if src_ip == new_ip:
                    print("Nothing Changed!")
                else:
                    update_url = "https://api.name.com/v4/domains/{0}/records/{1}".format(domain, id)
                    update_result = requests.put(update_url, auth = auth, json = {"answer":new_ip, "ttl":300})
                    if update_result.status_code == requests.codes.ok:
                        print("fqdn:{} is updated successfully!".format(fqdn))
                    else:
                        print("fqdn:{} is failed to update!".format(fqdn))
                        print(update_result.json())
print("----------Finish at {}----------".format(time.strftime('%H:%M:%S',time.localtime())))
