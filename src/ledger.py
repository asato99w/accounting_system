class GeneralLedger:
    def __init__(self, journal_book):
        self.__ledger_accounts = self.__create_legeder_accounts(journal_book)

    def __create_legeder_accounts(self, journal_book):
        ledgere_accounts = []
        for account_item in journal_book.get_account_items().get_items():
            postings = []
            for posting in journal_book.get_postings():
                if posting.get_account_item().get_name() == account_item.get_name():
                    postings.append(posting)
            ledgere_accounts.append(LedgerAccount(account_item, postings))
        return ledgere_accounts


    def create_trial_balance(self):
        result = []
        for ledger_account in self.__ledger_accounts:
            result.append(ledger_account.create_balance())

        return TrialBalance(result)

class LedgerAccount:
    def __init__(self, account_item, postings):
        self.__account_item = account_item
        self.__postings = postings

    def get_account_item(self):
        return self.__account_item

    def __get_balance(self):
        balance = sum(self.__account_item.calculate_balance_delta(posting) for posting in self.__postings)
        return balance

    def create_balance(self):
        return Balance(self.__account_item, self.__get_balance())

class TrialBalance:
    def __init__(self, data):
        self.data = data

    def get_items(self):
        return self.data

class Balance:
    def __init__(self, account_item, balance):
        self.__account_item = account_item
        self.__balance = balance

    def get_account_item(self):
        return self.__account_item

    def get_balance(self):
        return self.__balance

    def belongs_to(self, account_type):
        return self.__account_item.belongs_to(account_type)
