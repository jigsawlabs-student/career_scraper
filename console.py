from sqlalchemy import inspect

from src.adapters.indeed_client import *
from src.adapters.indeed_adapter import *
from src.models import *
from src import db

# cards = get_job_cards(position = 'data engineer', location = 'United States', start = 0)
# first_card = cards[0]

# state = State(name = 'New York')
# new_york.cities.append(city)
# db.session.add(new_york)
# db.session.commit()
    # both city and state now added