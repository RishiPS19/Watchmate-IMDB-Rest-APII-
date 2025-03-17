from rest_framework import serializers
# from .views import WatchList
# from watchlist_app.models import Movie
from watchlist_app.models import WatchList,StreamPlatform,Review

# model = serializers.ModelSerializer
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only =True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('watchList',)
        # for create of review excluded watchlist, ReviewCreateMethod under views.py
class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many = True,read_only = True)
    # len_name = serializers.SerializerMethodField()
    platform  = serializers.CharField(source ='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"
        #or ['id','name','description'] 
        # exclude = ['id']
        
#     def get_len_name(self,object):
# # get len_name 
#         length = len(object.name)
#         return length
#     def validate(self,data):
#         if data['name'] ==  data['description']:
#             raise serializers.ValidationError("Title and description should no tbe same")
#         return data
    
#     def validate_name(self,value):
# # validating the name
#         if len(value)<2:
#             raise serializers.ValidationError("Name is too short")
#         else:
#             return value
class StreamPlatformSerializer(serializers.ModelSerializer):

# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    # it will give access to the URl instead of ID
    # watchlist = serializers.StringRelatedField(many = True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many =True,
    #     read_only =True,
    #     view_name ='movie-deatils'
    #     # movie-details definded under URLand add context under get method
    # )
    watchlist = WatchListSerializer(many = True,read_only = True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"
       
        
        
















# model = serializers.Serializer

# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is too short") 
    
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     name=serializers.CharField(validators  = [name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
#     def update(self,instance, validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
#         return instance
#     # object validation
#     def validate(self,data):
#         if data['name'] ==  data['description']:
#             raise serializers.ValidationError("Title and description should no tbe same")
#         return data
    
#     def validate_name(self,value):
# # validating the name
#         if len(value)<2:
#             raise serializers.ValidationError("Name is too short")
#         else:
#             return value

# field level, object level , class level

# serializers fileds and core arguements:
# e.g: read_only = True, no access for client to read, validators
# 
        
    


