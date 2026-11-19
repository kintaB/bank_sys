import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.demo import BankDemo
from src.reports import ReportBuilder

demo = BankDemo()
demo.run()

builder = ReportBuilder(
    bank=demo.bank,
    transactions=demo.transactions,
    risk_analyzer=demo.risk,
    balance_flow=demo.balance_flow,
    output_dir='reports',
)

client_report = builder.build_client_report('c1')
bank_report = builder.build_bank_report()
risk_report = builder.build_risk_report()

print('=== TEXT CLIENT ===')
print(builder.to_text(client_report))

json_client = builder.export_to_json(client_report, 'client_c1.json')
json_bank = builder.export_to_json(bank_report, 'bank.json')
json_risk = builder.export_to_json(risk_report, 'risks.json')
csv_risk = builder.export_to_csv(risk_report['items'], 'risks.csv')
charts = builder.save_charts()

print('saved json:', json_client, json_bank, json_risk)
print('saved csv:', csv_risk)
print('saved charts:', charts)
print('Day 7 reports finished')
