from .ledger import GeneralLedger

class JournalBook:
    def __init__(self):
        self.__account_items = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "受取利息", "給料", "地代家賃", "水道光熱費"]
        self.__entries = []

    def __get_entries(self):
        return self.__entries

    def make_a_entry(self, entry):
        self.__entries.append(entry)

    def make_entries(self, entries):
        for entry in entries:
            if not ("credit" in entry and "debit" in entry):
                raise ValueError
            entry = CompoundJournalEntry(entry)
            self.make_a_entry(entry)

    def create_general_ledger(self):
        postings = []
        for entry in self.__entries:
            postings.extend(entry.get_postings())

        result = {}
        for account_item in self.__account_items:
            result.update({account_item: []})

        for posting in postings:
            for account_item in result:
                if posting["勘定科目"] == account_item:
                    result[account_item].append(posting)

        return GeneralLedger(result)


class CompoundJournalEntry:
    def __init__(self, data):
        self.__debit = data["debit"]
        self.__credit = data["credit"]

    def get_postings(self):
        postings = []
        for account_item in self.__debit:
            postings.append({"勘定科目": account_item, "仕分": "debit", "金額": self.__debit[account_item]})
        for account_item in self.__credit:
            postings.append({"勘定科目": account_item, "仕分": "credit", "金額": self.__credit[account_item]})
        return postings