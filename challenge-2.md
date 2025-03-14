## Scope
Project 2 - Web Header Reporting 

Scenario: Red Planet has assigned you to do a web app penetration test against a few target domains. There are a few findings that your team regularly report on, but aren't very fun to detect or write up. As such, you are looking to automate this portion of your test so that you can spend more time going for something more critical. 

Beginner Task: Write a script that will have the user input a HTTPS URL. The script should pull down the web headers for the URL entered and report back if the Strict-Transport-Security header is missing. 

Intermediate Task: Have the script run multiple URLs from a file and process them all at once. Additionally, have it output both the URL and the IP address of each URL missing the Strict-Transport-Security header. 

Expert: Have the code perform all of the tasks above while also checking for the Content-Security-Policy and X-Frame-Options header, also reporting back if they are missing. It should also detect if a Server header is present, if it is it should return the value of the header. 

Bonus: Have the script evaluate if the URL is HTTP or HTTPS. If it is HTTP, it should ignore the need for a Strict-Transport-Security header while still evaluating all the others. URLs to start with: 
- [https://www.redsiege.com/](https://www.redsiege.com/ "https://www.redsiege.com/") 
- [https://www.yahoo.com/](https://www.yahoo.com/ "https://www.yahoo.com/") 
- [https://www.usbank.com/index.html](https://www.usbank.com/index.html "https://www.usbank.com/index.html") 
- [https://www.sidretail.com/](https://www.sidretail.com/ "https://www.sidretail.com/") 
- [https://www.microsoft.com/en-us](https://www.microsoft.com/en-us "https://www.microsoft.com/en-us")
## Beginner Task
In order to complete this task, we will first have to collect the headers for the provided IP, check if "Strict-Transport-Security" is included, and finally return a boolean. I found a snippet [here](https://www.geeksforgeeks.org/response-headers-python-requests/) that was useful for getting started with headers. This code returns some details about the request and a json response including all of the headers we are looking for. Since 'headers' is automatically created as an object, we can check for the presence of the Strict-Transport-Security header with a simple 'if' x 'in' y statement. I also have been meaning to figure out printing colored text in python, so I added red and green outputs depending on the result (based on snippet found [here](https://www.geeksforgeeks.org/print-colors-python-terminal/)).
```python
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
```
Beginner task complete, this is what the output looked like.
![[Pasted image 20250314060432.png]]
## Intermediate Task
### Snippet from Previous Challenge
Similar to challenge one, I now need the script to take multiple addresses in a file and output the results for each. This is similar to the intermediate task from challenege 1 so i went and grabbed one of the functions from that (see below).
```python
with open('addresses.txt', 'r') as file:
    #Reade each line in file
    for line in file:
        #Run get_data fucntion on IP
        print_data(line.strip())
```
### Preliminary Code
I pasted this into my code and got to work combining it with what I had. This is what I came out with.
```python
# imports
import requests
from colorama import Fore, Style
def check_headers(x):
    # get url from user
    url = x

    # Making a get request
    response = requests.get(url)

    # Check header exists in response
    if 'Strict-Transport-Security' in response.headers:
        print(Fore.GREEN + f"Strict-Transport-Security header was found for {url}")
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"Strict-Transport-Security header was not found for {url}")
        print(Style.RESET_ALL)

with open('links.txt', 'r') as file:
    #Reade each line in file
    for line in file:
        #Run get_data fucntion on IP
        check_headers(line.strip())
```
This was the output I got.
![[Pasted image 20250314063929.png]]
### Adding IP resolution
Using the code from [this snippet](https://nekkantimadhusri.medium.com/how-to-get-ip-address-of-website-using-python-f03707c50499) combined with the function `check_headers` I was able to include the IP for each site in the output. After what felt like forever playing with regex to parse the URL (slashes were giving me issues), I was able to get this output.
![[Pasted image 20250314070903.png]]
### Final Intermediate Code
```python
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
    #Read each line in file
    for line in file:
        #Run get_data fucntion on IP
        check_headers(line.strip())

```
## Expert Task
### Other Headers
Adding checks for the different standard headers was easy, I just used the same syntax that I used for the other header.
```python
    # Check 'Content-Security-Policy' header exists in response
    if 'Content-Security-Policy' in response.headers:
        print(Fore.GREEN + f"Content-Security-Policy header was found for {host}")
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"Content-Security-Policy header was not found for {host}")
        print(Style.RESET_ALL)

    # Check 'X-Frame-Options' header exists in response
    if 'X-Frame-Options' in response.headers:
        print(Fore.GREEN + f"X-Frame-Options header was found for {host}")
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"X-Frame-Options header was not found for {host}")
        print(Style.RESET_ALL)    
```
### Server Header
This was also straightforward.
```python
    # Check 'Server' header exists in response, return value
    if 'Server' in response.headers:
        print(Fore.GREEN + f"Server was found for {host}")
        print("Server Header Value:" + response.headers['Server'])
        print(Style.RESET_ALL)
    else: 
        print(Fore.RED + f"Server was not found for {host}")
        print(Style.RESET_ALL)
```
## Bonus Task
Honestly I have not taken much time to make this code pretty or modular yet. I am going to do this now so that it is easier to complete the bonus task. 

I wasted a bunch of time figuring out how to check for HTTPS, for some reason my first thought was to use a library to solve this problem. When I finally realized I could just check the URL variable for https, it only took a few minutes to get the code working. The final code had the following functions:

- `extract_host(url)`: Takes a URL and strips away the "http://" or "https://" prefix and any trailing slashes to get just the website name.
- `is_https(url)`: Checks if a URL uses secure HTTPS protocol by seeing if it starts with "https://".
- `get_ip_address(host)`: Finds the IP address for a given website name (though it's hardcoded to return the IP for "[www.redsiege.com](http://www.redsiege.com)").
- `print_header_status(header_name, headers, host, show_value=False)`: Checks if a security header exists in a website's response and prints the result in color (green if found, red if not). Can also show the actual header value if needed.
- `check_headers(x)`: The main function that:
    - Takes a URL
    - Gets the website's IP address
    - Makes a request to the website
    - Checks various security headers (like Content-Security-Policy)
    - Only checks HTTPS-specific headers if the site uses HTTPS
- `process_url_file(filename)`: Opens a text file containing a list of URLs (one per line) and runs the header check on each URL.

This is how it looked. By no means perfect, but I was content. I plan on spending a bit more time perfecting the output on the next challenge.
```python
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

def is_https(url):
    # Check if URL uses HTTPS
    return url.lower().startswith("https://")

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

    # Check if URL is HTTPS
    is_secure = is_https(url)
    
    # Check security headers, only check Strict-Transport-Security if URL is HTTPS
    if is_secure:
        print_header_status('Strict-Transport-Security', response.headers, host)
    else:
        print(Fore.YELLOW + f"Skipping Strict-Transport-Security check for HTTP URL: {url}" + Style.RESET_ALL)
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
```