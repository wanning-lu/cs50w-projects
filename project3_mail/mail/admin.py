from django.contrib import admin
from .models import User, Email

# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = ("sender", "subject", "body")
    filter_horizontal = ("recipients",)

admin.site.register(Email, EmailAdmin)
admin.site.register(User)