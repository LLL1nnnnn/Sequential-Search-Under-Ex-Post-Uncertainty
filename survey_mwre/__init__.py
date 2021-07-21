from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    last_name = models.StringField(label='What is your last name?')
    first_name = models.StringField(label='What is your first name?')
    # ucscID = models.IntegerField(label='What is your UCSC student ID number', min=0000000, max=9999999)
    email = models.StringField(label='What is your university email address?')
    age = models.IntegerField(label='What is your age?', min=13, max=100)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Other', 'Other']], 
        label='What is your gender?',
        # widget=widgets.RadioSelect,
    )
    ethnicity = models.StringField(
        choices=[['American Indian or Alaska Native', 'American Indian or Alaska Native'], 
        ['Asian', 'Asian'], ['Black or African American', 'Black or African American'], 
        ['Native Hawaiian or Other Pacific Islander', 'Native Hawaiian or Other Pacific Islander'], 
        ['White', 'White'], ['Other', 'Other'] , ['Prefer not to say', 'Prefer not to say']], 
        label='What is your ethnic group?',
        # widget=widgets.RadioSelect,
    )
    participantID = models.StringField(label='What is your participant ID (Zoom Username)?')
    # venmoID = models.StringField(label='What is your Venmo ID?')
    major = models.StringField(label='What is your major?')
    fun = models.IntegerField(
        choices=[[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10]], 
        label='How much fun did you have when doing the task? (1 = no fun, 10 = great fun)',
        widget=widgets.RadioSelect,
    )
    work_experience = models.StringField(
        choices=[['Yes', 'Yes'], ['No', 'No'], ['Prefer not to say', 'Prefer not to say']], 
        label='Do you have previous working experience?',
        # widget=widgets.RadioSelect,
    )
    suggest = models.LongStringField(label='Do you have any other suggestion on the experiment?')


# FUNCTIONS
# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['last_name', 'first_name', 'email', 'age', 'gender', 'ethnicity', 'participantID', 'major', 'fun', 'work_experience', 'suggest']


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player=player)


page_sequence = [Survey, Results]
