from .models import Property
from django.views.generic import ListView


class PropertyView(ListView):
    model = Property
    context_object_name = 'properties'
    template_name = 'propertyzw/property-zw.html'
