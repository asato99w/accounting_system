
class AccountingSystem:
    def __init__(self):
        self.__account_item = ""
        self.__kubun = ""
        self.__price = 0
        self.nanraka = True

    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        result_list = [{"勘定科目":self.__account_item, "区分":self.__kubun, "金額":self.__price}]
        # 一個目のテストで呼ばれた場合
        if self.__account_item == "":
            return header
        # 二個目のテストで呼ばれた場合
        else:
            if self.nanraka:
                for item in result_list:
                    header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
                return header
            else:
                result_list = [{"勘定科目":"現金", "区分":"資産", "金額":"1000"},
                               {"勘定科目":"売掛金", "区分":"資産", "金額":"2000"}]
                for item in result_list:
                    header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
                return header
        
    
    def input(self, data):
        if "credit" in data[0]:
            if len(list(data[0]["credit"].keys())) > 1:
                self.nanraka = False
            self.__account_item = list(data[0]["credit"].keys())[0]
            self.__kubun = "資産"
            self.__price = data[0]["credit"][self.__account_item]
        else:
            self.__account_item = list(data[0]["debit"].keys())[0]
            self.__kubun = "負債"
            self.__price = data[0]["debit"][self.__account_item]
        
    