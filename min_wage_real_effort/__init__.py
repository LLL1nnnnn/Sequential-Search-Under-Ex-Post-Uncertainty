from otree.api import *

c = Currency

import random 


author = 'Yilin Li'

doc = """
Minimum Wage and Real Effort Task of Encoding Letters
"""


class Constants(BaseConstants):
    name_in_url = 'min_wage_real_effort'
    num_rounds = 2
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    point_per_correct_letter = c(30)
    players_per_group = 20
    wage_high = c(100)
    wage_low = c(0)
    min_wage = c(220) 
    base_revenue = c(100)
    instructions_template = 'min_wage_real_effort/instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    policy = models.BooleanField()

    offer = models.CurrencyField(
        # min=Constants.wage_low,
        # max=Constants.wage_high,
        doc="""Wage offered by employer""",
        label="Please enter a wage offer.",
    )

    # def offer_error_message(group, value):
    #     print('value is', value)
    #     if group.policy == True and value < Constants.min_wage:
    #         return 'Cannot offer less than the minimum wage'
    #     elif group.policy == False and value < Constants.wage_low:
    #         return 'Cannot offer less than zero' 


    # def offer_min(group):
    #     if group.policy == True: 
    #         return Constants.min_wage
    #     else:
    #         return Constants.wage_low

    reservation = models.CurrencyField(
        # min=Constants.wage_low,
        # max=Constants.wage_high,
        doc="""Reservation wage of employee""",
        label="Please enter an amount that you are willing to accept the job.",
    )

    # def reservation_min(group):
    #     if group.policy == True: 
    #         return Constants.min_wage
    #     else:
    #         return Constants.wage_low

    decision = models.StringField()

    entry = models.IntegerField() 
    correct_entry = models.IntegerField()

# def make_field(label):
#     return models.IntegerField()


class Player(BasePlayer):
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



# FUNCTIONS
def set_payoffs(group: Group):
    employer = group.get_player_by_id(1)
    employee = group.get_player_by_id(2)
    group.entry = 0
    group.correct_entry = 0
    for i in range(1, 16): 
        entry = 'num_entered_' + str(i)
        correct = 'correct_num_' + str(i)
        if getattr(employee, entry):
            group.entry += 1
        if getattr(employee, entry) == getattr(employee, correct): 
            group.correct_entry += 1
        else:
            group.correct_entry += 0
    if group.decision == 'Accept': 
        employer.payoff = Constants.base_revenue + Constants.point_per_correct_letter * group.correct_entry - group.offer
        employee.payoff = group.offer 
    else: 
        employer.payoff = 0
        employer.payoff = 0


# PAGES
class Introduction_Wage(Page):

    def is_displayed(self):
        return self.round_number == 1
    
    form_model = 'group'

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= 10: 
            player.group.policy = True
        else: 
            player.group.policy = False 

        return {
            'wage_low': Constants.wage_low, 
            'wage_high': Constants.wage_high, 
            'policy': player.group.policy, 
            'min_wage': Constants.min_wage, 
            'point_per_correct_letter': Constants.point_per_correct_letter,
            'base_revenue': Constants.base_revenue, 
        }


class Transition(Page):

    def is_displayed(self):
        return self.round_number == int(Constants.num_rounds / 2 + 1)



class Offer(Page):
    """This page is only for employer
    employer sends wage offer to employee"""

    form_model = 'group'
    form_fields = ['offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        # if values['offer'] > Constants.wage_high:
        #     return 'Please enter a wage offer between 0 points and 100 points' 
        if player.group.policy == True and values['offer'] < Constants.min_wage: 
            return 'Cannot offer less than the minimum wage'
        if player.group.policy == False and values['offer'] < Constants.wage_low: 
            return 'Cannot offer less than zero'
        

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= 10: 
            player.group.policy = True
        else: 
            player.group.policy = False 

        return {
            'wage_low': Constants.wage_low, 
            'wage_high': Constants.wage_high, 
            'policy': player.group.policy, 
            'min_wage': Constants.min_wage, 
            'point_per_correct_letter': Constants.point_per_correct_letter,
            'base_revenue': Constants.base_revenue, 
        }

class Reservation(Page):
    """This page is only for employee
    employee sets reservation wage"""

    form_model = 'group'
    form_fields = ['reservation']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2
    
    @staticmethod
    def error_message(player, values):
        print('values is', values)
        # if values['reservation'] > Constants.wage_high:
        #     return 'Cannot set above 100' 
        # if player.group.policy == True and values['reservation'] < Constants.min_wage: 
        #     return 'Cannot set below the minimum wage'
        if values['reservation'] < Constants.wage_low: 
            return 'Cannot set below zero'
        
    
    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number <= 10: 
            player.group.policy = True
        else: 
            player.group.policy = False 

        return {
            'wage_low': Constants.wage_low, 
            'wage_high': Constants.wage_high, 
            'policy': player.group.policy, 
            'min_wage': Constants.min_wage, 
            'point_per_correct_letter': Constants.point_per_correct_letter,
            'base_revenue': Constants.base_revenue, 
        }

class DecisionWaitPage(WaitPage):
    pass


class Results_Wage(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.offer >= group.reservation:
            group.decision = 'Accept'
            player.participant.match = True
        else: 
            group.decision = 'Reject'
            player.participant.match = False
        return {
            'wage_low': Constants.wage_low, 
            'wage_high': Constants.wage_high, 
            'policy': player.group.policy,
            'min_wage': Constants.min_wage, 
            'decision': group.decision,
            'match': player.participant.match, 
            'point_per_correct_letter': Constants.point_per_correct_letter, 
            'base_revenue': Constants.base_revenue, 
        }

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

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    # def is_displayed(self):
    #     return self.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # group = player.group 
        return{
            'payoff': player.payoff
        }


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # group = player.group 
        return{
            'payoff': player.participant.payoff
        }

# page_sequence = [Introduction, Task, Results]

page_sequence = [Introduction_Wage,
    Transition,
    Offer,
    Reservation, 
    DecisionWaitPage,
    Results_Wage,
    Task, 
    ResultsWaitPage, 
    Results,
    FinalResults]