import sys,json,urllib.request,uuid,getopt;

dns = input("Local DNS IPv4 Address: ")
local_gw = input("Local Gateway IPv4 Address: ")
mikrotik = input("Generate Mikrotik Address List? (Y/N): ")
route_t = input("Generate linux routing tables? (Y/N): ")

url = 'https://endpoints.office.com/endpoints/Worldwide?ClientRequestId='+str(uuid.uuid1())
print('Fetching endpoints....')
data = json.loads(urllib.request.urlopen(url).read())

urls = []
ips = []

print("Parsing....")

for endpoint in data:
	if endpoint['serviceArea'] != "Common":
		if 'urls' in endpoint:
			for url in endpoint['urls']:
				if url not in urls:
					if url[0:1] == '*':
						if url[1:] not in urls:
							urls.append(url[1:])
					else:
						urls.append(url)
		if 'ips' in endpoint:
			for ip in endpoint['ips']:
				if ip not in ips and '.' in ip:
					ips.append(ip)

print("Writing dnsmasq conf....")

with open('o365.conf','w') as f:
	for url in urls:
		f.write("\nserver=/"+url+"/"+dns)
if mikrotik.lower() == 'y':
	print("Writing mikrotik....")
	with open('o365_mikrotik.rsc','w') as f:
		for ip in ips:
			f.write("\n/ip firewall address-list add address=%s list=o365" % ip)
if route_t.lower() == 'y':
	print("Writing linux routing tables....")
	with open('route.sh', 'w') as f:
		for ip in ips:
			f.write("\nroute add "+ip+" gw "+local_gw)

print("o365.conf		-	dnsmasq conf file")
print("o365_mikrotik.rsc	-	mikrotik address list")
print("route.sh		-	route bash file")
print("Done.")

