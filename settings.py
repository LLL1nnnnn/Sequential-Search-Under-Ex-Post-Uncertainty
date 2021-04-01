from os import environ


SESSION_CONFIGS = [
    # dict(
    #     name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    # ),
    # dict(
    #     name='certainty', app_sequence=['certainty'],
    #     num_demo_participants=2
    # ),
    dict(
        name='mpl', app_sequence=['mpl'],
        num_demo_participants=1,
        lottery_a = 280, 
        lottery_b_hi = 500,
        lottery_b_lo = 100, 
    ),
    dict(
        name='search_experiment_1', app_sequence=['search','mpl','demographics'],
        num_demo_participants=1,
        # config_file = "search_pilot.csv",
        value_high = 500,
        value_low = 100,
        search_cost = 5,
        lottery_a = 280, 
        lottery_b_hi = 500,
        lottery_b_lo = 100, 
        certainty = True, 
        random = True,
    ),
    dict(
        name='search_experiment_2', app_sequence=['search','mpl','demographics'],
        num_demo_participants=1,
        # config_file = "search_pilot.csv",
        value_high = 200,
        value_low = 100,
        search_cost = 5,
        lottery_a = 145, 
        lottery_b_hi = 200,
        lottery_b_lo = 100, 
        certainty = True, 
        random = True,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3922710227462'

INSTALLED_APPS = ['otree']
