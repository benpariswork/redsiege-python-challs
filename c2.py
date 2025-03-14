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

def print_header_status(header_name, headers, host, show_value=False):
    # Check if header exists and print status
    if header_name in headers:
        print(Fore.GREEN + f"{header_name} header was found for {host}")
        if show_value:
            print(f"{header_name} Header Value:" + headers[header_name])
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"{header_name} header was not found for {host}")
        print(Style.RESET_ALL)

def check_headers(x):
    # get url from user
    url = x

    host = extract_host(url)
    print(f'IP of {host} is {get_ip_address(host)}')

    # Making a get request
    response = requests.get(url)

    # Check security headers
    print_header_status('Strict-Transport-Security', response.headers, host)
    print_header_status('Content-Security-Policy', response.headers, host)
    print_header_status('X-Frame-Options', response.headers, host)
    print_header_status('Server', response.headers, host, show_value=True)

def process_url_file(filename):
    with open(filename, 'r') as file:
        #Read each line in file
        for line in file:
            #Run get_data function on IP
            check_headers(line.strip())

# Main execution
if __name__ == "__main__":
    process_url_file('links.txt')