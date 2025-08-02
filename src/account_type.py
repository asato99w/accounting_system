from .side import Side

class AccountType:
    ASSET = "資産"
    LIABILITY = "負債"
    EQUITY = "純資産"
    REVENUE = "収益"
    EXPENSE = "費用"

    def __init__(self, account_type, accounts, side):
        self.__account_type = account_type
        self.__accounts = accounts
        self.__side = side

    def __eq__(self, other):
        return self.__account_type == other.__account_type

    def __hash__(self):
        return hash(self.__account_type)

    def get_side(self):
        return self.__side

    def get_type(self):
        return self.__account_type

class Asset(AccountType):
    accounts = ["現金", "売掛金"]
    side = Side(Side.DEBIT)
    def __init__(self):
        super().__init__(AccountType.ASSET, self.accounts, self.side)

class Liability(AccountType):
    accounts = ["未払金", "買掛金"]
    side = Side(Side.CREDIT)
    def __init__(self):
        super().__init__(AccountType.LIABILITY, self.accounts, self.side)

class Equity(AccountType):
    accounts = ["資本金"]
    side = Side(Side.CREDIT)
    def __init__(self):
        super().__init__(AccountType.EQUITY, self.accounts, self.side)

class Revenue(AccountType):
    accounts = ["売上", "受取利息"]
    side = Side(Side.CREDIT)
    def __init__(self):
        super().__init__(AccountType.REVENUE, self.accounts, self.side)

class Expense(AccountType):
    accounts = ["給料", "地代家賃", "水道光熱費", "仕入"]
    side = Side(Side.DEBIT)
    def __init__(self):
        super().__init__(AccountType.EXPENSE, self.accounts, self.side)
