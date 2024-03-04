from otree.api import *

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'questionaire'
    players_per_group = None
    num_rounds = 1

    svo_mine_l_1 = 85
    svo_mine_r_1 = 85
    svo_other_l_1 = 85
    svo_other_r_1 = 15

    svo_mine_l_2 = 85
    svo_mine_r_2 = 100
    svo_other_l_2 = 15
    svo_other_r_2 = 50

    svo_mine_l_3 = 50
    svo_mine_r_3 = 85
    svo_other_l_3 = 100
    svo_other_r_3 = 85

    svo_mine_l_4 = 50
    svo_mine_r_4 = 85
    svo_other_l_4 = 100
    svo_other_r_4 = 15

    svo_mine_l_5 = 100
    svo_mine_r_5 = 50
    svo_other_l_5 = 50
    svo_other_r_5 = 100

    svo_mine_l_6 = 100
    svo_mine_r_6 = 85
    svo_other_l_6 = 50
    svo_other_r_6 = 85

    width = '850px'
    height = 1.7


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    sex = models.StringField()

    age = models.IntegerField(
        choices=[i for i in range(18, 100)],
        label='2. 您的年齡是？'
    )

    blood = models.StringField(
        choices=['A型', 'B型', 'AB型', 'O型', 'Rh陰性', '未知', '以上皆非'],
        widget=widgets.RadioSelect,
        label='3. 您的血型是？'
    )

    native = models.StringField(
        choices=['台灣本地生', '非台灣本地生(例如僑生、外籍交換生學生) '],
        widget=widgets.RadioSelect,
        label='4. 您是否為台灣本地生？'
    )

    university = models.StringField()

    department = models.StringField()

    grade = models.StringField()

    trust = models.IntegerField(
        choices=[[1, '1 = 與人相處須謹慎提防'], [2, '2'], [
            3, '3'], [4, '4'], [5, '5 = 大多數人是可以信任的']],
        widget=widgets.RadioSelect,
        label='8. 一般來說，您是否認為大多數的人是可以信任的，或者您認為與人相處時須謹慎提防？請在1到5的等級中，選擇最能描述您觀點的數字。'
    )

    svo_mine_1 = models.IntegerField()
    svo_other_1 = models.IntegerField()
    svo_mine_2 = models.IntegerField()
    svo_other_2 = models.IntegerField()
    svo_mine_3 = models.IntegerField()
    svo_other_3 = models.IntegerField()
    svo_mine_4 = models.IntegerField()
    svo_other_4 = models.IntegerField()
    svo_mine_5 = models.IntegerField()
    svo_other_5 = models.IntegerField()
    svo_mine_6 = models.IntegerField()
    svo_other_6 = models.IntegerField()


class redirect_page(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.jump_to_questionaire == True

    @staticmethod
    def vars_for_template(player: Player):

        return {
            "pgg_id": player.participant.pgg_id,
            "wait_for_15_mins": player.participant.wait_for_15_mins,
            "is_dropout": player.participant.other_member_is_dropout,
        }


class Questionaire_1(Page):
    form_model = 'player'
    form_fields = ['sex', 'age', 'blood', 'native', 'department', 'university', 'grade', 'trust']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pgg_role": player.participant.pgg_role,
        }


class Questionaire_2(Page):
    form_model = 'player'
    form_fields = ['svo_mine_1', 'svo_other_1', 'svo_mine_2', 'svo_other_2', 'svo_mine_3', 'svo_other_3', 'svo_mine_4',
                   'svo_other_4', 'svo_mine_5', 'svo_other_5', 'svo_mine_6', 'svo_other_6']


page_sequence = [redirect_page, Questionaire_1, Questionaire_2]
