from db import Document, StringField, IntField

class flip_phones(Document):
    name = StringField()
    price = IntField()
    meta={
        'indexes':[
            'name',
            'price',
    ]
    }


class snap_phones(Document):
    name = StringField()
    price = IntField()
    meta={
        'indexes':[
            'name',
            'price',
    ]
    }