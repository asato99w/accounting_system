from .account_type import Asset, Liability, Equity, Revenue, Expense
from .csv_exporter import CSVExporter
from .financial_statements import FinancialStatements

class AccountingSystem:
    def __init__(self):
        self.__fs = None

    def output_balance_sheet(self):
        if self.__fs is None:
            return "勘定科目,区分,金額\n"

        return self.__fs.export_bs(CSVExporter())

    def output_pl(self):
        if self.__fs is None:
            return "勘定科目,区分,金額\n"

        return self.__fs.export_pl(CSVExporter())


    def input(self, data):

        def shukei_motochou(motochou_titel, motochou_dict):
            karikata_goukei = 0
            kashikata_goukei = 0
            for kamokugoto_dict in motochou_dict[motochou_titel]:
                if kamokugoto_dict["仕分"] == "debit":
                    karikata_goukei += kamokugoto_dict["金額"]
                else:
                    kashikata_goukei += kamokugoto_dict["金額"]
            if karikata_goukei - kashikata_goukei > 0:
                shiwake = "debit"
                kingaku = karikata_goukei - kashikata_goukei
            else:
                shiwake = "credit"
                kingaku = kashikata_goukei - karikata_goukei
            return [kingaku, shiwake]

        
        jb = JournalBook()
        jb.make_entries(data)
        motochou_dict = jb.create_general_ledger()

        kamoku_list = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "受取利息", "給料", "地代家賃", "水道光熱費"]

        kamokugoto_zandaka_dict = {}
        for account_item in kamoku_list:
            kamokugoto_zandaka_dict.update({account_item: 0})

        for motochou_title in motochou_dict:
            kamokugoto_zandaka_dict[motochou_title] = shukei_motochou(motochou_title, motochou_dict)

        dict_of_kamoku_and_kingaku_list = []
        for kamokumei in kamokugoto_zandaka_dict:
            dict_of_kamoku_and_kingaku_list.append({"勘定科目": kamokumei, "金額": kamokugoto_zandaka_dict[kamokumei]})


        self.__fs = FinancialStatements(dict_of_kamoku_and_kingaku_list)

class JournalBook:
    def __init__(self):
        self.__entries = []

    def __get_entries(self):
        return self.__entries

    def make_a_entry(self, entry):
        self.__entries.append(entry)

    def make_entries(self, entries):
        for entry in entries:
            if not ("credit" in entry and "debit" in entry):
                raise ValueError

            for kamokumei in entry["debit"]:
                self.__entries.append({"勘定科目": kamokumei, "仕分": "debit", "金額": entry["debit"][kamokumei]})
            for kamokumei in entry["credit"]:
                self.__entries.append({"勘定科目": kamokumei, "仕分": "credit", "金額": entry["credit"][kamokumei]})

    def create_general_ledger(self):
        result = {}
        account_items = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "受取利息", "給料", "地代家賃", "水道光熱費"]

        for account_item in account_items:
            result.update({account_item: []})

        for entry in self.__get_entries():
            for account_item in account_items:
                if entry["勘定科目"] == account_item:
                    result[account_item].append(entry)

        return result
