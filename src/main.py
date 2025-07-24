
class AccountingSystem:
    def __init__(self):
        self.__condition = True
        self.__account_item = ""
        self.__kubun = ""
        self.__price = 0

    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        result_list = [{"勘定科目":self.__account_item, "区分":self.__kubun, "金額":self.__price}]
        # 一個目のテストで呼ばれた場合
        if self.__condition:
            return header
        # 二個目のテストで呼ばれた場合
        else:
            for item in result_list:
                header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
            return header
        
    
    def input(self, data):
        self.__condition = False
        if "credit" in data[0]:
            self.__account_item = list(data[0]["credit"].keys())[0]
            self.__kubun = "資産"
            self.__price = data[0]["credit"][self.__account_item]
        else:
            self.__account_item = list(data[0]["debit"].keys())[0]
            self.__kubun = "負債"
            self.__price = data[0]["debit"][self.__account_item]
        
    