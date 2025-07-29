class GeneralLedger:
    def __init__(self, ledgers):
        self.__ledgers= []
        for account_item in ledgers:
            self.__ledgers.append(LedgerAccount({"勘定科目": account_item, "記入内容": ledgers[account_item]}))

    def create_trial_balance(self):
        balances = {}

        for ledger in self.__ledgers:
            balances[ledger.get_account_item()] = ledger.get_amount()

        result = []
        for account_item in balances:
            result.append({"勘定科目": account_item, "残高": balances[account_item]})

        return result

class LedgerAccount:
    def __init__(self, ledger):
        self.ledger = ledger
        self.__account_item = ledger["勘定科目"]
        self.__entries = ledger["記入内容"]

    def get_account_item(self):
        return self.__account_item

    def get_entries(self):
        return self.__entries

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