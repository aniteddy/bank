from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('b/', include('b.urls')),
    path('admin/', admin.site.urls),
]
