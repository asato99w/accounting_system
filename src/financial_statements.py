from .account_type import Asset, Liability, Equity, Revenue, Expense

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