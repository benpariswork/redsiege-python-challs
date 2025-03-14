# Red Siege Python Challenge 1

## Context
I have been using python to automate redundant tasks for a while now, but I usually have an LLM do its best to write my script then go from there. This no doubt has saved me time, it is really impressive what can be done with a little coding know-how halfway-decent AI. That being said, I have a couple python courses coming up and I am pretty sure I will not be able to use AI on the test. I want to get ahead and prepare by doing some python projects with zero help from AI.

I have been a big fan of Red Siege and their content for a while now, and found that they have a collection of python challenges in their discord server. I am going to use these to refresh my hands-on python skills.
## Scope
Project 1 - The Scope!

[Free IP Geolocation API and Accurate IP Geolocation Database](https://ipgeolocation.io/)

Scenario: Congrats, your Penetration testing company Red Planet has landed an external assessment for Microsoft! Your point of contact has give you a few IP addresses for you to test. Like with any test you should always verify the scope given to you to make sure there wasn't a mistake.

Beginner Task: Write a script that will have the user input an IP address. The script should output the ownership and geolocation of the IP. The output should be presented in a way that is clean and organized in order to be added to your report.

Intermediate Task:  Have the script read multiple IP addresses from a text file and process them all at once.

Expert Task: Have the script read from a file containing both single IP addresses and CIDR notation, having it process it both types.

Here are your IP addresses to check:
131.253.12.5
131.91.4.55
192.224.113.15
199.60.28.111

For the Expert Task here are two networks in CIDR notation:
20.128.0.0/16
208.76.44.0/22
## Beginner Task
- Get IP from User
- Return owner and Geo-location data
- Present data in a pretty way

The first thing I did was open up the link provided for the free API recommended for the challenge. I made my free account and immediately went to the docs. This company clearly puts a lot of work into their documentation, love to see it. Bad docs make me sad.

The first thing I needed to do was look up how to properly use an API key (LOL), and then grab a free one. After doing this I was ready to start working on the script. That being said, I was able to get a script that satisfied the first bullet point (above) pretty quickly. Most of the work was done in the snippet I found below.

### Snippet from [the API provider](https://ipgeolocation.io/ip-location-api.html#documentation-overview)
```python
import requests

url = "https://api.ipgeolocation.io/ipgeo?apiKey=API_KEY&ip=8.8.8.8"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```
### Version 1
```python
import requests
from keys import GEO_API_KEY

ip = input("What IP Address are you interested in?")

url = "https://api.ipgeolocation.io/ipgeo?apiKey=" + GEO_API_KEY + "&ip=" + ip

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```
This version would ask the user for an IP, call the API, and return JSON with all of the data like so... not so pretty.
```
What IP Address are you interested in?8.8.8.8
{"ip":"8.8.8.8","continent_code":"NA","continent_name":"North America","country_code2":"US","country_code3":"USA","country_name":"United States","country_name_official":"United States of America","country_capital":"Washington, D.C.","state_prov":"California","state_code":"US-CA","district":"Santa Clara","city":"Mountain View","zipcode":"94043-1351","latitude":"37.42240","longitude":"-122.08421","is_eu":false,"calling_code":"+1","country_tld":".us","languages":"en-US,es-US,haw,fr","country_flag":"https://ipgeolocation.io/static/flags/us_64.png","geoname_id":"6301403","isp":"Google LLC","connection_type":"","organization":"Google LLC","country_emoji":"\uD83C\uDDFA\uD83C\uDDF8","currency":{"code":"USD","name":"US Dollar","symbol":"$"},"time_zone":{"name":"America/Los_Angeles","offset":-8,"offset_with_dst":-8,"current_time":"2025-03-01 16:37:02.437-0800","current_time_unix":1740875822.437,"is_dst":false,"dst_savings":0,"dst_exists":true,"dst_start":{"utc_time":"2025-03-09 TIME 10","duration":"+1H","gap":true,"dateTimeAfter":"2025-03-09 TIME 03","dateTimeBefore":"2025-03-09 TIME 02","overlap":false},"dst_end":{"utc_time":"2025-11-02 TIME 09","duration":"-1H","gap":false,"dateTimeAfter":"2025-11-02 TIME 01","dateTimeBefore":"2025-11-02 TIME 02","overlap":true}}}
```
### Version 2
Next I needed to single out the requested data from the JSON response. I have not worked with JSON before so I went to google, not chatGPT. [This](https://reqbin.com/code/python/g4nr6w3u/python-parse-json-example) is what I found.
```python
data = json.loads(json_str)

customer = data['Customer']
order_1 = data['Orders'][0]['Id']
order_2 = data['Orders'][1]['Id']
total = len(data['Orders'])

print(f"Customer: {customer}, Orders: {order_1}, {order_2}, Total: {total}")
```
Assuming `json_str` is a string holding JSON data and JSON has been imported, this code showed me how to quickly transform JSON into a python dictionary. From there I quickly parsed out the country, state, city, coordinates, and IP owner. Here is the final script for the beginner level challenge as well as a screenshot showing the usage.
```python
# Imports libraries for http requests, json, and API key.
import requests
import json
from keys import GEO_API_KEY

# Gets IP Addr. from user.
ip = input("What IP Address are you interested in?   ")

# Sets API endpoint to reach out to.
# Also adds the API key and user provided IP Addr.
url = "https://api.ipgeolocation.io/ipgeo?apiKey=" + GEO_API_KEY + "&ip=" + ip

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
print(f"\nThe IP Address you are interested in is returning the following data.")
print(f"\nCountry: {country} \nState/Province: {state} \nCity: {city} \nLongitude: {longitude} \nLatitude: {latitude} \nOwner: {owner}")
```
## Intermediate Task
- Modify the script to read a text file list of addresses as input.
### Version 1
At first could not think of a good way to do this portion of the challenge. I felt like it was a good breaking point, so I went for a walk with my dog, Winnie. 

While walking the dog, I realized that the first thing I needed to do was turn the beginner script into a function that takes IP as input to make things more modular. I also needed to modify the output to include the IP. This is what I wound up with. Now the function `print_data` takes an IP Address as a string and prints the data, including IP.
##### Code
```python
# Imports libraries for http requests, json, and API key.
import requests
import json
from keys import GEO_API_KEY

def print_data(x):
    ip = x
    # Sets API endpoint to reach out to.
    # Also adds the API key and user provided IP Addr.
    url = "https://api.ipgeolocation.io/ipgeo?apiKey=" + GEO_API_KEY + "&ip=" + ip

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

print_data("8.8.8.8")
```
### Version 2
Adding a pretty basic for loop, I was able to quickly get the script to ask for an input file and iterate through IPs. It has been a while since I took intro to python so i google "python read file lines for loop" and found [this](https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/) source (snippet below) had exactly what I needed.
##### Snippet:
```python
# Open the file in read mode
with open('filename.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Print each line
        print(line.strip())
```
##### My new code:
```python
# Imports libraries for http requests, json, and API key.
import requests
import json
from keys import GEO_API_KEY

def print_data(x):
    ip = x
    # Sets API endpoint to reach out to.
    # Also adds the API key and user provided IP Addr.
    url = "https://api.ipgeolocation.io/ipgeo?apiKey=" + GEO_API_KEY + "&ip=" + ip

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
    #Read line in file
    for line in file:
        #Run get_data function on IP
        print_data(line.strip())
```
I made these changes, created the `addresses.txt` file with the addresses provided in the scope, then ran the script. I was pleasantly surprised to see it worked the first time.
## Expert Task
- All I have to do this time is make a CIDR notation a valid input.
I am not really sure how I would get the script to read CIDR notation properly, probably an if-statement that is longer than it needs to be. This is why python libraries were invented. The first result for my google search 'python cidr library' was [this](https://docs.python.org/3/library/ipaddress.html). I quickly realized I did not want to read the whole documentation, so I went back to my google search and found [this](https://www.tutorialspoint.com/how-to-generate-ip-addresses-from-a-cidr-address-using-python) snippet showing me how to read addresses from an address space in CIDR notation. Once I saw this, I was able to quickly jam a function into my code form the intermediate challenge. The only error I had was that I accidentally did `netIpv4Address = ipaddress.ip_network(line)` instead of `netIpv4Address = ipaddress.ip_network(line.strip())`. This caused the ipaddress library to throw a ValueError that took me a few minutes to figure out. After that, I had working code that would print the relevant data for all of the IP addresses, even provided CIDR notation.
### Code
```python
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
```
