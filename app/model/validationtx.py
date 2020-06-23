import datetime

from mongoengine import StringField, DictField, DateTimeField, Document

class ValidationStatus(object):
      PENDING = "Pending"
      WAITING_RESPONSE = "Waiting response"
      SUCCEDED = "Succeded"
      FAILED = "Failed"

class ValidationTx(Document):
    did = StringField(max_length=128)
    provider = StringField(max_length=128)
    validationType = StringField(max_length=32)
    requestParams = DictField()
    status = StringField(max_length=32)
    reason = StringField(max_length=128)
    verifiedCredential = DictField()
    created = DateTimeField()
    modified = DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return str(self.as_dict())

    def as_dict(self):
        return {
            "id": str(self.id),
            "did": self.did,
            "provider": self.provider,
            "validationType": self.validationType,
            "requestParams": self.requestParams,
            "status": self.status,
            "reason": self.reason,
            "verifiedCredential": self.verifiedCredential,
            "created": str(self.created),
            "modified": str(self.modified)
        }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        return super(ValidationTx, self).save(*args, **kwargs)
