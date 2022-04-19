# Import necessary libraries
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt

# read search terms from csv into a list


def get_title_and_desc(card):
    id_string = card['data-jk']
    title = card.find('a', {'class': 'jobtitle'}).text[1:]
    desc_string = f"https://www.indeed.com/rpc/jobdescs?jks={id_string}"
    desc_response = requests.get(desc_string, headers=header)
    description_response = desc_response.json()
    desc = description_response[id_string]
    return id_string, title, desc

def title_and_description_from(cards):
    return pd.DataFrame(data = [get_title_and_desc(card) for card in cards], 
                        columns = ['id_string', 'title', 'desc'])

def tech_tags(idx, requirements_df):
    requirement_row = requirements_df.iloc[idx]
    return [(idx, requirement_row['listing_id'], technology) for technology in technologies 
             if technology.lower() in requirement_row['detail'].lower()]

def extract_requirements_from(idx, card_row):
    requirements = []
    row_id_string = card_row['id_string']
    uls = bs(card_row['desc'], 'html.parser').find_all('ul')
    for ul in uls:
        if ul.find_previous():
            label_text = ul.find_previous().text
        else:
            label_text = 'no label'
        requirements += [(idx, label_text[:30], li.text) for li in ul.find_all('li')]
    return pd.DataFrame(requirements, columns = ['listing_id', 'tag', 'detail'])