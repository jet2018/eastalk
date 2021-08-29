from django.conf.urls import include
from django.urls import path

from authors.views import SponsorListOrCreate, BriefSponsors
from .views import BlogListCreateView, IndexView, Subscribe, Unsubscribe, GetCategories, MostRecentStories, VoteUp, \
    VoteDown

app_name = "blog"
urlpatterns = [
    path('', IndexView.as_view(), name="splash"),
    path('articles', BlogListCreateView.as_view()),
    path('articles/brief/', MostRecentStories.as_view()),
    path('authors/', include("authors.urls")),
    path("subscribe/", Subscribe),
    path("unsubscribe/", Unsubscribe),
    path("upvote/<slug>/", VoteUp),
    path("downvote/<slug>/", VoteDown),
    path("categories/", GetCategories.as_view()),
    path('sponsors/', SponsorListOrCreate.as_view()),
    path('sponsors/brief/', BriefSponsors.as_view()),

]
