from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from authors.models import Author, Sponsor
from authors.serializers import AuthorSerializer, MyTokenObtainPairSerializer, UserSerializer, SponsorSerializer

class SponsorListOrCreate(generics.ListCreateAPIView):
    serializer_class = SponsorSerializer
    model=Sponsor
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Sponsor.objects.all()


class BriefSponsors(generics.ListAPIView):
    serializer_class = SponsorSerializer
    model=Sponsor
    queryset = Sponsor.objects.all()[:3]


class AuthorCreateView(generics.ListCreateAPIView):
    model = Author
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def perform_create(self, serializer):
        try:
            Author.objects.get(user=self.request.user)
            return Response({"error": "You are already a user"}, status=403)
        except Author.DoesNotExist:
            serializer.save(user=self.request.user)

class BriefAuthors(generics.ListAPIView):
    serializer_class = AuthorSerializer
    model=Author
    queryset = Author.objects.all()[:3]



class MyTokenObtainPairView(TokenObtainPairView):
    """
        Override the default behaviour of jwt. Returns username, email, is_author, token_type, exp, jti, user_id
        Takes up, username and password
        Request method allowed is post only
    """
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST', ])
def create_account(request):
    """
        Create a new user, requires username, email, password, password2, first_name, last_name, role
    """
    if request.method == 'POST':

        if request.POST.get('username') != "" and request.POST.get('email') != "" and request.POST.get(
                'password') != "" and request.POST.get('password2') != "" and request.POST.get(
            'first_name') != "" and request.POST.get('last_name') != "":

            serializer = UserSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                user = serializer.save()
                # if the user is created, update their role, set it to the sent role
                if user:
                    data['success'] = "Account created successfully"
                    data['email'] = user.email
                    data['username'] = user.username
                    data['first_name'] = user.first_name
                    data['last_name'] = user.last_name
                else:
                    data['success'] = "An error occured while creating the user"
            else:
                data = serializer.errors
            return Response(data)
        else:
            return Response({"error": "Some fields are missing"})
