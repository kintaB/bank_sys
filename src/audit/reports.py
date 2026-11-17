from src.models import AuditSeverity, RiskLevel


class AuditReports:
    def __init__(self, audit_log, risk_analyzer, processor=None):
        self.audit_log = audit_log
        self.risk_analyzer = risk_analyzer
        self.processor = processor

    def suspicious_operations(self):
        result = []
        for item in self.risk_analyzer.last_results:
            if item['level'] == RiskLevel.MEDIUM or item['level'] == RiskLevel.HIGH:
                result.append(item)
        return result

    def client_risk_profile(self, client_id, bank):
        client = bank.clients[client_id]
        medium = 0
        high = 0

        for item in self.risk_analyzer.last_results:
            if item['sender'] in client.accounts:
                if item['level'] == RiskLevel.MEDIUM:
                    medium = medium + 1
                if item['level'] == RiskLevel.HIGH:
                    high = high + 1

        if high > 0:
            profile = RiskLevel.HIGH
        elif medium > 0:
            profile = RiskLevel.MEDIUM
        else:
            profile = RiskLevel.LOW

        return {
            'client_id': client_id,
            'profile': profile,
            'medium': medium,
            'high': high,
            'suspicious_marks': client._susp_operations,
        }

    def error_statistics(self):
        errors = len(self.audit_log.filter(severity=AuditSeverity.ERROR))
        critical = len(self.audit_log.filter(severity=AuditSeverity.CRITICAL))
        processor_errors = 0
        if self.processor is not None:
            processor_errors = len(self.processor.errors)

        return {
            'audit_errors': errors,
            'audit_critical': critical,
            'processor_errors': processor_errors,
        }
