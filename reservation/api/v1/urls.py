from django.urls import path
from .views import PaymentCreateApiView

urlpatterns = [
    path("v1/payment/",PaymentCreateApiView.as_view(),name = "create_payment"),
]