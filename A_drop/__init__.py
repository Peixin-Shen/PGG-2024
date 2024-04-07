from otree.api import *
import random
import json

from otree.models import player

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'drop'
    players_per_group = None
    num_rounds = 1

    svo_mine_l_1 = 85
    svo_mine_r_1 = 85
    svo_other_l_1 = 85
    svo_other_r_1 =15

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
    svo_other_r_4 =15

    svo_mine_l_5 = 100
    svo_mine_r_5 = 50
    svo_other_l_5 = 50
    svo_other_r_5 =100

    svo_mine_l_6 = 100
    svo_mine_r_6 = 85
    svo_other_l_6 = 50
    svo_other_r_6 = 85

    width = '850px'
    height = 1.7
    
# /////////////////////////

    mpl_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    mpl_dict = {}

    width = '850px'
    height = 1.7

    password = "T@ssEL864"
    wrong_password = "T@ssEL468"
    meet_link = "https://reurl.cc/jkrOl2"

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pgg_id = models.StringField(label='請輸入您剛才為自已取的 id ')
    sex = models.StringField()
    age = models.IntegerField(
        choices=[i for i in range(18,100)],
        label='2. 您的年齡是？'
    )

    blood = models.StringField(
        choices=['A型', 'B型', 'AB型', 'O型', 'Rh陰性', '未知', '以上皆非'], 
        widget = widgets.RadioSelect,
        label= '3. 您的血型是？'
    )

    native = models.StringField(
        choices=['台灣本地生', '非台灣本地生(例如僑生、外籍交換生學生) '],
        widget = widgets.RadioSelect,
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

# //////////////////
    mpl_0 = models.IntegerField()
    mpl_10 = models.IntegerField()
    mpl_20 = models.IntegerField()
    mpl_30 = models.IntegerField()
    mpl_40 = models.IntegerField()
    mpl_50 = models.IntegerField()
    mpl_60 = models.IntegerField()
    mpl_70 = models.IntegerField()
    mpl_80 = models.IntegerField()
    mpl_90 = models.IntegerField()
    mpl_100 = models.IntegerField()

    mpl_number = models.IntegerField(initial=-1)  # 電腦隨機抽價格
    mpl_agree = models.IntegerField(initial=-1)  # 有沒有成功賣出
    mpl_payoff = models.IntegerField(initial=0)  # 這個階段拿到多少錢

    check = models.IntegerField()  # 是否被抽中驗證

    password = models.StringField(label="密碼輸入", blank=True)  # 輸入RA給的密碼
    pass_check = models.IntegerField(initial=-1)  # 是否通過驗證

    link = models.StringField(blank=True)

    suggestion = models.LongStringField(
        blank=True, label="你即將完成本實驗，在今天的實驗過程中，你是否有任何的建議或感想呢？請在下方跟我們分享。")


def creating_session(subsession: Subsession):
    subsession.group_randomly()
    for p in subsession.get_players():
        if p.id % 2 == 1:
            p.check = 1
        else:
            p.check = 0

        p.link = Constants.meet_link


# PAGES
class Questionaire_1(Page):
    form_model = 'player'
    form_fields = ['pgg_id', 'sex', 'age', 'blood', 'native', 'department', 'university', 'grade', 'trust']


class Questionaire_2(Page):
    form_model = 'player'
    form_fields = ['svo_mine_1', 'svo_other_1', 'svo_mine_2', 'svo_other_2', 'svo_mine_3', 'svo_other_3', 'svo_mine_4', 'svo_other_4', 'svo_mine_5', 'svo_other_5', 'svo_mine_6', 'svo_other_6']


class Screen1(Page):
    form_model = 'player'
    form_fields = ['mpl_0', 'mpl_10', 'mpl_20', 'mpl_30', 'mpl_40',
                   'mpl_50', 'mpl_60', 'mpl_70', 'mpl_80', 'mpl_90', 'mpl_100']

    @staticmethod
    def before_next_page(player, timeout_happened):
        Constants.mpl_dict[0] = player.mpl_0
        Constants.mpl_dict[10] = player.mpl_10
        Constants.mpl_dict[20] = player.mpl_20
        Constants.mpl_dict[30] = player.mpl_30
        Constants.mpl_dict[40] = player.mpl_40
        Constants.mpl_dict[50] = player.mpl_50
        Constants.mpl_dict[60] = player.mpl_60
        Constants.mpl_dict[70] = player.mpl_70
        Constants.mpl_dict[80] = player.mpl_80
        Constants.mpl_dict[90] = player.mpl_90
        Constants.mpl_dict[100] = player.mpl_100

        player.mpl_number = random.choice(Constants.mpl_list)

        # MPL 決定捐個資與否
        if Constants.mpl_dict[player.mpl_number] == 1:
            player.mpl_agree = 1
            player.mpl_payoff = player.mpl_number
            # save_info_if_agree(player)
        else:
            player.mpl_agree = 0
            player.mpl_payoff = 0

        player.participant.payoff += player.mpl_payoff + 50

    @staticmethod
    def is_displayed(player: Player):
        return True


class Screen2(Page):
    @staticmethod
    def vars_for_template(player: Player):
    	    return {
            "total_payoff": int(player.participant.payoff+0.5)
        }


    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.check == 0:
            player.participant.payoff += 100


class Screen3(Page):
    form_model = 'player'
    form_fields = ['password']

    @staticmethod
    def is_displayed(player: Player):
        return player.check == 1

    @staticmethod
    def error_message(player: Player, values):
        if (values['password'] != Constants.password) and (values['password'] != Constants.wrong_password):
            return "請正確地輸入密碼"

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.password == Constants.password:
            player.participant.payoff += 200
            player.pass_check = 1
        else:
            player.participant.payoff += 0
            player.pass_check = 0

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "link": player.link,
            "total_payoff": int(player.participant.payoff+0.5),
            "pgg_id": '123',
        }

class Suggestion(Page):
    form_model = 'player'
    form_fields = ['suggestion']


class Screen4(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if player.pass_check == 1:
            check_payoff = 200
        elif player.pass_check == 0:
            check_payoff = 0
        else:
            check_payoff = 100

        return {

            "total_payoff": int(player.participant.payoff+0.5)
        }


page_sequence = [Questionaire_1, Questionaire_2,
                 Screen1, Screen2, Screen3, Suggestion, Screen4]
