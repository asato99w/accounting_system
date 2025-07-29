from .financial_statements import FinancialStatements
from .csv_exporter import CSVExporter
from .journal import JournalBook

class AccountingSystem:
    def __init__(self):
        self.__jb = JournalBook()
        self.__gl = self.__jb.create_general_ledger()

    def output_balance_sheet(self):
        self.__fs = FinancialStatements(self.__gl.create_trial_balance())
        return self.__fs.export_bs(CSVExporter())

    def output_pl(self):
        self.__fs = FinancialStatements(self.__gl.create_trial_balance())
        return self.__fs.export_pl(CSVExporter())


    def input(self, entries):
        self.__jb.make_entries(entries)
        self.__gl = self.__jb.create_general_ledger()
