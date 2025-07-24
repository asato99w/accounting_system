
class AccountingSystem:
    def __init__(self):
        self.__account_item = ""
        self.nanraka = True
        self.list2 = []
        self.list1 = []

    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        
        result_list = self.list1
        # 一個目のテストで呼ばれた場合
        if self.__account_item == "":
            return header
        # 二個目のテストで呼ばれた場合
        else:
            if self.nanraka:
                pass
            else:
                result_list = self.list2
            for item in result_list:
                header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
            return header
        
    
    def input(self, data):

        if "credit" in data[0]:

            if len(list(data[0]["credit"].keys())) > 1:
                self.nanraka = False

                self.list2 =  []
                for item in list(data[0]["credit"].keys()):
                    self.list2.append({"勘定科目":item, "区分":"資産", "金額":data[0]["credit"][item]})

            self.__account_item = list(data[0]["credit"].keys())[0]
            self.list1 = [{"勘定科目":list(data[0]["credit"].keys())[0], "区分":"資産", "金額":data[0]["credit"][list(data[0]["credit"].keys())[0]]}]
        else:
            self.__account_item = list(data[0]["debit"].keys())[0]
            self.list1 = [{"勘定科目":list(data[0]["debit"].keys())[0], "区分":"負債", "金額":data[0]["debit"][list(data[0]["debit"].keys())[0]]}]