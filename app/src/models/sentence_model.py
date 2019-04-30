from neomodel import (
    StructuredNode,
    StringProperty,
    DateTimeProperty,
    UniqueIdProperty
)

from datetime import datetime

class Sentence(StructuredNode):

    nodeId = UniqueIdProperty()
    sentence = StringProperty(required=True)
    addedOn = DateTimeProperty(default_now=True)
    updatedOn = DateTimeProperty()
    sentimentScore = StringProperty()
    magnitudeScore = StringProperty()

    def pre_save(self):
        self.updatedOn = datetime.utcnow()
        