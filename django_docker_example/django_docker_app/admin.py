from django.contrib import admin
from .models import *


class DDUserAdmin(admin.ModelAdmin):
    list_display = ('email',)


admin.site.register(DDUser, DDUserAdmin)
