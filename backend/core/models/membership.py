from typing import TYPE_CHECKING

from django.db import models
from django.db.models.manager import Manager
from django.utils.crypto import get_random_string
from typing_extensions import Literal

from core.models.base import CommonInfo

if TYPE_CHECKING:
    from core.models.team import Team  # noqa: F401
    from core.models.user import User  # noqa: F401


def get_random_ical_id() -> str:
    return get_random_string(length=48)


class Membership(CommonInfo):
    ADMIN: Literal["admin"] = "admin"
    CONTRIBUTOR: Literal["contributor"] = "contributor"
    READ_ONLY: Literal["read"] = "read"

    MEMBERSHIP_CHOICES = (
        (ADMIN, ADMIN),
        (CONTRIBUTOR, CONTRIBUTOR),
        (READ_ONLY, READ_ONLY),
    )

    level = models.CharField(
        max_length=11, choices=MEMBERSHIP_CHOICES, default=CONTRIBUTOR
    )

    team = models.ForeignKey["Team"]("Team", on_delete=models.CASCADE)
    user = models.ForeignKey["User"]("User", on_delete=models.CASCADE)

    calendar_sync_enabled = models.BooleanField(
        default=False,
        help_text="When enabled, accept requests that have the valid secret key.",
    )
    calendar_secret_key = models.TextField(
        default=get_random_ical_id,
        help_text="Secret key used to construct the icalendar url.",
    )

    objects = Manager["Membership"]()

    class Meta:
        unique_together = (("user", "team"),)

    # A user is activated once they accept their invite
    is_active = models.BooleanField(default=False)

    def set_active(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            # NOTE: although we check inside the serializer to prevent demoting the
            # last admin, this forms a last line of defence
            current = Membership.objects.get(pk=self.pk)
            one_admin_left = len(self.team.admins()) == 1
            demoting_admin = current.level == self.ADMIN and self.level != self.ADMIN
            if one_admin_left and demoting_admin:
                raise ValueError("cannot demote self as last admin")
        super().save(*args, **kwargs)

    def delete(self):
        last_member = self.team.membership_set.count() == 1
        if last_member:
            raise ValueError("cannot delete last member of team")
        super().delete()

    def __str__(self):
        return f"<Membership • user_email: {self.user.email}, team: {self.team.id} level: {self.level}>"
