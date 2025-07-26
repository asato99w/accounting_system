import unittest
from src.main import AccountingSystem

class TestBsPl(unittest.TestCase):

  def test_income_and_balance_sheet_link(self):
    data = [
        {
            "debit": {
                "現金": 200000
            },
            "credit": {
                "売上": 200000
            }
        },
        {
            "debit": {
                "給料": 50000
            },
            "credit": {
                "現金": 50000
            }
        },
        {
            "debit": {
                "売上": 200000
            },
            "credit": {
                "損益": 200000
            }
        },
        {
            "debit": {
                "損益": 50000
            },
            "credit": {
                "給料": 50000
            }
        },
        {
            "debit": {
                "損益": 150000
            },
            "credit": {
                "繰越利益剰余金": 150000
            }
        }
    ]
    accounting_system = AccountingSystem()
    accounting_system.input(data)

    # 損益計算書の検証
    income = accounting_system.output_income_statement()
    expected_income = (
        "勘定科目,区分,金額\n"
        "売上,収益,200000\n"
        "給料,費用,50000\n"
        "当期純利益,純利益,150000\n"
    )
    assert income == expected_income

    # 貸借対照表の検証
    balance = accounting_system.output_balance_sheet()
    expected_balance = (
        "勘定科目,区分,金額\n"
        "現金,資産,150000\n"
        "売掛金,資産,0\n"
        "未払金,負債,0\n"
        "買掛金,負債,0\n"
        "資本金,純資産,0\n"
        "繰越利益剰余金,純資産,150000\n"
    )
    assert balance == expected_balance
