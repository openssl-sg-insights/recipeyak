from __future__ import annotations

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.auth.permissions import has_recipe_access
from core.models import Recipe, ScheduledRecipe, User
from core.recipes.serializers import RecipeTimelineSerializer
from core.request import AuthedRequest


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_recipe_timeline(request: AuthedRequest, recipe_pk: int) -> Response:
    user: User = request.user
    team = user.schedule_team

    recipe = get_object_or_404(Recipe, pk=recipe_pk)

    if not has_recipe_access(recipe=recipe, user=user):
        return Response(status=status.HTTP_403_FORBIDDEN)

    scheduled_recipes = ScheduledRecipe.objects.filter(
        Q(team=team) | Q(user=user)
    ).filter(recipe=recipe_pk)

    return Response(RecipeTimelineSerializer(scheduled_recipes, many=True).data)
