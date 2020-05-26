from django.contrib import admin

from .models import ImageFile, RecognitionResult


class ImageFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'date_added')
    readonly_fields = ('name',)


class RecognitionResultAdmin(admin.ModelAdmin):
    list_display = ('image_file', 'letter', 'date_added')


admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(RecognitionResult, RecognitionResultAdmin)
