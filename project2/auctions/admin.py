from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.Bidding)
admin.site.register(models.User)
admin.site.register(models.Comment)
admin.site.register(models.Category)

class ImageInline(admin.TabularInline):
    model = models.Image
    
@admin.register(models.Listing)
class ListingAdmin(admin.ModelAdmin):
        inlines = [ImageInline]
admin.site.register(models.Image)
        
