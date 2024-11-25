from django.urls import path
from .views import *
# from .views import home
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('certificate_check/', certificate_check, name='certificate_check'),
    path('contact_process/', contact_process, name='contact_process'),
    path('generate', generate_qr, name='generate_qr'),
    path('verify_code/', verify_code, name='verify_code'),
    path('subscribe/', subscribe, name='subscribe'),
    path('subscribe/', subscribe, name='subscribe'),
    # path('show_qr/', show_user_details, name='show_qr'),
    path('certificate/<int:certificate_id>/', view_certificate, name='view_certificate'),
    path('download_certificate/<int:certificate_id>/', download_certificate, name='download_certificate')
    #  path('download_certificate/<int:certificate_id>/', download_certificate, name='download_certificate'),
]
