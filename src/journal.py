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

            for account_item in entry["debit"]:
                self.__entries.append({"勘定科目": account_item, "仕分": "debit", "金額": entry["debit"][account_item]})
            for account_item in entry["credit"]:
                self.__entries.append({"勘定科目": account_item, "仕分": "credit", "金額": entry["credit"][account_item]})

    def create_general_ledger(self):
        result = {}

        for account_item in self.__account_items:
            result.update({account_item: []})

        for entry in self.__get_entries():
            for account_item in self.__account_items:
                if entry["勘定科目"] == account_item:
                    result[account_item].append(entry)

        return GeneralLedger(result)
