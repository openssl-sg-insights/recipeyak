from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from core.export.serializers import RecipeExportSerializer
from core.models import user_and_team_recipes
from core.request import AuthedRequest
from core.response import YamlResponse


@require_http_methods(["GET"])
@login_required(login_url="/login/")
def export_recipes(request: AuthedRequest, filetype: str, pk: Optional[str] = None):

    queryset = user_and_team_recipes(request.user).prefetch_related(
        "owner", "step_set", "ingredient_set", "scheduledrecipe_set"
    )

    if pk is not None:
        queryset = get_object_or_404(queryset, pk=pk)  # type: ignore[assignment]

    many = pk is None

    recipes = RecipeExportSerializer(queryset, many=many).data

    if filetype in ("yaml", "yml"):
        return YamlResponse(recipes)

    if filetype == "json":
        # we need safe=False so we can serializer both lists and dicts
        return JsonResponse(recipes, json_dumps_params={"indent": 2}, safe=False)

    raise Http404("unknown export filetype")
