from neomodel.contrib import SemiStructuredNode
from neomodel import (
    StructuredRel,
    UniqueIdProperty,
    StringProperty,
    DateTimeProperty
)

class Word(SemiStructuredNode):
    
    nodeId = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    addedOn = DateTimeProperty(default_now=True)
