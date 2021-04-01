import random
import numpy as np 
from otree.api import *


doc = """
Sequential search task -- Uncertainty treatment
"""


class Constants(BaseConstants):
    name_in_url = 'uncertainty'
    players_per_group = 2
    num_rounds = 2
    endowment = 100
    search_cost = 5
    value_high = 100
    value_low = 10


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    n = int(Constants.endowment / Constants.search_cost)
    for p in subsession.get_players():
        indices = [j for j in range(1, n + 1)]
        form_fields = ['prob_' + str(k) for k in indices]
        p.participant.vars['probabilities'] = list(
            zip(indices, form_fields)
            )
        # print(p.participant.vars['probabilities'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_of_search = models.IntegerField()
    probability = models.FloatField()
    threshold = models.FloatField()
    total_cost = models.IntegerField() 

    for i in range(1, Constants.endowment + 1): 
        locals()['prob_' + str(i)] = models.FloatField()
    del i 

# FUNCTIONS
def compute_player_payoff(player: Player):
    player.threshold = random.uniform(0, 1) 
    if player.probability >= player.threshold: 
        player.payoff = Constants.endowment + Constants.value_high - \
        player.number_of_search * Constants.search_cost
    else: 
        player.payoff = Constants.endowment + Constants.value_low - \
        player.number_of_search * Constants.search_cost

# PAGES

class Cover(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instruction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Decision(Page):
    probabilities = {}

    @staticmethod
    def live_method(player: Player, data=None):
        my_id = player.id_in_group
        if not data or data['type'] == 'search':
            p = round(np.random.uniform(0, 1), 2)
            if my_id not in Decision.probabilities:
                Decision.probabilities[my_id] = []
            probabilities = Decision.probabilities[my_id]
            probabilities.append(p)
            response = {
                'probability': p
            }
            player.number_of_search = len(probabilities)
            player.total_cost = player.number_of_search * Constants.search_cost 
            return {my_id: response}
        elif data['type'] == 'purchase':
            probabilities = Decision.probabilities[my_id]
            player.probability = Decision.probabilities[my_id][data['i'] - 1]
            compute_player_payoff(player)

            Decision.probabilities[my_id] = []

            response = {
                'type': 'game_finished'
            }

            form_fields = [list(t) 
                    for t in zip(*player.participant.vars['probabilities'])][1]
            indices = [list(t)
                    for t in zip(*player.participant.vars['probabilities'])][0]
            # print(probabilities)
            # if choices are displayed in tabular format
            for j, choice in zip(indices, form_fields):
                if j <= player.number_of_search:
                    setattr(player, choice, probabilities[j-1])
                else: 
                    setattr(player, choice, 0)
            return {my_id: response}


class Results(Page):
    def vars_for_template(player: Player):
        Decision.probabilities[player.id_in_group] = []
        return dict(player=player)


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds



page_sequence = [Cover, Instruction, Decision, Results, FinalResults]
