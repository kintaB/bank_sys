import csv
import json
import os

from src.models import RiskLevel, TransactionStatus


class ReportBuilder:
    def __init__(self, bank, transactions, risk_analyzer, balance_flow=None, output_dir='reports'):
        self.bank = bank
        self.transactions = transactions
        self.risk_analyzer = risk_analyzer
        self.balance_flow = balance_flow
        if self.balance_flow is None:
            self.balance_flow = []
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def build_client_report(self, client_id):
        client = self.bank.clients[client_id]
        accounts = []
        for number in client.accounts:
            account = self.bank.accounts[number]
            accounts.append({
                'account_number': number,
                'balance': account._balance,
                'status': account.account_status.value,
                'currency': account.currency.value,
            })

        return {
            'type': 'client',
            'client_id': client_id,
            'name': client.full_name.name + ' ' + client.full_name.surname,
            'total_balance': self.bank.get_total_balance(client_id),
            'accounts': accounts,
            'suspicious_marks': list(client._susp_operations),
        }

    def build_bank_report(self):
        completed = 0
        failed = 0
        rejected = 0
        cancelled = 0
        for tx in self.transactions:
            if tx.transaction_status == TransactionStatus.COMPLETED:
                completed = completed + 1
            elif tx.transaction_status == TransactionStatus.FAILED:
                failed = failed + 1
            elif tx.transaction_status == TransactionStatus.REJECTED:
                rejected = rejected + 1
            elif tx.transaction_status == TransactionStatus.CANCELLED:
                cancelled = cancelled + 1

        ranking = self.bank.get_clients_ranking()
        top3 = []
        i = 0
        while i < 3 and i < len(ranking):
            top3.append({'client_id': ranking[i][0], 'balance': ranking[i][1]})
            i = i + 1

        return {
            'type': 'bank',
            'clients': len(self.bank.clients),
            'accounts': len(self.bank.accounts),
            'total_balance': self.bank.get_bank_total_balance(),
            'top3': top3,
            'transactions': {
                'completed': completed,
                'failed': failed,
                'rejected': rejected,
                'cancelled': cancelled,
                'total': len(self.transactions),
            },
        }

    def build_risk_report(self):
        low = 0
        medium = 0
        high = 0
        rows = []
        for item in self.risk_analyzer.last_results:
            if item['level'] == RiskLevel.LOW:
                low = low + 1
            elif item['level'] == RiskLevel.MEDIUM:
                medium = medium + 1
            elif item['level'] == RiskLevel.HIGH:
                high = high + 1
            rows.append({
                'transaction_id': item['transaction_id'],
                'sender': item['sender'],
                'level': item['level'].value,
                'reasons': ', '.join(item['reasons']),
            })

        return {
            'type': 'risks',
            'counts': {'low': low, 'medium': medium, 'high': high},
            'items': rows,
        }

    def to_text(self, report):
        lines = ['Report: ' + report['type']]
        for key in report:
            if key == 'type':
                continue
            lines.append(str(key) + ': ' + str(report[key]))
        return '\n'.join(lines)

    def export_to_json(self, report, filename):
        path = os.path.join(self.output_dir, filename)
        file = open(path, 'w', encoding='utf-8')
        json.dump(report, file, ensure_ascii=False, indent=2)
        file.close()
        return path

    def export_to_csv(self, rows, filename):
        path = os.path.join(self.output_dir, filename)
        if len(rows) == 0:
            file = open(path, 'w', encoding='utf-8')
            file.write('')
            file.close()
            return path

        fieldnames = []
        for key in rows[0]:
            fieldnames.append(key)

        file = open(path, 'w', encoding='utf-8', newline='')
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        file.close()
        return path

    def save_charts(self):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        bank_report = self.build_bank_report()
        risk_report = self.build_risk_report()

        # 1) pie: transaction statuses
        labels = ['completed', 'failed', 'rejected', 'cancelled']
        values = [
            bank_report['transactions']['completed'],
            bank_report['transactions']['failed'],
            bank_report['transactions']['rejected'],
            bank_report['transactions']['cancelled'],
        ]
        plt.figure()
        plt.pie(values, labels=labels, autopct='%1.0f%%')
        plt.title('Transactions by status')
        pie_path = os.path.join(self.output_dir, 'chart_pie_statuses.png')
        plt.savefig(pie_path)
        plt.close()

        # 2) bar: top clients
        names = []
        balances = []
        for item in bank_report['top3']:
            names.append(item['client_id'])
            balances.append(item['balance'])
        plt.figure()
        plt.bar(names, balances)
        plt.title('Top-3 client balances')
        plt.xlabel('client')
        plt.ylabel('balance')
        bar_path = os.path.join(self.output_dir, 'chart_bar_top3.png')
        plt.savefig(bar_path)
        plt.close()

        # 3) balance flow line
        plt.figure()
        x = []
        i = 0
        while i < len(self.balance_flow):
            x.append(i)
            i = i + 1
        plt.plot(x, self.balance_flow, marker='o')
        plt.title('Balance flow (sample account)')
        plt.xlabel('step')
        plt.ylabel('balance')
        flow_path = os.path.join(self.output_dir, 'chart_balance_flow.png')
        plt.savefig(flow_path)
        plt.close()

        # optional risk bar
        plt.figure()
        plt.bar(
            ['low', 'medium', 'high'],
            [
                risk_report['counts']['low'],
                risk_report['counts']['medium'],
                risk_report['counts']['high'],
            ],
        )
        plt.title('Risk levels')
        risk_path = os.path.join(self.output_dir, 'chart_bar_risks.png')
        plt.savefig(risk_path)
        plt.close()

        return [pie_path, bar_path, flow_path, risk_path]
