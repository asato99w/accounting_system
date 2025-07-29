class GeneralLedger:
    def __init__(self, journal_book):
        self.__ledger_accounts = self.__create_legeder_accounts(journal_book)

    def __create_legeder_accounts(self, journal_book):
        ledgere_accounts = []
        for account_item in journal_book.get_account_items():
            postings = []
            for posting in journal_book.get_postings():
                if posting["勘定科目"] == account_item:
                    postings.append(posting)
            ledgere_accounts.append(LedgerAccount({"勘定科目": account_item, "転記内容": postings}))
        return ledgere_accounts


    def create_trial_balance(self):
        balances = {}

        for ledger in self.__ledger_accounts:
            balances[ledger.get_account_item()] = ledger.get_amount()

        result = []
        for account_item in balances:
            result.append({"勘定科目": account_item, "残高": balances[account_item]})

        return result

class LedgerAccount:
    def __init__(self, ledger):
        self.ledger = ledger
        self.__account_item = ledger["勘定科目"]
        self.__entries = ledger["転記内容"]

    def get_account_item(self):
        return self.__account_item

    def get_amount(self):
        debit_amount = self.__calculate_debit_amount()
        credit_amount = self.__calculate_credit_amount()

        if debit_amount - credit_amount > 0:
            side = "debit"
            amount = debit_amount - credit_amount
        else:
            side = "credit"
            amount = credit_amount - debit_amount
        return [amount, side]

    def __calculate_debit_amount(self):
        return sum(entry["金額"] for entry in self.__entries if entry["仕分"] == "debit")

    def __calculate_credit_amount(self):
        return sum(entry["金額"] for entry in self.__entries if entry["仕分"] == "credit")