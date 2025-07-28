from .account_type import Asset, Liability, Equity, Revenue, Expense

class AccountingSystem:
    def __init__(self):
        self.__fs = None

    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        if self.__fs is None:
            return header
        
        for item in self.__fs.get_bs().get_line_items():
            header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
        return header

    def output_pl(self):
        header = "勘定科目,区分,金額\n"
        if self.__fs is None:
            return header
        
        for item in self.__fs.get_pl().get_line_items():
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


        self.__fs = FinancialStatements(dict_of_kamoku_and_kingaku_list)

class FinancialStatements:
    def __init__(self, worksheet):
        self.__pl = ProfitAndLoss(worksheet)
        self.__bs = BalanceSheet(worksheet, self.__pl)

    def get_pl(self):
        return self.__pl

    def get_bs(self):
        return self.__bs

class ProfitAndLoss:
    def __init__(self, worksheet):
        self.__profit_and_expense_account_types = [Revenue(), Expense()]

        self.__line_items_without_net_income = self.__create_line_items_without_net_income(worksheet)
        self.__net_income = self.__calculate_net_income(self.__line_items_without_net_income)

        self.__line_items = self.__line_items_without_net_income + self.__create_net_income_line(self.__net_income)

    def __create_line_items_without_net_income(self, worksheet):
        line_items = []
        for account_type in self.__profit_and_expense_account_types:
            profit_and_expense_content = account_type.create_statement(worksheet)
            line_items.extend(profit_and_expense_content)

        return line_items

    def __calculate_net_income(self, line_items):
        net_income = 0
        for item in line_items:
            if item["区分"] == "収益":
                net_income += item["金額"]
            elif item["区分"] == "費用":
                net_income -= item["金額"]
        return net_income

    def __create_net_income_line(self, net_income):
        if self.is_profit():
            return [{"勘定科目": "当期純利益", "区分": "純利益", "金額": net_income}]
        elif self.is_loss():
            return [{"勘定科目": "当期純損失", "区分": "純損失", "金額": net_income * -1}]
        else:
            return []

    def is_profit(self):
        return self.__net_income > 0

    def is_loss(self):
        return self.__net_income < 0

    def get_line_items(self):
        return self.__line_items

    def get_net_income(self):
        return self.__net_income

class BalanceSheet:
    def __init__(self, worksheet, pl):
        self.__balance_sheet_account_types = [Asset(), Liability(), Equity()]
        self.__pl = pl

        self.__line_items = self.__create_line_items(worksheet)

    def __create_line_items(self, worksheet):
        line_items = []
        for account_type in self.__balance_sheet_account_types:
            balance_sheet_content = account_type.create_statement(worksheet)
            line_items.extend(balance_sheet_content)

        if self.__pl.is_profit():
            line_items.append({"勘定科目": "利益剰余金", "区分": "純資産", "金額": self.__pl.get_net_income()})
        elif self.__pl.is_loss():
            line_items.append({"勘定科目": "利益剰余金", "区分": "純資産", "金額": self.__pl.get_net_income()})

        return line_items

    def get_line_items(self):
        return self.__line_items