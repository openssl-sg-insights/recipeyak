from rest_framework import serializers

from core.models import Recipe
from core.recipes.serializers import IngredientSerializer, OwnerRelatedField
from core.serialization import BaseModelSerializer


class RecipeExportSerializer(BaseModelSerializer):

    steps = serializers.ListField(child=serializers.CharField(), source="step_set.all")

    ingredients = IngredientSerializer(
        many=True,
        read_only=True,
        fields=("quantity", "name", "description", "optional"),
        source="ingredient_set",
    )
    owner = OwnerRelatedField(read_only=True, export=True)

    class Meta:
        model = Recipe
        read_only = True
        fields = (
            "id",
            "name",
            "author",
            "time",
            "source",
            "servings",
            "ingredients",
            "steps",
            "owner",
            "tags",
        )
