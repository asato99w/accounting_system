class AccountType:
    ASSET = "資産"
    LIABILITY = "負債"
    EQUITY = "純資産"
    REVENUE = "収益"
    EXPENSE = "費用"

    def __init__(self, account_type, accounts):
        self.__account_type = account_type
        self.__accounts = accounts
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

    def get_side(self):
        return self.__side

    def get_type(self):
        return self.__account_type

    def belongs_to(self, account_name):
        return account_name in self.__accounts

class Asset(AccountType):
    accounts = ["現金", "売掛金"]
    def __init__(self):
        super().__init__(AccountType.ASSET, self.accounts)

class Liability(AccountType):
    accounts = ["未払金", "買掛金"]
    def __init__(self):
        super().__init__(AccountType.LIABILITY, self.accounts)

class Equity(AccountType):
    accounts = ["資本金"]
    def __init__(self):
        super().__init__(AccountType.EQUITY, self.accounts)

class Revenue(AccountType):
    accounts = ["売上", "受取利息"]
    def __init__(self):
        super().__init__(AccountType.REVENUE, self.accounts)

class Expense(AccountType):
    accounts = ["給料", "地代家賃", "水道光熱費", "仕入"]
    def __init__(self):
        super().__init__(AccountType.EXPENSE, self.accounts)

        