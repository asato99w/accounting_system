from .account_type import Asset, Liability, Equity, Revenue, Expense

class FinancialStatements:
    def __init__(self, worksheet):
        self.__pl = ProfitAndLoss(worksheet)
        self.__bs = BalanceSheet(worksheet, self.__pl)

    def __get_pl(self):
        return self.__pl

    def __get_bs(self):
        return self.__bs

    def export_pl(self, exporter):
        return self.__pl.export(exporter)

    def export_bs(self, exporter):
        return self.__bs.export(exporter)

class ProfitAndLoss:
    def __init__(self, worksheet):
        self.__profit_and_expense_account_types = [Revenue(), Expense()]

        self.__profit_line_items = self.__create_line_items(worksheet, Revenue())
        self.__expense_line_items = self.__create_line_items(worksheet, Expense())
        self.__line_items_without_net_income = self.__profit_line_items + self.__expense_line_items

        self.__net_income = self.__calculate_net_income(self.__line_items_without_net_income)
        self.__line_items = self.__line_items_without_net_income + self.__create_net_income_line(self.__net_income)

    def __create_line_items(self, worksheet, account_type):
        line_items = []
        for row in worksheet:
            if row["残高"] == 0:
                continue
            if account_type.belongs_to(row["勘定科目"]):
                line_items.append({"勘定科目": row["勘定科目"], "区分": account_type.get_type(), "金額": row["残高"]})
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

    def __get_line_items(self):
        return self.__line_items

    def get_net_income(self):
        return self.__net_income

    def export(self, exporter):
        exporter.set_header("勘定科目,区分,金額")
        exporter.set_rows(self.__get_line_items())
        return exporter.export()

class BalanceSheet:
    def __init__(self, worksheet, pl):
        self.__balance_sheet_account_types = [Asset(), Liability(), Equity()]
        self.__pl = pl

        self.__asset_line_items = self.__create_line_items(worksheet, Asset())
        self.__liability_line_items = self.__create_line_items(worksheet, Liability())
        self.__equity_line_items = self.__create_line_items(worksheet, Equity())
        self.__profit_line_items = self.__create_profit_line_items(worksheet)

    def __create_line_items(self, worksheet, account_type):
        line_items = []
        for row in worksheet:
            if account_type.belongs_to(row["勘定科目"]):
                line_items.append({"勘定科目": row["勘定科目"], "区分": account_type.get_type(), "金額": row["残高"]})

        return line_items

    def __create_profit_line_items(self, worksheet):
        line_items = []
        if self.__pl.is_profit() or self.__pl.is_loss():
            line_items.append({"勘定科目": "利益剰余金", "区分": "純資産", "金額": self.__pl.get_net_income()})

        return line_items

    def __get_line_items(self):
        return self.__asset_line_items + self.__liability_line_items + self.__equity_line_items + self.__profit_line_items

    def export(self, exporter):
        exporter.set_header("勘定科目,区分,金額")
        exporter.set_rows(self.__get_line_items())
        return exporter.export()