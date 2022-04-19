from bs4 import BeautifulSoup as bs
from src.adapters.position_builder import *
import src.models as models
import pdb
import pytest
from tests.data.description import description_text
from src import create_app



@pytest.fixture()
def build_db():
    test_url = "postgresql://postgres:postgres@localhost/test_career_scraper"
    app = create_app(test_url)
    with app.app_context():
        engine = db.engine
        db.drop_all()
        db.create_all()
        
        yield db

        # db.drop_all()
        # db.create_all()

def test_skills_relation(build_db):
    skill = models.Skill.get_or_create(build_db.session, name = 'aws')
    position = models.Position(description = description_text)
    session = build_db.session
    session.add(skill)
    session.add(position)
    session.commit()
    position_skill = models.PositionSkill(position_id = position.id,
     skill_id = skill.id)
    session.add(position_skill)
    session.commit()
    assert len(position.skills) == 1
    
def test_position_skills_relation(build_db):
    skill = models.Skill.get_or_create(build_db.session, name = 'aws')
    position = models.Position(description = description_text)
    session = build_db.session
    session.add(skill)
    session.add(position)
    session.commit()
    position_skill = models.PositionSkill(position_id = position.id,
     skill_id = skill.id)
    position.position_skills.append(position_skill)
    session.commit()
    assert len(skill.position_skills) == 1
    assert len(position.position_skills) == 1 

# def test_remaining_untagged_positions(build_db):
#     pass