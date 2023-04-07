from django.contrib import admin
from .models import User, Bid, Listing, Comment

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "price")

# Register your models here.
admin.site.register(User)
admin.site.register(Bid, BidAdmin)
admin.site.register(Listing)
admin.site.register(Comment)