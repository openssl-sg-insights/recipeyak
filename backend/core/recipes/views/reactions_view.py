from __future__ import annotations

import logging

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from psycopg2.errors import UniqueViolation  # type: ignore
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing_extensions import Literal

from core.models import user_and_team_notes, user_reactions
from core.models.reaction import Reaction
from core.recipes.serializers import serialize_reactions
from core.request import AuthedRequest
from core.serialization import RequestParams

logger = logging.getLogger(__name__)

EMOJIS = Literal["❤️", "😆", "🤮"]


class ReactToNoteViewParams(RequestParams):
    type: EMOJIS


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def note_reaction_create_view(request: AuthedRequest, note_pk: int) -> Response:
    params = ReactToNoteViewParams.parse_obj(request.data)

    note = get_object_or_404(user_and_team_notes(request.user), pk=note_pk)
    reaction = Reaction(emoji=params.type, created_by=request.user, note=note)
    try:
        reaction.save()
    except IntegrityError as e:
        if (
            isinstance(e.__cause__, UniqueViolation)
            and e.__cause__.diag.constraint_name == "one_reaction_per_user"
        ):
            reaction = user_reactions(request.user).filter(note=note).get()
        else:
            raise
    return Response(list(serialize_reactions([reaction]))[0])


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def note_reaction_delete_view(request: AuthedRequest, reaction_pk: str) -> Response:
    user_reactions(request.user).filter(pk=reaction_pk).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
