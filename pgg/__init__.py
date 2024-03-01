from otree.api import *
import random, json, os
import re

c = Currency

doc = """
"""


class Constants(BaseConstants):
    ''' oTree 基本設定 '''
    name_in_url = 'PGG'
    players_per_group = 4
    num_rounds = 1

    '''PGG 參數'''
    multiplier = 2
    endowment = 20
    pgg_num_rounds = 10

    '''「甲」和「乙」的驗證基數'''
    a_role_val_num = 2
    b_role_val_num = 2

    '''跟報酬有關的變數'''
    a_role_payoff = 100
    a_role_bonus = 100
    b_role_payoff = 100
    b_role_bonus = 100
    viewer_guess_bonus = 5

    '''自行輸入 ID 的字數限制'''
    user_id_len_min = 6
    user_id_len_max = 12

    '''個資問題的數量變數'''
    num_quest = 25
    num_quest_need = 20 # 暫時改掉 20/1

    info_ques_lst = ["q" + str(i) for i in range(1, num_quest + 1)]

    with open('./html_txt/A_info_ques_dct.json', 'r', encoding='utf-8') as f1:
        A_info_ques_dct = json.load(f1)
    f1.close

    with open('./html_txt/B_info_ques_dct.json', 'r', encoding='utf-8') as f2:
        B_info_ques_dct = json.load(f2)
    f2.close

    width = '850px'
    height = '1.7'


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


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    '''是否同意「知情同意書」'''
    approval = models.BooleanField(label="請勾選以下選項。", choices=[[True, "我已詳閱此同意書，並同意參與這個研究案"], [False, "我不願意參與這個研究案"]])

    '''跟 treatment 有關的參數'''
    id_treatment = models.StringField()
    contri_treatment = models.StringField()
    file = models.StringField()
    pgg_role = models.StringField()
    pgg_id = models.StringField(label='請輸入您為自己取的 ID：(ID 只可使用英文大小寫及數字，6-12位元)', blank=True)
    pgg_id_checking = models.StringField(label='請輸入您被系統分配的 ID：', blank=True)

    wait_page_arrival = models.FloatField()
    started_pgg_decision = models.BooleanField()
    jump_to_questionaire = models.BooleanField()
    '''quit id:
    對於 sys_id 的人來說，quit id 就是他被系統分配的 id；
    但對於 user_id 的人，需要在一開始分配一個 ID 給他。'''
    quit_id = models.StringField(blank=True)

    '''
    個資填答框
    - 對「甲」來說：他需要挑選「20 個」進行回答。
    - 對「乙」來說：他需要將某甲授權給他的 20 項資料填入
    '''
    q1 = models.StringField(blank=True)
    q2 = models.StringField(blank=True)
    q3 = models.StringField(blank=True)
    q4 = models.StringField(blank=True)
    q5 = models.StringField(blank=True)
    q6 = models.StringField(blank=True)
    q7 = models.StringField(blank=True)
    q8 = models.StringField(blank=True)
    q9 = models.StringField(blank=True)
    q10 = models.StringField(blank=True)
    q11 = models.StringField(blank=True)
    q12 = models.StringField(blank=True)
    q13 = models.StringField(blank=True)
    q14 = models.StringField(blank=True)
    q15 = models.StringField(blank=True)
    q16 = models.StringField(blank=True)
    q17 = models.StringField(blank=True)
    q18 = models.StringField(blank=True)
    q19 = models.StringField(blank=True)
    q20 = models.StringField(blank=True)
    q21 = models.StringField(blank=True)
    q22 = models.StringField(blank=True)
    q23 = models.StringField(blank=True)
    q24 = models.StringField(blank=True)
    q25 = models.StringField(blank=True)

    '''理解測驗'''
    comprehension_answer = models.StringField(blank=True)


def choose_file_for_B(): #file_lst
    import math
    file = str()
    index = str()

    with open("./generated_data/id_for_info_authorization.json", "r") as f1:
        info_from_A = json.load(f1)
        lst = []
        for key, value in info_from_A.items():
            lst.append(value["name"])
        return random.sample(lst, 1)[0] + ".json"


# 建立 Session
def creating_session(subsession: Subsession):
    id_generated = tuple()
    id_generated = subsession.gen_id_for_session()

    # 用來記錄「乙」所使用的授權資料，避免重複。
    info_from_A_lst = list()
    file_lst = []

    # 開始分配「角色」、「ID Treatment」、「Contri Treatment」
    for player in subsession.get_players():
        player.participant.jump_to_questionaire = False
        player.participant.pgg_role = player.pgg_role = subsession.pgg_role()
        player.participant.id_treatment = player.id_treatment = subsession.id_treatment()
        player.participant.contri_treatment = player.contri_treatment = subsession.contri_treatment()

        # 若 ID Treatment 為系統分配，在此進行分配。
        if subsession.id_treatment() == 'id_sys':
            player.participant.pgg_id = id_generated[player.id_in_group - 1]
            player.pgg_id = id_generated[player.id_in_group - 1]
            player.quit_id = id_generated[player.id_in_group - 1]
        else:
            player.quit_id = id_generated[player.id_in_group - 1]

        # 若 PGG 的角色為「乙」，將其需要填寫的「某甲」資訊，存入其 field 中。

        if subsession.pgg_role() == 'B':
            path = "./generated_data/info_authorization/"
            file = str()

            file = choose_file_for_B() #file_lst
            print(file)
            player.file = file

            with open(os.path.join(path, file), 'r', encoding='utf-8') as f2:
                data = json.load(f2)
                for key, value in data.items():
                    if key in Constants.info_ques_lst:
                        player.participant.vars[key] = value


# User ID 檢查函數：ID 只可使用英文大小寫及數字、6-12位元
def id_user_format_error(user_id):
    # 6-12 位元
    if len(user_id) < Constants.user_id_len_min or len(user_id) > Constants.user_id_len_max:
        return True
    # ID 只可使用英文大小寫及數字
    try:
        re.search("[^A-Za-z0-9]+", user_id).group()
        return True
    except:
        return False


# ID 檢查函數：檢查此 ID 未被其他場次或其他組別的任何玩家使用。
def check_user_id_is_unique(entered_id, player: Player):
    # System ID 全被保留，不可以被使用。
    with open('./generated_data/sys_id.json', 'r', encoding='utf-8') as f1:
        data = json.load(f1)
        for key, value in data.items():
            if value["ID"] == entered_id:
                return True

    # 已被使用過的 User ID 不可以再使用
    with open('./generated_data/user_id.json', 'r+', encoding='utf-8') as f2:
        data = json.load(f2)
        for value in data.values():
            if value == entered_id:
                return True
        f2.close()


# 個資檢查函數 for 甲：確保甲填寫的格式符合要求
def check_info_format(info_id, submit_ans):
    if submit_ans == "":
        return "pass"

    # 視力（左/右）
    if info_id == "q1":
        try:
            left, right = submit_ans.split("/")
        except:
            return "請以「斜線」分隔左、右眼視力"

        error_message = "左、右眼視力的格式錯誤"
        try:
            left_digit, left_decimal = left.split(".")
            right_digit, right_decimal = right.split(".")
        except:
            return error_message
        if len(left_digit) != 1 or len(left_decimal) != 1 or len(right_digit) != 1 or len(
                right_decimal) != 1 or not left_digit.isdigit() or not left_decimal.isdigit() or not right_digit.isdigit() or not right_decimal.isdigit() or "-" in submit_ans:
            return error_message
    # 血壓（收縮壓和舒張壓）
    elif info_id == "q2":
        try:
            low, high = submit_ans.split("/")
        except:
            return "請以「斜線」分隔收縮壓和舒張壓"

        error_message = "收縮壓和舒張壓皆需為正整數"
        if not low.isdigit() or not high.isdigit() or "-" in submit_ans:
            return error_message
    # 身高
    elif info_id == "q3":
        error_message = "身高必須為數字"
        if not submit_ans.isdigit() and "." not in submit_ans:
            return error_message
        elif "-" in submit_ans:
            return error_message
    # 齲齒:
    elif info_id == "q4":
        error_message = "答案必須為「有」或「無」"
        if submit_ans != "有" and submit_ans != "無":
            return error_message
    # 牙結石:
    elif info_id == "q5":
        error_message = "答案必須為「有」或「無」"
        if submit_ans != "有" and submit_ans != "無":
            return error_message
    # 性別：
    elif info_id == "q6":
        error_message = "答案必須為「M」或「F」"
        if submit_ans != "M" and submit_ans != "F":
            return error_message
    # 姓氏
    elif info_id == "q7":
        pass
    # 身分證第一碼（英文字母）
    elif info_id == "q8":
        error_message = "答案的長度需為一"
        if len(submit_ans) != 1:
            return error_message

        error_message = "輸入必須為大寫英文字母"
        if ord(submit_ans) < ord("A") or ord(submit_ans) > ord("Z"):
            return error_message

    # 身分證後三碼
    elif info_id == "q9":
        error_message = "身分證後三碼必須為數字"
        if not submit_ans.isdigit() or "-" in submit_ans:
            return error_message

        error_message = "答案的長度需為三"
        if len(submit_ans) != 3:
            return error_message
    # 婚姻狀態
    elif info_id == "q10":
        error_message = "答案必須為「未婚」、「已婚」、「配偶歿」"
        if submit_ans != "未婚" and submit_ans != "已婚" and submit_ans != "配偶歿":
            return error_message
    # 生日
    elif info_id == "q11":
        error_message = "請以「斜線」分隔收縮壓和舒張壓"
        try:
            month, day = submit_ans.split("/")
        except:
            return error_message

        error_message = "月份和日期皆須為數字"
        if not month.isdigit() or not day.isdigit() or "-" in submit_ans:
            return error_message
    # 母親姓氏
    elif info_id == "q12":
        pass
    # 身分證上地址的里
    elif info_id == "q13":
        error_message = "答案請以「村」、「里」結尾"
        if submit_ans[-1] != "村" and submit_ans[-1] != "里":
            return error_message
    # 手機末三碼
    elif info_id == "q14":
        error_message = "手機末三碼必須為數字"
        for number in submit_ans:
            if not number.isdigit():
                return error_message

        error_message = "答案的長度需為三"
        if len(submit_ans) != 3:
            return error_message
    # 瀏覽器最近關閉的3個分頁名稱（非連結）
    elif info_id == "q15":
        error_message = "三個欄位都需要填寫"
        if submit_ans["web1"] == "" or submit_ans["web2"] == "" or submit_ans["web3"] == "":
            return error_message
    # 當前位置（經緯度）
    elif info_id == "q16":
        error_message = "請以「逗點」分隔經度和緯度"
        try:
            latitude, longitude = submit_ans.split(",")
        except:
            return error_message

    # 一部最近瀏覽/按讚的Youtube影片或一位訂閱的youtuber
    elif info_id == "q17":
        pass
    # 最近一學期，週三週四下午的任一門課
    elif info_id == "q18":
        pass
    # 入學至今一門停修的課（從未停修請填無）
    elif info_id == "q19":
        pass
    # 任一兩個月內發票的消費金額
    elif info_id == "q20":
        error_message = "消費金額必須為數字"
        if not submit_ans.isdigit() or "-" in submit_ans:
            return error_message
    # 手機型號（廠牌及機型）
    elif info_id == "q21":
        pass
    # 是否使用助學貸款
    elif info_id == "q22":
        error_message = "答案必須為「是」、「否」"
        if submit_ans != "是" and submit_ans != "否":
            return error_message
    # 是否曾接受新冠肺炎檢測
    elif info_id == "q23":
        error_message = "答案必須為「是」、「否」"
        if submit_ans != "是" and submit_ans != "否":
            return error_message
    # 是否接種新冠肺炎疫苗
    elif info_id == "q24":
        error_message = "答案必須為「是」、「否」"
        if submit_ans != "是" and submit_ans != "否":
            return error_message
    # 就醫紀錄中的一個醫院名稱
    elif info_id == "q25":
        pass

    return "pass"


# 決定 PGG 報酬
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
            group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    for p in players:
        p.payoff = Constants.endowment - p.contribution + group.individual_share


class Arrival_Page_Before_Screen_1(WaitPage):
    template_name = '_templates/global/MyWaitPage.html'
    group_by_arrival_time = True

    title_text = "請您耐心等待"
    body_text = "實驗可能隨時開始，您至多需要等待十五分鐘。"

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Quit_after_Screen_0(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.approval == False

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "participation_fee": 50,
        }


# Screen 1
class Screen_1(Page):
    @staticmethod
    def js_vars(player: Player):
        return Constants.A_info_ques_dct

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


# Screen 1 理解測驗
class Screen_1_comprehension_info(Page):
    form_model = 'player'
    form_fields = ['comprehension_answer']
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


# Screen 2
class Screen_2(Page):
    form_model = 'player'
    form_fields = Constants.info_ques_lst.copy()

    @staticmethod
    def js_vars(player: Player):
        if player.pgg_role == 'A':
            return Constants.A_info_ques_dct
        elif player.pgg_role == 'B':
            info_from_A = dict()
            Constants.B_info_ques_dct.copy()
            for index in Constants.info_ques_lst:
                if player.participant.vars[index] != str():
                    info_from_A[index] = dict()
                    info_from_A[index]["info"] = Constants.B_info_ques_dct[index]["info"]
                    info_from_A[index]["val"] = Constants.B_info_ques_dct[index]["val"]
                    info_from_A[index]["info_from_A"] = player.participant.vars[index]
            return info_from_A

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def live_method(player: Player, values):
        error_message = "pass"
        if player.pgg_role == 'A':
            error_message = check_info_format(values["info_no"], values["ans"])

        return {
            player.id_in_group: {"id": values["info_no"], "message": error_message, "ans": values["ans"]}
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.pgg_role == 'A':
            player.participant.q1 = player.q1
            player.participant.q2 = player.q2
            player.participant.q3 = player.q3
            player.participant.q4 = player.q4
            player.participant.q5 = player.q5
            player.participant.q6 = player.q6
            player.participant.q7 = player.q7
            player.participant.q8 = player.q8
            player.participant.q9 = player.q9
            player.participant.q10 = player.q10
            player.participant.q11 = player.q11
            player.participant.q12 = player.q12
            player.participant.q13 = player.q13
            player.participant.q14 = player.q14
            player.participant.q15 = player.q15
            player.participant.q16 = player.q16
            player.participant.q17 = player.q17
            player.participant.q18 = player.q18
            player.participant.q19 = player.q19
            player.participant.q20 = player.q20
            player.participant.q21 = player.q21
            player.participant.q22 = player.q22
            player.participant.q23 = player.q23
            player.participant.q24 = player.q24
            player.participant.q25 = player.q25


# Screen 3: feedback page
class Screen_3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    def vars_for_template(player: Player):
        info = [player.q1, player.q2, player.q3, player.q4, player.q5, player.q6, player.q7, player.q8, player.q9,
                player.q10, player.q11, player.q12, player.q13, player.q14, player.q15, player.q16, player.q17,
                player.q18, player.q19, player.q20, player.q21, player.q22, player.q23, player.q24, player.q25]

        cnt = 1
        card_dct = dict()
        for index, item in enumerate(info):
            if item != "" and player.pgg_role == 'A':
                card_dct["info_{}".format(cnt)] = Constants.A_info_ques_dct['q' + str(index + 1)]["info_short"]
                cnt += 1
            elif item != "" and player.pgg_role == 'B':
                card_dct["info_{}".format(cnt)] = Constants.B_info_ques_dct['q' + str(index + 1)]["info_short"]
                cnt += 1

        while cnt <= 20:
            card_dct["info_{}".format(cnt)] = "上頁有未填"
            cnt += 1

        return card_dct


# 第一個決策項目結束
class Screen_3_completed(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


# Screen_4
class Screen_4(Page):
    form_model = 'player'
    form_fields = ['pgg_id', 'pgg_id_checking']

    @staticmethod
    def error_message(player: Player, values):
        if player.id_treatment == 'id_sys' and values['pgg_id_checking'] != player.pgg_id:
            return "您輸入的id需和系統分配的id一致。"
        elif player.id_treatment == 'id_user' and id_user_format_error(values["pgg_id"]):
            return "id只可使用英文大小寫及數字，且長度須介於6-12位元。"
        elif player.id_treatment == 'id_user':
            if check_user_id_is_unique(values["pgg_id"], player):
                return "此id已被其他玩家使用。"

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.id_treatment == 'id_user':
            player.participant.pgg_id = player.pgg_id
        # import time
        # player.wait_page_arrival = time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


# Screen_5
class Screen_5(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Screen_5_comprehension_pgg(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time
        player.participant.wait_page_arrival = time.time()
        player.participant.started_pgg_decision = False

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        group_count = Constants.players_per_group
        should_skip_pgg_decistion = False
        checked_in_count = 1  # 先算自己一份

        # 取得有開始第一階段的總人數
        for p in player.get_others_in_subsession():
            if p.participant.vars.get('approval') == True:
                checked_in_count += 1
        # sprint('每組人數: ' + str(group_count) + ', 已報到總人數: ' + str(checked_in_count))

        if checked_in_count % group_count == 0:
            # 整除，可以恰恰好分組，無需作任何跳過
            return upcoming_apps[0]

        # 取得其他已進到下一階段的人數
        started_pgg_decision_count = 0
        for p in player.get_others_in_subsession():
            if p.participant.vars.get('started_pgg_decision') == True:
                started_pgg_decision_count += 1

        # 三個條件都滿足
        not_first_group = started_pgg_decision_count >= group_count  # 第一組的不算，不然無法判斷。
        not_divisible = ((
                                 started_pgg_decision_count + 1) % group_count) > 0  # 其他已完成的人加上我，如果不能夠被該組人數整除就代表我會是多出來的人。 # +1 代表要算自己一份。
        is_remainder = (
                               checked_in_count - started_pgg_decision_count) < group_count  # 全部 approved 人數 扣掉已經去到下一階段的人，也就是我和剩下的其他人，如果湊不成一組，就代表需要跳過遊戲。
        # 例如，考慮這個 case：1. 已報到 10人 每組4人，我是第8號，如果只看 10-7 < 4，會出問題，因為我第8號是可以剛好湊齊，其他第二組的人正在等我。
        # 例如，考慮這個 case：2. 已報到 5人 每組2人，我是第5號，我是會多出來的人，而且 5-4 < 2 也成立，我必須跳過。
        if not_first_group and not_divisible and is_remainder:
            should_skip_pgg_decistion = True

        print('  其他已進到下一階段的人數: ' + str(started_pgg_decision_count))
        print('should_skip_pgg_decistion: ' + str(should_skip_pgg_decistion))
        print('---')
        if should_skip_pgg_decistion:
            player.participant.jump_to_questionaire = True
            # 自己是多出來無法整除的人，跳到下下階段
            return upcoming_apps[1]
        else:
            return upcoming_apps[0]


page_sequence = [Quit_after_Screen_0, Screen_1, Screen_1_comprehension_info, Screen_2,
                 Screen_3, Screen_3_completed, Screen_4, Screen_5,
                 Screen_5_comprehension_pgg]
# Arrival_Page_Before_Screen_1
