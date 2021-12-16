from enum import Enum
from typing import TYPE_CHECKING

from django.db import models
from softdelete.models import SoftDeleteManager, SoftDeleteObject

from core.models.base import CommonInfo

if TYPE_CHECKING:
    from core.models import User, Recipe  # noqa: F401


class TimelineEventKind(Enum):
    created = "created"
    archived = "archived"
    unarchived = "unarchived"
    deleted = "deleted"


class TimelineEvent(CommonInfo, SoftDeleteObject):
    action = models.CharField(max_length=255)
    created_by = models.ForeignKey["User"]("User", on_delete=models.CASCADE, null=True)
    recipe = models.ForeignKey["Recipe"]("Recipe", on_delete=models.CASCADE)

    objects = SoftDeleteManager["TimelineEvent"]()

    class Meta:
        db_table = "timeline_event"
        ordering = ["-created"]