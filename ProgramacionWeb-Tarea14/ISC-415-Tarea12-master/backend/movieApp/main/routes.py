from flask import request, Blueprint
from flask import jsonify
from flask import make_response
from movier.data.models import db, Movie, Review
import urllib.request
import os

main = Blueprint('main', __name__, template_folder='templates')

@main.route('movies', methods=["POST"])
def movie_handler():
  if request.method == 'POST':
    data = request.get_json()
    movies = data["movies"]
    for i in range(len(movies)):
        if 'poster_path' in movies[i]:
          posterUrl = "http://image.tmdb.org/t/p/w150" + movies[i]["poster_path"]
          localUrl = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\client\static\images\posters" + str(movies[i]["id"]) + ".jpg"
          urllib.request.urlretrieve(posterUrl, localUrl)
          movie = Movie(movies[i]["id"], movies[i]["title"], movies[i]["overview"], movies[i]["poster_path"])
        else:
          movie = Movie(movies[i]["id"], movies[i]["title"], movies[i]["overview"], None)
        db.session.add(movie)
        db.session.commit()
  return "SAVED!"

@main.route('movies/search/', methods=["GET"])
def movies_search_handler():
  if request.method == 'GET':
    query = request.args.get('query')
    movies = Movie.query.filter(Movie.name.like(query+"%")).all()
    movies = [movie.serialize() for movie in movies]
    print(movies)
    return jsonify(movies)

@main.route('movies/all/', methods=["GET"])
def movies_all_handler():
  if request.method == 'GET':
    movies = Movie.query.all()
    movies = [movie.__dict__ for movie in movies]
    return jsonify(movies)

@main.route('reviews', methods=["POST"])
def review_handler():
  if request.method == 'POST':
    data = request.form.to_dict()
    if "movie_name" and "description" and "poster" and "score" and "review" and "user" and "device_id" not in data:
      resp = make_response("", 404)
      return resp

@main.route('reviews/<movie>' methods = ["GET"])
def reviews_by_movies_handler(movie):
  if request.method == 'GET':
    movie = Movie.query.filter_by(tittle=movie).first()
    movie = movie.serialize()
    reviews = Review.query.filter_by(movie_id=movie["id"]).all()
    reviews = [review.serialize() for review in reviews]
    return jsonify(reviews);

@main.route('movies/reviewed' methods = ["GET"])
def reviews_by_movies_handler(movie):
  if request.method == 'GET':
    movies = Movie.query.all(;
      movies = [movie.serialize() for movie in movies]
      movies_reviewed = [movie for movie in movies if len(movie.reviews) > 0]
      return jsonify(movies_reviewed)