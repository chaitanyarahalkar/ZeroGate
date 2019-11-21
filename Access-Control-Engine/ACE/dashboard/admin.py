from django.contrib import admin
from dashboard.models import User, Resources

# Register your models here.

admin.site.site_header = 'Access Control Engine'
admin.site.site_title = 'Access Control Engine'
admin.site.site_url = None

admin.site.register(User)
admin.site.register(Resources)