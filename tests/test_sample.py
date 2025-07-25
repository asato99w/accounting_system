from src.main import AccountingSystem

def test_first():
    accounting_system = AccountingSystem()
    result = accounting_system.output_balance_sheet()
    expected = "勘定科目,区分,金額\n"
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

def test_accounts_receivable():
  data = [
          {
            "credit": {
              "現金": 1000,
              "売掛金": 2000
            }
          }
        ]
  accounting_system = AccountingSystem()
  accounting_system.input(data)
  result = accounting_system.output_balance_sheet()
  expected = "勘定科目,区分,金額\n現金,資産,1000\n売掛金,資産,2000\n"
  assert result == expected

def test_accounts_payable():
  data = [
          {
            "debit": {
              "未払金": 500,
              "買掛金": 2500,
            }
          }
        ]
  accounting_system = AccountingSystem()
  accounting_system.input(data)
  result = accounting_system.output_balance_sheet()
  expected = "勘定科目,区分,金額\n未払金,負債,500\n買掛金,負債,2500\n"
  assert result == expected

def test_debit_and_credit():
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
    expected = "勘定科目,区分,金額\n現金,資産,1000\n未払金,負債,1000\n"
    assert result == expected

def test_multi_debit_and_credit():
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
  expected = "勘定科目,区分,金額\n現金,資産,3000\n未払金,負債,500\n買掛金,負債,2500\n"
  assert result == expected

def test_multi_debit_and_multi_credit():
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
  expected = "勘定科目,区分,金額\n現金,資産,1500\n売掛金,資産,1500\n未払金,負債,500\n買掛金,負債,2500\n"
  assert result == expected

def test_debit_cash():
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
  expected = "勘定科目,区分,金額\n現金,資産,1500\n売掛金,資産,1500\n未払金,負債,500\n買掛金,負債,2500\n"
  assert result == expected