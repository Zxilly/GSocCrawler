import requests

targetURL = "https://summerofcode.withgoogle.com/archive/2020/organizations/"

socPage = requests.get(targetURL).content

print(socPage)
