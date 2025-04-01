from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name='login'),
    path("logout", views.logout_view, name="logout"),
    path("profile",  views.profile_view, name="profile"),
    path("request_admin", views.request_admin, name="request_admin"),
    path("remove_admin", views.remove_admin, name="remove_admin"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)