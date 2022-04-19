from bs4 import BeautifulSoup as bs
from src.adapters.position_builder import *
from src.adapters.position_skill_builder import PositionSkillBuilder
import src.models as models
import pdb
import pytest
from src.adapters.seed_builder import load_skills, build_skills
from tests.data.description import description_text
from src import create_app

@pytest.fixture()
def build_db(scope = 'module'):
    test_url = "postgresql://postgres:postgres@localhost/test_career_scraper"
    app = create_app(test_url)
    with app.app_context():
        engine = db.engine
        db.drop_all()
        db.create_all()
        combined_skills = load_skills()

        build_skills(combined_skills, db)
        yield db

def test_position_skill_builder(build_db):
    position = models.Position(description = description_text)
    
    session = build_db.session
    session.add(position)
    session.commit()
    position_skill_builder = PositionSkillBuilder()
    pos_skills = position_skill_builder.build_skills_for(position, build_db.session)
    skill_ids = [pos_skill.skill_id for pos_skill in pos_skills]
    assert len(pos_skills) == len(set(skill_ids))


def test_position_skill_builder_does_not_duplicate_relations(build_db):
    position = models.Position(description = description_text)
    session = build_db.session
    session.add(position)
    session.commit()
    position_skill_builder = PositionSkillBuilder()
    pos_skills = position_skill_builder.build_skills_for(position, build_db.session)
    session.commit()
    initial_skills = position.position_skills
    position_skill_builder.build_skills_for(position, build_db.session)
    session.commit()
    assert len(initial_skills) == len(position.position_skills)

def test_position_skill_builder_does_not_duplicate_relations(build_db):
    first_position = models.Position(description = description_text)
    session = build_db.session
    session.add(first_position)
    session.commit()
    
    second_position = models.Position(description = "be good at AWS, and react native")
    session = build_db.session
    session.add(second_position)
    session.commit()


    position_skill_builder = PositionSkillBuilder()
    positions = [first_position, second_position]
    pos_skills = position_skill_builder.build_skills_for_multiple(positions, build_db.session)
    assert len(first_position.position_skills) == 27
    assert len(second_position.position_skills) == 3

def test_only_builds_relevant_skills(build_db):
    position = models.Position(description = "be good at AWS, and react native")
    session = build_db.session
    session.add(position)
    session.commit()

    position_skill_builder = PositionSkillBuilder()
    pos_skills = position_skill_builder.build_skills_for(position, build_db.session)
    skill_names = [skill.name for skill in position.skills]
    assert set(skill_names) == set(['react', 'react native', 'aws'])

def test_positions_after_last_tagged(build_db):
    first_position = models.Position(description = description_text)
    session = build_db.session
    session.add(first_position)
    session.commit()
    position_skill_builder = PositionSkillBuilder()
    pos_skills = position_skill_builder.build_skills_for(first_position, build_db.session)

    second_position = models.Position(description = "be good at AWS, and react native")
    session = build_db.session
    session.add(second_position)
    session.commit()
    remaining_positions = position_skill_builder.positions_after_last_tagged(session)
    
    assert remaining_positions == [second_position]


def test_build_remaining_skills(build_db):
    first_position = models.Position(description = description_text)
    session = build_db.session
    session.add(first_position)
    session.commit()
    position_skill_builder = PositionSkillBuilder()
    pos_skills = position_skill_builder.build_skills_for(first_position, build_db.session)

    second_position = models.Position(description = "be good at AWS, and react native")
    session = build_db.session
    session.add(second_position)
    session.commit()
    
    assert len(second_position.skills) == 0
    remaining_positions = position_skill_builder.build_skills_for_untagged_positions(session)
    assert remaining_positions == [second_position]
    skill_names = [skill.name for skill in second_position.skills]
    assert set(skill_names) == set(['react', 'react native', 'aws'])
    
    

    
    


    