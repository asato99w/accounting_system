class GeneralLedger:
    def __init__(self, ledgers):
        self.__ledgers= []
        for account_item in ledgers:
            self.__ledgers.append(LedgerAccount({"勘定科目": account_item, "記入内容": ledgers[account_item]}))

    def create_trial_balance(self):
        balances = {}

        for ledger in self.__ledgers:
            balances[ledger.get_account_item()] = self.__calculate_amount(ledger)

        result = []
        for account_item in balances:
            result.append({"勘定科目": account_item, "残高": balances[account_item]})

        return result

    def __calculate_amount(self, ledger):
        credit_amount = 0
        debit_amount = 0
        for entry in ledger.get_entries():
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

class LedgerAccount:
    def __init__(self, ledger):
        self.ledger = ledger
        self.__account_item = ledger["勘定科目"]
        self.__entries = ledger["記入内容"]

    def get_account_item(self):
        return self.__account_item

    def get_entries(self):
        return self.__entries