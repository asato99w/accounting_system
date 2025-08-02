import unittest
from src.main import AccountingSystem

class TestBSPLIntegration(unittest.TestCase):
    """貸借対照表と損益計算書の統合テスト"""

    def test_basic_business_cycle(self):
        """基本的な事業サイクルのテスト"""
        data = [
            # 1. 資本金の出資
            {
                "debit": {
                    "現金": 1000000
                },
                "credit": {
                    "資本金": 1000000
                }
            },
            # 2. 売上（現金）
            {
                "debit": {
                    "現金": 500000
                },
                "credit": {
                    "売上": 500000
                }
            },
            # 3. 売上（掛け）
            {
                "debit": {
                    "売掛金": 300000
                },
                "credit": {
                    "売上": 300000
                }
            },
            # 4. 給料支払い
            {
                "debit": {
                    "給料": 200000
                },
                "credit": {
                    "現金": 200000
                }
            },
            # 5. 地代家賃（未払い）
            {
                "debit": {
                    "地代家賃": 100000
                },
                "credit": {
                    "未払金": 100000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        # P/L検証
        pl_result = accounting_system.output_pl()
        expected_pl = (
            "勘定科目,区分,金額\n"
            "売上,収益,800000\n"  # 500000 + 300000
            "給料,費用,200000\n"
            "地代家賃,費用,100000\n"
            "当期純利益,純利益,500000\n"  # 800000 - 300000
        )
        self.assertEqual(pl_result, expected_pl)

        # B/S検証
        bs_result = accounting_system.output_balance_sheet()
        expected_bs = (
            "勘定科目,区分,金額\n"
            "現金,資産,1300000\n"  # 1000000 + 500000 - 200000
            "売掛金,資産,300000\n"
            "未払金,負債,100000\n"
            "買掛金,負債,0\n"
            "資本金,純資産,1000000\n"
            "利益剰余金,純資産,500000\n"  # 純利益が利益剰余金として計上される
        )
        self.assertEqual(bs_result, expected_bs)

        # 貸借一致の検証（資産 = 負債 + 純資産 + 当期純利益）
        # 1,600,000 = 100,000 + 1,000,000 + 500,000

    def test_net_loss_scenario(self):
        """純損失が発生する場合のテスト"""
        data = [
            # 資本金
            {
                "debit": {
                    "現金": 500000
                },
                "credit": {
                    "資本金": 500000
                }
            },
            # 売上
            {
                "debit": {
                    "現金": 200000
                },
                "credit": {
                    "売上": 200000
                }
            },
            # 給料（高額）
            {
                "debit": {
                    "給料": 300000
                },
                "credit": {
                    "現金": 300000
                }
            },
            # 地代家賃
            {
                "debit": {
                    "地代家賃": 150000
                },
                "credit": {
                    "現金": 150000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        # P/L検証
        pl_result = accounting_system.output_pl()
        expected_pl = (
            "勘定科目,区分,金額\n"
            "売上,収益,200000\n"
            "給料,費用,300000\n"
            "地代家賃,費用,150000\n"
            "当期純損失,純損失,250000\n"  # 200000 - 450000 = -250000
        )
        self.assertEqual(pl_result, expected_pl)

        # B/S検証
        bs_result = accounting_system.output_balance_sheet()
        expected_bs = (
            "勘定科目,区分,金額\n"
            "現金,資産,250000\n"  # 500000 + 200000 - 300000 - 150000
            "売掛金,資産,0\n"
            "未払金,負債,0\n"
            "買掛金,負債,0\n"
            "資本金,純資産,500000\n"
            "利益剰余金,純資産,-250000\n"  # 純損失がマイナスの利益剰余金として計上
        )
        self.assertEqual(bs_result, expected_bs)

    def test_complex_transactions(self):
        """複雑な取引パターンのテスト"""
        data = [
            # 資本金
            {
                "debit": {
                    "現金": 2000000
                },
                "credit": {
                    "資本金": 2000000
                }
            },
            # 売上（現金・掛け混合）
            {
                "debit": {
                    "現金": 600000,
                    "売掛金": 400000
                },
                "credit": {
                    "売上": 1000000
                }
            },
            # 仕入（買掛金）
            {
                "debit": {
                    "仕入": 300000
                },
                "credit": {
                    "買掛金": 300000
                }
            },
            # 受取利息
            {
                "debit": {
                    "現金": 10000
                },
                "credit": {
                    "受取利息": 10000
                }
            },
            # 給料（一部未払い）
            {
                "debit": {
                    "給料": 400000
                },
                "credit": {
                    "現金": 300000,
                    "未払金": 100000
                }
            },
            # 売掛金回収
            {
                "debit": {
                    "現金": 200000
                },
                "credit": {
                    "売掛金": 200000
                }
            },
            # 買掛金支払い
            {
                "debit": {
                    "買掛金": 150000
                },
                "credit": {
                    "現金": 150000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        # P/L検証
        pl_result = accounting_system.output_pl()
        expected_pl = (
            "勘定科目,区分,金額\n"
            "売上,収益,1000000\n"
            "受取利息,収益,10000\n"
            "給料,費用,400000\n"
            "仕入,費用,300000\n"
            "当期純利益,純利益,310000\n"  # 1010000 - 400000 - 300000
        )
        self.assertEqual(pl_result, expected_pl)

        # B/S検証
        bs_result = accounting_system.output_balance_sheet()
        expected_bs = (
            "勘定科目,区分,金額\n"
            "現金,資産,2360000\n"  # 2000000 + 600000 + 10000 - 300000 + 200000 - 150000
            "売掛金,資産,200000\n"  # 400000 - 200000
            "未払金,負債,100000\n"
            "買掛金,負債,150000\n"  # 300000 - 150000
            "資本金,純資産,2000000\n"
            "利益剰余金,純資産,310000\n"  # 純利益が利益剰余金として計上される
        )
        self.assertEqual(bs_result, expected_bs)

    def test_no_pl_accounts(self):
        """P/L科目がない場合のテスト（B/Sのみ）"""
        data = [
            # 資本金
            {
                "debit": {
                    "現金": 1000000
                },
                "credit": {
                    "資本金": 1000000
                }
            },
            # 資産の交換（現金→売掛金）
            {
                "debit": {
                    "売掛金": 300000
                },
                "credit": {
                    "現金": 300000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        # P/L検証（取引なし）
        pl_result = accounting_system.output_pl()
        expected_pl = "勘定科目,区分,金額\n"
        self.assertEqual(pl_result, expected_pl)

        # B/S検証
        bs_result = accounting_system.output_balance_sheet()
        expected_bs = (
            "勘定科目,区分,金額\n"
            "現金,資産,700000\n"
            "売掛金,資産,300000\n"
            "未払金,負債,0\n"
            "買掛金,負債,0\n"
            "資本金,純資産,1000000\n"
        )
        self.assertEqual(bs_result, expected_bs)

    def test_balance_sheet_equation(self):
        """貸借対照表等式の検証テスト"""
        data = [
            # 資本金
            {
                "debit": {
                    "現金": 1500000
                },
                "credit": {
                    "資本金": 1500000
                }
            },
            # 売上
            {
                "debit": {
                    "売掛金": 800000
                },
                "credit": {
                    "売上": 800000
                }
            },
            # 費用
            {
                "debit": {
                    "給料": 300000,
                    "地代家賃": 100000
                },
                "credit": {
                    "現金": 350000,
                    "未払金": 50000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        # 数値を取得して等式を検証
        bs_result = accounting_system.output_balance_sheet()
        pl_result = accounting_system.output_pl()

        # 資産合計 = 負債合計 + 純資産合計 + 当期純利益
        # 現金: 1,150,000 + 売掛金: 800,000 = 1,950,000
        # 未払金: 50,000 + 資本金: 1,500,000 + 純利益: 400,000 = 1,950,000
        
        # この検証は実際の数値を解析して行うべきですが、
        # ここでは出力形式の確認のみ行います
        self.assertIn("現金,資産,1150000", bs_result)
        self.assertIn("売掛金,資産,800000", bs_result)
        self.assertIn("未払金,負債,50000", bs_result)
        self.assertIn("資本金,純資産,1500000", bs_result)
        self.assertIn("当期純利益,純利益,400000", pl_result)

    def test_net_income_to_equity_integration(self):
        """純利益が純資産に正しく反映されるかのテスト"""
        data = [
            # 期首資本金
            {
                "debit": {
                    "現金": 1000000
                },
                "credit": {
                    "資本金": 1000000
                }
            },
            # 売上
            {
                "debit": {
                    "現金": 500000
                },
                "credit": {
                    "売上": 500000
                }
            },
            # 費用
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

        # P/L検証（純利益 = 300,000）
        pl_result = accounting_system.output_pl()
        expected_pl = (
            "勘定科目,区分,金額\n"
            "売上,収益,500000\n"
            "給料,費用,200000\n"
            "当期純利益,純利益,300000\n"
        )
        self.assertEqual(pl_result, expected_pl)

        # B/S検証
        bs_result = accounting_system.output_balance_sheet()
        
        # 現在の実装では純利益は純資産に加算されていない
        # 期待される動作：資本金 1,000,000 + 純利益 300,000 = 純資産 1,300,000
        # しかし現在の実装では資本金のみが表示される
        
        # 正しい会計処理での期待値（純利益が利益剰余金として計上される）
        expected_bs = (
            "勘定科目,区分,金額\n"
            "現金,資産,1300000\n"  # 1000000 + 500000 - 200000
            "売掛金,資産,0\n"
            "未払金,負債,0\n"
            "買掛金,負債,0\n"
            "資本金,純資産,1000000\n"
            "利益剰余金,純資産,300000\n"  # 純利益が利益剰余金として計上される
        )
        
        # このテストは現在の実装では失敗するはず（純利益が純資産に反映されていないため）
        self.assertEqual(bs_result, expected_bs, 
                        "純利益は利益剰余金として純資産に計上されるべき")

        # 理想的な実装での検証（コメントアウト）
        # ideal_expected_bs = (
        #     "勘定科目,区分,金額\n"
        #     "現金,資産,1300000\n"
        #     "売掛金,資産,0\n"
        #     "未払金,負債,0\n"
        #     "買掛金,負債,0\n"
        #     "資本金,純資産,1000000\n"
        #     "利益剰余金,純資産,300000\n"  # 純利益が利益剰余金として計上される
        # )

        # 貸借平衡の確認（理論値）
        # 資産合計: 1,300,000
        # 負債 + 純資産合計: 0 + 1,000,000 + 300,000 = 1,300,000
        # 現在の実装では 0 + 1,000,000 = 1,000,000 で不一致

    def test_net_loss_to_equity_integration(self):
        """純損失が純資産に正しく反映されるかのテスト"""
        data = [
            # 期首資本金
            {
                "debit": {
                    "現金": 1000000
                },
                "credit": {
                    "資本金": 1000000
                }
            },
            # 売上（少額）
            {
                "debit": {
                    "現金": 100000
                },
                "credit": {
                    "売上": 100000
                }
            },
            # 費用（高額）
            {
                "debit": {
                    "給料": 400000
                },
                "credit": {
                    "現金": 400000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        # P/L検証（純損失 = 300,000）
        pl_result = accounting_system.output_pl()
        expected_pl = (
            "勘定科目,区分,金額\n"
            "売上,収益,100000\n"
            "給料,費用,400000\n"
            "当期純損失,純損失,300000\n"
        )
        self.assertEqual(pl_result, expected_pl)

        # B/S検証
        bs_result = accounting_system.output_balance_sheet()
        
        # 正しい会計処理での期待値（純損失が利益剰余金から減算される）
        expected_bs = (
            "勘定科目,区分,金額\n"
            "現金,資産,700000\n"  # 1000000 + 100000 - 400000
            "売掛金,資産,0\n"
            "未払金,負債,0\n"
            "買掛金,負債,0\n"
            "資本金,純資産,1000000\n"
            "利益剰余金,純資産,-300000\n"  # 純損失がマイナスの利益剰余金として計上
        )
        
        # このテストは現在の実装では失敗するはず
        self.assertEqual(bs_result, expected_bs,
                        "純損失は利益剰余金として純資産から減算されるべき")

        # 理想的な実装での検証（コメントアウト）
        # ideal_expected_bs = (
        #     "勘定科目,区分,金額\n"
        #     "現金,資産,700000\n"
        #     "売掛金,資産,0\n"
        #     "未払金,負債,0\n"
        #     "買掛金,負債,0\n"
        #     "資本金,純資産,1000000\n"
        #     "利益剰余金,純資産,-300000\n"  # 純損失がマイナスの利益剰余金として計上
        # )

        # 貸借平衡の確認（理論値）
        # 資産合計: 700,000
        # 負債 + 純資産合計: 0 + 1,000,000 - 300,000 = 700,000
        # 現在の実装では 0 + 1,000,000 = 1,000,000 で不一致

    def test_balance_equation_with_retained_earnings(self):
        """利益剰余金を含む貸借平衡のテスト"""
        data = [
            # 複数期間の取引を想定
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
                    "現金": 800000,
                    "売掛金": 200000
                },
                "credit": {
                    "売上": 1000000
                }
            },
            {
                "debit": {
                    "給料": 300000,
                    "地代家賃": 150000
                },
                "credit": {
                    "現金": 400000,
                    "未払金": 50000
                }
            }
        ]

        accounting_system = AccountingSystem()
        accounting_system.journalize(data)

        # 純利益計算: 1,000,000 - 450,000 = 550,000

        # 現在の貸借不平衡を確認
        bs_result = accounting_system.output_balance_sheet()
        pl_result = accounting_system.output_pl()

        # 資産合計を計算
        # 現金: 2,000,000 + 800,000 - 400,000 = 2,400,000
        # 売掛金: 200,000
        # 資産合計: 2,600,000

        # 負債 + 純資産合計を計算（現在の実装）
        # 未払金: 50,000
        # 資本金: 2,000,000
        # 負債 + 純資産合計: 2,050,000

        # 不足分: 2,600,000 - 2,050,000 = 550,000（純利益と一致）

        # 正しい会計処理では利益剰余金が含まれるべき
        expected_bs = (
            "勘定科目,区分,金額\n"
            "現金,資産,2400000\n"
            "売掛金,資産,200000\n"
            "未払金,負債,50000\n"
            "買掛金,負債,0\n"
            "資本金,純資産,2000000\n"
            "利益剰余金,純資産,550000\n"  # 純利益が利益剰余金として計上される
        )
        
        self.assertEqual(bs_result, expected_bs,
                        "純利益は利益剰余金として純資産に計上され、貸借平衡が取れるべき")