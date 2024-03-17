from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='A_sysID_money',
    #     app_sequence=['check_in', 'pgg', 'pgg_decision', 'questionaire', 'mpl'],
    #     num_demo_participants=16,
    #     pgg_role='A',
    #     id_treatment='id_sys',
    #     contri_treatment='money',
    # ),

    # dict(
    #     name='A_sysID_ownInfo',
    #     app_sequence=['check_in', 'pgg', 'pgg_decision', 'questionaire', 'mpl'],
    #     num_demo_participants=16,
    #     pgg_role='A',
    #     id_treatment='id_sys',
    #     contri_treatment='own_info',F
    # ),

    dict(
        name='A_userID_money',
        app_sequence=['check_in', 'pgg', 'pgg_decision', 'questionaire', 'mpl'],
        num_demo_participants=16,
        pgg_role='A',
        id_treatment='id_user',
        contri_treatment='money',
    ),

    dict(
        name='A_userID_ownInfo',
        app_sequence=['check_in', 'pgg', 'pgg_decision', 'questionaire', 'mpl'],
        num_demo_participants=16,
        pgg_role='A',
        id_treatment='id_user',
        contri_treatment='own_info',
    ),

    # dict(
    #     name='B_sysID_otherInfo',
    #     app_sequence=['check_in', 'pgg', 'pgg_decision', 'questionaire', 'mpl'],
    #     num_demo_participants=16,
    #     pgg_role='B',
    #     id_treatment='id_sys',
    #     contri_treatment='other_info',
    # ),

    dict(
        name='B_userID_otherInfo',
        app_sequence=['check_in', 'pgg', 'pgg_decision', 'questionaire', 'mpl'],
        num_demo_participants=16,
        pgg_role='B',
        id_treatment='id_user',
        contri_treatment='other_info',
    ),

    dict(
        name='test',
        app_sequence=['check_in', 'pgg', 'mpl'],
        num_demo_participants=4,
        pgg_role='A',
        id_treatment='id_user',
        contri_treatment='own_info',
    ),
]

ROOMS = [

    dict(
        name='room_1',
        display_name='room_1'
    ),

    dict(
        name='room_2',
        display_name='room_2'
    ),

    dict(
        name='room_3',
        display_name='room_3'
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=50, doc="",
    pgg_role=str(),
    id_treatment=str(),
    contri_treatment=str(),
)

PARTICIPANT_FIELDS = dict(
    approval=bool(),
    pgg_id=str(),
    pgg_role=str(),
    id_treatment=str(),
    contri_treatment=str(),
    wait_page_arrival=float(),
    q1=str(),
    q2=str(),
    q3=str(),
    q4=str(),
    q5=str(),
    q6=str(),
    q7=str(),
    q8=str(),
    q9=str(),
    q10=str(),
    q11=str(),
    q12=str(),
    q13=str(),
    q14=str(),
    q15=str(),
    q16=str(),
    q17=str(),
    q18=str(),
    q19=str(),
    q20=str(),
    q21=str(),
    q22=str(),
    q23=str(),
    q24=str(),
    q25=str(),
    started_pgg_decision=bool(),
    jump_to_questionaire = bool(),
    wait_for_15_mins = bool(),
    is_dropout = bool(),
    other_member_is_dropout = bool(),
    all_contribution = str(),
    all_contributions_dict = str(),
    pgg_questionnaire_payoff = float(),
    questionnaire_guess_other = bool(),
)

SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9820427527334'
