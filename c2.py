# imports
import requests
from colorama import Fore, Style

# get url from user
url = input("Enter URL: ")

# Making a get request
response = requests.get(url)

# Check header exists in response
if 'Strict-Transport-Security' in response.headers:
    print(Fore.GREEN + f"Strict-Transport-Security header was found for {url}")
    print(Style.RESET_ALL)
else: 
    print(Fore.RED + f"Strict-Transport-Security header was not found for {url}")
    print(Style.RESET_ALL)

