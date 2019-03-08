
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('', include('django_docker_example.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
