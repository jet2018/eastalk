from django.urls import path

from .views import AuthorCreateView, BriefAuthors, FollowAuthor, GetAllUsers, RegisterAsAuthor

app_name = "authors"
urlpatterns = [
    path('', AuthorCreateView.as_view()),
    path('brief/', BriefAuthors.as_view()),
    path("add/", RegisterAsAuthor),
    path("all-users/", GetAllUsers.as_view()),
    path("follow/<pk>", FollowAuthor),
]
