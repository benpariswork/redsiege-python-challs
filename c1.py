# Imports libraries for http requests, json, and API key.
import requests
import ipaddress
import json
from keys import GEO_API_KEY

def print_data(x):
    ip = x
    # Sets API endpoint to reach out to.
    # Also adds the API key and user provided IP Addr.
    url = "https://api.ipgeolocation.io/ipgeo?apiKey=" + GEO_API_KEY + "&ip=" + str(ip)

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    json_txt = response.text

    data = json.loads(json_txt)

    ### Checks to make sure data made it to dictionary format.
    # x = type(data)
    # print(x)

    # Sets all necessary data to individual variables.
    country = data['country_name']
    state = data['state_prov']
    city = data['city']
    longitude = data['longitude']
    latitude = data['latitude']
    owner = data['organization']

    # Print results to user in a semi-presentable format.
    print(f"\nIP Address: {ip} \nCountry: {country} \nState/Province: {state} \nCity: {city} \nLongitude: {longitude} \nLatitude: {latitude} \nOwner: {owner}")

with open('addresses.txt', 'r') as file:
    # Read each line in file
    for line in file:
        if "/" in line:
            # Get all the addresses in the CIDR address space.
            netIpv4Address = ipaddress.ip_network(line.strip())
            # Run get_data on each IP for CIDR IP addr.
            for i in netIpv4Address:
                print_data(i)
        else:
            # Run print_data function for standard IP addr.
            print_data(line.strip())