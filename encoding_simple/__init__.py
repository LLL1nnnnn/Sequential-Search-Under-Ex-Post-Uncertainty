from otree.api import *

c = Currency
import random 


doc = """
Real Effort Task of Encoding Letters
"""


class Constants(BaseConstants):
    name_in_url = 'encoding_simple'
    players_per_group = None
    num_rounds = 1
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    point_per_correct_combo = 0



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    correct_entry = models.IntegerField()
    entry = models.IntegerField()

    letter_1 = models.StringField()
    letter_2 = models.StringField()
    letter_3 = models.StringField()
    letter_4 = models.StringField()
    letter_5 = models.StringField()
    letter_6 = models.StringField()
    letter_7 = models.StringField()
    letter_8 = models.StringField()
    letter_9 = models.StringField()
    letter_10 = models.StringField()
    letter_11 = models.StringField()
    letter_12 = models.StringField()
    letter_13 = models.StringField()
    letter_14 = models.StringField()
    letter_15 = models.StringField() 

    correct_num_1 = models.IntegerField()
    correct_num_2 = models.IntegerField()
    correct_num_3 = models.IntegerField()
    correct_num_4 = models.IntegerField() 
    correct_num_5 = models.IntegerField() 
    correct_num_6 = models.IntegerField() 
    correct_num_7 = models.IntegerField() 
    correct_num_8 = models.IntegerField() 
    correct_num_9 = models.IntegerField() 
    correct_num_10 = models.IntegerField() 
    correct_num_11 = models.IntegerField() 
    correct_num_12 = models.IntegerField() 
    correct_num_13 = models.IntegerField() 
    correct_num_14 = models.IntegerField() 
    correct_num_15 = models.IntegerField() 
    

    num_entered_1 = models.IntegerField(
        doc="user's transcribed text 1",
        label="Code for letter 1",
    )
    num_entered_2 = models.IntegerField(
        doc="user's transcribed text 2",
        label="Code for letter 2",
    )
    num_entered_3 = models.IntegerField(
        doc="user's transcribed text 3",
        label="Code for letter 3",
    )
    num_entered_4 = models.IntegerField(
        doc="user's transcribed text 4",
        label="Code for letter 4",
    )
    num_entered_5 = models.IntegerField(
        doc="user's transcribed text 5",
        label="Code for letter 5",
    )
    num_entered_6 = models.IntegerField(
        doc="user's transcribed text 6",
        label="Code for letter 6",
    )
    num_entered_7 = models.IntegerField(
        doc="user's transcribed text 7",
        label="Code for letter 7",
    )
    num_entered_8 = models.IntegerField(
        doc="user's transcribed text 8",
        label="Code for letter 8",
    )
    num_entered_9 = models.IntegerField(
        doc="user's transcribed text 9",
        label="Code for letter 9",
    )
    num_entered_10 = models.IntegerField(
        doc="user's transcribed text 10",
        label="Code for letter 10",
    )
    num_entered_11 = models.IntegerField(
        doc="user's transcribed text 11",
        label="Code for letter 11",
    )
    num_entered_12 = models.IntegerField(
        doc="user's transcribed text 12",
        label="Code for letter 12",
    )
    num_entered_13 = models.IntegerField(
        doc="user's transcribed text 13",
        label="Code for letter 13",
    )
    num_entered_14 = models.IntegerField(
        doc="user's transcribed text 14",
        label="Code for letter 14",
    )
    num_entered_15 = models.IntegerField(
        doc="user's transcribed text 15",
        label="Code for letter 15",
    )

    # def set_payoffs(self): 
    #     if self.num_entered_1 == self.correct_num_1 and self.num_entered_2 == self.correct_num_2 and self.num_entered_3 == self.correct_num_3:
    #         self.payoff = Constants.point_per_correct_combo
    #     else:
    #         self.payoff = 0



# PAGES
class Cover(Page):

    def is_displayed(self):
        return self.round_number == 1


class Introduction(Page):

    def is_displayed(self):
        return self.round_number == 1


class Task(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = [
        'num_entered_1', 
        'num_entered_2', 
        'num_entered_3', 
        'num_entered_4',
        'num_entered_5',
        'num_entered_6',
        'num_entered_7',
        'num_entered_8',
        'num_entered_9',
        'num_entered_10',
        'num_entered_11',
        'num_entered_12',
        'num_entered_13',
        'num_entered_14',
        'num_entered_15',
    ]

    @staticmethod
    def vars_for_template(player: Player): 
        encryption_dict = {}
        for i in range(len(Constants.alphabet)):
             encryption_dict[Constants.alphabet[i]] = random.randint(100, 999)

        randomlist = random.sample(range(0, 26), 15)
        player.letter_1 = Constants.alphabet[randomlist[0]]
        player.letter_2 = Constants.alphabet[randomlist[1]]
        player.letter_3 = Constants.alphabet[randomlist[2]]
        player.letter_4 = Constants.alphabet[randomlist[3]]
        player.letter_5 = Constants.alphabet[randomlist[4]]
        player.letter_6 = Constants.alphabet[randomlist[5]]
        player.letter_7 = Constants.alphabet[randomlist[6]]
        player.letter_8 = Constants.alphabet[randomlist[7]]
        player.letter_9 = Constants.alphabet[randomlist[8]]
        player.letter_10 = Constants.alphabet[randomlist[9]]
        player.letter_11 = Constants.alphabet[randomlist[10]]
        player.letter_12 = Constants.alphabet[randomlist[11]]
        player.letter_13 = Constants.alphabet[randomlist[12]]
        player.letter_14 = Constants.alphabet[randomlist[13]]
        player.letter_15 = Constants.alphabet[randomlist[14]]

        player.correct_num_1 = encryption_dict[player.letter_1]
        player.correct_num_2 = encryption_dict[player.letter_2]
        player.correct_num_3 = encryption_dict[player.letter_3]
        player.correct_num_4 = encryption_dict[player.letter_4]
        player.correct_num_5 = encryption_dict[player.letter_5]
        player.correct_num_6 = encryption_dict[player.letter_6]
        player.correct_num_7 = encryption_dict[player.letter_7]
        player.correct_num_8 = encryption_dict[player.letter_8]
        player.correct_num_9 = encryption_dict[player.letter_9]
        player.correct_num_10 = encryption_dict[player.letter_10]
        player.correct_num_11 = encryption_dict[player.letter_11]
        player.correct_num_12 = encryption_dict[player.letter_12]
        player.correct_num_13 = encryption_dict[player.letter_13]
        player.correct_num_14 = encryption_dict[player.letter_14]
        player.correct_num_15 = encryption_dict[player.letter_15]

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
            'letter_4': player.letter_4,
            'letter_5': player.letter_5,
            'letter_6': player.letter_6,
            'letter_7': player.letter_7,
            'letter_8': player.letter_8,
            'letter_9': player.letter_9,
            'letter_10': player.letter_10,
            'letter_11': player.letter_11,
            'letter_12': player.letter_12,
            'letter_13': player.letter_13,
            'letter_14': player.letter_14,
            'letter_15': player.letter_15,
            'dict1': shuffled_encryption_dict_1,
            'dict2': shuffled_encryption_dict_2,
        }


# class Results(Page):
#     # def is_displayed(self):
#     #     return self.round_number == Constants.num_rounds

#     @staticmethod
#     def vars_for_template(player: Player):
#         player.set_payoffs()
#         return{
#             'payoff': player.payoff
        # }

# class Results(Page):
#     def is_displayed(self):
#         return self.round_number == Constants.num_rounds



class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        player.entry = 0
        player.correct_entry = 0
        for i in range(1, 16): 
            entry = 'num_entered_' + str(i)
            correct = 'correct_num_' + str(i)
            if getattr(player, entry):
                player.entry += 1
            if getattr(player, entry) == getattr(player, correct): 
                player.correct_entry += 1
            else:
                player.correct_entry += 0
        return {
            'entry': player.entry, 
            'correct_entry': player.correct_entry, 
        }

page_sequence = [Cover, Introduction, Task, FinalResults]
