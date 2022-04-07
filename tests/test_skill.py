from bs4 import BeautifulSoup as bs
from src.adapters.position_builder import *

import src.models as models
import pdb
import pytest

from src import create_app

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()



def drop_all():
    models.PositionLocation.query.delete()
    models.Position.query.delete()
    models.Company.query.delete()
    models.State.query.delete()
    models.City.query.delete()
    models.Skill.query.delete()

def test_get_or_create_by():
    models.Skill.get_or_create(name = 'aws')
    models.Skill.get_or_create(name = 'aws')
    assert models.Skill.query.first().name == 'aws'
    assert len(models.Skill.query.all()) == 1