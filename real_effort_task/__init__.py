from otree.api import *

c = Currency

import random 


doc = """
Real effort task of word encryption
"""


class Constants(BaseConstants):
    name_in_url = 'real_effort'
    players_per_group = 2
    num_rounds = 1
    wage_high = c(100)
    wage_low = c(10)
    policy = True
    min_wage = c(70) 
    instructions_template = 'real_effort_task/instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    wage_offer = models.CurrencyField(
        min=Constants.wage_low,
        max=Constants.wage_high,
        doc="""Wage offered by employer""",
        label="Please enter a wage offer (between 0 and 100). ",
    )

    reservation_wage = models.CurrencyField(
        min=Constants.wage_low,
        max=Constants.wage_high,
        doc="""Reservation wage of employee""",
        label="Please enter an amount (between 0 and 100) that you are willing to accept the job.",
    )

    decision = models.StringField()


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    employer = group.get_player_by_id(1)
    employee = group.get_player_by_id(2)
    employer.payoff = 0 - group.wage_offer
    employee.payoff = group.wage_offer - 0


# PAGES
class Introduction(Page):
    form_model = 'group'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'wage_low': Constants.wage_low, 
            'wage_high': Constants.wage_high, 
            'policy': Constants.policy,
            'min_wage': Constants.min_wage, 
        }

class Offer(Page):
    """This page is only for employer
    employer sends wage offer to employee"""

    form_model = 'group'
    form_fields = ['wage_offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'wage_low': Constants.wage_low, 
            'wage_high': Constants.wage_high, 
            'policy': Constants.policy,
            'min_wage': Constants.min_wage, 
        }

class Reservation(Page):
    """This page is only for employee
    employee sets reservation wage"""

    form_model = 'group'
    form_fields = ['reservation_wage']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2
    
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'wage_low': Constants.wage_low, 
            'wage_high': Constants.wage_high, 
            'policy': Constants.policy,
            'min_wage': Constants.min_wage, 
        }


# class DecisionWaitPage(WaitPage):
#     pass


# class Decision(Page):
#     """This page is only for employee
#     employee indicate a reservation wage and decides whether to accept or reject the wage offer"""

#     form_model = 'group'
#     form_fields = ['decision']

#     @staticmethod
#     def is_displayed(player: Player):
#         return player.id_in_group == 2

#     # @staticmethod
#     # def vars_for_template(player: Player):
#     #     group = player.group

#     #     tripled_amount = 0
#     #     return dict(
#     #         tripled_amount=tripled_amount,
#     #     )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.wage_offer >= group.reservation_wage:
            group.decision = 'Accept'
            player.participant.match = True
        else: 
            group.decision = 'Reject'
            player.participant.match = False
        return {
            'wage_low': Constants.wage_low, 
            'wage_high': Constants.wage_high, 
            'policy': Constants.policy,
            'min_wage': Constants.min_wage, 
            'decision': group.decision,
            'match': player.participant.match, 
        }


page_sequence = [
    Introduction,
    Offer,
    Reservation, 
    ResultsWaitPage,
    Results,
]