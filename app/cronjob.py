from datetime import datetime, timedelta
from mongoengine.queryset.visitor import Q
from app import log, config, redisBroker
from app.model import ValidationTx, ValidationStatus, Provider

LOG = log.get_logger()


def resend_validations_without_response():
    LOG.info('Running cron job: resend_validations_without_response')
    start_timestamp = datetime.utcnow() - timedelta(minutes=10)
    rows = ValidationTx.objects.filter((Q(status=ValidationStatus.NEW) & Q(created__lte=start_timestamp)) | Q(
        status=ValidationStatus.CANCELATION_IN_PROGRESS))

    if not rows:
        LOG.info("No pending validations to resend...")
        return

    for transaction in rows:

        if transaction.retries == config.TRANSACTION_RETRIES:
            LOG.info(f"Tried to resend the request {str(transaction.id)} too many times. It'll now be cancelled")
            transaction.reason = "Canceled - Too many retries, no response from provider"
            transaction.status = ValidationStatus.CANCELED
        else:
            if transaction.status == ValidationStatus.NEW:
                action = "create"
            else:
                action = "cancel"

            providers_rows = Provider.objects(id=transaction.provider)
            if providers_rows:
                provider = providers_rows[0]

                if not provider.validation[transaction.validationType]["manual"]:
                    doc = {
                        "type": transaction.validationType,
                        "action": action,
                        "transactionId": f'{str(transaction.id)}',
                        "params": transaction.requestParams,
                        'did': transaction.did
                    }
                    redisBroker.send_validator_message(doc, provider.did)

                    transaction.retries += 1
                    LOG.info(f"Resent the request {str(transaction.id)} to {provider.name}")
            else:
                LOG.error(f'Provider from transaction {str(transaction.id)} not found - Automatic canceling')
                transaction.reason = "Canceled automatic - Provider not found"
                transaction.status = ValidationStatus.CANCELED
        transaction.save()
