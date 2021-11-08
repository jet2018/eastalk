from django.conf.urls import include
from django.urls import path

from authors.views import SponsorListOrCreate, BriefSponsors
from .views import BlogListCreateView, BlogUpdateDeleteRetrieveAPIView, Bookmark, ContactUs, IndexView, SavedArticles, Subscribe, GetCategories, MostRecentStories, TopAuthors, TopReaders, TopSponsors, VoteUp, VoteDown

app_name = "blog"
urlpatterns = [
    path('', IndexView.as_view(), name="splash"),
    path('articles', BlogListCreateView.as_view()),
    path('article/<slug>/', BlogUpdateDeleteRetrieveAPIView.as_view()),
    path('articles/brief/', MostRecentStories.as_view()),
    path('articles/save/<slug>', Bookmark),
    path('authors/', include("authors.urls")),
    path("subscribe/", Subscribe),
    # path("unsubscribe/", Unsubscribe),
    path("<slug>/like", VoteUp),
    path("<slug>/unlike", VoteDown),
    path("categories/", GetCategories.as_view()),
    path('sponsors/', SponsorListOrCreate.as_view()),
    path('sponsors/brief/', BriefSponsors.as_view()),
    path("community/top/authors", TopAuthors.as_view()),
    path("community/top/readers", TopReaders.as_view()),
    path("community/top/sponsors", TopSponsors.as_view()),
    path("contact_us/", ContactUs)
]
