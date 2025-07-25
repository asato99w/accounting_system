
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

                mid_mid_data = [
                    {"勘定科目": "未払金", "仕分": "debit", "金額": 500},
                    {"勘定科目": "買掛金", "仕分": "debit", "金額": 2500},
                    {"勘定科目": "現金", "仕分": "debit", "金額": 500},
                    {"勘定科目": "現金", "仕分": "credit", "金額": 2000},
                    {"勘定科目": "売掛金", "仕分": "credit", "金額": 1500}
                ]
                
                nanika = {"未払金":0, "買掛金":0, "現金":0, "売掛金":0}
                # nanika = {"未払金":0, "買掛金":2500, "現金":1500, "売掛金":1500}
                # nanika_a = {"未払金":[], "買掛金":[], "現金":[], "売掛金":[]}
                nanika29 = {"未払金":[], "買掛金":[], "現金":[], "売掛金":[]}

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

                for target_dict in mid_mid_data:
                    account_item = target_dict["勘定科目"]

                    if account_item == "未払金":
                        nanika["未払金"] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]
                        
                    if account_item == "買掛金":
                        if target_dict["仕分"] == "debit":
                            nanika["買掛金"] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]
                        else:
                            nanika["買掛金"] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]
                    
                    if account_item == "現金":
                        if target_dict["仕分"] == "credit":
                            nanika["現金"] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]
                        else:
                            nanika["現金"] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]

                    if account_item == "売掛金":
                        if target_dict["仕分"] == "credit":
                            nanika["売掛金"] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]
                        else:
                             nanika["売掛金"] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]

                # nanika3 = {"未払金":[500], "買掛金":[2500], "現金":[2000, -500], "売掛金":[1500]}
                # nanika3 = nanika29

                # new_nanika2 = {}
                # for key in nanika3:
                #     total_price = 0
                #     for price in nanika3[key]:
                #         total_price += price
                #     new_nanika2[key] = total_price

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