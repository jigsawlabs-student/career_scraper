from re import L
from src.adapters.indeed_client import get_page
from src.adapters.page_runner import PageRunner
from src.models import Scraping, ScrapedPage, Skill, PositionSkill, Position
from src import db

class PositionSkillBuilder:
    def __init__(self):
        pass
    
    def build_skills_for_untagged_positions(self, session):
        remaining_positions = self.positions_after_last_tagged(session)
        positions_with_skills = self.build_skills_for_multiple(remaining_positions, session)
        return positions_with_skills

    def positions_after_last_tagged(self, session):
        position_id = PositionSkill.last_position_id()
        if position_id:
            return Position.query.filter(Position.id > position_id).all()
        else:
            return Position.query.all()
    
    def build_skills_for_multiple(self, positions, session):
        
        for position in positions:
            self.build_skills_for(position, session)
        return positions
            

    def build_skills_for(self, position, session):
        
        skills = Skill.query.all()
        
        for skill in skills:
            position_skill = self.build_position_skill(position, skill, session)
        return position.position_skills

    def format_description(self, description):
        return description.lower().replace(',', ' ').replace('.', ' ') + ' '

    def build_position_skill(self, position, skill, session):
        padded_skill = f' {skill.name} '
        
        if padded_skill in self.format_description(position.description):
            position_skill = PositionSkill.get_or_create(session = session, skill_id = skill.id, 
            position_id = position.id)
            session.add(position_skill)
            session.commit()
            return position_skill

    def save_skills_for(position):
        db.session.add(position)
        db.session.commit()