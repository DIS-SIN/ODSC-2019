from neomodel import (
        StructuredNode, 
        StructuredRel, 
        StringProperty, 
        UniqueIdProperty, 
        DateTimeProperty,
        BooleanProperty,
        Relationship,
        RelationshipTo,
        One,
        OneOrMore
)
from datetime import datetime

class ScheduleItemPresenter(StructuredRel):
    addedOn = DateTimeProperty(default_now=True)
    rating = StringProperty(
        choices={
            '0':'Extremely Bad',
            '1':'Very Bad',
            '2':'Bad',
            '3':'Okay',
            '4':'Good',
            '4':'Very Good',
            '5':'Extremely Good'
        }
    )
    wasLate= BooleanProperty()
    updatedOn = DateTimeProperty()
    def pre_save(self):
        self.updatedOn = datetime.utcnow()

class ScheduleItemCategory(StructuredRel):
    addedOn = DateTimeProperty(default_now=True)

class ScheduleItemText(StructuredRel):
    addedOn = DateTimeProperty(default_now=True)

class ScheduleItem(StructuredNode):
    nodeId = UniqueIdProperty()
    title = StringProperty(required=True, unique_index=True)
    addedOn = DateTimeProperty(default_now=True)
    updatedOn = DateTimeProperty()
    itemTime = DateTimeProperty(required=True)
    presenters = RelationshipTo(
        '.presenter_model.Presenter',
        'PRESENTER',
        model=ScheduleItemPresenter,
        cardinality=OneOrMore
    )
    categories = Relationship(
        '.category_model.Category', 
        'CATEGORY',
        model=ScheduleItemCategory
    )
    excerpt = RelationshipTo(
        '.text_model.Text',
        'EXCERPT',
        model=ScheduleItemText,
        cardinality=One
    )
    
    
    def pre_save(self) -> None:
        self.updatedOn = datetime.utcnow()
    
    
