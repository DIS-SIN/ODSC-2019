from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    DateTimeProperty,
    StringProperty,
    RelationshipFrom,
    One
)
from datetime import datetime
from .item_model import ScheduleItemText
class Text(StructuredNode):

    nodeId = UniqueIdProperty()
    text = StringProperty(required=True)
    addedOn = DateTimeProperty(default_now=True)
    updatedOn = DateTimeProperty()
    sentimentScore = StringProperty()
    magnitudeScore = StringProperty()
    scheduleItem = RelationshipFrom(
        '.item_model.ScheduleItem', 
        'EXCERPT',
        model=ScheduleItemText,
        cardinality=One
    )
    def pre_save(self):
        self.updatedOn = datetime.utcnow()

