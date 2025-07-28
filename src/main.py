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
        jb = JournalBook()
        jb.make_entries(data)
        gl = GeneralLedger(jb.create_general_ledger())
        tb = gl.create_trial_balance()
        self.__fs = FinancialStatements(tb)

class JournalBook:
    def __init__(self):
        self.__entries = []
        self.__account_items = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "受取利息", "給料", "地代家賃", "水道光熱費"]

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

        return result

class GeneralLedger:
    def __init__(self, ledgers):
        self.__ledgers = ledgers

    def create_trial_balance(self):
        balances = {}

        for account_item in self.__ledgers:
            balances[account_item] = self.__calculate_amount(account_item)

        result = []
        for account_item in balances:
            result.append({"勘定科目": account_item, "残高": balances[account_item]})

        return result

    def __calculate_amount(self, account_item):
        credit_amount = 0
        debit_amount = 0
        for entry in self.__ledgers[account_item]:
            if entry["仕分"] == "debit":
                debit_amount += entry["金額"]
            else:
                credit_amount += entry["金額"]

        if debit_amount - credit_amount > 0:
            side = "debit"
            amount = debit_amount - credit_amount
        else:
            side = "credit"
            amount = credit_amount - debit_amount
        return [amount, side]
