from django.shortcuts import render,HttpResponse,get_object_or_404
# from watchlist_app.models import Movie
from watchlist_app.models import WatchList,StreamPlatform,Review
from django.http import JsonResponse,response
# from watchlist_app.api.serializers import MovieSerializer
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
# from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        # username =  self.kwargs['username']
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username = username)


class ReviewCreate(generics.CreateAPIView):
    throttle_classes =[ReviewCreateThrottle]
    permission_classes = [IsAuthenticated]
    # for authenticattion
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        watchList = WatchList.objects.get(pk = pk)
        review_user = self.request.user
        review_queryset  = Review.objects.filter(watchList =watchList,review_user = review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reveiewed")
        if watchList.number_rating ==0:
            watchList.avg_rating=serializer.validated_data['rating']
        else:
            watchList.avg_rating =  (watchList.avg_rating +serializer.validated_data['rating'])/2
        number_rating  = watchList.number_rating +1
        watchList.save()
        serializer.save(watchList = watchList,review_user=review_user)
        
    
    
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']
    # permission_classes = [IsAuthenticated]
    # for authenticattion
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchList =pk)
    # watchlist is from models.py under review class
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    
    # for authenticattion
    
    

# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
    
# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg-rating'] required to remove those filters as by default cursor pagination is using created field filter, which will be contradictory
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination

class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]

    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,pk):
        
            try: 
                movie = WatchList.objects.get(pk =pk)
            except WatchList.DoesNotExist:
                return Response({'error':'Movie not found'},status = status.HTTP_404_NOT_FOUND)

            serializer = WatchListSerializer(movie)
            return Response(serializer.data)
    
    def put(self,request,pk):
        movie = WatchList.objects.get(pk =pk)
        serializer = WatchListSerializer(movie,data =  request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk =pk)
        movie.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
 
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class =  StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]
# it will give access to get and POST 
# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class =  StreamPlatformSerializer
# it will giveacces to get method only
 
 
 
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self,request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset,many = True)
#         return Response(serializer.data)
#     def retrieve(self,request,pk = None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset,pk = pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
#     def create(self,request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():  
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
    
 
 
    
    
class StreamPlatformAV(APIView):
    permission_classes = [AdminOrReadOnly]

    def get(self,request):
        platform  =  StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many =True,context = {'request':request})
        # context={'request':request}
        return Response(serializer.data)
    def post(self,request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():  
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlatformDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]

    def get(self,request,pk):
            try: 
                platform = StreamPlatform.objects.get(pk =pk)
            except StreamPlatform.DoesNotExist:
                return Response({'error':'Movie not found'},status = status.HTTP_404_NOT_FOUND)

            serializer = StreamPlatformSerializer(platform,context={'request':'request'})
            return Response(serializer.data)
    
    def put(self,request,pk):
        platform = StreamPlatform.objects.get(pk =pk)
        serializer = StreamPlatformSerializer(platform,data =  request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST) 
        
    def delete(self,request,pk):
        platform = StreamPlatform.objects.get(pk =pk)
        platform.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
        
        






# class MovieListAV(APIView):
#     def get(self,request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many = True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
# class MovieDetailAV(APIView):
#     def get(self,request,pk):
#         if request.method=='GET':
#             try: 
#                 movie = Movie.objects.get(pk =pk)
#             except Movie.DoesNotExist:
#                 return Response({'error':'Movie not found'},status = status.HTTP_404_NOT_FOUND)

#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     def put(self,request,pk):
#         movie = Movie.objects.get(pk =pk)
#         serializer = MovieSerializer(movie,data =  request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors) 
        
#     def delete(self,request,pk):
#         movie = Movie.objects.get(pk =pk)
#         movie.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)
       
        
        
        






# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many = True)
#         return Response(serializer.data)
#     if request.method == "POST":
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
        
        
# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method=='GET':
#         try: 
#             movie = Movie.objects.get(pk =pk)
#         except Movie.DoesNotExist:
#             return Response({'error':'Movie not found'},status = status.HTTP_404_NOT_FOUND)

#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':#rewrite everything
#         movie = Movie.objects.get(pk =pk)
#         serializer = MovieSerializer(movie,data =  request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors) 
        
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk =pk)
#         movie.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)


        
        
    
    