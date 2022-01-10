from os import environ


SESSION_CONFIGS = [
    dict(
        name='hl_mpl', 
        display_name='HL MPL', 
        app_sequence=['mpl'],
        num_demo_participants=1,
        lottery_a = 280, 
        lottery_b_hi = 500,
        lottery_b_lo = 100, 
    ),
    dict(
        name='search_experiment_control', 
        display_name='Search Experiment (Manual Certainty)', 
        app_sequence=['search', 'bret_practice', 'bret', 'mpl','demographics'],
        num_demo_participants=1,
        # config_file = "search_pilot.csv",
        value_high = 500,
        value_low = 100,
        search_cost = 5,
        lottery_a = 280, 
        lottery_b_hi = 500,
        lottery_b_lo = 100,
        random = True, 
        certainty = False, 
        control = True, 
        automatic = False, 
    ),
    dict(
        name='search_experiment_uncertainty', 
        display_name='Search Experiment (Manual Uncertainty)', 
        app_sequence=['search', 'bret_practice', 'bret', 'mpl','demographics'],
        num_demo_participants=1,
        # config_file = "search_pilot.csv",
        value_high = 500,
        value_low = 100,
        search_cost = 5,
        lottery_a = 280, 
        lottery_b_hi = 500,
        lottery_b_lo = 100,
        random = True, 
        certainty = False, 
        control = False, 
        automatic = False,
    ),
    dict(
        name = 'complete_c',
        display_name='Search Experiment (Auto Control)', 
        app_sequence=['search', 'bret_practice', 'bret', 'mpl','demographics'],
        num_demo_participants=1,
        value_high = 500,
        value_low = 100,
        search_cost = 5,
        lottery_a = 280, 
        lottery_b_hi = 500,
        lottery_b_lo = 100,
        certainty = True, 
        random = True,
        control = True, 
        automatic = True, 
    ),
    dict(
        name = 'complete_uc',
        display_name='Search Experiment (Auto Uncertainty)', 
        app_sequence=['search', 'bret_practice', 'bret', 'mpl','demographics'],
        num_demo_participants=1,
        value_high = 500,
        value_low = 100,
        search_cost = 5,
        lottery_a = 280, 
        lottery_b_hi = 500,
        lottery_b_lo = 100,
        certainty = False, 
        random = True,
        control = False, 
        automatic = True, 
    ),
    dict(
        name = 'bret',
        display_name='BRET', 
        app_sequence=['bret_practice', 'bret'],
        num_demo_participants=1,
    ),
]

# PARTICIPANT_FIELDS = ['match', 'encoding_payoff']


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=2.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(name='live_demo', 
        display_name='Room for live demo (no participant labels)'
    ),
    dict(
        name='sequential_search',
        display_name='Sequential Search',
        participant_label_file='_rooms/participant_label.txt',
        # use_secure_urls=True
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3922710227462'

INSTALLED_APPS = ['otree']
