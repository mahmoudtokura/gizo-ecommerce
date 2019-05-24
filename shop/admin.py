from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product

# Register your models here.


class CategoryAdmin(ImportExportModelAdmin):
    list_display = ["pk", "name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(ImportExportModelAdmin):
    list_display = ["name", "slug", "price", "stock", "available", "created", "updated"]
    list_editable = ["price", "stock", "available"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 20
    list_filter = ("category",)
    search_fields = ("name",)


admin.site.register(Product, ProductAdmin)
