from datetime import datetime, timedelta

from app import log, config, redisBroker
from app.model import ValidationTx, ValidationStatus, Provider

LOG = log.get_logger()

def resend_validations_without_response():
    LOG.info('Running cron job: resend_validations_without_response')
    start_timestamp = datetime.utcnow() - timedelta(minutes=10)
    rows = ValidationTx.objects(status=ValidationStatus.NEW, created__gte=start_timestamp)
    if rows:
        transactions = [each.as_dict() for each in rows]
        for transaction in transactions:
            providersRows = Provider.objects(id=transaction["provider"])
            if providersRows:
                provider = providersRows[0]
                doc = {
                    "type": transaction["validationType"],
                    "action": "create",
                    "transactionId": f'{transaction["id"]}',
                    "params": transaction["requestParams"],
                    'did': transaction["did"]
                }
                redisBroker.send_validator_message(doc, provider.apiKey)
            else:
                LOG.error(f'Provider from transaction {str(transaction.id)} not found')
            
            