from rest_framework import serializers
import json

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    released_year = serializers.CharField(max_length=100)
    rating = serializers.CharField(max_length=100)
    movie_id = serializers.CharField(max_length=100)
    genres = serializers.SerializerMethodField('get_genres')

    def get_genres(self, data):
        return [genre.name for genre in data.genres.all()]
