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


from blog.models import Blog, Subscribers, Category
from blog.serializers import BlogSerializer, CategoriesSerializer, CategorySerializer, SponsorSerializer


# Create your views here.
class IndexView(TemplateView):
    template_name = "splash.html"


class BlogListCreateView(generics.ListCreateAPIView):
    """
        Get all articles or create one
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]
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

    def perform_create(self, serializer):
        try:
            author = Author.objects.get(user=self.request.user)
            print(author)
            return serializer.save(author=author)
        except Author.DoesNotExist:
            return JsonResponse({"error": "You need to be an author to create an article"})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAuthor])
def Create_Article(request):
    """
        Create a brand new article.

        Must be authenticated and an author.
    """
    colors = request.data['colors'] if request.data['colors'] else "i"
    try:
        author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        return JsonResponse({"error": "You have to be an author to proceed."})
    title = request.data['title']
    if title == "":
        return JsonResponse({"error": "A unique title is to your article is required."})

    check_title = Blog.objects.filter(title__iexact=title)
    if check_title.count() > 3:
        return JsonResponse({"error": "Only three articles maximumly can have related titles, otherwise, titles are unique"})

    seriliser = BlogSerializer()


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


# @api_view(['POST'])
# def Unsubscribe(request):
#     email = request.POST.get("email")
#     try:
#         check_1 = Subscribers.objects.get(email=email)
#         check_1.delete()
#         return JsonResponse({"success": email + " unsubscribed successfully"})
#     except Subscribers.DoesNotExist:
#         return JsonResponse({"error": email + " is not among subscribed emails"})


# done with subscription!

class GetCategories(generics.ListAPIView):
    """Get all categories in the back"""
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


# done with fetching categories

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def VoteUp(request, slug):
    user = request.user
    try:
        blog = Blog.objects.get(slug=slug)
        if blog.upvotes.filter(id=user.id).exists():
            blog.upvotes.remove(user)
        else:
            blog.upvotes.add(user)

    except Blog.DoesNotExist:
        return Response({"error": "Blog does not exist"}, status=401)
    serialiser = BlogSerializer(blog)
    return Response(serialiser.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def VoteDown(request, slug):
    user = request.user
    try:
        blog = Blog.objects.get(slug=slug)
        if blog.downvotes.filter(id=user.id).exists():
            blog.downvotes.remove(user)
        else:
            blog.downvotes.add(user)

    except Blog.DoesNotExist:
        return Response({"error": "Blog does not exist"}, status=401)
    serialiser = BlogSerializer(blog)
    return Response(serialiser.data, status=200)


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
    print(name)
    print(message)
    print(email)
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
