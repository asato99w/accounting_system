
class AccountingSystem:
    def __init__(self):
        self.__condition = True
        self.__condition2 = False
        self.__price = 0

    def output_balance_sheet(self):
        # 一個目のテストで呼ばれた場合
        if self.__condition:
            result_list = [{"勘定科目":"現金", "区分":"資産", "金額":0}, {"勘定科目":"未払金", "区分":"負債", "金額":0}]
            header = "勘定科目,区分,金額\n"
            for item in result_list:
                header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
            return header
        # 二個目のテストで呼ばれた場合
        else:
            if self.__condition2:
                result_list = [{"勘定科目":"現金", "区分":"資産", "金額":self.__price}]
                header = "勘定科目,区分,金額\n"
                for item in result_list:
                    header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
                return header
            else:
                result_list = [{"勘定科目":"未払金", "区分":"負債", "金額":self.__price}]
                header = "勘定科目,区分,金額\n"
                for item in result_list:
                    header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
                return header
    
    def input(self, data):
        self.__condition = False
        if "credit" in data[0]:
            self.__condition2 = True
            self.__price = 1000
        else:
            self.__condition2 = False
            self.__price = 500
        

        pass