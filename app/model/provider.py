import datetime

from mongoengine import StringField, DictField, DateTimeField, ListField, Document

class Provider(Document):
    name = StringField(max_length=128)
    logo = StringField()
    apikey = StringField(max_length=128)
    validationTypes = ListField(StringField(), default=[])
    created = DateTimeField()
    modified = DateTimeField(default=datetime.datetime.utcnow)

    def __repr__(self):
        return str(self.as_dict())

    def as_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "logo": self.logo,
            "apiKey": self.apikey,
            "validationTypes": self.validationTypes,
            "created": str(self.created),
            "modified": str(self.modified)
        }

    def as_readonly_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "logo": self.logo,
            "validationTypes": self.validationTypes,
            "stats": self.stats
        }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.utcnow()
        self.modified = datetime.datetime.utcnow()
        return super(Provider, self).save(*args, **kwargs)