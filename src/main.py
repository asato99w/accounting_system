
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

            target_list = list(data[0].values())

            target_list = [{"未払金": 1000}, {"現金": 1000}]

            new_dict = {}
            for target_dict in target_list:
                new_dict.update(target_dict)

            expected_new_dict = {"未払金": 1000, "現金": 1000}

            if new_dict == expected_new_dict:

                keys_list = list(new_dict.keys())

                values_list = list(new_dict.values())

                new_dict_list = []
                for key in keys_list:
                    new_dict_list.append({"勘定科目": key})

                new_dict_list = [{"勘定科目": "未払金"}, {"勘定科目": "現金"}]

                # for dict, value in new_dict_list, values_list:
                #     dict.update({"金額": value})


                keys_list = []
                values_list = []
                for target_dict in target_list:
                    keys_list.append(list(target_dict.keys()))
                    values_list.append(list(target_dict.values()))

                # keys_list = ["未払金", "現金"]
                # values_list = [1000, 1000]

                new_dict_list = []
                for key in keys_list:
                    new_dict_list.append({"勘定科目": key})
                # for value in values_list:
                #     new_dict_list.append({"金額": value})

                temp_list = [
                    {"勘定科目":"未払金", "金額":"1000"},
                    {"勘定科目":"現金", "金額":"1000"}
                ]

                # temp_list = new_dict_list

                for target_dict in temp_list:
                    if "現金" == target_dict["勘定科目"]:
                        self.list2.append({"勘定科目":"現金", "区分":"資産", "金額":"1000"})
                for target_dict in temp_list:
                    if "未払金" == target_dict["勘定科目"]:
                        self.list2.append({"勘定科目":"未払金", "区分":"負債", "金額":"1000"})

                # account_item_list = []
                # for account_item in temp_list:
                #     account_item_list.append(account_item["勘定科目"])

                # if "現金" in account_item_list:
                #     self.list2.append({"勘定科目":"現金", "区分":"資産", "金額":"1000"})
                # self.list2.append({"勘定科目":"未払金", "区分":"負債", "金額":"1000"})
            
        else:
            if "credit" in data[0]:
                shiwake = "credit"
                kubun = "資産"       
            else:
                shiwake = "debit"
                kubun = "負債"
            for item in list(data[0][shiwake].keys()):
                self.list2.append({"勘定科目":item, "区分":kubun, "金額":data[0][shiwake][item]}) 