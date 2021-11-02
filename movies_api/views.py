from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movies, Genre
import json
from .omdb_api import get_movie
from .serializers import MovieSerializer

# Create your views here.
@api_view(['GET'])
def search_title(request):  #api view to search movie by title
    title = request.query_params['title']
    movies_object = Movies.objects.filter(title__icontains=title) #search local database for the exact title string
    if movies_object.exists():
        movies_object = MovieSerializer(movies_object[0])
        return Response({'msg':'success', 'movie': movies_object.data}, status=status.HTTP_200_OK)
    else:
        data = get_movie(title)
        if not Movies.objects.filter(movie_id=data['imdbID']):
            genre_list = []
            for genre in data['Genre'].split(","):
                genre_obj, created = Genre.objects.get_or_create(name=genre.strip())
                genre_list.append(genre_obj)

            movie_obj = Movies.objects.create(
                title=data['Title'],
                released_year=data['Year'],
                rating=float(data['imdbRating']),
                movie_id=data['imdbID'],
            )
            movie_obj.genres.add(*genre_list)
            movie_obj.save()
            movies_object = MovieSerializer(movie_obj)
        else:
            movie_obj = Movies.objects.get(movie_id=data['imdbID'])
            movies_object = MovieSerializer(movie_obj)
        return Response({'msg':'success', 'movie': movies_object.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def search(request):  #api view to search movie by id, year, imdb rating, genre
    if len(list(request.query_params)) == 0:
        return Response({'msg':'Please provide query params'}, status=status.HTTP_400_BAD_REQUEST)
    for query in list(request.query_params):
        if query not in ["id", "year", "rating", "genre", "movie_id"]:
            return Response({'msg':'Invalid query parameters'}, status=status.HTTP_400_BAD_REQUEST)

        if query == "id":
            try:
                id = int(request.query_params[query])
            except:
                return Response({'msg':'id can only be integer'}, status=status.HTTP_400_BAD_REQUEST)
            movie_obj = Movies.objects.filter(id=int(request.query_params[query]))
            movies_object = MovieSerializer(movie_obj, many=True)
            return Response({'msg':'success', 'movies': movies_object.data}, status=status.HTTP_200_OK)
        
        if query == "movie_id":
            movie_obj = Movies.objects.filter(movie_id=request.query_params[query])
            movies_object = MovieSerializer(movie_obj, many=True)
            return Response({'msg':'success', 'movies': movies_object.data}, status=status.HTTP_200_OK)

        if query == "year":
            movie_obj = Movies.objects.filter(released_year=request.query_params[query])
            movies_object = MovieSerializer(movie_obj, many=True)
            return Response({'msg':'success', 'movies': movies_object.data}, status=status.HTTP_200_OK)

        if query == "genre":
            movie_obj = Movies.objects.filter(genres__name=request.query_params[query])
            movies_object = MovieSerializer(movie_obj, many=True)
            return Response({'msg':'success', 'movies': movies_object.data}, status=status.HTTP_200_OK)
        
        if query == "rating":
            movie_obj = Movies.objects.filter(rating__gt=request.query_params[query])
            movies_object = MovieSerializer(movie_obj, many=True)
            return Response({'msg':'success', 'movies': movies_object.data}, status=status.HTTP_200_OK)

        
    return Response({'msg':'success'}, status=status.HTTP_200_OK)