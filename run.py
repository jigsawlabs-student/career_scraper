from src.adapters.indeed_client import *
from src.adapters.position_builder import *
from src.models import *

cards = get_page(position = 'data engineer', location = 'United States', start = 0)
first_card = cards[0]

position = PositionBuilder(first_card)


