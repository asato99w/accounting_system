from src.main import AccountingSystem

def test_first():
    accounting_system = AccountingSystem()
    result = accounting_system.output_balance_sheet()
    expected = "勘定科目,区分,金額\n現金,資産,0\n未払金,負債,0\n"
    assert result == expected

def test_2():
    data = [
            {
              "credit": {
                "現金": 1000
              }
            }
          ]
    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_balance_sheet()
    expected = "勘定科目,区分,金額\n現金,資産,1000\n"
    assert result == expected

def test_3():
    data = [
            {
              "debit": {
                "未払金": 500,
              }
            }
          ]
    accounting_system = AccountingSystem()
    accounting_system.input(data)
    result = accounting_system.output_balance_sheet()
    expected = "勘定科目,区分,金額\n未払金,負債,500\n"
    assert result == expected

# def test_2():
#     data = [
#             {
#              "debit": {
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
#     expected = "勘定科目,区分,金額\n現金,資産,1000\n未払金,負債,1000\n"
#     assert result == expected