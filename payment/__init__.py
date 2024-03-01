from otree.api import *

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1

    width = '850px'
    height = 1.7


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

# PAGES
class payment(Page):
    pass

class Results(Page):
    pass


page_sequence = [payment, Results]
