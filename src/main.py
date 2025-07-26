
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
        mid_data = []
        zandaka = {}
        kamoku_list = []
        for trade in data:
            if not ("credit" in trade and "debit" in trade):
                raise ValueError

            for key in trade["debit"]:
                mid_data.append({"勘定科目": key, "仕分": "debit", "金額": trade["debit"][key]})
            for key in trade["credit"]:
                mid_data.append({"勘定科目": key, "仕分": "credit", "金額": trade["credit"][key]})

            motocho = {
                    "未払金": [],
                    "買掛金": [],
                    "現金": [],
                    "売掛金": [],
                    "資本金": []
                }

            for target_dict in mid_data:
                for key in motocho:
                    if target_dict["勘定科目"] == key:
                        motocho[key].append(target_dict)

            shiwakehyou = {
                "debit": {
                    "未払金": 1,
                    "買掛金": 1,
                    "現金": -1,
                    "売掛金": -1,
                    "資本金": 1
                },
                "credit": {
                    "未払金": -1,
                    "買掛金": -1,
                    "現金": 1,
                    "売掛金": 1,
                    "資本金": -1
                }
            }

            shiwakehyou2 = {
                "debit": {
                    "未払金": "debit",
                    "買掛金": "debit",
                    "現金": "credit",
                    "売掛金": "credit",
                    "資本金": "debit"
                },
                "credit": {
                    "未払金": "debit",
                    "買掛金": "debit",
                    "現金": "credit",
                    "売掛金": "credit",
                    "資本金": "debit"
                }
            }

            for account_item in shiwakehyou["debit"]:
                zandaka.update({account_item: 0})

            # for target_dict in mid_data:
            #     account_item = target_dict["勘定科目"]
            #     zandaka[account_item] += target_dict["金額"] * shiwakehyou[target_dict["仕分"]][account_item]

            for key in motocho:
                nanika = 0
                nanika2 = 0
                for target_dict in motocho[key]:
                    if target_dict["仕分"] == "debit":
                        nanika += target_dict["金額"]
                    else:
                        nanika2 += target_dict["金額"]

                if nanika - nanika2 > 0:
                    shiwake = "debit"
                    kingaku = nanika - nanika2
                else:
                    shiwake = "credit"
                    kingaku = nanika2 - nanika

                zandaka[key] = [kingaku, shiwake]

            # for item in zandaka:
            #     zandaka[item] = [zandaka[item], shiwakehyou2["credit"][item]]

            for key in zandaka:
                kamoku_list.append({"勘定科目": key, "金額": zandaka[key]})

            # kamoku_list = [
            #     {"勘定科目": "未払金", "金額": [500, "debit"]},
            #     {"勘定科目": "買掛金", "金額": [2500, "debit"]},
            #     {"勘定科目": "現金", "金額": [1500, "credit"]},
            #     {"勘定科目": "売掛金", "金額": [1500, "credit"]},
            #     {"勘定科目": "資本金", "金額": [0, "debit"]}
            # ]



        credit_list = ["現金", "売掛金"]
        for target_dict in kamoku_list:
            if target_dict["勘定科目"] in credit_list:
                self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"資産", "金額":target_dict["金額"][0]})

        debit_list = ["未払金", "買掛金"]
        for target_dict in kamoku_list:
            if target_dict["勘定科目"] in debit_list:
                self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"負債", "金額":target_dict["金額"][0]})

        debit_list = ["資本金"]
        for target_dict in kamoku_list:
            if target_dict["勘定科目"] in debit_list:
                self.list2.append({"勘定科目":target_dict["勘定科目"], "区分":"純資産", "金額":target_dict["金額"][0]})
    