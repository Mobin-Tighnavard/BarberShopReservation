from django.urls import path
from .views.public import PaymentCreateApiView
from .views.admin import (AdminReservationListApiView , AdminPendingPaymentListApiView,AdminPaymentStatusUpdateApiView,
                          AdminReservationRetrieveApiview,AdminReservationPendingRetrieveApiView)

urlpatterns = [
    path("v1/payment/",PaymentCreateApiView.as_view(),name = "create-payment"),
    path("v1/list/",AdminReservationListApiView.as_view(),name = "admin-reservation-list"),
    path("v1/retrieve/<int:pk>/",AdminReservationRetrieveApiview.as_view(),name = "admin-reservation-retrieve"),
    path("v1/pending-payments/",AdminPendingPaymentListApiView.as_view(),
         name = "admin-pending-payment-list"),
    path("v1/pending-payments/retrieve/<int:pk>/", AdminReservationPendingRetrieveApiView.as_view(),
         name="admin-pending-payment-retrieve"),
    path("v1/payment/<int:pk>/status", AdminPaymentStatusUpdateApiView.as_view(),
         name="admin-payment-status-update"),
]