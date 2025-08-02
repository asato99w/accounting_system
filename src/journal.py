from .ledger import GeneralLedger
from .account_item import AccountItems
from .side import CreditSide, DebitSide

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
        self.__postings = self.__create_postings(data, account_items)

    def __create_postings(self, data, account_items):
        postings = []
        for side in ["credit", "debit"]:
            for account_item in data[side]:
                if side == "credit":
                    side_instance = CreditSide()
                else:
                    side_instance = DebitSide()
                postings.append(Posting(account_items.get_item(account_item), side_instance, data[side][account_item]))
        return postings

    def get_postings(self):
        return self.__postings

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
