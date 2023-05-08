from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys
from models import app, db, Theater, Movie, Showings, Time, StreamingService
from flask_sqlalchemy import SQLAlchemy, pagination
import io
import sys
import unittest
import requests


@app.route('/')  # home page route
def index():
    return render_template("index.html")


@app.route('/movies/')  # route for the movies page with 5 movies per page
def movies():
    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', type=str)
    sortorder = request.args.get('sortorder', type=str)
    search = request.args.get('search', type=str)
    if search == None:
        search = ''
    search = search.title()
    if sortorder == 'descending':
        if sort == 'title':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.title.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'duration':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.duration.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'genre':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.genre.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'rottentomatoes':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.rotten_tomatoes_rating.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'imdb':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.imdb_rating.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'director':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.director.desc()), page=page, per_page=ROWS_PER_PAGE)
        else:
            movies = db.paginate(db.session.query(Movie).filter(
                Movie.title.like('%' + search + '%')), page=page, per_page=ROWS_PER_PAGE)
    else:
        if sort == 'title':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.title.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'duration':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.duration.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'genre':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.genre.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'rottentomatoes':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.rotten_tomatoes_rating.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'imdb':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.imdb_rating.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'director':
            movies = db.paginate(db.session.query(Movie).filter(Movie.title.like('%' + search + '%')).order_by(
                Movie.director.asc()), page=page, per_page=ROWS_PER_PAGE)
        else:
            movies = db.paginate(db.session.query(Movie).filter(
                Movie.title.like('%' + search + '%')), page=page, per_page=ROWS_PER_PAGE)
    paginated_movies = (movies.items)
    return render_template("movies.html", movies=paginated_movies, pagination=movies, endpoint='movies', sort=sort, sortorder=sortorder, search=search)


@app.route('/theaters')  # route for theaters with 4 theaters per page
def theaters():
    ROWS_PER_PAGE = 4
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', type=str)
    sortorder = request.args.get('sortorder', type=str)
    search = request.args.get('search', type=str)
    if search == None:
        search = ''
    search = search.title()
    if sortorder == 'descending':
        if sort == 'name':
            theaters = db.paginate(db.session.query(Theater).filter(Theater.name.like('%' + search + '%')).order_by(
                Theater.name.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'google':
            theaters = db.paginate(db.session.query(Theater).filter(Theater.name.like('%' + search + '%')).order_by(
                Theater.google_maps.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'location':
            theaters = db.paginate(db.session.query(Theater).filter(Theater.name.like('%' + search + '%')).order_by(
                Theater.location.desc()), page=page, per_page=ROWS_PER_PAGE)
        else:
            theaters = db.paginate(db.session.query(Theater).filter(
                Theater.name.like('%' + search + '%')), page=page, per_page=ROWS_PER_PAGE)
    else:
        if sort == 'name':
            theaters = db.paginate(db.session.query(Theater).filter(Theater.name.like('%' + search + '%')).order_by(
                Theater.name.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'google':
            theaters = db.paginate(db.session.query(Theater).filter(Theater.name.like('%' + search + '%')).order_by(
                Theater.google_maps.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'location':
            theaters = db.paginate(db.session.query(Theater).filter(Theater.name.like('%' + search + '%')).order_by(
                Theater.location.asc()), page=page, per_page=ROWS_PER_PAGE)
        else:
            theaters = db.paginate(db.session.query(Theater).filter(
                Theater.name.like('%' + search + '%')), page=page, per_page=ROWS_PER_PAGE)
    paginated_theaters = (theaters.items)
    return render_template("theaters.html", theaters=paginated_theaters, pagination=theaters, endpoint='theaters', sort=sort, sortorder=sortorder, search=search)


@app.route('/movies/@movieid')  # route for specific movie
def individual_movie(movieid):
    movie = db.session.filter_by(id=movieid)
    return render_template("individualmovie.html", movie=movie)


@app.route('/theater/<int:theater_id>')  # route for specific theater
def theater_detail(theater_id):
    theater = []
    theater.append(db.session.query(Theater).filter_by(id=theater_id).one())
    return render_template("individualtheater.html", theaters=theater)


@app.route('/movie/<movie_id>')  # route for specific movie
def movie_detail(movie_id):
    movie = []
    movie.append(db.session.query(Movie).filter_by(id=movie_id).one())
    return render_template("individualmovie.html", movies=movie)


@app.route('/services/<service_id>')  # route for specific service
def service_detail(service_id):
    service = []
    service.append(db.session.query(
        StreamingService).filter_by(id=service_id).one())
    return render_template("individualservice.html", services=service)


# route for streaming services page with 3 services per page
@app.route('/services/')
def services():
    ROWS_PER_PAGE = 3
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', type=str)
    sortorder = request.args.get('sortorder', type=str)
    search = request.args.get('search', type=str)
    if search == None:
        search = ''
    search = search.title()
    if sortorder == 'descending':
        if sort == 'name':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.name.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'price':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.base_price.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'country':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.country_origin.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'users':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.user_base.desc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'revenue':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.revenue2022.desc()), page=page, per_page=ROWS_PER_PAGE)
        else:
            services = db.paginate(db.session.query(StreamingService).filter(
                StreamingService.name.like('%' + search + '%')), page=page, per_page=ROWS_PER_PAGE)
    else:
        if sort == 'name':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.name.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'price':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.base_price.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'country':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.country_origin.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'users':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.user_base.asc()), page=page, per_page=ROWS_PER_PAGE)
        elif sort == 'revenue':
            services = db.paginate(db.session.query(StreamingService).filter(StreamingService.name.like('%' + search + '%')).order_by(
                StreamingService.revenue2022.asc()), page=page, per_page=ROWS_PER_PAGE)
        else:
            services = db.paginate(db.session.query(StreamingService).filter(
                StreamingService.name.like('%' + search + '%')), page=page, per_page=ROWS_PER_PAGE)
    paginated_services = (services.items)
    return render_template("services.html", services=paginated_services, pagination=services, endpoint='services', sort=sort, sortorder=sortorder, search=search)


@app.route('/about/')  # route for about page
def about():
    # c1 = len(requests.get("https://gitlab.com/api/v4/projects/42858665/repository/commits?author=Gordon Liu&per_page=300",
    #                       headers={"PRIVATE-TOKEN": "glpat-jS7VsXn3cQY3iy5wxa6t"}).json())
    # c2 = len(requests.get("https://gitlab.com/api/v4/projects/42858665/repository/commits?author=ryanvanillabrownie&per_page=300",
    #                       headers={"PRIVATE-TOKEN": "glpat-jS7VsXn3cQY3iy5wxa6t"}).json())
    # c3 = len(requests.get("https://gitlab.com/api/v4/projects/42858665/repository/commits?author=Evan&per_page=300",
    #                       headers={"PRIVATE-TOKEN": "glpat-jS7VsXn3cQY3iy5wxa6t"}).json())
    # c4 = len(requests.get("https://gitlab.com/api/v4/projects/42858665/repository/commits?author=Grant Jacobs&per_page=300",
    #                       headers={"PRIVATE-TOKEN": "glpat-jS7VsXn3cQY3iy5wxa6t"}).json())
    # c5 = len(requests.get("https://gitlab.com/api/v4/projects/42858665/repository/commits?author=Sharan Liu&per_page=300",
    #                       headers={"PRIVATE-TOKEN": "glpat-jS7VsXn3cQY3iy5wxa6t"}).json())
    c1 = 63
    c2 = 55
    c3 = 75
    c4 = 51
    c5 = 46
    # i1 = len(requests.get("https://gitlab.com/api/v4/projects/42858665/issues?author_id=12354598&scope=all&per_page=300",
    #                       headers={"PRIVATE-TOKEN": "glpat-jS7VsXn3cQY3iy5wxa6t"}).json())
    i1 = 10
    i2 = 10
    # i3 = len(requests.get("https://gitlab.com/api/v4/projects/42858665/issues?author_id=12354538&scope=all&per_page=300",
    #                       headers={"PRIVATE-TOKEN": "glpat-jS7VsXn3cQY3iy5wxa6t"}).json())
    i3 = 14
    i4 = 11
    i5 = 10

    issues = [i1, i2, i3, i4, i5, i1 + i2 + i3 + i4 + i5]
    commits = [c1, c2, c3, c4, c5, c1 + c2 + c3 + c4 + c5]

    return render_template("about.html", issues=issues, commits=commits)


@app.route('/run-tests', methods=['POST'])  # route to run unit tests
def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = unittest.TextTestRunner()
    results = runner.run(suite)
    print(str(results))
    return render_template("tests.html", results=str(results))


# api endpoint to get all theaters
@app.route('/api/theaters', methods=['GET'])
def get_theaters():
    try:
        theaters = Theater.query.all()
        response = []
        for theater in theaters:
            theater_data = {
                'id': theater.id,
                'name': theater.name,
                'location': theater.location,
                'google_maps': theater.google_maps,
                'img': theater.img
            }
            response.append(theater_data)
        return jsonify(response), 200
    except:
        error_message = "An error occurred"
        response = jsonify({'error': error_message})
        response.status_code = 500
        return response


@app.route('/api/movies', methods=['GET'])  # api endpoint to get all movies
def get_movies():
    try:
        movies = Movie.query.all()
        response = {'movies': []}
        for movie in movies:
            movie_data = {}
            movie_data['title'] = movie.title
            movie_data['id'] = movie.id
            movie_data['poster'] = movie.poster
            movie_data['duration'] = movie.duration
            movie_data['genre'] = movie.genre
            movie_data['rotten_tomatoes_rating'] = movie.rotten_tomatoes_rating
            movie_data['imdb_rating'] = movie.imdb_rating
            movie_data['director'] = movie.director
            movie_data['plot'] = movie.plot
            response['movies'].append(movie_data)
        return jsonify(response), 200
    except:
        error_message = "An error occurred"
        response = jsonify({'error': error_message})
        response.status_code = 500
        return response


# api endpoints to get all streaming services
@app.route('/api/services', methods=['GET'])
def get_streaming_services():
    try:
        streaming_services = StreamingService.query.all()
        response = {'streaming_services': []}
        for service in streaming_services:
            service_data = {}
            service_data['name'] = service.name
            service_data['id'] = service.id
            service_data['logo'] = service.logo
            service_data['website'] = service.website
            service_data['country_origin'] = service.country_origin
            service_data['base_price'] = service.base_price
            service_data['ad_free_available'] = service.ad_free_available
            service_data['revenue2022'] = service.revenue2022
            service_data['user_base'] = service.user_base
            response['streaming_services'].append(service_data)
        return jsonify(response), 200
    except:
        error_message = "An error occurred"
        response = jsonify({'error': error_message})
        response.status_code = 500
        return response


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5003)
