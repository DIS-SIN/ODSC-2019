from neomodel import (
    StringProperty,
    DateTimeProperty,
    UniqueIdProperty,
    RelationshipFrom
)
from neomodel.contrib import SemiStructuredNode
from datetime import datetime

class Position(SemiStructuredNode):

    nodeId = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    addedOn = DateTimeProperty(default_now=True)
    updatedOn = DateTimeProperty()
    presenters = RelationshipFrom(
        '.presenter_model.Presenter', 
        'POSITION', 
        model='.presenter_model.PresenterPosition')

    def pre_save(self) -> None:
        self.updatedOn = datetime.utcnow()