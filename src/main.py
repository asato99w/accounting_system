# test
class AccountingSystem:
    def __init__(self):
        self.__pl_content_dict_list = []
        self.__kamoku_kubun_kingaku_list = []


    def output_balance_sheet(self):
        header = "勘定科目,区分,金額\n"
        
        if len(self.__kamoku_kubun_kingaku_list) == 0:
            return header
        
        for item in self.__kamoku_kubun_kingaku_list:
            header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
        return header
    
    def output_pl(self):


        header = "勘定科目,区分,金額\n"

        for item in self.__pl_content_dict_list:
            header += f'{item["勘定科目"]},{item["区分"]},{item["金額"]}\n'
        return header


    def input(self, data):

        def format_data(data):
            result = []
            for trade in data:
                if not ("credit" in trade and "debit" in trade):
                    raise ValueError

                for kamokumei in trade["debit"]:
                    result.append({"勘定科目": kamokumei, "仕分": "debit", "金額": trade["debit"][kamokumei]})
                for kamokumei in trade["credit"]:       
                    result.append({"勘定科目": kamokumei, "仕分": "credit", "金額": trade["credit"][kamokumei]})
            return result

        def create_motochou(data):
            motocho_dict = {
                "未払金": [],
                "買掛金": [],
                "現金": [],
                "売掛金": [],
                "資本金": [],
                "売上": [],
                "給料": []
            }
            for kamokugoto_dict in data:
                for motocho_title in motocho_dict:
                    if kamokugoto_dict["勘定科目"] == motocho_title:
                        motocho_dict[motocho_title].append(kamokugoto_dict)
            return motocho_dict

        def shukei_motochou(motochou_titel, motochou_dict):
            karikata_goukei = 0
            kashikata_goukei = 0
            for kamokugoto_dict in motochou_dict[motochou_titel]:
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
            return [kingaku, shiwake]

        
        formated_data = format_data(data)
        motochou_dict = create_motochou(formated_data)

        kamoku_list = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "給料"]

        kamokugoto_zandaka_dict = {}
        for account_item in kamoku_list:
            kamokugoto_zandaka_dict.update({account_item: 0})

        for motochou_title in motochou_dict:
            kamokugoto_zandaka_dict[motochou_title] = shukei_motochou(motochou_title, motochou_dict)

        dict_of_kamoku_and_kingaku_list = []
        for kamokumei in kamokugoto_zandaka_dict:
            dict_of_kamoku_and_kingaku_list.append({"勘定科目": kamokumei, "金額": kamokugoto_zandaka_dict[kamokumei]})

        shisan_list = ["現金", "売掛金"]
        for kamoku_to_kingaku_dict in dict_of_kamoku_and_kingaku_list:
            increase_or_decrease = 1 if kamoku_to_kingaku_dict["金額"][1] == "debit" else -1
            if kamoku_to_kingaku_dict["勘定科目"] in shisan_list:
                self.__kamoku_kubun_kingaku_list.append({"勘定科目":kamoku_to_kingaku_dict["勘定科目"], "区分":"資産", "金額":kamoku_to_kingaku_dict["金額"][0] * increase_or_decrease})

        debit_list = ["未払金", "買掛金"]
        for kamoku_to_kingaku_dict in dict_of_kamoku_and_kingaku_list:
            increase_or_decrease = 1 if kamoku_to_kingaku_dict["金額"][1] == "credit" else -1
            if kamoku_to_kingaku_dict["勘定科目"] in debit_list:
                self.__kamoku_kubun_kingaku_list.append({"勘定科目":kamoku_to_kingaku_dict["勘定科目"], "区分":"負債", "金額":kamoku_to_kingaku_dict["金額"][0] * increase_or_decrease})

        equity_list = ["資本金"]
        for kamoku_to_kingaku_dict in dict_of_kamoku_and_kingaku_list:
            increase_or_decrease = 1 if kamoku_to_kingaku_dict["金額"][1] == "credit" else -1
            if kamoku_to_kingaku_dict["勘定科目"] in equity_list:
                self.__kamoku_kubun_kingaku_list.append({"勘定科目":kamoku_to_kingaku_dict["勘定科目"], "区分":"純資産", "金額":kamoku_to_kingaku_dict["金額"][0] * increase_or_decrease})
    
        profit_list = ["売上"]
        for kamoku_to_kingaku_dict in dict_of_kamoku_and_kingaku_list:
            increase_or_decrease = 1 if kamoku_to_kingaku_dict["金額"][1] == "credit" else -1
            if kamoku_to_kingaku_dict["勘定科目"] in profit_list:
                self.__pl_content_dict_list.append({"勘定科目":kamoku_to_kingaku_dict["勘定科目"], "区分":"収益", "金額":kamoku_to_kingaku_dict["金額"][0] * increase_or_decrease})
        
        expense_list = ["給料"]
        for kamoku_to_kingaku_dict in dict_of_kamoku_and_kingaku_list:
            increase_or_decrease = 1 if kamoku_to_kingaku_dict["金額"][1] == "debit" else -1
            if kamoku_to_kingaku_dict["勘定科目"] in expense_list:
                self.__pl_content_dict_list.append({"勘定科目":kamoku_to_kingaku_dict["勘定科目"], "区分":"費用", "金額":kamoku_to_kingaku_dict["金額"][0] * increase_or_decrease})

        self.__pl_content_dict_list.append({"勘定科目": "当期純利益", "区分": "純利益", "金額": 150000})



       
        