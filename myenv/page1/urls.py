from django.urls import path
from .import views

#URL conf module
urlpatterns = [
    path('disease/',views.disease_info_view),
    path('disease_info/',views.disease_info_viewV2),
]
