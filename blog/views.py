from django.conf import settings
from django.core.mail import send_mail
from authors.serializers import AuthorSerializer, UserSerializer
from blog.permissions import IsAuthor
from authors.models import Author, Sponsor
import datetime

from django.db.models import Q
from django.http.response import JsonResponse
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User


from blog.models import Blog, SubCategory, Subscribers, Category
from blog.serializers import BlogSerializer, CategoriesSerializer, CategorySerializer, SponsorSerializer
now = datetime.datetime.now()


# Create your views here.
class IndexView(TemplateView):
    template_name = "splash.html"


class BlogListView(generics.ListAPIView):
    """
        Get all articles 
    """
    model = Blog
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "author__user__username",
                     "category__category_name", "sub_category__sub_category_name"]
    filterset_fields = ["title", "author__user__username",
                        "category__category_name", "sub_category__sub_category_name"]

    def get_queryset(self):
        now = datetime.datetime.now()
        return Blog.objects.filter(Q(schedule_to__lte=now) | Q(schedule_to=None))


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAuthor])
def CreateArticle(request):
    """
        Create a brand new article.
        Must be authenticated and an author.
    """
    # colors
    # if non is sent, info is defaulted
    colors = request.data['blog_color'] if request.data['blog_color'] else "i"

    # author
    try:
        author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        return JsonResponse({"error": "You have to be an author to proceed."})

    # title
    title = request.data['title']
    if title == "":
        return JsonResponse({"error": "A unique title is to your article is required."})
    check_title = Blog.objects.filter(title__iexact=title)
    if check_title.count() > 10:
        return JsonResponse({"error": "A maximum of 10 articles can have similar titles, found "+check_title.count()+" with a similar title"})

    # image
    introductory_file = request.FILES['introductory_file'] if request.FILES['introductory_file'] else None

    # body
    body = request.data['body']
    if body == "":
        return JsonResponse({"error": "The body of your article is required."})

    # scheduling
    schedule_to = request.data['schedule_to'] if request.data['schedule_to'] and int(
        request.data['schedule_to']) > 0 else None
    if schedule_to:
        schedule_to = now+int(schedule_to)
    else:
        schedule_to = now
    # saving an article
    article = Blog.objects.create(
        title=title,
        author=author,
        schedule_to=schedule_to,
        body=body,
        blog_color=colors,
        introductory_file=introductory_file
    )
    # get categories
    categories = list(request.data['categories'])
    for id in categories:
        if id != ",":
            article.category.add(id)

    # get sub categories
    sub_categories = list(request.data['sub_categories'])
    for id in sub_categories:
        if id != ",":
            article.sub_category.add(id)

    blog = BlogSerializer(article)
    return JsonResponse({"success": "Article created successfully", "blog": blog.data})


# now = datetime.datetime.now()
# print(now)
# print(now + datetime.timedelta(days=3))
# print(datetime.datetime.date(datetime.timedelta(days=3)))

# create a new article
# class CreateArticle(generics.CreateAPIView):
#     """
#         Create a brand new article.
#         Must be authenticated and an author.
#     """
#     permission_classes = [IsAuthenticated, IsAuthor]
#     model = Blog
#     serializer_class = BlogSerializer
#     queryset = Blog.objects.all()

#     def perform_create(self, serializer):
#         author = Author.objects.get(user=self.request.user)
#         serializer.save(author=author)


class BlogUpdateDeleteRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        Get all articles or create one
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    model = Blog
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "author__user__username",
                     "category__category_name", "sub_category__sub_category_name"]
    filterset_fields = ["title", "author__user__username",
                        "category__category_name", "sub_category__sub_category_name"]

    def get_queryset(self):
        now = datetime.datetime.now()
        return Blog.objects.filter(Q(schedule_to__lte=now) | Q(schedule_to=None))


class MostRecentStories(generics.ListAPIView):
    serializer_class = BlogSerializer
    model = Blog

    def get_queryset(self):
        now = datetime.datetime.now()
        return Blog.objects.filter(Q(schedule_to__lte=now) | Q(schedule_to=None)).order_by('-posted_on')[:3]


@api_view(['POST'])
def Subscribe(request):
    if request.data["email"]:
        email = request.data["email"]
        try:
            check_1 = Subscribers.objects.get(email=email)
            check_1.delete()
            return JsonResponse({"message": "You have unsubscribed successfully"})
        except Subscribers.DoesNotExist:
            subscribe = Subscribers(
                email=email
            )
            subscribe.save()
            return Response({"message": "{} has been subscribed successfully".format(email)})
    else:
        return JsonResponse({"message": "Email is required to complete this action"})


class GetCategories(generics.ListAPIView):
    """Get all categories in the back"""
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


# done with fetching categories

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def VoteUp(request, slug):
    user = request.user

    try:
        message = ""
        blog = Blog.objects.get(slug=slug)
        if blog.upvotes.filter(id=user.id).exists():
            blog.upvotes.remove(user)
            message = "Your thumb-up has been removed from this post"
        else:
            blog.upvotes.add(user)
            message = "You have thumb-upped this article!"
        total_thumbs_up = blog.total_upvotes
        return JsonResponse({"success": message, "total_likes": total_thumbs_up})
    except Blog.DoesNotExist:
        return Response({"error": "Blog does not exist"}, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def VoteDown(request, slug):
    user = request.user
    try:
        message = ""
        blog = Blog.objects.get(slug=slug)
        if blog.downvotes.filter(id=user.id).exists():
            blog.downvotes.remove(user)
            message = "Your thumb-down has been removed from this post"
        else:
            blog.downvotes.add(user)
            message = "You have down-thumbed this article!"
        total_thumbs_down = blog.total_downvotes
        return JsonResponse({"success": message, "total_likes": total_thumbs_down})
    except Blog.DoesNotExist:
        return Response({"error": "Blog does not exist"}, status=401)


class TopSponsors(generics.ListAPIView):
    model = Sponsor
    serializer_class = SponsorSerializer
    queryset = Sponsor.objects.all().order_by('?')[:6]


class TopAuthors(generics.ListAPIView):
    model = Author
    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by('?')[:6]


class TopReaders(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('?')[:6]


@api_view(['POST'])
def ContactUs(request):
    name = request.data['first_name'] + " " + request.data['last_name']
    message = request.data['message']
    email = request.data['email']
    if request.data['first_name'] == "" and request.data['last_name']:
        return JsonResponse({"error": "Your name is not full!!"})
    elif message == "":
        return JsonResponse({"error": "Are you submitting an empty message"})
    elif email == "":
        return JsonResponse({"error": "Your email is required"})
    else:
        sender = send_mail("Tap from "+name, message, email,
                           [settings.EMAIL_HOST_USER], fail_silently=False,)
        if sender:
            return JsonResponse({"success": "Ok, we have received your message"})
        else:
            return JsonResponse({"error": "Sorry, we did not receive your message"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Bookmark(request, slug):
    """
        Bookmark a blog
    """
    user = request.user
    try:
        blog = Blog.objects.get(slug=slug)
        if blog.bookmarks.filter(id=user.id).exists():
            blog.bookmarks.remove(user)
            return JsonResponse({"success": "You have removed this post from your bookmarks", "bookmarked": False})
        else:
            blog.bookmarks.add(user)
            return JsonResponse({"success": "You have added this post to your bookmarks", "bookmarked": True})
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Blog does not exist"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def TopThreeSavedArticles(request):
    """
        Get the top three saved articles
        Requires authentication to access this endpoint
    """
    user = request.user
    try:
        blogs = Blog.objects.filter(
            bookmarks__id=user.id).order_by('-posted_on')[:3]
        serializer = BlogSerializer(blogs, many=True)
        return JsonResponse({"success": serializer.data})
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Blog does not exist"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SavedArticles(request):
    """
        Returns all articles saved by the user
        Requires authentication to access this endpoint 
    """
    user = request.user
    try:
        blogs = Blog.objects.filter(
            bookmarks__id=user.id).order_by('-posted_on')
        serializer = BlogSerializer(blogs, many=True)
        return JsonResponse({"success": serializer.data})
    except Blog.DoesNotExist:
        return JsonResponse({"error": "Blog does not exist"})
