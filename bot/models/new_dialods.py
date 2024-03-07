from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class NewDialogs(models.Model):
    client_session = models.ForeignKey('django_telethon.ClientSession',
                                       on_delete=models.CASCADE, verbose_name=_('Client session'))
    have_to_start = models.BooleanField(default=True, verbose_name=_('Have to start dialog'))
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('Phone number'),
    )
    created_at = models.DateTimeField(
        default=now,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('New Dialog')
        verbose_name_plural = _('New Dialogs')
