from django.urls import path
from .views.public import PaymentCreateApiView
from .views.admin import (AdminReservationListApiView , AdminPendingPaymentListApiView,AdminPaymentStatusUpdateApiView,
                          AdminReservationRetrieveApiview,AdminReservationPendingRetrieveApiView,
                          AdminPaymentStatusUpdateAcceptedApiView,AdminPaymentStatusUpdateRejectedApiView,
                          AdminReservationCreateApiView)

urlpatterns = [
    path("v1/payment/upload_img/",PaymentCreateApiView.as_view(),name = "create-payment"),
    path("v1/list/",AdminReservationListApiView.as_view(),name = "admin-reservation-list"),
    path("v1/create/",AdminReservationCreateApiView.as_view(),name = "admin-reservation-create"),
    path("v1/retrieve/<int:pk>/",AdminReservationRetrieveApiview.as_view(),name = "admin-reservation-retrieve"),
    path("v1/pending-payments/",AdminPendingPaymentListApiView.as_view(),
         name = "admin-pending-payment-list"),
    path("v1/pending-payments/retrieve/<int:pk>/", AdminReservationPendingRetrieveApiView.as_view(),
         name="admin-pending-payment-retrieve"),
    # path("v1/payment/<int:pk>/status/", AdminPaymentStatusUpdateApiView.as_view(),
    #      name="admin-payment-status-update"),
    path("v1/payment/<int:pk>/update/status/accepted/", AdminPaymentStatusUpdateAcceptedApiView.as_view(),
             name="admin-payment-status-update-accepted"),

    path("v1/payment/<int:pk>/update/status/rejected/", AdminPaymentStatusUpdateRejectedApiView.as_view(),
                 name="admin-payment-status-update-rejected"),
]