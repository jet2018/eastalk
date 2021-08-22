from django.conf.urls import include
from django.urls import path
from .views import BlogListCreateView, IndexView

app_name = "blog"
urlpatterns = [
    path('', IndexView.as_view(), name="splash"),
    path('articles', BlogListCreateView.as_view()),
    path('authors/', include("authors.urls")),
]
