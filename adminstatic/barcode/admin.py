from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import DateInput, ValidationError
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import *

# Unregister Group from admin if not needed
admin.site.unregister(Group)

# # class CertificateResource(resources.ModelResource):
#     def before_import_row(self, row, **kwargs):
#         certificate_number = row.get('certificate_number')
#         if Certificate.objects.filter(certificate_number=certificate_number).exists():
#             raise ValidationError(f"Certificate number '{certificate_number}' already exists.")
    
#     class Meta:
#         model = Certificate
#         fields = ('id', 'name', 'certificate_number', 'start_date', 'end_date')  # Include 'id' here
#         skip_unchanged = True
#         report_skipped = True

class CertificateResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        certificate_number = row.get('certificate_number')

        # Check for duplicate certificate numbers
        if Certificate.objects.filter(certificate_number=certificate_number).exists():
            raise ValidationError(f"Certificate number '{certificate_number}' already exists.")
        
        # Convert name to title case
        if 'name' in row:
            row['name'] = row['name'].title()  # Convert to title case

    class Meta:
        model = Certificate
        fields = ('id', 'title', 'name', 'certificate_number', 'start_date', 'end_date')
        skip_unchanged = True
        report_skipped = True

@admin.register(Certificate)
class CertificateAdmin(ImportExportModelAdmin):
    resource_class = CertificateResource
    formfield_overrides = {
        models.DateField: {'widget': DateInput(attrs={'type': 'date'})},
    }
    list_display = ['name', 'certificate_number', 'start_date', 'end_date', 'image']
    list_filter = ['start_date', 'end_date']


admin.site.register(ContactMessage)