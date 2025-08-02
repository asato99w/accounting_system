from .account_type import AccountType, Asset, Liability, Equity, Revenue, Expense

class AccountItems:
    def __init__(self):
        self.account_item_names = Asset.accounts + Liability.accounts + Equity.accounts + Revenue.accounts + Expense.accounts
        self.__account_items = []
        for account_item_name in self.account_item_names:
            self.__account_items.append(self.create_account_item(account_item_name))

    def create_account_item(self, name):
        for account_name in Asset.accounts:
            if account_name == name:
                return AccountItem(name, Asset())
        for account_name in Liability.accounts:
            if account_name == name:
                return AccountItem(name, Liability())
        for account_name in Equity.accounts:
            if account_name == name:
                return AccountItem(name, Equity())
        for account_name in Revenue.accounts:
            if account_name == name:
                return AccountItem(name, Revenue())
        for account_name in Expense.accounts:
            if account_name == name:
                return AccountItem(name, Expense())
        raise ValueError

    def get_items(self):
        return self.__account_items

    def get_item(self, name):
        for account_item in self.__account_items:
            if account_item.get_name() == name:
                return account_item
        raise ValueError

class AccountItem:
    def __init__(self, name, account_type):
        self.__name = name
        self.__account_type = account_type

    def __eq__(self, other):
        return self.__name == other.__name

    def __hash__(self):
        return hash(self.__name)

    def get_name(self):
        return self.__name

    def get_side(self):
        return self.__account_type.get_side()

    def calculate_balance_delta(self, posting):
        if posting.get_side() == self.get_side():
            return posting.get_amount()
        else:
            return posting.get_amount() * -1

    def belongs_to(self, account_type):
        return self.__account_type == account_type