from django.contrib import admin

from .models import NewDialogs


class NewDialogsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'client_session',
        'phone_number',
        'have_to_start',
        'created_at',
    ]
    list_filter = ['created_at', 'client_session__name']


admin.site.register(NewDialogs, NewDialogsAdmin)
