from otree.api import *
import random, json


from otree.models import player

c = Currency

doc = """
PGG version 1.0.0
"""


class Constants(BaseConstants):
    ''' oTree 基本設定 '''
    name_in_url = 'PGG_decision'
    players_per_group = 4
    num_rounds = 10 # 暫時改掉 10/3

    '''PGG 參數'''
    multiplier = 2
    endowment = 20

    '''「甲」和「乙」的驗證基數'''
    a_role_val_num = 2
    b_role_val_num = 2

    '''跟報酬有關的變數'''
    a_role_payoff = 100
    a_role_bonus = 100
    b_role_payoff = 100
    b_role_bonus = 100
    viewer_guess_bonus = 5

    '''提醒作答的秒數'''
    timeout_seconds = 45
    remind_seconds = 5
    timeout_seconds_5mins_left = 600 #暫時改掉 600/180
    num_quest = 25
    num_quest_need = 20

    width = '850px'
    height = '1.7'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # PGG 中該組的總貢獻量
    total_contribution = models.IntegerField()
    # PGG 中個人能分到的小組份額
    individual_share = models.CurrencyField()


def make_field(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        label=label,
        widget=widgets.RadioSelect,
    )

class Player(BasePlayer):
    '''跟 treatment 有關的參數'''
    pgg_role = models.StringField()
    id_treatment = models.StringField()
    contri_treatment = models.StringField()
    pgg_id = models.StringField()
    wait_page_arrival = models.FloatField()

    '''跟報酬有關的 treatment '''
    contribution = models.IntegerField(
        label='',
        min=0,
        max=Constants.endowment,
    )

    '''決策時間'''
    decision_duration = models.StringField()

    ## 給報酬頁面使用
    id_1 = models.StringField()
    id_2 = models.StringField()
    id_3 = models.StringField()
    id_4 = models.StringField()

    contribution_1 = models.IntegerField()
    contribution_2 = models.IntegerField()
    contribution_3 = models.IntegerField()
    contribution_4 = models.IntegerField()

    # 跟 eliciting belief 有關的參數
    level_increasing_1 = make_field('我後來意識到__對我沒這麼重要')
    level_increasing_2 = make_field('我後來意識到__對其他人來說很重要')
    level_increasing_3 = make_field('我試圖影響其他組員下期的貢獻量')
    level_increasing_4 = make_field('我受到其他組員上期的貢獻量影響')
    level_increasing_5 = make_field('我感覺我的貢獻量對他人無影響')
    level_increasing_other = models.StringField(blank=True)

    level_decreasing_1 = make_field('我後來意識到__對我來說很重要')
    level_decreasing_2 = make_field('我後來意識到__對其他人來說沒這麼重要')
    level_decreasing_3 = make_field('我試圖影響其他組員下期的貢獻量')
    level_decreasing_4 = make_field('我受到其他組員上期的貢獻量影響')
    level_decreasing_5 = make_field('我感覺我的貢獻量對他人無影響')
    level_decreasing_other = models.StringField(blank=True)

    level_unchanging_1 = make_field('__對我來說的重要性')
    level_unchanging_2 = make_field('__對其他人來的重要性')
    level_unchanging_3 = make_field('我試圖影響其他組員的貢獻量')
    level_unchanging_4 = make_field('我受到其他組員的貢獻量影響')
    level_unchanging_5 = make_field('我感覺我的貢獻量對他人無影響')
    level_unchanging_other = models.StringField(blank=True)

    other_increasing = models.BooleanField()
    other_decreasing = models.BooleanField()
    other_increasing_dict = models.StringField()
    other_decreasing_dict = models.StringField()

    level_guess_increasing_1 = make_field('他們後來意識到__對他們沒這麼重要')
    level_guess_increasing_2 = make_field('他們後來意識到__對其他人來說很重要')
    level_guess_increasing_3 = make_field('他們試圖影響其他組員下期的貢獻量')
    level_guess_increasing_4 = make_field('他們受到其他組員上期的貢獻量影響')
    level_guess_increasing_5 = make_field('他們感覺他們的貢獻量對他人無影響')
    level_guess_increasing_other = models.StringField(blank=True)

    level_guess_decreasing_1 = make_field('他們後來意識到__對他們來說很重要')
    level_guess_decreasing_2 = make_field('他們後來意識到__對其他人來說沒這麼重要')
    level_guess_decreasing_3 = make_field('他們試圖影響其他組員下期的貢獻量')
    level_guess_decreasing_4 = make_field('他們受到其他組員上期的貢獻量影響')
    level_guess_decreasing_5 = make_field('他們感覺他們的貢獻量對他人無影響')
    level_guess_decreasing_other = models.StringField(blank=True)




def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            player.participant.all_contribution = str("[]")
            player.participant.all_contributions_dict = str("{}")
            player.participant.pgg_questionnaire_payoff = 0
            player.other_increasing = False
            player.other_decreasing = False
            player.other_increasing_dict = str('{}')
            player.other_decreasing_dict = str('{}')

            player.pgg_role = player.participant.pgg_role
            player.id_treatment = player.participant.id_treatment
            player.contri_treatment = player.participant.contri_treatment
            if player.id_treatment == 'id_sys':
                player.pgg_id = player.participant.pgg_id
        else:
            player.pgg_role = player.in_round(1).pgg_role
            player.id_treatment = player.in_round(1).id_treatment
            player.contri_treatment = player.in_round(1).contri_treatment
            if player.id_treatment == 'id_sys':
                player.pgg_id = player.in_round(1).pgg_id


# 決定 PGG 報酬
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
            group.total_contribution * Constants.multiplier / Constants.players_per_group
    )

    for p in players:

        # 紀錄個人每回合的貢獻量，給 questionaire 使用
        ind_contribution = eval(p.participant.all_contribution)
        ind_contribution.append(p.contribution)
        p.participant.all_contribution = str(ind_contribution)

        # 紀錄組員每回合的貢獻量，給 questionaire 使用
        others=p.get_others_in_group()
        all_contributions = eval(p.participant.all_contributions_dict)
        for member in others:
            member_contribution = all_contributions.get(member.pgg_id, [])
            member_contribution.append(member.contribution)
            all_contributions[member.pgg_id] = member_contribution
        p.participant.all_contributions_dict = str(all_contributions)

        # 計算報酬
        p.payoff = Constants.endowment - p.contribution + group.individual_share

    ##給報酬頁面使用

    id_list = []
    contribution_list = []
    for p in random.sample(players, 4):
        id_list.append(p.participant.pgg_id)
        contribution_list.append(p.contribution)

    for p in players:
        number_list = [0, 1, 2, 3]
        num_1 = random.choice(number_list)
        number_list.remove(num_1)
        num_2 = random.choice(number_list)
        number_list.remove(num_2)
        num_3 = random.choice(number_list)
        number_list.remove(num_3)
        num_4 = random.choice(number_list)
        number_list.remove(num_4)

        p.id_1 = id_list[num_1]
        p.id_2 = id_list[num_2]
        p.id_3 = id_list[num_3]
        p.id_4 = id_list[num_4]

        p.contribution_1 = contribution_list[num_1]
        p.contribution_2 = contribution_list[num_2]
        p.contribution_3 = contribution_list[num_3]
        p.contribution_4 = contribution_list[num_4]


def waiting_too_long(player):
    participant = player.participant
    import time
    print(time.time())
    return time.time() - participant.wait_page_arrival > 900 # 暫時改掉 900/120


def group_by_arrival_time_method(subsession, waiting_players):
    num_players = [p for p in waiting_players]
    if len(num_players) >= Constants.players_per_group:
        return num_players[0:Constants.players_per_group]
    for player in waiting_players:
        if waiting_too_long(player):
            return [player]


class Arrival_Page_Before_Screen_6(WaitPage):
    template_name = 'pgg_decision/Arrival_Page_Before_Screen_6.html'
    group_by_arrival_time = True
    title_text = "請等待"
    body_text = "請您耐心等待其他受試者完成第一階段的決策項目後，再一同進入實驗。"

    @staticmethod
    def is_displayed(player: Player):
        should_display = player.round_number == 1
        return should_display

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        group = player.group
        if len(group.get_players()) == 1:
            player.participant.wait_for_15_mins = True
            player.participant.jump_to_questionaire = True
            return upcoming_apps[0]

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pgg_id": player.participant.pgg_id,
        }


# 第二個決策項目 - 決策
class Screen_6(Page):
    form_model = 'player'
    form_fields = ['contribution', 'decision_duration']

    timeout_seconds = 900 #暫時改掉 900/300
    timer_text = '倒數計時 5 分鐘仍未作答，系統將結束此階段實驗：'

    @staticmethod
    def js_vars(player):
        player.participant.started_pgg_decision = True ###
        return {
            "timeout_seconds": Constants.timeout_seconds,
            "remind_seconds": Constants.remind_seconds,
            "timeout_seconds_5mins_left": Constants.timeout_seconds_5mins_left,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.pgg_id = player.participant.pgg_id
        if timeout_happened:
            player.participant.is_dropout = True
            player.contribution = 20

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pgg_id": player.participant.pgg_id,
        }


# 第二個決策項目 - 等待頁面
class Wait_Page_Before__Screen_7(WaitPage):
    template_name = '_templates/global/MyWaitPage.html'
    title_text = "請等待"
    body_text = "請您耐心等待您的組員。"

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)


# 第二個決策項目 - 報酬
class Screen_7(Page):
    timeout_seconds = 300 #暫時改掉 300/120
    timer_text = '請確認您此回合的報酬，倒數計時 5 分鐘仍未按下一頁，系統將自動跳轉：'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "player_preserve": Constants.endowment - player.contribution,
            "pgg_id": player.participant.pgg_id,
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        group = player.group
        players = group.get_players()
        group_is_dropout = [p.participant.is_dropout for p in players]
        if True in group_is_dropout:
            player.participant.jump_to_questionaire = True
            player.participant.other_member_is_dropout = True
            # player
            return upcoming_apps[0]


class Screen_8(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "pgg_total_payoff": sum([p.payoff for p in player.in_all_rounds()]),
        }



def is_increasing(data):
    increasing = False
    for i in range(1, len(data)):
        num_1 = data[i-1]
        num_2 = data[i]
        if num_1 < num_2:
            increasing = True
            break
    return increasing
    

def is_decreasing(data):
    decreasing = False
    for i in range(1, len(data)):
        num_1 = data[i-1]
        num_2 = data[i]
        if num_1 > num_2:
            decreasing = True
            break
    return decreasing


# 第二階段 - 影響貢獻量原因問卷（增加）
class questionnaire_1(Page):
    form_model = 'player'
    form_fields = ['level_increasing_1', 'level_increasing_2', 'level_increasing_3', 'level_increasing_4', 'level_increasing_5', 'level_increasing_other']
    
    timeout_seconds = 300 # 暫時改掉 300/120
    timer_text = '請盡速作答，倒數計時 5 分鐘仍未作答，系統將自動跳到下一頁：'

    @staticmethod
    def is_displayed(player: Player):
        all_contribution = eval(player.participant.all_contribution)
        if player.round_number == Constants.num_rounds and is_increasing(all_contribution) == True:
            return True
        else:
            return False
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.level_increasing_1 = 99
            player.level_increasing_2 = 99
            player.level_increasing_3 = 99
            player.level_increasing_4 = 99
            player.level_increasing_5 = 99


# 第二階段 - 影響貢獻量原因問卷（減少）    
class questionnaire_2(Page):
    form_model = 'player'
    form_fields = ['level_decreasing_1', 'level_decreasing_2', 'level_decreasing_3', 'level_decreasing_4', 'level_decreasing_5', 'level_decreasing_other']

    timeout_seconds = 300 # 暫時改掉 300/120
    timer_text = '請盡速作答，倒數計時 5 分鐘仍未作答，系統將自動跳到下一頁：'

    @staticmethod
    def is_displayed(player: Player):
        all_contribution = eval(player.participant.all_contribution)
        if player.round_number == Constants.num_rounds and is_decreasing(all_contribution) == True:
            return True
        else:
            return False
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.level_decreasing_1 = 99
            player.level_decreasing_2 = 99
            player.level_decreasing_3 = 99
            player.level_decreasing_4 = 99
            player.level_decreasing_5 = 99

# 第二階段 - 影響貢獻量原因問卷（不變）
class questionnaire_3(Page):
    form_model = 'player'
    form_fields = ['level_unchanging_1', 'level_unchanging_2', 'level_unchanging_3', 'level_unchanging_4', 'level_unchanging_5', 'level_unchanging_other']

    timeout_seconds = 300 # 暫時改掉 300/120
    timer_text = '請盡速作答，倒數計時 5 分鐘仍未作答，系統將自動跳到下一頁：'

    @staticmethod
    def is_displayed(player: Player):
        all_contribution = eval(player.participant.all_contribution)
        if player.round_number == Constants.num_rounds and is_increasing(all_contribution) == False and is_decreasing(all_contribution) == False:
            return True
        else:
            return False
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.level_unchanging_1 = 99
            player.level_unchanging_2 = 99
            player.level_unchanging_3 = 99
            player.level_unchanging_4 = 99
            player.level_unchanging_5 = 99
    

def record_member_questionnaire_data(group: Group):
    players = group.get_players()
    for p in players:
        all_contributions = eval(p.participant.all_contributions_dict)
        for member_contribution in all_contributions.values():
            p.other_increasing = False
            if is_increasing(member_contribution) == True:
                p.other_increasing = True # 供 page 判斷要不要顯示組員增加貢獻量原因的問卷
                others=p.get_others_in_group()
                answer_dict = {'1':[], '2':[], '3':[], '4':[], '5':[]}
                for member in others:
                    if member.field_maybe_none('level_increasing_1'):
                        answer_dict['1'].append(member.level_increasing_1)
                    if member.field_maybe_none('level_increasing_2'):
                        answer_dict['2'].append(member.level_increasing_2)
                    if member.field_maybe_none('level_increasing_3'):
                        answer_dict['3'].append(member.level_increasing_3)
                    if member.field_maybe_none('level_increasing_4'):
                        answer_dict['4'].append(member.level_increasing_4)
                    if member.field_maybe_none('level_increasing_5'):
                        answer_dict['5'].append(member.level_increasing_5)
                p.other_increasing_dict = str(answer_dict)
                break
        for member_contribution in all_contributions.values():
            p.other_decreasing = False
            if is_decreasing(member_contribution) == True:
                p.other_decreasing = True
                others=p.get_others_in_group()
                answer_dict = {'1':[], '2':[], '3':[], '4':[], '5':[]}
                for member in others:
                    if member.field_maybe_none('level_decreasing_1'):
                        answer_dict['1'].append(member.level_decreasing_1)
                    if member.field_maybe_none('level_decreasing_2'):
                        answer_dict['2'].append(member.level_decreasing_2)
                    if member.field_maybe_none('level_decreasing_3'):
                        answer_dict['3'].append(member.level_decreasing_3)
                    if member.field_maybe_none('level_decreasing_4'):
                        answer_dict['4'].append(member.level_decreasing_4)
                    if member.field_maybe_none('level_decreasing_5'):
                        answer_dict['5'].append(member.level_decreasing_5)
                p.other_decreasing_dict = str(answer_dict)
                break

# 第二階段 - 猜測影響組員貢獻量的原因問卷（前置等待頁面）
class Wait_Page_Before_questionnaire_4(WaitPage):
    template_name = '_templates/global/MyWaitPage.html'
    title_text = "請等待"
    body_text = "請您耐心等待您的組員。"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def after_all_players_arrive(group: Group):
        record_member_questionnaire_data(group)


import math
def myround(val):
  d,v = math.modf(val)
  if d==0.5:
    val += 0.000000001
  return round(val)

# 第二階段 - 猜測影響組員貢獻量的原因問卷（增加）
class questionnaire_4(Page):
    form_model = 'player'
    form_fields = ['level_guess_increasing_1', 'level_guess_increasing_2', 'level_guess_increasing_3', 'level_guess_increasing_4', 'level_guess_increasing_5', 'level_guess_increasing_other']
    
    timeout_seconds = 300 # 暫時改掉 300/120
    timer_text = '請盡速作答，倒數計時 5 分鐘仍未作答，系統將自動跳到下一頁：'

    @staticmethod
    def is_displayed(player: Player):

        if player.round_number == Constants.num_rounds and player.other_increasing == True:
            return True
        else:
            return False
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        if timeout_happened:
            player.level_guess_increasing_1 = 99
            player.level_guess_increasing_2 = 99
            player.level_guess_increasing_3 = 99
            player.level_guess_increasing_4 = 99
            player.level_guess_increasing_5 = 99
        
        correct_count = 0
        data = eval(player.other_increasing_dict)
        if player.level_guess_increasing_1 == myround(sum(data['1'])/len(data['1'])):
            correct_count += 1
        if player.level_guess_increasing_2 == myround(sum(data['2'])/len(data['2'])):
            correct_count += 1
        if player.level_guess_increasing_3 == myround(sum(data['3'])/len(data['3'])):
            correct_count += 1
        if player.level_guess_increasing_4 == myround(sum(data['4'])/len(data['4'])):
            correct_count += 1
        if player.level_guess_increasing_5 == myround(sum(data['5'])/len(data['5'])):
            correct_count += 1

        player.participant.pgg_questionnaire_payoff += 5*correct_count
    


# 第二階段 - 猜測影響組員貢獻量的原因問卷（減少）
class questionnaire_5(Page):
    form_model = 'player'
    form_fields = ['level_guess_decreasing_1', 'level_guess_decreasing_2', 'level_guess_decreasing_3', 'level_guess_decreasing_4', 'level_guess_decreasing_5', 'level_guess_decreasing_other']
    
    timeout_seconds = 300 # 暫時改掉 300/120
    timer_text = '請盡速作答，倒數計時 5 分鐘仍未作答，系統將自動跳到下一頁：'

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == Constants.num_rounds and player.other_decreasing == True:
            return True
        else:
            return False
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        if timeout_happened:
            player.level_guess_decreasing_1 = 99
            player.level_guess_decreasing_2 = 99
            player.level_guess_decreasing_3 = 99
            player.level_guess_decreasing_4 = 99
            player.level_guess_decreasing_5 = 99

        correct_count = 0
        data = eval(player.other_decreasing_dict)
        if player.level_guess_decreasing_1 == myround(sum(data['1'])/len(data['1'])):
            correct_count += 1
        if player.level_guess_decreasing_2 == myround(sum(data['2'])/len(data['2'])):
            correct_count += 1
        if player.level_guess_decreasing_3 == myround(sum(data['3'])/len(data['3'])):
            correct_count += 1
        if player.level_guess_decreasing_4 == myround(sum(data['4'])/len(data['4'])):
            correct_count += 1
        if player.level_guess_decreasing_5 == myround(sum(data['5'])/len(data['5'])):
            correct_count += 1

        player.participant.pgg_questionnaire_payoff += 5*correct_count


class questionnaire_completed(Page):
    # 1. 有回答猜測組員貢獻量問卷的人：顯示問卷獲得多少錢
    # 2. 不必回答猜測組員貢獻量問卷的人：顯示第二階段結束的語句

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds
    
    @staticmethod
    def vars_for_template(player: Player):
        if player.other_increasing == True or player.other_decreasing == True:
            player.participant.questionnaire_guess_other = True
        return {
            "questionnaire_guess_other": player.participant.questionnaire_guess_other,
            "correct_count": int(player.participant.pgg_questionnaire_payoff/5), # int()
            "pgg_questionnaire_payoff":player.participant.pgg_questionnaire_payoff,
        }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.payoff += player.participant.pgg_questionnaire_payoff



        


page_sequence = [Arrival_Page_Before_Screen_6, Screen_6, Wait_Page_Before__Screen_7, Screen_7, Screen_8, 
                 questionnaire_1, questionnaire_2, questionnaire_3, Wait_Page_Before_questionnaire_4, questionnaire_4, questionnaire_5, questionnaire_completed]
