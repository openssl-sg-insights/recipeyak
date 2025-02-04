from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from core.models.ingredient import Ingredient  # noqa: F401
from core.models.invite import Invite  # noqa: F401
from core.models.membership import Membership, get_random_ical_id  # noqa: F401
from core.models.note import Note
from core.models.reaction import Reaction  # noqa: F401
from core.models.recipe import Recipe  # noqa: F401
from core.models.recipe_change import ChangeType, RecipeChange  # noqa: F401
from core.models.recipe_view import RecipeView  # noqa: F401
from core.models.scheduled_recipe import ScheduledRecipe  # noqa: F401
from core.models.scrape import Scrape  # noqa: F401
from core.models.section import Section  # noqa: F401
from core.models.shopping_list import ShoppingList  # noqa: F401
from core.models.step import Step  # noqa: F401
from core.models.team import Team  # noqa: F401
from core.models.timeline_event import TimelineEvent  # noqa: F401
from core.models.upload import Upload  # noqa: F401
from core.models.user import User  # noqa: F401


def user_active_team_ids(user):
    return user.membership_set.filter(is_active=True).values_list("team")


def user_and_team_recipes(user: User) -> QuerySet[Recipe]:
    return Recipe.objects.filter(
        Q(owner_user=user) | Q(owner_team__in=user_active_team_ids(user))
    ).prefetch_related(
        "owner",
        "step_set",
        "ingredient_set",
        "scheduledrecipe_set",
        "notes",
        "notes__created_by",
        "notes__last_modified_by",
        "notes__uploads",
        "notes__reactions",
        "notes__reactions__created_by",
        "timelineevent_set",
        "timelineevent_set__created_by",
        "section_set",
    )


def user_and_team_recipe_or_404(user: User, recipe_pk: str) -> Recipe:
    return get_object_or_404(user_and_team_recipes(user), pk=recipe_pk)


def user_and_team_ingredients(user: User) -> QuerySet[Ingredient]:
    return Ingredient.objects.filter(recipe__in=user_and_team_recipes(user))


def user_and_team_steps(user: User) -> QuerySet[Step]:
    return Step.objects.filter(recipe__in=user_and_team_recipes(user))


def user_and_team_notes(user: User) -> QuerySet[Note]:
    return Note.objects.filter(recipe__in=user_and_team_recipes(user))


def user_reactions(user: User) -> QuerySet[Reaction]:
    return Reaction.objects.filter(created_by=user)
