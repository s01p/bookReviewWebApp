from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Book,Comment,Record

@admin.register(Book,Comment,Record)
class BookAdmin(ImportExportModelAdmin):
    pass