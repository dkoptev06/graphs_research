import requests
from bs4 import BeautifulSoup
 
 
url = 'https://users.cecs.anu.edu.au/~bdm/data'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
urls = []
for link in soup.find_all('a'):
    name = link.get('href')
    if name.endswith("g6") or name.endswith("gz"):
        print(f"{url}/{name}")