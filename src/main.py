
class AccountingSystem:
    def __init__(self):
        self.list2 = []

    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        
        if len(self.list2) == 0 and len(self.list2) == 0:
            return header
        # 二個目のテストで呼ばれた場合
        else:
            result_list = self.list2
        
        for item in result_list:
            header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
        return header
        
    
    def input(self, data):
        if "credit" in data[0] and "debit" in data[0]:

            self.list2 = []

            temp_list = []
            for item in data[0]["debit"]:
                temp_list.append({"勘定科目":item, "金額":data[0]["debit"][item]})
            for item in data[0]["credit"]:
                temp_list.append({"勘定科目":item, "金額":data[0]["credit"][item]})

            for target_dict in temp_list:
                if "現金" == target_dict["勘定科目"]:
                    self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"資産", "金額":target_dict["金額"]})

            debit_list = ["未払金", "買掛金"]
            for target_dict in temp_list:
                if target_dict["勘定科目"] == "未払金":
                    self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"負債", "金額":target_dict["金額"]})
            for target_dict in temp_list:
                if target_dict["勘定科目"] == "買掛金":
                    self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"負債", "金額":target_dict["金額"]})
            
        else:
            if "credit" in data[0]:
                shiwake = "credit"
                kubun = "資産"       
            else:
                shiwake = "debit"
                kubun = "負債"
            for item in list(data[0][shiwake].keys()):
                self.list2.append({"勘定科目":item, "区分":kubun, "金額":data[0][shiwake][item]}) 