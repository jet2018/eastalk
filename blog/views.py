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

from blog.models import Blog, Subscribers, Category
from blog.serializers import BlogSerializer, CategorySerializer


# Create your views here.
class IndexView(TemplateView):
    template_name = "splash.html"


class BlogListCreateView(generics.ListCreateAPIView):
    """
        Get all articles or create one
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    """
        Subscribe to a category, for a while or everything
    """
    # TODO Subscribe on a specific category

    if request.POST.get('email'):
        email = request.POST.get('email')
        try:
            Subscribers.objects.get(email=email)
            return JsonResponse({"error": "Email already subscribed"}, status=403)
        except Subscribers.DoesNotExist:
            pass
    else:
        return JsonResponse({"error": "Email is required to subscribe"}, status=401)

    subscribe = Subscribers(
        email=email)
    subscribe.save()
    return Response({"success": "{} subscribed successfully".format(email)})


@api_view(['POST'])
def Unsubscribe(request):
    email = request.POST.get("email")
    try:
        check_1 = Subscribers.objects.get(email=email)
        check_1.delete()
        return JsonResponse({"success": email + " unsubscribed successfully"})
    except Subscribers.DoesNotExist:
        return JsonResponse({"error": email + " is not among subscribed emails"})


# done with subscription!

class GetCategories(generics.ListAPIView):
    """Get all categories in the back"""
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
