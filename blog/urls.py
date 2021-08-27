from django.conf.urls import include
from django.urls import path
from .views import BlogListCreateView, IndexView, Subscribe, Unsubscribe, GetCategories, MostRecentStories
from authors.views import SponsorListOrCreate, BriefSponsors
app_name = "blog"
urlpatterns = [
    path('', IndexView.as_view(), name="splash"),
    path('articles', BlogListCreateView.as_view()),
    path('recent', MostRecentStories.as_view()),
    path('authors/', include("authors.urls")),
    path("subscribe/", Subscribe),
    path("unsubscribe/", Unsubscribe),
    path("categories/", GetCategories.as_view()),
    path('sponsors/', SponsorListOrCreate.as_view()),
    path('sponsors/brief/', BriefSponsors.as_view()),

]
