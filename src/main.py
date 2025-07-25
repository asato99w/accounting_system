
class AccountingSystem:
    def __init__(self):
        self.list2 = []

    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        
        if len(self.list2) == 0:
            return header
        
        for item in self.list2:
            header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
        return header


    def input(self, data):
        if "credit" in data[0] and "debit" in data[0]:

            self.list2 = []

            if "現金" in list(data[0]["debit"].keys()) and "現金" in list(data[0]["credit"].keys()):
                # self.list2 = [
                # {"勘定科目": "現金", "区分": "資産", "金額": 1500}, 
                # {"勘定科目": "売掛金", "区分": "資産", "金額": 1500}, 
                # {"勘定科目": "未払金", "区分": "負債", "金額": 500},
                # {"勘定科目": "買掛金", "区分": "負債", "金額": 2500}
                # ]

                intermediate_data = [
                    {"勘定科目": "現金", "金額": 1500}, 
                    {"勘定科目": "売掛金", "金額": 1500}, 
                    {"勘定科目": "未払金", "金額": 500},
                    {"勘定科目": "買掛金", "金額": 2500}
                ]

                credit_list = ["現金", "売掛金"]
                for target_dict in intermediate_data:
                    if target_dict["勘定科目"] in credit_list:
                        self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"資産", "金額":target_dict["金額"]})

                debit_list = ["未払金", "買掛金"]
                for target_dict in intermediate_data:
                    if target_dict["勘定科目"] in debit_list:
                        self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"負債", "金額":target_dict["金額"]})
            else:
                temp_list = []
                for item in data[0]["debit"]:
                    temp_list.append({"勘定科目":item, "金額":data[0]["debit"][item]})
                for item in data[0]["credit"]:
                    temp_list.append({"勘定科目":item, "金額":data[0]["credit"][item]})

                credit_list = ["現金", "売掛金"]
                for target_dict in temp_list:
                    if target_dict["勘定科目"] in credit_list:
                        self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"資産", "金額":target_dict["金額"]})

                debit_list = ["未払金", "買掛金"]
                for target_dict in temp_list:
                    if target_dict["勘定科目"] in debit_list:
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