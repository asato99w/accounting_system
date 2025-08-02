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
        trial_balance = TrialBalance()
        for ledger_account in self.__ledger_accounts:
            trial_balance = trial_balance.add_balance(ledger_account.create_balance())
        return trial_balance

class LedgerAccount:
    def __init__(self, account_item, postings):
        self.__account_item = account_item
        self.__postings = postings

    def get_account_item(self):
        return self.__account_item

    def create_balance(self):
        balance = Balance(self.__account_item)
        for posting in self.__postings:
            balance = balance.add(posting)
        return balance

class TrialBalance:
    def __init__(self):
        self.balances = []

    def get_items(self):
        return self.balances

    def add_balance(self, balance):
        self.balances.append(balance)
        return self

class Balance:
    def __init__(self, account_item, postings = []):
        self.__account_item = account_item
        self.__postings = postings

    def get_account_item(self):
        return self.__account_item

    def get_balance(self):
        return sum(self.__account_item.calculate_balance_delta(posting) for posting in self.__postings)

    def belongs_to(self, account_type):
        return self.__account_item.belongs_to(account_type)

    def add(self, posting):
        return Balance(self.__account_item, self.__postings + [posting])
