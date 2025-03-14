# imports
import requests
import socket
import re
from colorama import Fore, Style

def extract_host(url):
    # Extract host from URL
    host = re.sub(r"^https?:\/\/", "", url)
    host = re.sub(r"\/?$", "", host)
    return host

def get_ip_address(host):
    # Get IP address for host
    return socket.gethostbyname("www.redsiege.com")

def check_strict_transport(headers, host):
    # Check 'Strict-Transport-Security' header exists in response
    if 'Strict-Transport-Security' in headers:
        print(Fore.GREEN + f"Strict-Transport-Security header was found for {host}")
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"Strict-Transport-Security header was not found for {host}")
        print(Style.RESET_ALL)

def check_content_security(headers, host):
    # Check 'Content-Security-Policy' header exists in response
    if 'Content-Security-Policy' in headers:
        print(Fore.GREEN + f"Content-Security-Policy header was found for {host}")
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"Content-Security-Policy header was not found for {host}")
        print(Style.RESET_ALL)

def check_frame_options(headers, host):
    # Check 'X-Frame-Options' header exists in response
    if 'X-Frame-Options' in headers:
        print(Fore.GREEN + f"X-Frame-Options header was found for {host}")
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"X-Frame-Options header was not found for {host}")
        print(Style.RESET_ALL)

def check_server(headers, host):
    # Check 'Server' header exists in response, return value
    if 'Server' in headers:
        print(Fore.GREEN + f"Server was found for {host}")
        print("Server Header Value:" + headers['Server'])
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"Server was not found for {host}")
        print(Style.RESET_ALL)

def check_headers(x):
    # get url from user
    url = x

    host = extract_host(url)
    print(f'IP of {host} is {get_ip_address(host)}')

    # Making a get request
    response = requests.get(url)

    # Check security headers
    check_strict_transport(response.headers, host)
    check_content_security(response.headers, host)
    check_frame_options(response.headers, host)
    check_server(response.headers, host)

def process_url_file(filename):
    with open(filename, 'r') as file:
        #Read each line in file
        for line in file:
            #Run get_data function on IP
            check_headers(line.strip())

# Main execution
if __name__ == "__main__":
    process_url_file('links.txt')