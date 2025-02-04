from datetime import date

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, ScheduledRecipe, Team, User

pytestmark = pytest.mark.django_db


def test_get_recipe_timeline(
    user: User, user2: User, client: APIClient, recipe: Recipe, empty_team: Team
) -> None:
    """
    Ensure our timeline endpoint returns the correct data shape. We could
    just serialize this every time in the recipe serialize but the size is will
    continue to grow and will require pagination so breaking it out into its
    own endpoint is eaiser.
    """

    assert recipe.owner == user

    url = f"/api/v1/recipes/{recipe.id}/timeline"
    res = client.get(url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, "Endpoint requires auth."

    client.force_authenticate(user)

    res = client.get("/api/v1/recipes/does_not_exist/timeline")
    assert res.status_code == status.HTTP_404_NOT_FOUND

    res = client.get(url)
    assert (
        ScheduledRecipe.objects.filter(recipe=recipe).exists() is False
    ), "We should start off without ScheduledRecipes"
    assert res.status_code == status.HTTP_200_OK
    assert (
        not res.json()
    ), "Should have an empty array since we haven't scheduled a recipe yet."

    scheduled = recipe.schedule(on=date(1776, 1, 1), user=user)

    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK

    # check response shape

    assert len(res.json()) == 1

    assert res.json()[0]["id"] == scheduled.id
    assert res.json()[0]["on"] == str(scheduled.on)

    # Fetch timeline for a recipe the user isn't allowed to access

    assert scheduled.team is None, (
        "We are testing that the user conditional works here "
        "so we need the team filter option to not be used."
    )

    client.force_authenticate(user2)
    res = client.get(url)
    assert (
        res.status_code == status.HTTP_403_FORBIDDEN
    ), "User field didn't match so we shouldn't return anything"

    # Setup `empty_team` as the owner of the recipe and scheduled recipe so we
    # test fetching against the team
    team = empty_team
    recipe.owner = team
    recipe.save()
    scheduled.team = team
    scheduled.save()
    team.force_join_admin(user2)
    user2.schedule_team = team
    user2.save()

    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 1, "should return the same response"


def test_get_recipe_timeline_ordering(
    user: User, client: APIClient, recipe: Recipe
) -> None:
    """
    ensure we return the timeline items in the correct ordering
    """

    for time in [date(1776, 1, 1), date(1776, 2, 1), date(1776, 3, 1)]:
        recipe.schedule(on=time, user=user)

    url = f"/api/v1/recipes/{recipe.id}/timeline"
    client.force_authenticate(user)
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK

    assert [scheduled["on"] for scheduled in res.json()] == [
        "1776-03-01",
        "1776-02-01",
        "1776-01-01",
    ]
