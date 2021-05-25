from otree.api import *

c = Currency

import random 


doc = """
Real Effort Task of Encoding Letters
"""


class Constants(BaseConstants):
    name_in_url = 'encoding'
    players_per_group = None
    num_rounds = 15
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    point_per_correct_combo = 10



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    letter_1 = models.StringField()
    letter_2 = models.StringField()
    letter_3 = models.StringField()

    correct_num_1 = models.IntegerField()
    correct_num_2 = models.IntegerField()
    correct_num_3 = models.IntegerField()

    num_entered_1 = models.IntegerField(
        doc="user's transcribed text 1",
        label="Code for first letter",
        # widget=widgets.TextInput(attrs={'autocomplete':'off'})
    )
    num_entered_2 = models.IntegerField(
        doc="user's transcribed text 2",
        label="Code for second letter",
        # widget=widgets.TextInput(attrs={'autocomplete':'off'})
    )
    num_entered_3 = models.IntegerField(
        doc="user's transcribed text 3",
        label="Code for third letter",
        # widget=widgets.TextInput(attrs={'autocomplete':'off'})
    )

    # def encryption(self): 
    #     encryption_dict = {}
    #     for i in range(len(Constants.alphabet)):
    #          encryption_dict[Constants.alphabet[i]] = random.randint(100, 999)

    #     randomlist = random.sample(range(0, 26), 3)
    #     self.letter_1 = Constants.alphabet[randomlist[0]]
    #     self.letter_2 = Constants.alphabet[randomlist[1]]
    #     self.letter_3 = Constants.alphabet[randomlist[2]]

    #     self.correct_num_1 = encryption_dict[self.letter_1]
    #     self.correct_num_2 = encryption_dict[self.letter_2]
    #     self.correct_num_3 = encryption_dict[self.letter_3]

    def set_payoffs(self): 
        if self.num_entered_1 == self.correct_num_1 and self.num_entered_2 == self.correct_num_2 and self.num_entered_3 == self.correct_num_3:
            self.payoff = Constants.point_per_correct_combo
            # self.participant.encoding_payoff += self.payoff
        else:
            self.payoff = 0
            # self.participant.encoding_payoff += self.payoff



# PAGES
class Introduction(Page):

    def is_displayed(self):
        return self.round_number == 1


class Task(Page):
    form_model = 'player'
    form_fields = ['num_entered_1', 'num_entered_2', 'num_entered_3']

    @staticmethod
    def vars_for_template(player: Player): 
        encryption_dict = {}
        for i in range(len(Constants.alphabet)):
             encryption_dict[Constants.alphabet[i]] = random.randint(100, 999)

        randomlist = random.sample(range(0, 26), 3)
        player.letter_1 = Constants.alphabet[randomlist[0]]
        player.letter_2 = Constants.alphabet[randomlist[1]]
        player.letter_3 = Constants.alphabet[randomlist[2]]

        player.correct_num_1 = encryption_dict[player.letter_1]
        player.correct_num_2 = encryption_dict[player.letter_2]
        player.correct_num_3 = encryption_dict[player.letter_3]

        keys = list(encryption_dict.keys())
        random.shuffle(keys)

        shuffled_encryption_dict = dict()
        for key in keys:
            shuffled_encryption_dict.update({key: encryption_dict[key]})
        
        shuffled_encryption_dict_1 = dict(list(shuffled_encryption_dict.items())[:13])
        shuffled_encryption_dict_2 = dict(list(shuffled_encryption_dict.items())[13:])

        return {
            'letter_1': player.letter_1, 
            'letter_2': player.letter_2,
            'letter_3': player.letter_3,
            'dict1': shuffled_encryption_dict_1,
            'dict2': shuffled_encryption_dict_2,
        }


class Results(Page):
    # def is_displayed(self):
    #     return self.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        player.set_payoffs()
        return{
            'payoff': player.payoff
        }



# page_sequence = [Introduction, Task, Results]

page_sequence = [Task, Results]