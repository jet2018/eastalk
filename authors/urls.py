from django.urls import path
from .views import AuthorCreateView

app_name = "blog"
urlpatterns = [
    path('', AuthorCreateView.as_view()),
    path('brief/', AuthorCreateView.as_view()),
]
