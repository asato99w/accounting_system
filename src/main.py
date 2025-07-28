from .account_type import Asset, Liability, Equity, Revenue, Expense
from .csv import CSVExporter
from .financial_statements import FinancialStatements

class AccountingSystem:
    def __init__(self):
        self.__fs = None

    def output_balance_sheet(self):
        if self.__fs is None:
            return "勘定科目,区分,金額\n"

        return self.__fs.export_bs(CSVExporter())

    def output_pl(self):
        if self.__fs is None:
            return "勘定科目,区分,金額\n"

        return self.__fs.export_pl(CSVExporter())


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
                "受取利息": [],
                "給料": [],
                "地代家賃": [],
                "水道光熱費": []
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

        kamoku_list = ["未払金", "買掛金", "現金", "売掛金", "資本金", "売上", "受取利息", "給料", "地代家賃", "水道光熱費"]

        kamokugoto_zandaka_dict = {}
        for account_item in kamoku_list:
            kamokugoto_zandaka_dict.update({account_item: 0})

        for motochou_title in motochou_dict:
            kamokugoto_zandaka_dict[motochou_title] = shukei_motochou(motochou_title, motochou_dict)

        dict_of_kamoku_and_kingaku_list = []
        for kamokumei in kamokugoto_zandaka_dict:
            dict_of_kamoku_and_kingaku_list.append({"勘定科目": kamokumei, "金額": kamokugoto_zandaka_dict[kamokumei]})


        self.__fs = FinancialStatements(dict_of_kamoku_and_kingaku_list)
