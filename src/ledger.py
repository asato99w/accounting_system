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
        for account_item in self.__ledger_accounts:
            result.append({"勘定科目": account_item.get_account_item().get_name(), "残高": account_item.get_balance()})

        return result

class LedgerAccount:
    def __init__(self, account_item, postings):
        self.__account_item = account_item
        self.__postings = postings

    def get_account_item(self):
        return self.__account_item

    def get_balance(self):
        balance = sum(self.__account_item.calculate_balance_delta(posting) for posting in self.__postings)
        return balance