from django.contrib import admin

from .models import Comment, Bid, Listing, Auction, Profile

admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Auction)
admin.site.register(Profile)
