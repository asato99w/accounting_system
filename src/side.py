class Side:
    DEBIT = "借方"
    CREDIT = "貸方"

    def __init__(self, side):
        self.__side = side

    def get_side(self):
        return self.__side

    def __eq__(self, other):
        return self.__side == other.__side

    def __hash__(self):
        return hash(self.__side)

class CreditSide(Side): # TODO: サブクラスでequalsが機能するようにする
    def __init__(self):
        super().__init__(Side.CREDIT)

class DebitSide(Side):
    def __init__(self):
        super().__init__(Side.DEBIT)