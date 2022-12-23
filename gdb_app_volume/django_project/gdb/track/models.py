from django.db import models
from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    DateTimeProperty,
    RelationshipTo,
    StructuredRel,
)


class Reference(StructuredRel):
    creation_date = DateTimeProperty(default_now=True)
    likes = IntegerProperty(default=0)


class Article(StructuredNode):
    creation_date = DateTimeProperty(default_now=True)
    author = StringProperty()
    title = StringProperty(required=True)
    body = StringProperty(required=True)

    reference = RelationshipTo('Article', 'refers_to', model=Reference)
