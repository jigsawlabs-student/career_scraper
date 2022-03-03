from src.adapters.indeed_client import *
from src.adapters.indeed_adapter import *

cards = get_job_cards(position = 'data engineer', location = 'United States', start = 0)
first_card = cards[0]

adapter = IndeedAdapter(first_card)

