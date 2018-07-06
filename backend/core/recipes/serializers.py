from rest_framework import serializers

from core.models import (
    MyUser,
    Recipe,
    Ingredient,
    Step,
    Team,
)


class OwnerRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `owner` generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, Team):
            if self.export:
                return {'team': value.name}
            return {'id': value.id, 'type': 'team', 'name': value.name}
        elif isinstance(value, MyUser):
            if self.export:
                return {'user': value.email}
            return {'id': value.id, 'type': 'user'}
        raise Exception('Unexpected type of owner object')

    def __init__(self, *args, **kwargs):
        export = kwargs.pop('export', None)
        super().__init__(*args, **kwargs)
        self.export = export


class IngredientSerializer(serializers.ModelSerializer):
    """
    serializer the ingredient of a recipe
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'quantity', 'name', 'description', 'position', 'optional')

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class StepSerializer(serializers.ModelSerializer):
    """
    serializer the step of a recipe
    """

    class Meta:
        model = Step
        fields = ('id', 'text', 'position')

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RecipeSerializer(serializers.ModelSerializer):
    """
    serializer recipe
    """

    steps = StepSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    owner = OwnerRelatedField(read_only=True)
    # specify default None so we can use this as an optional field
    team = serializers.IntegerField(write_only=True, default=None)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author', 'source', 'time', 'ingredients',
                  'steps', 'servings', 'edits', 'modified',
                  'owner', 'team', 'last_scheduled')
        read_only_fields = ('owner', 'last_scheduled')

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate_steps(self, value):
        if value == []:
            raise serializers.ValidationError('steps are required')
        return value

    def validate_ingredients(self, value):
        if value == []:
            raise serializers.ValidationError('ingredients are required')
        return value

    def validate_team(self, value):
        if value is None:
            return None
        team = Team.objects.filter(id=value).first()
        if team is None:
            raise serializers.ValidationError('invalid team id provided')
        return team

    def create(self, validated_data) -> Recipe:
        """
        Since this a nested serializer, we need to write a custom create method.
        """
        ingredients = validated_data.pop('ingredients')
        steps = validated_data.pop('steps')

        # essentially an optional field
        team = validated_data.pop('team')

        validated_data['owner'] = team if team is not None \
            else self.context['request'].user

        recipe: Recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)
        for step in steps:
            Step.objects.create(recipe=recipe, **step)
        return recipe


class RecipeMoveCopySerializer(serializers.Serializer):
    id = serializers.IntegerField(max_value=None, min_value=0, write_only=True)
    type = serializers.ChoiceField(choices=['user', 'team'], write_only=True)

    def validate(self, data):
        if data['type'] == 'team' and not Team.objects.filter(id=data['id']).exists():
            raise serializers.ValidationError("team must exist")
        elif data['type'] == 'user' and not MyUser.objects.filter(id=data['id']).exists():
            raise serializers.ValidationError("user must exist")
        return data