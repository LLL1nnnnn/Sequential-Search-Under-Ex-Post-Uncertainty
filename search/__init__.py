import random
import numpy as np 
from collections import ChainMap
from otree.api import *
from otree.models import subsession
import csv

doc = """
Sequential search task 
"""


class Constants(BaseConstants):
    name_in_url = 'search'
    players_per_group = None
    num_rounds = 25
    prac_rounds = 5


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    n = 500
    for p in subsession.get_players():
        indices = [j for j in range(1, n + 1)]
        form_fields = ['prob_' + str(k) for k in indices]
        p.participant.vars['probabilities'] = list(
            zip(indices, form_fields)
            )
        p.participant.vars['search_pay'] = int(0)
        # print(p.participant.vars['probabilities'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_of_search = models.IntegerField()
    probability = models.FloatField() # player's chosen prob
    res_prob = models.FloatField(
        min = 0,
        max = 1,
        label = " ",
    )
    res_value = models.IntegerField(
        min = 0,
        max = 500,
        label = " ", 
    )
    control_value = models.IntegerField() # expected value of item 
    total_cost = models.IntegerField() 
    threshold = models.FloatField() # threshold above which to have high value 
    paying_round = models.IntegerField()
    final_pay = models.CurrencyField()

    # no dynamic creating fields 
    for i in range(1, 501): 
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

    def loss_payoff(self):
        if self.session.config['certainty']:
            self.payoff = self.session.config['endowment'] - \
                ((1 - self.probability) * self.session.config['value_high'] + \
                self.probability * self.session.config['value_low']) - \
                self.number_of_search * self.session.config['search_cost']
        else:
            if self.probability >= self.threshold: 
                self.payoff = self.session.config['endowment'] - self.session.config['value_low'] - \
                self.number_of_search * self.session.config['search_cost']
            else: 
                self.payoff = self.session.config['endowment'] - self.session.config['value_high'] - \
                self.number_of_search * self.session.config['search_cost']

# PAGES

class Cover(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instruction(Page):
    def is_displayed(self):
        return self.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'value_high': player.session.config['value_high'],
            'value_low': player.session.config['value_low'],
            'search_cost': player.session.config['search_cost'],
            'certainty': player.session.config['certainty'],
            'loss_domain': player.session.config['loss_domain'], 
            'endowment': player.session.config['endowment'], 
        }

# class Reservation_v(Page):
#     form_model = 'player'
#     form_fields = ['res_value']

#     @staticmethod
#     def is_displayed(self):
#         return self.session.config['certainty'] == True
    
#     @staticmethod
#     def error_message(player, values):
#         if values['res_value'] < 0: 
#             return 'Values should be non-negative. Please enter a positive integer. '
#         if values['res_value'] > 500: 
#             return 'Values should be exceed the maximum outcome. '

#     @staticmethod
#     def vars_for_template(player: Player):
#         return {
#             'value_high': player.session.config['value_high'],
#             'value_low': player.session.config['value_low'],
#             'search_cost': player.session.config['search_cost'],
#             'certainty': player.session.config['certainty'],
#         }

# class Reservation_p(Page):
#     form_model = 'player'
#     form_fields = ['res_prob']

#     @staticmethod
#     def is_displayed(self):
#         return self.session.config['certainty'] == False
    
#     @staticmethod
#     def error_message(player, values):
#         if values['res_prob'] < 0: 
#             return 'Probabilities should be non-negative. Please enter a decimal in the form of 0.xx or .xx. '
#         if values['res_prob'] > 1: 
#             return 'Probabilities cannot exceed 1. Please enter a decimal in the form of 0.xx or .xx. '

#     @staticmethod
#     def vars_for_template(player: Player):
#         return {
#             'value_high': player.session.config['value_high'],
#             'value_low': player.session.config['value_low'],
#             'search_cost': player.session.config['search_cost'],
#             'certainty': player.session.config['certainty'],
#         }

class Decision(Page):
    probabilities = {}
    control_values = {}

    @staticmethod
    def live_method(player: Player, data=None):
        my_id = player.id_in_group
        if not data or data['type'] == 'search':
            p = round(np.random.uniform(0, 1), 2)
            if my_id not in Decision.probabilities:
                Decision.probabilities[my_id] = []
            probabilities = Decision.probabilities[my_id]
            probabilities.append(p)

            if player.session.config['loss_domain']: 
                value = player.session.config['value_low'] * p + player.session.config['value_high'] * (1 - p)
            else: 
                value = player.session.config['value_high'] * p + player.session.config['value_low'] * (1 - p)
            if my_id not in Decision.control_values:
                Decision.control_values[my_id] = []
            control_values = Decision.control_values[my_id]
            control_values.append(value)

            if player.session.config['certainty']: 
                response = {
                    'value': int(value),
                    'certainty': 'True', 
                }
            else: 
                response = {
                    'probability': p,
                    'certainty': 'False', 
                }
            player.number_of_search = len(probabilities)
            player.total_cost = player.number_of_search * player.session.config['search_cost']
            return {my_id: response}
        elif data['type'] == 'purchase':
            probabilities = Decision.probabilities[my_id]
            control_values = Decision.control_values[my_id]

            if data['i'] <= 0:
                raise ValueError('index <= 0') 
            player.probability = Decision.probabilities[my_id][data['i'] - 1]
            player.threshold = random.uniform(0, 1) 
            player.control_value = int(Decision.control_values[my_id][data['i'] - 1])
            if player.session.config['loss_domain']: 
                player.loss_payoff()
            else: 
                player.compute_player_payoff()

            # specify paying round 
            if player.round_number == Constants.num_rounds:
                player.paying_round = random.randint(Constants.prac_rounds + 1, Constants.num_rounds)
                player.final_pay = player.in_round(player.paying_round).payoff
                player.participant.vars['search_pay'] = player.final_pay

            Decision.probabilities[my_id] = []
            Decision.control_values[my_id] = []
            
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
            'value_high': player.session.config['value_high'],
            'value_low': player.session.config['value_low'],
            'search_cost': player.session.config['search_cost'],
            'certainty': player.session.config['certainty'],
            'loss_domain': player.session.config['loss_domain'], 
            'endowment': player.session.config['endowment'], 
        }


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        Decision.probabilities[player.id_in_group] = []
        var = dict(player=player)
        var['value_high'] = player.session.config['value_high']
        var['value_low'] = player.session.config['value_low']
        var['search_cost'] = player.session.config['search_cost']
        var['certainty'] = player.session.config['certainty']
        var['endowment'] = player.session.config['endowment']
        var['loss_domain'] = player.session.config['loss_domain']
        return var 

class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'paying_round': player.paying_round,
            'random_payoff': player.final_pay,
        }   



page_sequence = [Cover, Instruction, Decision, Results, FinalResults]
