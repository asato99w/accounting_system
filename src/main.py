from .financial_statements import FinancialStatements
from .csv_exporter import CSVExporter
from .journal import JournalBook, CompoundJournalEntry
from .ledger import GeneralLedger

class AccountingSystem:
    def __init__(self):
        self.__jb = JournalBook()
        self.__gl = GeneralLedger(self.__jb)

    def output_balance_sheet(self):
        self.__fs = FinancialStatements(self.__gl.create_trial_balance())
        return self.__fs.export_bs(CSVExporter())

    def output_pl(self):
        self.__fs = FinancialStatements(self.__gl.create_trial_balance())
        return self.__fs.export_pl(CSVExporter())


    def input(self, datas):
        entries = [CompoundJournalEntry(data, self.__jb.get_account_items()) for data in datas]
        self.__jb.make_entries(entries)
        self.__gl = GeneralLedger(self.__jb)
