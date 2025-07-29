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