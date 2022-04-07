import itertools
import requests
import spacy
from src.models import Skill
import pandas as pd
from src import db

def load_skills():
    skills_df = pd.read_csv('./skills.csv', index_col = 0)
    return skills_df['skills'].to_list()

combined_skills = load_skills()

def build_skills(skills):
    return [Skill.get_or_create(db.session, name = skill) for skill in combined_skills]




