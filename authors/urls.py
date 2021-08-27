from django.urls import path
from .views import AuthorCreateView, RegisterAsAuthor

app_name = "blog"
urlpatterns = [
    path('', AuthorCreateView.as_view()),
    path('brief/', AuthorCreateView.as_view()),
    path("add/", RegisterAsAuthor)
]
