from uuid import uuid4
from django.db import models

# Create your models here.
class SibAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    api_key = models.CharField(
        max_length=255,
        help_text="Dapatkan API-KEY di <a href='https://edikartono.com/' target='_blank' rel='noopener'>API KEY</a>"
    )

    class Meta:
        verbose_name_plural = "API KEY"

    def __str__(self) -> str:
        return self.api_key