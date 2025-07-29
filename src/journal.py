from .ledger import GeneralLedger

class JournalBook:
    def __init__(self):
        self.__account_items = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "受取利息", "給料", "地代家賃", "水道光熱費"]
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
    def __init__(self, data):
        if not ("credit" in data and "debit" in data):
            raise ValueError
        self.__debit_postings = self.__create_postings(data, "debit")
        self.__credit_postings = self.__create_postings(data, "credit")

    def __create_postings(self, data, side):
        postings = []
        for account_item in data[side]:
            postings.append({"勘定科目": account_item, "仕分": side, "金額": data[side][account_item]})
        return postings

    def get_postings(self):
        return self.__debit_postings + self.__credit_postings