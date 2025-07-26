import unittest
from src.main import AccountingSystem

class TestPl(unittest.TestCase):

  def test_income_statement_basic(self):
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
        }
    ]

    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_pl()

    expected = (
        "勘定科目,区分,金額\n"
        "売上,収益,200000\n"
        "給料,費用,50000\n"
        "当期純利益,純利益,150000\n"
    )
    assert result == expected
