from __future__ import annotations

import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from .graphql.mutations import Mutation
from .graphql.queries import Query

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[DjangoOptimizerExtension],
)
