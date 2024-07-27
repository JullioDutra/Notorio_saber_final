
from django.contrib import admin
from .models import CarouselImage

class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'order', 'image')
    list_display_links = ('caption',)
    list_editable = ('order',)

admin.site.register(CarouselImage, CarouselImageAdmin)
