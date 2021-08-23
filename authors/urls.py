from django.urls import path
from .views import AuthorCreateView, Subscribe

app_name = "blog"
urlpatterns = [
    path('', AuthorCreateView.as_view()),
    path("subscribe/", Subscribe)
]
