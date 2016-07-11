from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from serializers import UserSerializer, ReviewSerializer
from rest_framework.decorators import list_route
from models import Review

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions, viewsets
from rest_framework import generics

User = get_user_model()

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the core index.")

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        serializer.save()

class ReviewViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReviewSerializer

    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #
    #     if self.request.method == 'POST':
    #         return (permissions.AllowAny(),)
    #
    #     return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def list(self, request):
        if request.user.is_authenticated():
            queryset = Review.objects.filter(created_by = request.user)
        else:
            queryset = []
        # print queryset.keys
        # queryset = Review.objects.filter(created_by = request.user)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    # @list_route(
    #     methods=['post'],
    #     permission_classes=(IsAuthenticated,),
    #     # serializer_class=CustomPostSerializer,
    #     # pagination_class=LimitOffsetPagination,
    #     url_path='create',
    # )
    def create(self, request):

        serializer = self.serializer_class(data = request.data, context={'request':request})
        print 'what'
        if serializer.is_valid():
            print 'before'
            serializer.save()
            print 'why'
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
        #
        # print request.body
        # serializer = ReviewSerializer(data = request.body)
        # if serializer.is_valid():
        #     print 'valid'
        #     serializer.save()
        # return Response(serializer.data)

    # def perform_create(self, serializer):
    #     print 'blabla'
    #     print self.request.user.get_full_name()
    #     serializer.save()


    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        myreview = get_object_or_404(queryset, pk = pk)

        serializer = ReviewSerializer(myreview)
        return Response(serializer.data)


    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
#
# class LoginView(views.APIView):
#     def post(self, request, format=None):
#         data = json.loads(request.body)
#
#         email = data.get('email', None)
#         password = data.get('password')
#
#         account = authenticate(email=email, password=password)
#
#         if account is not None:
#             if account.is_active:
#                 login(request, account)
#
#                 serialized = AccountSerializer(account)
#
#                 return Response(serialized.data)
#             else:
#                 return Response({
#                     'status': 'Unauthorized',
#                     'message': 'This account has been disabled.'
#             }, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({
#                'status': 'Unauthorized',
#                'message': 'Username/password combination invalid.'
#         }, status=status.HTTP_401_UNAUTHORIZED)
#
#
# class LogoutView(views.APIView):
#     permissions = (permissions.IsAuthenticated,)
#
#     def post(self, request, format=None):
#         logout(request)
#
#         return Response({}, status=status.HTTP_204_NO_CONTENT)

# class ReviewViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.AllowAny,)
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def perform_create(self, serializer):
#         print 'blabla'
#         print self.request.user.get_full_name()
#         serializer.save()
