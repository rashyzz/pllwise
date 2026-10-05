from django.contrib import admin
from poll.models import Choice,CustomUser,Poll

# Register your models here.
admin.site.register(Choice)
admin.site.register(Poll)
admin.site.register(CustomUser)