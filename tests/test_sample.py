import unittest
from src.main import AccountingSystem

class TestAccountingSystem(unittest.TestCase):

  def test_2(self):
      data = [
              {
                "credit": {
                  "現金": 1000
                }
              }
            ]
      accounting_system = AccountingSystem()
      with self.assertRaises(ValueError):
        accounting_system.input(data)

  def test_3(self):
      data = [
              {
                "debit": {
                  "未払金": 500,
                }
              }
            ]
      accounting_system = AccountingSystem()
      with self.assertRaises(ValueError):
        accounting_system.input(data)

  def test_accounts_receivable(self):
    data = [
            {
              "credit": {
                "現金": 1000,
                "売掛金": 2000
              }
            }
          ]
    accounting_system = AccountingSystem()
    with self.assertRaises(ValueError):
        accounting_system.input(data)

  def test_accounts_payable(self):
    data = [
            {
              "debit": {
                "未払金": 500,
                "買掛金": 2500,
              }
            }
          ]
    accounting_system = AccountingSystem()
    with self.assertRaises(ValueError):
        accounting_system.input(data)

  # def test_debit_and_credit(self):
  #     data = [
  #             {
  #             "debit": {
  #                 "未払金": 1000,
  #               },
  #               "credit": {
  #                 "現金": 1000
  #               }
  #             }
  #           ]
  #     accounting_system = AccountingSystem()
  #     accounting_system.input(data)
  #     result = accounting_system.output_balance_sheet()
  #     expected = "勘定科目,区分,金額\n現金,資産,-1000\n売掛金,資産,0\n未払金,負債,-1000\n買掛金,負債,0\n資本金,純資産,0\n"
  #     assert result == expected

  # def test_multi_debit_and_credit(self):
  #   data = [
  #           {
  #           "debit": {
  #               "未払金": 500,
  #               "買掛金": 2500,
  #             },
  #             "credit": {
  #               "現金": 3000
  #             }
  #           }
  #         ]
  #   accounting_system = AccountingSystem()
  #   accounting_system.input(data)
  #   result = accounting_system.output_balance_sheet()
  #   expected = "勘定科目,区分,金額\n現金,資産,-3000\n売掛金,資産,0\n未払金,負債,-500\n買掛金,負債,-2500\n資本金,純資産,0\n"
  #   assert result == expected

  # def test_multi_debit_and_multi_credit(self):
  #   data = [
  #           {
  #           "debit": {
  #               "未払金": 500,
  #               "買掛金": 2500,
  #             },
  #             "credit": {
  #               "現金": 1500,
  #               "売掛金": 1500
  #             }
  #           }
  #         ]
  #   accounting_system = AccountingSystem()
  #   accounting_system.input(data)
  #   result = accounting_system.output_balance_sheet()
  #   expected = "勘定科目,区分,金額\n現金,資産,-1500\n売掛金,資産,-1500\n未払金,負債,-500\n買掛金,負債,-2500\n資本金,純資産,0\n"
  #   assert result == expected

  # def test_debit_cash(self):
  #   data = [
  #           {
  #           "debit": {
  #               "未払金": 500,
  #               "買掛金": 2500,
  #               "現金": 500
  #             },
  #             "credit": {
  #               "現金": 2000,
  #               "売掛金": 1500
  #             }
  #           }
  #         ]
  #   accounting_system = AccountingSystem()
  #   accounting_system.input(data)
  #   result = accounting_system.output_balance_sheet()
  #   expected = "勘定科目,区分,金額\n現金,資産,-1500\n売掛金,資産,-1500\n未払金,負債,-500\n買掛金,負債,-2500\n資本金,純資産,0\n"
  #   assert result == expected

  # def test_capital(self):
  #   data = [
  #           {
  #             "debit": {
  #                 "現金": 1000000
  #             },
  #             "credit": {
  #                 "資本金": 1000000
  #             }
  #           }
  #         ]
  #   accounting_system = AccountingSystem()
  #   accounting_system.input(data)
  #   result = accounting_system.output_balance_sheet()
  #   expected = (
  #       "勘定科目,区分,金額\n"
  #       "現金,資産,1000000\n"
  #       "売掛金,資産,0\n"
  #       "未払金,負債,0\n"
  #       "買掛金,負債,0\n"
  #       "資本金,純資産,1000000\n"
  #   )
  #   assert result == expected

  # def test_reverse_debit_and_credit(self):
  #     data = [
  #             {
  #               "debit": {
  #                 "現金": 1000
  #               },
  #               "credit": {
  #                 "未払金": 1000,
  #               },
  #             }
  #           ]
  #     accounting_system = AccountingSystem()
  #     accounting_system.input(data)
  #     result = accounting_system.output_balance_sheet()
  #     expected = "勘定科目,区分,金額\n現金,資産,1000\n売掛金,資産,0\n未払金,負債,1000\n買掛金,負債,0\n資本金,純資産,0\n"
  #     assert result == expected

  # def test_multiple_transactions(self):
  #   data = [
  #       # 1件目：売上取引（売掛金増加）
  #       {
  #           "debit": {
  #               "売掛金": 100000
  #           },
  #           "credit": {
  #               "売上": 100000
  #           }
  #       },
  #       # 2件目：売掛金の回収（現金増加、売掛金減少）
  #       {
  #           "debit": {
  #               "現金": 60000
  #           },
  #           "credit": {
  #               "売掛金": 60000
  #           }
  #       },
  #       # 3件目：仕入（買掛金発生）
  #       {
  #           "debit": {
  #               "仕入": 40000
  #           },
  #           "credit": {
  #               "買掛金": 40000
  #           }
  #       },
  #       # 4件目：買掛金の支払い（現金減少、買掛金減少）
  #       {
  #           "debit": {
  #               "買掛金": 20000
  #           },
  #           "credit": {
  #               "現金": 20000
  #           }
  #       },
  #       # 5件目：資本金の出資（現金と資本金増加）
  #       {
  #           "debit": {
  #               "現金": 50000
  #           },
  #           "credit": {
  #               "資本金": 50000
  #           }
  #       }
  #   ]

  #   accounting_system = AccountingSystem()
  #   accounting_system.input(data)

  #   result = accounting_system.output_balance_sheet()

  #   expected = (
  #       "勘定科目,区分,金額\n"
  #       "現金,資産,90000\n"          # +60000（回収） -20000（支払い） +50000（出資）
  #       "売掛金,資産,40000\n"        # +100000（売上） -60000（回収）
  #       "未払金,負債,0\n"
  #       "買掛金,負債,20000\n"        # +40000（仕入） -20000（支払い）
  #       "資本金,純資産,50000\n"      # +50000（出資）
  #   )

  #   assert result == expected
