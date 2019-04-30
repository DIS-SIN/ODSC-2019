from neomodel import (
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    StringProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
    OneOrMore
)
from datetime import datetime
from .item_model import ScheduleItemPresenter
##################################### OUTGOING RELATIONSHIP DEFINITIONS ################################################################################## 
class PresenterPosition(StructuredRel):
    addedOn = DateTimeProperty(default_now=True)
class PresenterOrganization(StructuredRel):
    addedOn = DateTimeProperty(default_now=True)

##################################### MODEL ##############################################################################################################
class Presenter(StructuredNode):
    nodeId = UniqueIdProperty()
    name = StringProperty(required=True)
    image = StringProperty(unique_index=True)
    linkedin = StringProperty()
    addedOn = DateTimeProperty(default_now=True)
    updatedOn = DateTimeProperty()
    positions = RelationshipTo(
        '.position_model.Position',
        'POSITION',
        model=PresenterPosition
    )
    organizations = RelationshipTo(
        '.position_model.Organization', 
        'ORGANIZATION', 
        model=PresenterOrganization)
    scheduleItems = RelationshipFrom(
        '.item_model.ScheduleItem',
        'PRESENTER',
        model=ScheduleItemPresenter,
        cardinality=OneOrMore
    )
    def pre_save(self):
        self.updatedOn = datetime.utcnow()