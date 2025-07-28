# test
class AccountingSystem:
    def __init__(self):
        self.__pl_content_dict_list = []
        self.__kamoku_kubun_kingaku_list = []


    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        
        if len(self.__kamoku_kubun_kingaku_list) == 0:
            return header
        
        for item in self.__kamoku_kubun_kingaku_list:
            header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
        return header
    
    def output_pl(self):


        header = "勘定科目,区分,金額\n"

        for item in self.__pl_content_dict_list:
            header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
        return header


    def input(self, data):

        def format_data(data):
            result = []
            for trade in data:
                if not ("credit" in trade and "debit" in trade):
                    raise ValueError

                for kamokumei in trade["debit"]:
                    result.append({"勘定科目": kamokumei, "仕分": "debit", "金額": trade["debit"][kamokumei]})
                for kamokumei in trade["credit"]:       
                    result.append({"勘定科目": kamokumei, "仕分": "credit", "金額": trade["credit"][kamokumei]})
            return result

        def create_motochou(data):
            motocho_dict = {
                "未払金": [],
                "買掛金": [],
                "現金": [],
                "売掛金": [],
                "資本金": [],
                "売上": [],
                "受取利息": [],
                "給料": [],
                "地代家賃": [],
                "水道光熱費": []
            }
            for kamokugoto_dict in data:
                for motocho_title in motocho_dict:
                    if kamokugoto_dict["勘定科目"] == motocho_title:
                        motocho_dict[motocho_title].append(kamokugoto_dict)
            return motocho_dict

        def shukei_motochou(motochou_titel, motochou_dict):
            karikata_goukei = 0
            kashikata_goukei = 0
            for kamokugoto_dict in motochou_dict[motochou_titel]:
                if kamokugoto_dict["仕分"] == "debit":
                    karikata_goukei += kamokugoto_dict["金額"]
                else:
                    kashikata_goukei += kamokugoto_dict["金額"]
            if karikata_goukei - kashikata_goukei > 0:
                shiwake = "debit"
                kingaku = karikata_goukei - kashikata_goukei
            else:
                shiwake = "credit"
                kingaku = kashikata_goukei - karikata_goukei
            return [kingaku, shiwake]

        
        formated_data = format_data(data)
        motochou_dict = create_motochou(formated_data)

        kamoku_list = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "受取利息", "給料", "地代家賃", "水道光熱費"]

        kamokugoto_zandaka_dict = {}
        for account_item in kamoku_list:
            kamokugoto_zandaka_dict.update({account_item: 0})

        for motochou_title in motochou_dict:
            kamokugoto_zandaka_dict[motochou_title] = shukei_motochou(motochou_title, motochou_dict)

        dict_of_kamoku_and_kingaku_list = []
        for kamokumei in kamokugoto_zandaka_dict:
            dict_of_kamoku_and_kingaku_list.append({"勘定科目": kamokumei, "金額": kamokugoto_zandaka_dict[kamokumei]})

        balance_sheet_account_types = [Asset(), Liability(), Equity()]
        for account_type in balance_sheet_account_types:
            balance_sheet_content = account_type.create_statement(dict_of_kamoku_and_kingaku_list)
            self.__kamoku_kubun_kingaku_list.extend(balance_sheet_content)

        profit_and_expense_account_types = [Revenue(), Expense()]
        for account_type in profit_and_expense_account_types:
            profit_and_expense_content = account_type.create_statement(dict_of_kamoku_and_kingaku_list)
            self.__pl_content_dict_list.extend(profit_and_expense_content)

        net_income = 0
        for item in self.__pl_content_dict_list:
            if item["区分"] == "収益":
                net_income += item["金額"]
            elif item["区分"] == "費用":
                net_income -= item["金額"]

        if net_income > 0:
            self.__pl_content_dict_list.append({"勘定科目": "当期純利益", "区分": "純利益", "金額": net_income})
            self.__kamoku_kubun_kingaku_list.append({"勘定科目": "利益剰余金", "区分": "純資産", "金額": net_income})
        elif net_income < 0:
            self.__pl_content_dict_list.append({"勘定科目": "当期純損失", "区分": "純損失", "金額": net_income * -1})
            self.__kamoku_kubun_kingaku_list.append({"勘定科目": "利益剰余金", "区分": "純資産", "金額": net_income})


class AccountType:
    ASSET = "資産"
    LIABILITY = "負債"
    EQUITY = "純資産"
    REVENUE = "収益"
    EXPENSE = "費用"

    def __init__(self, account_type, accounts, skip_zero=False):
        self.__account_type = account_type
        self.__accounts = accounts
        self.__skip_zero = skip_zero
        self.__side = self.__set_side(account_type)

    def __set_side(self, account_type):
        if account_type == "資産":
            self.__side = "debit"
        elif account_type == "負債":
            self.__side = "credit"
        elif account_type == "純資産":
            self.__side = "credit"
        elif account_type == "収益":
            self.__side = "credit"
        elif account_type == "費用":
            self.__side = "debit"
        return self.__side

    def create_statement(self, worksheet):
        result = []
        for row in worksheet:
            if self.__skip_zero and row["金額"][0] == 0:
                continue

            if row["勘定科目"] in self.__accounts:
                increase_or_decrease = 1 if row["金額"][1] == self.__side else -1
                result.append({"勘定科目":row["勘定科目"], "区分":self.__account_type, "金額":row["金額"][0] * increase_or_decrease})
        return result


class Asset(AccountType):
    accounts = ["現金", "売掛金"]
    def __init__(self, skip_zero=False):
        super().__init__(AccountType.ASSET, self.accounts, skip_zero)

class Liability(AccountType):
    accounts = ["未払金", "買掛金"]
    def __init__(self, skip_zero=False):
        super().__init__(AccountType.LIABILITY, self.accounts, skip_zero)

class Equity(AccountType):
    accounts = ["資本金"]
    def __init__(self, skip_zero=False):
        super().__init__(AccountType.EQUITY, self.accounts, skip_zero)

class Revenue(AccountType):
    accounts = ["売上", "受取利息"]
    def __init__(self, skip_zero=True):
        super().__init__(AccountType.REVENUE, self.accounts, skip_zero)

class Expense(AccountType):
    accounts = ["給料", "地代家賃", "水道光熱費"]
    def __init__(self, skip_zero=True):
        super().__init__(AccountType.EXPENSE, self.accounts, skip_zero)

        