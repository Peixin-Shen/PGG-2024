from otree.api import *
import random, json, os

doc = """
"""

class Constants(BaseConstants):
    name_in_url = 'check_in'
    players_per_group = None
    num_rounds = 1
    width = '850px'
    height = '1.7'

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    '''是否同意「知情同意書」'''
    approval = models.BooleanField(label = "請勾選以下選項。", choices = [[True, "我已詳閱此同意書，並同意參與這個研究案"], [False, "我不願意參與這個研究案"]])

    quit_id = models.StringField(blank = True)
    wait_for_15_mins = models.BooleanField()
    is_dropout = models.BooleanField()
    other_member_is_dropout = models.BooleanField()


class Subsession(BaseSubsession):
    def pgg_role(self):
        return self.session.config['pgg_role']

    def id_treatment(self):
        return self.session.config['id_treatment']

    def contri_treatment(self):
        return self.session.config['contri_treatment']

    # 回傳該 session 中的玩家人數
    def all_player_num(self):
        return len(self.get_players())

    # 為 session 製作 ID ：在 id_sys: pgg_id; id_user: quit_id.
    def gen_id_for_session(self):
        with open('./generated_data/sys_id.json', 'r') as f_read:
            data = json.load(f_read)
            lst = list()

            for key, value in data.items():
                if value['Session_code'] == "" and len(lst) < self.all_player_num():
                    lst.append(value['ID'])
            f_read.close()

            return tuple(lst)

def creating_session(subsession: Subsession):
    id_generated = subsession.gen_id_for_session()

    # 開始分配「角色」、「ID Treatment」、「Contri Treatment」
    for player in subsession.get_players():
        player.quit_id = id_generated[player.id_in_group - 1]

# Screen 0
class Screen_0(Page):
    form_model = 'player'
    form_fields = ['approval']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "participation_fee": int(player.session.participation_fee),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.approval = player.approval
        player.participant.wait_for_15_mins = False
        player.participant.is_dropout = False
        player.participant.other_member_is_dropout = False
        if player.approval == 1:
            player.payoff += 50

page_sequence = [Screen_0]
