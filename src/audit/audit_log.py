import os
from datetime import datetime

from src.models import AuditSeverity


class AuditLog:
    def __init__(self, file_path='logs/audit.log'):
        self.records = []
        self.file_path = file_path

    def add(self, message, severity=AuditSeverity.INFO, transaction_id=None):
        record = {
            'time': datetime.now(),
            'severity': severity,
            'message': message,
            'transaction_id': transaction_id,
        }
        self.records.append(record)
        self._save_to_file(record)
        return record

    def _save_to_file(self, record):
        folder = os.path.dirname(self.file_path)
        if folder != '':
            os.makedirs(folder, exist_ok=True)

        line = (
            str(record['time'])
            + ' | '
            + record['severity'].value
            + ' | '
            + str(record['transaction_id'])
            + ' | '
            + record['message']
            + '\n'
        )
        file = open(self.file_path, 'a', encoding='utf-8')
        file.write(line)
        file.close()

    def filter(self, severity=None, transaction_id=None):
        result = []
        for record in self.records:
            ok = True
            if severity is not None and record['severity'] != severity:
                ok = False
            if transaction_id is not None and record['transaction_id'] != transaction_id:
                ok = False
            if ok:
                result.append(record)
        return result
