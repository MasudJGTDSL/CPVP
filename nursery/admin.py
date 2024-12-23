from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

admin.site.register(Satvai,ImportExportModelAdmin)
admin.site.register(Brihat,ImportExportModelAdmin)
admin.site.register(CPVP,ImportExportModelAdmin)

