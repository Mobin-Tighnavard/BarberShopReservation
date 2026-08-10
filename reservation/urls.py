from django.urls import path,include

urlpatterns = [
    path("api/",include("reservation.api.v1.urls")),
]