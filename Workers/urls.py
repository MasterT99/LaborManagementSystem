from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('AddWork/', views.add_worker, name="AddWork"),
    path('Owner/', include("Owner.urls")),
    # path('Owner/', include("Owner.urls")),
    # path('Manager/', include("Manager.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
