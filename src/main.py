
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
                
                new_mid_mid_data = []
                for key in data[0]["debit"]:
                    new_mid_mid_data.append({"勘定科目": key, "仕分": "debit", "金額": data[0]["debit"][key]})
                for key in data[0]["credit"]:
                    new_mid_mid_data.append({"勘定科目": key, "仕分": "credit", "金額": data[0]["credit"][key]})

                shiwakehyou = {
                    "debit": {
                        "未払金": 1,
                        "買掛金": 1,
                        "現金": -1,
                        "売掛金": -1
                    },
                    "credit": {
                        "未払金": -1,
                        "買掛金": -1,
                        "現金": 1,
                        "売掛金": 1
                    }
                }

                new_nanika = {}
                for account_item in shiwakehyou["debit"]:
                    new_nanika.update({account_item: 0})

                nanika = new_nanika

                mid_mid_data = new_mid_mid_data

                for target_dict in mid_mid_data:
                    account_item = target_dict["勘定科目"]
                    nanika[account_item] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]

                nanika2 = {"未払金":500, "買掛金":2500, "現金":1500, "売掛金":1500}

                nanika2 = nanika
                

                nanika2_list = []
                for key in nanika2:
                    nanika2_list.append({"勘定科目": key, "金額": nanika2[key]})

                intermediate_data = [
                    {"勘定科目": "未払金", "金額": 500},
                    {"勘定科目": "買掛金", "金額": 2500},
                    {"勘定科目": "現金", "金額": 1500}, 
                    {"勘定科目": "売掛金", "金額": 1500} 
                ]

                intermediate_data = nanika2_list

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