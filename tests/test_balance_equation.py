import unittest
from src.main import AccountingSystem

class TestBalanceEquation(unittest.TestCase):
    """貸借平衡を厳密にテストするクラス"""

    def test_balance_equation_failure(self):
        """現在の実装で貸借平衡が取れていないことを確認"""
        data = [
            {
                "debit": {
                    "現金": 1000000
                },
                "credit": {
                    "資本金": 1000000
                }
            },
            {
                "debit": {
                    "現金": 500000
                },
                "credit": {
                    "売上": 500000
                }
            },
            {
                "debit": {
                    "給料": 200000
                },
                "credit": {
                    "現金": 200000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        bs_result = accounting_system.output_balance_sheet()
        pl_result = accounting_system.output_pl()

        # B/Sから数値を抽出して貸借平衡をチェック
        assets_total = self.calculate_assets_total(bs_result)
        liabilities_equity_total = self.calculate_liabilities_equity_total(bs_result)
        net_income = self.extract_net_income(pl_result)

        print(f"B/S結果:\n{bs_result}")
        print(f"P/L結果:\n{pl_result}")
        print(f"資産合計: {assets_total}")
        print(f"負債+純資産合計: {liabilities_equity_total}")
        print(f"純利益: {net_income}")
        print(f"差額: {assets_total - liabilities_equity_total}")

        # 現在の実装では利益剰余金が追加されているため、貸借平衡が取れるはず
        self.assertEqual(assets_total, liabilities_equity_total,
                        "現在の実装では利益剰余金が含まれるため、貸借平衡が取れるはず")

    def test_proper_balance_equation_expectation(self):
        """正しい会計処理での貸借平衡を期待値として示す"""
        data = [
            {
                "debit": {
                    "現金": 2000000
                },
                "credit": {
                    "資本金": 2000000
                }
            },
            {
                "debit": {
                    "売掛金": 800000
                },
                "credit": {
                    "売上": 800000
                }
            },
            {
                "debit": {
                    "給料": 300000
                },
                "credit": {
                    "現金": 300000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        bs_result = accounting_system.output_balance_sheet()
        pl_result = accounting_system.output_pl()

        assets_total = self.calculate_assets_total(bs_result)
        liabilities_equity_total = self.calculate_liabilities_equity_total(bs_result)
        net_income = self.extract_net_income(pl_result)

        # 現在の実装では利益剰余金が含まれるため、直接貸借平衡が取れるはず
        print(f"\n=== 現在の実装での検証 ===")
        print(f"資産合計: {assets_total}")
        print(f"負債+純資産合計（利益剰余金含む）: {liabilities_equity_total}")
        print(f"純利益: {net_income}")

        self.assertEqual(assets_total, liabilities_equity_total,
                        "現在の実装では利益剰余金が含まれるため、資産合計 = 負債+純資産合計が成立するはず")

    def calculate_assets_total(self, bs_result):
        """B/Sから資産合計を計算"""
        total = 0
        for line in bs_result.split('\n')[1:]:  # ヘッダーをスキップ
            if line and ',資産,' in line:  # 純資産を除外するため、カンマで囲む
                parts = line.split(',')
                amount = int(parts[2])
                total += amount
        return total

    def calculate_liabilities_equity_total(self, bs_result):
        """B/Sから負債+純資産合計を計算"""
        total = 0
        for line in bs_result.split('\n')[1:]:  # ヘッダーをスキップ
            if line and ('負債' in line or '純資産' in line):
                parts = line.split(',')
                amount = int(parts[2])
                total += amount
        return total

    def extract_net_income(self, pl_result):
        """P/Lから純利益を抽出"""
        for line in pl_result.split('\n')[1:]:  # ヘッダーをスキップ
            if line and ('純利益' in line or '純損失' in line):
                parts = line.split(',')
                amount = int(parts[2])
                # 純損失の場合は負の値として扱う
                if '純損失' in line:
                    amount = -amount
                return amount
        return 0  # 純利益/純損失がない場合

if __name__ == '__main__':
    unittest.main()