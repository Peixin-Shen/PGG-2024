from otree.api import *
import random, json
import math
# from otree.models import player

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mpl'
    players_per_group = None
    num_rounds = 1
    mpl_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    mpl_dict = {}

    width = '850px'
    height = 1.7

    password = "T@ssEl864"
    wrong_password = "T@ssEl468"
    meet_link = "https://ntucc.webex.com/meet/klchang"

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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

    mpl_number = models.IntegerField(initial=-1) ##電腦隨機抽價格
    mpl_agree = models.IntegerField(initial=-1) ##有沒有成功賣出
    mpl_payoff = models.IntegerField(initial=0) ##這個階段拿到多少錢

    check = models.IntegerField() ##是否被抽中驗證

    password = models.StringField(label="密碼輸入", blank=True) ##輸入RA給的密碼
    pass_check = models.IntegerField(initial=-1) ##是否通過驗證

    link = models.StringField(blank=True)

    suggestion = models.LongStringField(blank=True, label="你即將完成本實驗，在今天的實驗過程中，你是否有任何的建議或感想呢？請在下方跟我們分享。")

def creating_session(subsession:Subsession):
    subsession.group_randomly()
    for p in subsession.get_players():
        p.check = 1 #暫時改掉 random.randint(0,1)/1
        p.link = Constants.meet_link

# # 若「甲」同意授權，將他的個資另外存成 json 檔
# def save_info_if_agree(player: Player):
#     with open('./generated_data/info_authorization/{}.json'.format(player.participant.vars["pgg_id"]), 'w') as f1:
#         info = dict()
#         info["player_id"] = player.participant.vars["pgg_id"]

#         for i in range(1, 26):
#             index = "q" + str(i)
#             info[index] = player.participant.vars[index]
#         json.dump(info, f1, ensure_ascii=False, indent=4)
#         f1.close()

#     with open('./generated_data/id_for_info_authorization.json', 'r+') as f2:
#         data = json.load(f2)
#         data[str(len(data))] = {
#             "name": player.participant.vars["pgg_id"],
#             "usage": 0
#         }

#         with open('./generated_data/id_for_info_authorization.json','w') as f_write:
#             json.dump(data, f_write, ensure_ascii=False, indent=4)

#             f_write.close()
#         f2.close()

class Screen1(Page):
    form_model = 'player'
    form_fields = ['mpl_0', 'mpl_10', 'mpl_20', 'mpl_30', 'mpl_40', 'mpl_50', 'mpl_60', 'mpl_70', 'mpl_80', 'mpl_90', 'mpl_100']
    
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

        player.participant.payoff += player.mpl_payoff

    
    @staticmethod
    def is_displayed(player: Player):
        if player.participant.pgg_role == "A":
            return True
        else:
            return False



class Screen2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if player.participant.pgg_role == "A":
            return {
                "pgg_questionnaire_payoff": player.participant.pgg_questionnaire_payoff,
                "pgg_payoff": math.ceil(player.participant.payoff - player.mpl_payoff - player.participant.pgg_questionnaire_payoff - 50),
                "total_payoff": math.ceil(player.participant.payoff)
                }
        else:
            return {
                "pgg_questionnaire_payoff": player.participant.pgg_questionnaire_payoff,
                "pgg_payoff": math.ceil(player.participant.payoff - player.participant.pgg_questionnaire_payoff - 50),
                "total_payoff": math.ceil(player.participant.payoff)
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
        if player.participant.pgg_role == "A":          
            return {
                "link": player.link,
                "pgg_payoff": math.ceil(player.participant.payoff - player.mpl_payoff - 50 -100),
                "total_payoff": math.ceil(player.participant.payoff),
                "pgg_id": player.participant.pgg_id,
            }
        else:
            return {
                "link": player.link,
                "pgg_payoff": math.ceil(player.participant.payoff - 50-100),
                "total_payoff": math.ceil(player.participant.payoff),
                "pgg_id": player.participant.pgg_id,
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

        if player.participant.pgg_role == "A":
            return {
                "pgg_questionnaire_payoff": player.participant.pgg_questionnaire_payoff,
                "pgg_payoff": math.ceil(player.participant.payoff - player.mpl_payoff - player.participant.pgg_questionnaire_payoff - 50 - check_payoff),
                "total_payoff": math.ceil(player.participant.payoff),
                "pgg_id": player.participant.pgg_id,
            }
        else:
            return {
                "pgg_questionnaire_payoff": player.participant.pgg_questionnaire_payoff,
                "pgg_payoff": math.ceil(player.participant.payoff - player.participant.pgg_questionnaire_payoff - 50 - check_payoff),
                "total_payoff": math.ceil(player.participant.payoff),
                "pgg_id": player.participant.pgg_id,
            }


page_sequence = [Screen1, Screen2, Screen3, Suggestion, Screen4]
