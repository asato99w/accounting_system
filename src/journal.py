from .ledger import GeneralLedger
from .account_type import AccountType, Asset, Liability, Equity, Revenue, Expense

class JournalBook:
    def __init__(self):
        self.__account_items = AccountItems()
        self.__entries = []

    def __get_entries(self):
        return self.__entries

    def get_account_items(self):
        return self.__account_items

    def make_a_entry(self, entry):
        self.__entries.append(entry)

    def make_entries(self, entries):
        for entry in entries:
            self.make_a_entry(entry)

    def get_postings(self):
        postings = []
        for entry in self.__entries:
            postings.extend(entry.get_postings())
        return postings


class CompoundJournalEntry:
    def __init__(self, data, account_items):
        if not ("credit" in data and "debit" in data):
            raise ValueError
        self.__debit_postings = self.__create_postings(data, "debit", account_items)
        self.__credit_postings = self.__create_postings(data, "credit", account_items)

    def __create_postings(self, data, side, account_items):
        postings = []
        for account_item in data[side]:
            postings.append(Posting(account_items.get_item(account_item), side, data[side][account_item]))
        return postings

    def get_postings(self):
        return self.__debit_postings + self.__credit_postings

class Posting:
    def __init__(self, account_item, side, amount):
        self.__account_item = account_item
        self.__side = side
        self.__amount = amount

    def get_account_item(self):
        return self.__account_item
    
    def get_side(self):
        return self.__side

    def get_amount(self):
        return self.__amount

class AccountItems:
    def __init__(self):
        self.account_item_names = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "受取利息", "給料", "仕入", "地代家賃", "水道光熱費"]
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
                return AccountItem(name, Revenue(skip_zero=True))
        for account_name in Expense.accounts:
            if account_name == name:
                return AccountItem(name, Expense(skip_zero=True))
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

    def get_name(self):
        return self.__name