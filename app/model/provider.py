import datetime

from mongoengine import StringField, DictField, DateTimeField, ListField, Document

class Provider(Document):
    name = StringField(max_length=128)
    logo = StringField()
    apikey = StringField(max_length=128)
    validationTypes = ListField(StringField(), default=[])
    created = DateTimeField()
    modified = DateTimeField(default=datetime.datetime.now)

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

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        return super(Provider, self).save(*args, **kwargs)