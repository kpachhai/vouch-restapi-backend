import datetime

from mongoengine import StringField, DictField, DateTimeField, ListField, Document


class Provider(Document):
    did = StringField(max_length=128)
    name = StringField(max_length=128)
    logo = StringField()
    validation = DictField()
    created = DateTimeField()
    modified = DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return str(self.as_dict())

    def as_dict(self):
        return {
            "id": str(self.id),
            "did": self.did,
            "name": self.name,
            "logo": self.logo,
            "validation": self.validation,
            "created": str(self.created),
            "modified": str(self.modified)
        }

    def as_readonly_dict(self, stats={}):
        return {
            "id": str(self.id),
            "did": self.did,
            "name": self.name,
            "logo": self.logo,
            "validation": self.validation,
            "stats": stats
        }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()
        return super(Provider, self).save(*args, **kwargs)
