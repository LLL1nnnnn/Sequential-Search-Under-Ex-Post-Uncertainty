import random
from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'certainty'
    players_per_group = 2
    num_rounds = 2
    search_cost = 10
    value_high = 100
    value_low = 50


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_of_search = models.IntegerField()
    probability = models.FloatField()


# FUNCTIONS
def compute_player_payoff(player: Player):
    player.payoff = player.probability * Constants.value_high + \
        (1 - player.probability) * Constants.value_low - \
        player.number_of_search * Constants.search_cost

# PAGES


class Introduction(Page):
    pass


class Decision(Page):
    probabilities = {}

    @staticmethod
    def live_method(player: Player, data=None):
        my_id = player.id_in_group
        if not data or data['type'] == 'search':
            p = round(random.random(), 2)
            if my_id not in Decision.probabilities:
                Decision.probabilities[my_id] = []
            probabilities = Decision.probabilities[my_id]
            probabilities.append(p)
            response = {
                'probability': p
            }
            player.number_of_search = len(probabilities)
            return {my_id: response}
        elif data['type'] == 'purchase':
            player.probability = Decision.probabilities[my_id][data['i'] - 1]
            compute_player_payoff(player)

            Decision.probabilities[my_id] = []

            response = {
                'type': 'game_finished'
            }
            return {my_id: response}


class Results(Page):
    def vars_for_template(player: Player):
        Decision.probabilities[player.id_in_group] = []
        return dict(player=player)


page_sequence = [Introduction, Decision, Results]
