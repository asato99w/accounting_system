class GeneralLedger:
    def __init__(self, journal_book):
        self.__ledger_accounts = self.__create_legeder_accounts(journal_book)

    def __create_legeder_accounts(self, journal_book):
        ledgere_accounts = []
        for account_item in journal_book.get_account_items():
            postings = []
            for posting in journal_book.get_postings():
                if posting.get_account_item() == account_item:
                    postings.append(posting)
            ledgere_accounts.append(LedgerAccount(account_item, postings))
        return ledgere_accounts


    def create_trial_balance(self):
        balances = {}

        for ledger in self.__ledger_accounts:
            balances[ledger.get_account_item()] = ledger.get_balance()

        result = []
        for account_item in balances:
            result.append({"勘定科目": account_item, "残高": balances[account_item]})

        return result

class LedgerAccount:
    def __init__(self, account_item, postings):
        self.__account_item = account_item
        self.__postings = postings

    def get_account_item(self):
        return self.__account_item

    def get_balance(self):
        debit_balance = self.__calculate_debit_balance()
        credit_balance = self.__calculate_credit_balance()

        if debit_balance - credit_balance > 0:
            side = "debit"
            balance = debit_balance - credit_balance
        else:
            side = "credit"
            balance = credit_balance - debit_balance
        return [balance, side]

    def __calculate_debit_balance(self):
        return sum(posting.get_amount() for posting in self.__postings if posting.get_side() == "debit")

    def __calculate_credit_balance(self):
        return sum(posting.get_amount() for posting in self.__postings if posting.get_side() == "credit")