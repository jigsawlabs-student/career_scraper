import itertools
import requests
import spacy
from src.models import Skill, JobTitle
from seed.job_titles import titles
import pandas as pd
from src import db

def load_skills():
    skills_df = pd.read_csv('./seed/skills.csv', index_col = 0)    
    return skills_df['skills'].dropna().to_list()

def build_skills(db):
    skills = load_skills()
    return [Skill.get_or_create(db.session, name = skill) for skill in skills]


def build_job_titles():
    job_titles = [JobTitle.get_or_create(db.session, name = title)
     for title in titles]
    return job_titles

