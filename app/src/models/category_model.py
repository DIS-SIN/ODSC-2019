from neomodel import (
    UniqueIdProperty,
    StructuredNode,
    StringProperty,
    DateTimeProperty,
    Relationship
)
from .item_model import ScheduleItemCategory
from datetime import datetime

class Category(StructuredNode):

    nodeId = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    addedOn = DateTimeProperty(default_now=True)
    updatedOn = DateTimeProperty()
    scheduleItems = Relationship('.item_model.ScheduleItem',
                                 'CATEGORY',
                                  model=ScheduleItemCategory)
    def pre_save(self) -> None:
        self.updatedOn = datetime.utcnow()
                               