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

  def test_multiple_revenues_and_expenses(self):
    """複数の収益・費用科目のテスト"""
    data = [
        # 売上
        {
            "debit": {
                "現金": 300000
            },
            "credit": {
                "売上": 300000
            }
        },
        # 受取利息
        {
            "debit": {
                "現金": 5000
            },
            "credit": {
                "受取利息": 5000
            }
        },
        # 給料
        {
            "debit": {
                "給料": 100000
            },
            "credit": {
                "現金": 100000
            }
        },
        # 地代家賃
        {
            "debit": {
                "地代家賃": 50000
            },
            "credit": {
                "現金": 50000
            }
        },
        # 水道光熱費
        {
            "debit": {
                "水道光熱費": 20000
            },
            "credit": {
                "現金": 20000
            }
        }
    ]

    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_pl()

    expected = (
        "勘定科目,区分,金額\n"
        "売上,収益,300000\n"
        "受取利息,収益,5000\n"
        "給料,費用,100000\n"
        "地代家賃,費用,50000\n"
        "水道光熱費,費用,20000\n"
        "当期純利益,純利益,135000\n"  # 305000 - 170000
    )
    assert result == expected

  def test_net_loss(self):
    """赤字（純損失）のテスト"""
    data = [
        {
            "debit": {
                "現金": 50000
            },
            "credit": {
                "売上": 50000
            }
        },
        {
            "debit": {
                "給料": 80000
            },
            "credit": {
                "現金": 80000
            }
        },
        {
            "debit": {
                "地代家賃": 30000
            },
            "credit": {
                "現金": 30000
            }
        }
    ]

    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_pl()

    expected = (
        "勘定科目,区分,金額\n"
        "売上,収益,50000\n"
        "給料,費用,80000\n"
        "地代家賃,費用,30000\n"
        "当期純損失,純損失,60000\n"  # 50000 - 110000 = -60000
    )
    assert result == expected

  def test_revenue_only(self):
    """収益のみのテスト"""
    data = [
        {
            "debit": {
                "現金": 100000
            },
            "credit": {
                "売上": 100000
            }
        }
    ]

    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_pl()

    expected = (
        "勘定科目,区分,金額\n"
        "売上,収益,100000\n"
        "当期純利益,純利益,100000\n"
    )
    assert result == expected

  def test_expense_only(self):
    """費用のみのテスト"""
    data = [
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
        "給料,費用,50000\n"
        "当期純損失,純損失,50000\n"
    )
    assert result == expected

  def test_zero_transactions(self):
    """取引なしのテスト"""
    data = []

    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_pl()

    expected = "勘定科目,区分,金額\n"
    assert result == expected

  def test_duplicate_accounts(self):
    """同一勘定科目の重複テスト"""
    data = [
        # 売上1
        {
            "debit": {
                "現金": 100000
            },
            "credit": {
                "売上": 100000
            }
        },
        # 売上2
        {
            "debit": {
                "売掛金": 150000
            },
            "credit": {
                "売上": 150000
            }
        },
        # 給料1
        {
            "debit": {
                "給料": 30000
            },
            "credit": {
                "現金": 30000
            }
        },
        # 給料2
        {
            "debit": {
                "給料": 40000
            },
            "credit": {
                "未払金": 40000
            }
        }
    ]

    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_pl()

    expected = (
        "勘定科目,区分,金額\n"
        "売上,収益,250000\n"  # 100000 + 150000
        "給料,費用,70000\n"   # 30000 + 40000
        "当期純利益,純利益,180000\n"  # 250000 - 70000
    )
    assert result == expected
