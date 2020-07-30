import datetime

from mongoengine import StringField, DictField, DateTimeField, Document, BooleanField, IntField

class ValidationStatus(object):
      NEW = "New"
      IN_PROGRESS = "In progress"
      CANCELATION_IN_PROGRESS = "Cancelation in progress"
      CANCELED = "Canceled"
      APPROVED = "Approved"
      REJECTED = "Rejected"

class ValidationTx(Document):
    did = StringField(max_length=128)
    provider = StringField(max_length=128)
    validationType = StringField(max_length=32)
    requestParams = DictField()
    status = StringField(max_length=32)
    reason = StringField(max_length=128)
    verifiedCredential = DictField()
    isSavedOnProfile=BooleanField()
    created = DateTimeField()
    retries = IntField()
    modified = DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return str(self.as_dict())

    def as_dict(self):
        if not self.isSavedOnProfile:
           self.isSavedOnProfile = False
        return {
            "id": str(self.id),
            "did": self.did,
            "provider": self.provider,
            "validationType": self.validationType,
            "requestParams": self.requestParams,
            "status": self.status,
            "reason": self.reason,
            "isSavedOnProfile": self.isSavedOnProfile,
            "verifiedCredential": self.verifiedCredential,
            "retries": self.retries,
            "created": str(self.created),
            "modified": str(self.modified)
        }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()
        return super(ValidationTx, self).save(*args, **kwargs)
