from django.contrib import admin
from django.contrib.auth.views import *
from django.urls import path, include
from VHStore.views import *
from django.contrib.auth import get_user_model
from django.conf.urls.static import static
from django.conf import settings

User = get_user_model()

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(template_name="registration/signup.html"), name="signup"),
    path("", catalog, name="catalog"),
    path("seller/", seller_dashboard, name="seller_dashboard"),
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path("place_order/", place_order, name="place_order")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
