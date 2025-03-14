from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("vehicle/<int:id>/", views.details, name="details"),
    path('edit/<int:id>/', views.edit, name='edit'),
    path("delete/<int:id>/", views.delete, name="delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)