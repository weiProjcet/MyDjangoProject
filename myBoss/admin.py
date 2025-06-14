from django.contrib import admin
from .models import JobInfo, User, History

# Register your models here.
admin.site.register(JobInfo)
admin.site.register(User)
admin.site.register(History)
