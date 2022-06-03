from uuid import uuid4
from django.db import models

class SibAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    api_key = models.CharField(
        max_length=255,
        help_text="Dapatkan API-KEY di <a href='https://www.sendinblue.com/?tap_a=30591-fb13f0&tap_s=2662645-7d6da9' target='_blank' rel='noopener'>Send In Blue</a>"
    )

    class Meta:
        verbose_name_plural = "API KEY"

    def __str__(self) -> str:
        return self.api_key