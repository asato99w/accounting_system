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
            if self.__skip_zero and row["残高"][0] == 0:
                continue

            if row["勘定科目"] in self.__accounts:
                increase_or_decrease = 1 if row["残高"][1] == self.__side else -1
                result.append({"勘定科目":row["勘定科目"], "区分":self.__account_type, "金額":row["残高"][0] * increase_or_decrease})
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

        