from django.contrib import admin
from rango.models import Category,Page,Review


# Register your models here.
from rango.models import Category, Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category','url')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('username','stars','reviews')
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
admin.site.register(Page, PageAdmin)    
admin.site.register(Category,CategoryAdmin)
admin.site.register(Review,ReviewAdmin)


