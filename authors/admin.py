from django.contrib import admin

# Register your models here.

from .models import Author, Sponsor


admin.site.register(Author)
admin.site.register(Sponsor)
