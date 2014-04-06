from django.contrib import admin

from photo.models import *

# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)

