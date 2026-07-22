from django.urls import path , include

urlpatterns = [
    path("api/",include("salon.api.v1.urls")),
]