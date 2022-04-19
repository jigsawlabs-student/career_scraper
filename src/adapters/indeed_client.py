from urllib.request import urlopen
import re
from bs4 import BeautifulSoup as bs
import requests
import pdb
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}

def get_page(position = 'data engineer', location = 'United States', experience_level = '', start = 0):
    url = 'https://www.indeed.com/jobs'
    params = {'q': position, 'l': location, 'start': start, "sort": "date"}
    if experience_level:
      params.update({'explvl':experience_level})
    response = requests.get(url, params = params, headers=header, timeout=10)
    print(response.url)
    return response.text
    

def get_card_from(id):
    desc_string = f"https://www.indeed.com/rpc/jobdescs?jks={id}"
    desc_response = requests.get(desc_string, headers=header)
    description_response = desc_response.json()
    return description_response


def get_page_from(id):
  desc_string = f"https://www.indeed.com/viewjob?jk={id}"
  response = urlopen(desc_string).read().decode('utf8')
  return response