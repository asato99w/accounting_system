import unittest
from src.main import AccountingSystem

class TestAccountingSystem(unittest.TestCase):

  def test_first(self):
      accounting_system = AccountingSystem()
      result = accounting_system.output_balance_sheet()
      expected = "勘定科目,区分,金額\n"
      assert result == expected

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

  def test_debit_and_credit(self):
      data = [
              {
              "debit": {
                  "未払金": 1000,
                },
                "credit": {
                  "現金": 1000
                }
              }
            ]
      accounting_system = AccountingSystem()
      accounting_system.input(data)
      result = accounting_system.output_balance_sheet()
      expected = "勘定科目,区分,金額\n現金,資産,1000\n売掛金,資産,0\n未払金,負債,1000\n買掛金,負債,0\n資本金,純資産,0\n"
      assert result == expected

  def test_multi_debit_and_credit(self):
    data = [
            {
            "debit": {
                "未払金": 500,
                "買掛金": 2500,
              },
              "credit": {
                "現金": 3000
              }
            }
          ]
    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_balance_sheet()
    expected = "勘定科目,区分,金額\n現金,資産,3000\n売掛金,資産,0\n未払金,負債,500\n買掛金,負債,2500\n資本金,純資産,0\n"
    assert result == expected

  def test_multi_debit_and_multi_credit(self):
    data = [
            {
            "debit": {
                "未払金": 500,
                "買掛金": 2500,
              },
              "credit": {
                "現金": 1500,
                "売掛金": 1500
              }
            }
          ]
    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_balance_sheet()
    expected = "勘定科目,区分,金額\n現金,資産,1500\n売掛金,資産,1500\n未払金,負債,500\n買掛金,負債,2500\n資本金,純資産,0\n"
    assert result == expected

  def test_debit_cash(self):
    data = [
            {
            "debit": {
                "未払金": 500,
                "買掛金": 2500,
                "現金": 500
              },
              "credit": {
                "現金": 2000,
                "売掛金": 1500
              }
            }
          ]
    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_balance_sheet()
    expected = "勘定科目,区分,金額\n現金,資産,1500\n売掛金,資産,1500\n未払金,負債,500\n買掛金,負債,2500\n資本金,純資産,0\n"
    assert result == expected

  def test_capital(self):
    data = [
            {
              "debit": {
                  "現金": 1000000
              },
              "credit": {
                  "資本金": 1000000
              }
            }
          ]
    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_balance_sheet()
    expected = (
        "勘定科目,区分,金額\n"
        "現金,資産,1000000\n"
        "売掛金,資産,0\n"
        "未払金,負債,0\n"
        "買掛金,負債,0\n"
        "資本金,純資産,1000000\n"
    )
    assert result == expected

  def test_reverse_debit_and_credit(self):
      data = [
              {
                "debit": {
                  "現金": 1000
                },
                "credit": {
                  "未払金": 1000,
                },
              }
            ]
      accounting_system = AccountingSystem()
      accounting_system.input(data)
      result = accounting_system.output_balance_sheet()
      expected = "勘定科目,区分,金額\n現金,資産,1000\n売掛金,資産,0\n未払金,負債,1000\n買掛金,負債,0\n資本金,純資産,0\n"
      assert result == expected
