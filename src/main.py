
class AccountingSystem:
    def __init__(self):
        self.kamoku_kubun_kingaku_list = []

    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        
        if len(self.kamoku_kubun_kingaku_list) == 0:
            return header
        
        for item in self.kamoku_kubun_kingaku_list:
            header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
        return header


    def input(self, data):

        def format_data(data):
            all_data = []
            for trade in data:
                if not ("credit" in trade and "debit" in trade):
                    raise ValueError

                for kamokumei in trade["debit"]:
                    all_data.append({"勘定科目": kamokumei, "仕分": "debit", "金額": trade["debit"][kamokumei]})
                for kamokumei in trade["credit"]:
                    all_data.append({"勘定科目": kamokumei, "仕分": "credit", "金額": trade["credit"][kamokumei]})
            return all_data
        
        all_data = format_data(data)

        motocho_dict = {
                "未払金": [],
                "買掛金": [],
                "現金": [],
                "売掛金": [],
                "資本金": []
            }
        for kamokugoto_dict in all_data:
            for motocho_title in motocho_dict:
                if kamokugoto_dict["勘定科目"] == motocho_title:
                    motocho_dict[motocho_title].append(kamokugoto_dict)
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
        
        kamokugoto_zandaka_dict = {}
        for account_item in shiwakehyou["debit"]:
            kamokugoto_zandaka_dict.update({account_item: 0})
        
        for motocho_title in motocho_dict:
            karikata_goukei = 0
            kashikata_goukei = 0
            for kamokugoto_dict in motocho_dict[motocho_title]:
                if kamokugoto_dict["仕分"] == "debit":
                    karikata_goukei += kamokugoto_dict["金額"]
                else:
                    kashikata_goukei += kamokugoto_dict["金額"]
            if karikata_goukei - kashikata_goukei > 0:
                shiwake = "debit"
                kingaku = karikata_goukei - kashikata_goukei
            else:
                shiwake = "credit"
                kingaku = kashikata_goukei - karikata_goukei
            kamokugoto_zandaka_dict[motocho_title] = [kingaku, shiwake]
        
        dict_of_kamoku_and_kingaku_list = []
        for kamokumei in kamokugoto_zandaka_dict:
            dict_of_kamoku_and_kingaku_list.append({"勘定科目": kamokumei, "金額": kamokugoto_zandaka_dict[kamokumei]})
        
        shisan_list = ["現金", "売掛金"]
        for kamoku_to_kingaku_dict in dict_of_kamoku_and_kingaku_list:
            if kamoku_to_kingaku_dict["勘定科目"] in shisan_list:
                self.kamoku_kubun_kingaku_list.append({"勘定科目":kamoku_to_kingaku_dict["勘定科目"], "区分":"資産", "金額":kamoku_to_kingaku_dict["金額"][0]})

        debit_list = ["未払金", "買掛金"]
        for kamoku_to_kingaku_dict in dict_of_kamoku_and_kingaku_list:
            if kamoku_to_kingaku_dict["勘定科目"] in debit_list:
                self.kamoku_kubun_kingaku_list.append({"勘定科目":kamoku_to_kingaku_dict["勘定科目"], "区分":"負債", "金額":kamoku_to_kingaku_dict["金額"][0]})

        debit_list = ["資本金"]
        for kamoku_to_kingaku_dict in dict_of_kamoku_and_kingaku_list:
            if kamoku_to_kingaku_dict["勘定科目"] in debit_list:
                self.kamoku_kubun_kingaku_list.append({"勘定科目":kamoku_to_kingaku_dict["勘定科目"], "区分":"純資産", "金額":kamoku_to_kingaku_dict["金額"][0]})
    