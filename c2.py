# imports
import requests
import socket
import re
from colorama import Fore, Style
def check_headers(x):
    # get url from user
    url = x

    host = re.sub(r"^https?:\/\/", "", url)
    host = re.sub(r"\/?$", "", host)
    print(f'IP of {host} is {socket.gethostbyname("www.redsiege.com")}')

    # Making a get request
    response = requests.get(url)

    # Check header exists in response
    if 'Strict-Transport-Security' in response.headers:
        print(Fore.GREEN + f"Strict-Transport-Security header was found for {host}")
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"Strict-Transport-Security header was not found for {host}")
        print(Style.RESET_ALL)

with open('links.txt', 'r') as file:
    #Reade each line in file
    for line in file:
        #Run get_data fucntion on IP
        check_headers(line.strip())
