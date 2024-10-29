import requests

response = requests.get("https://users.cecs.anu.edu.au/~bdm/data/graph9c.g6")

print(response)
if response.status_code != 200:
    print("Terminating")
    exit(0)

with open('data/graph9c.g6', 'w') as f:
    f.write(response.text)

print("Success")
