import random
import numpy as np 
from otree.api import *
from otree.models import subsession
import csv

doc = """
Sequential search task 
"""


class Constants(BaseConstants):
    name_in_url = 'search'
    players_per_group = None
    num_rounds = 10
    # endowment = 100
    # search_cost = 5
    # value_high = 500
    # value_low = 100
    # certainty = True
    # random = True

# def parse_config(config_file):
#     with open('certainty/configs/' + config_file) as f:
#         rows = list(csv.DictReader(f))

#     rounds = []
#     for row in rows:
#         rounds.append({
#             'endowment': int(row['endowment']),
#             'value_high': int(row['value_high']),
#             'value_low': int(row['value_low']),
#             'search_cost': int(row['search_cost']),
#             'certainty': True if row['certainty'] == 'TRUE' else False,
#             'random': True if row['random'] == 'TRUE' else False,
#         })
#     print(round)
#     return rounds


class Subsession(BaseSubsession):
    pass
    # pass 
    # print('subsession')
    # def endowment(self):
    #     return parse_config(self.session.config['config_file'])[0]['endowment']

    # def value_high(self):
    #     return parse_config(self.session.config['config_file'])[0]['value_high']

    # def value_low(self):
    #     return parse_config(self.session.config['config_file'])[0]['value_low']

    # def search_cost(self):
    #     return parse_config(self.session.config['config_file'])[0]['search_cost']

    # def certainty(self):
    #     return parse_config(self.session.config['config_file'])[0]['certainty']

    # def random(self):
    #     return parse_config(self.session.config['config_file'])[0]['random']

def creating_session(subsession: Subsession):
    # config = self.config
    # if not config:
    #     return
    print("creating session")
    n = 50
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
    total_cost = models.IntegerField() 
    threshold = models.FloatField()
    
    # no dynamic creating fields 
    for i in range(1, 51): 
        locals()['prob_' + str(i)] = models.FloatField()
    del i 

# FUNCTIONS
    def compute_player_payoff(self):
        if self.session.config['certainty']:
            self.payoff = self.probability * self.session.config['value_high'] + \
                (1 - self.probability) * self.session.config['value_low'] - \
                self.number_of_search * self.session.config['search_cost']
        else:
            if self.probability >= self.threshold: 
                self.payoff = self.session.config['value_high'] - \
                self.number_of_search * self.session.config['search_cost']
            else: 
                self.payoff = self.session.config['value_low'] - \
                self.number_of_search * self.session.config['search_cost']

# def compute_player_payoff(player: Player):
# if Constants.certainty:
#     player.payoff = Constants.endowment + player.probability * Constants.value_high + \
#         (1 - player.probability) * Constants.value_low - \
#         player.number_of_search * Constants.search_cost
# else:
#     if player.probability >= player.threshold: 
#         player.payoff = Constants.endowment + Constants.value_high - \
#         player.number_of_search * Constants.search_cost
#     else: 
#         player.payoff = Constants.endowment + Constants.value_low - \
#         player.number_of_search * Constants.search_cost

# PAGES

class Cover(Page):
    print('cover')
    def is_displayed(self):
        return self.round_number == 1

class Instruction(Page):
    print('instruction')
    def is_displayed(self):
        return self.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'value_high': c(player.session.config['value_high']),
            'value_low': c(player.session.config['value_low']),
            'search_cost': c(player.session.config['search_cost']),
            'certainty': player.session.config['certainty']
        }

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
            player.total_cost = player.number_of_search * player.session.config['search_cost']
            return {my_id: response}
        elif data['type'] == 'purchase':
            probabilities = Decision.probabilities[my_id]
            # print(probabilities)
            player.probability = Decision.probabilities[my_id][data['i'] - 1]
            player.threshold = random.uniform(0, 1) 
            player.compute_player_payoff()
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
    
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'value_high': c(player.session.config['value_high']),
            'value_low': c(player.session.config['value_low']),
            'search_cost': c(player.session.config['search_cost']),
            'certainty': player.session.config['certainty']
        }


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        Decision.probabilities[player.id_in_group] = []
        var = dict(player=player)
        var['value_high'] = c(player.session.config['value_high'])
        var['value_low'] = c(player.session.config['value_low'])
        var['search_cost'] = c(player.session.config['search_cost']) 
        var['certainty']= player.session.config['certainty']
        return var
    
    # @staticmethod
    # def vars_for_template(player: Player):
    #     return {
    #         'value_high': c(player.session.config['value_high']),
    #         'value_low': c(player.session.config['value_low']),
    #         'search_cost': c(player.session.config['search_cost']),
    #         'certainty': player.session.config['certainty']
    #     }


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds



page_sequence = [Cover, Instruction, Decision, Results, FinalResults]
