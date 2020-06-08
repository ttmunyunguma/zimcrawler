from django.urls import path

from propertyzw.views import PropertyView

urlpatterns = [
    path('', PropertyView.as_view(), name='properties')
]
