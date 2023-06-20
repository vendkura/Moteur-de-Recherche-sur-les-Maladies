from django.urls import path
from .import views

#URL conf module
urlpatterns = [
    path('index/', views.gotoindex),
    path('testin/', views.my_view),
    path('dialogflow/', views.dialog_flow_Prompt),
]
