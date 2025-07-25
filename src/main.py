
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
        if not ("credit" in data[0] and "debit" in data[0]):
            raise ValueError
        

        self.list2 = []

        mid_data = []
        for key in data[0]["debit"]:
            mid_data.append({"勘定科目": key, "仕分": "debit", "金額": data[0]["debit"][key]})
        for key in data[0]["credit"]:
            mid_data.append({"勘定科目": key, "仕分": "credit", "金額": data[0]["credit"][key]})

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

        zandaka = {}
        for account_item in shiwakehyou["debit"]:
            zandaka.update({account_item: 0})
            
        for target_dict in mid_data:
            account_item = target_dict["勘定科目"]
            zandaka[account_item] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]
        kamoku_list = []
        for key in zandaka:
            kamoku_list.append({"勘定科目": key, "金額": zandaka[key]})
        credit_list = ["現金", "売掛金"]
        for target_dict in kamoku_list:
            if target_dict["勘定科目"] in credit_list:
                self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"資産", "金額":target_dict["金額"]})
        debit_list = ["未払金", "買掛金"]
        for target_dict in kamoku_list:
            if target_dict["勘定科目"] in debit_list:
                self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"負債", "金額":target_dict["金額"]})
    