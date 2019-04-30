from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    DateTimeProperty,
    RelationshipFrom
)

from datetime import datetime

class Organization(StructuredNode):

    nodeId = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    addedOn = DateTimeProperty(default_now=True)
    updatedOn = DateTimeProperty()
    presenters = RelationshipFrom(
        '.presenter_model.Presenter',
        'ORGANIZATION',
        model='presenter_model.PresenterOrganization')

    def pre_save(self) -> None:
        self.updatedOn = datetime.utcnow() 