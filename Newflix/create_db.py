from models import app, db, Theater, Movie, StreamingService, Showings, Time
from create_theaters import get_showings
from find_movies import find_movies_in_services
import requests

MOVIES_API_KEY = 'f37abaab'
MOVIES_API = f'https://www.omdbapi.com/?apikey={MOVIES_API_KEY}'
STREAMING_API_KEY = 'a61c974b28405c28cbc8e508d4854414'

STREAMING_API_KEY = 'a61c974b28405c28cbc8e508d4854414'

STREAMING_API = "https://streaming-availability.p.rapidapi.com/v2/search/basic"

headers = {
    "X-RapidAPI-Key": "a54ebe8c18msh53adf323aaf817dp18f933jsnafd27041c503",
    "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}

with app.app_context():
    def create_theaters():  # add the theaters to the database and establishing a link to showings and times
        theaters_list = get_showings()
        theater_id = 1
        showings_id = 1
        time_id = 1
        for theater in theaters_list:
            t = Theater(name=theater["name"], id=theater_id,
                        location=theater["location"], google_maps=theater["map"], img=theater["img"])
            db.session.add(t)
            db.session.commit()
            for i in range(0, 2):
                for movie in theater["showtimes"][i]["movies"]:
                    for showing in movie["showing"]:
                        if "type" not in showing:
                            showing["type"] = "Standard"
                        movie_id = Movie.query.filter_by(
                            title=movie["name"]).first()
                        if movie_id == None:
                            movie_id = add_movie(movie["name"])
                            if movie_id == "Movie not available":
                                # think of what to do here later
                                continue
                        movie_id = Movie.query.filter_by(
                            title=movie["name"]).first()
                        s = Showings(id=showings_id, day=theater["showtimes"][i]["day"],
                                     type=showing["type"], theater_id=theater_id, movie_id=movie_id.id)
                        # add movie_id = Movie.query.filter_by(name=movie.name).first()
                        db.session.add(s)
                        db.session.commit()

                        for time in showing["time"]:
                            ti = Time(
                                id=time_id, time=time, showings_id=showings_id)
                            db.session.add(ti)
                            db.session.commit()
                            time_id += 1
                        showings_id += 1
            theater_id += 1

    # function for getting the rotten tomatoes and returing N/A if there is not one given
    def get_rotten_tomatoes(movie_data):
        ratings = movie_data['Ratings']
        for rating in ratings:
            if rating["Source"] == 'Rotten Tomatoes':
                return rating['Value']
        return 'N/A'

    def add_movie(name):  # function to add a specific movie to the database; some hard-coded cases since the theater and movie api had different capitalization/grammar
        response = requests.get(f'{MOVIES_API}&t={name}')
        if response.status_code == 200:
            movie_data = response.json()
            if movie_data['Response'] == 'False':
                return 'Movie not available'
            title = movie_data['Title']
            if title == 'Yes, Madam!':
                title = 'Yes, Madam'
            if title == 'Operation Fortune: Ruse de guerre':
                title = 'Operation Fortune: Ruse de Guerre'
            if movie_data['Poster'] == 'N/A':
                poster = "../static/imgs/movie.jpg"
            else:
                poster = movie_data['Poster']
            movie = Movie(
                title=title,
                id=movie_data['imdbID'],
                poster=poster,
                duration=movie_data['Runtime'],
                genre=movie_data['Genre'],
                rotten_tomatoes_rating=get_rotten_tomatoes(movie_data),
                imdb_rating=movie_data['imdbRating'],
                director=movie_data['Director'],
                plot=movie_data['Plot']
            )
        db.session.add(movie)
        db.session.commit()
        return movie.id

    def create_movies():  # create a base list of movies
        movie_titles = ['The Matrix', 'The Godfather', 'The Dark Knight',
                        'Inception', '12 Angry Men', 'Avatar: The Way of Water',
                        'Titanic', 'Pulp Fiction', 'Puss in Boots: The Last Wish', 'Forrest Gump']
        movies = []
        for title in movie_titles:
            response = requests.get(f'{MOVIES_API}&t={title}')
            if response.status_code == 200:
                movie_data = response.json()
                movie = Movie(
                    title=movie_data['Title'],
                    poster=movie_data['Poster'],
                    id=movie_data['imdbID'],
                    duration=movie_data['Runtime'],
                    genre=movie_data['Genre'],
                    rotten_tomatoes_rating=movie_data['Ratings'][1]['Value'],
                    imdb_rating=movie_data['imdbRating'],
                    director=movie_data['Director'],
                    plot=movie_data['Plot']
                )
                movies.append(movie)

        # add movies to the database
        for movie in movies:
            db.session.add(movie)
        db.session.commit()

    def create_services():  # add the list of streaming services to the database
        Netflix = StreamingService(name='netflix', id='1', website='http://netflix.com', logo="../static/imgs/netflix.png",
                                   country_origin='United States', base_price=6.99,
                                   ad_free_available='Yes', revenue2022=31.6,
                                   user_base=230.7)
        db.session.add(Netflix)
        db.session.commit()
        Hulu = StreamingService(name='hulu', id='2', website='https://www.hulu.com/welcome', logo="../static/imgs/hulu.png",
                                country_origin='United States', base_price=6.99,
                                ad_free_available='Yes', revenue2022=10.7,
                                user_base=48)
        db.session.add(Hulu)
        db.session.commit()
        DisneyPlus = StreamingService(name='disney', id='3', website='https://www.disneyplus.com', logo="../static/imgs/disney.png",
                                      country_origin='United States', base_price=8.00,
                                      ad_free_available='Yes', revenue2022=7.4,
                                      user_base=161.8)
        db.session.add(DisneyPlus)
        db.session.commit()
        HBOMax = StreamingService(name='hbo', id='4', website='https://www.hbomax.com', logo="../static/imgs/hbomax.png",
                                  country_origin='United States', base_price=9.99,
                                  ad_free_available='Yes', revenue2022=7.7,
                                  user_base=96.1)
        db.session.add(HBOMax)
        db.session.commit()
        AmazonPrime = StreamingService(name='prime', id='5', website='https://www.amazon.com/Prime-Video/b?node=2676882011',
                                       logo="../static/imgs/prime.png",
                                       country_origin='United States', base_price=8.99,
                                       ad_free_available='Yes', revenue2022=5.16,
                                       user_base=200)
        db.session.add(AmazonPrime)
        db.session.commit()
        AppleTV = StreamingService(name='apple', id='6', website='https://tv.apple.com', logo="../static/imgs/apple.png",
                                   country_origin='United States', base_price=6.99,
                                   ad_free_available='No', revenue2022=9.4,
                                   user_base=25)
        db.session.add(AppleTV)
        db.session.commit()
        ParamountPlus = StreamingService(name='paramount', id='7', website='https://www.paramountplus.com',
                                         logo="../static/imgs/paramount.png",
                                         country_origin='United States', base_price=4.99,
                                         ad_free_available='Yes', revenue2022=5.6,
                                         user_base=56)
        db.session.add(ParamountPlus)
        db.session.commit()
        Peacock = StreamingService(name='peacock', id='8', website='https://www.peacocktv.com',
                                   logo="../static/imgs/peacock.png",
                                   country_origin='United States', base_price=0.00,
                                   ad_free_available='Yes', revenue2022=0.6,
                                   user_base=20)
        db.session.add(Peacock)
        db.session.commit()
        Showtime = StreamingService(name='showtime', id='9', website='https://www.showtime.com',
                                    logo="../static/imgs/showtime.png",
                                    country_origin='United States', base_price=6.99,
                                    ad_free_available='Yes', revenue2022=0.95,
                                    user_base=27)
        db.session.add(Showtime)
        db.session.commit()

    db.drop_all()  # drop all the tables
    db.create_all()  # create all the tables
    create_services()  # add streaming services to database
    create_movies()  # add movies to database
    create_theaters()  # add theaters to database
    find_movies_in_services()  # establish link between movies and streaming services
    # these lines of code just check that the data was added properly
    all_movies = db.session.query(Movie).all()
    for movie in all_movies:
        print(movie.title)
    all_theaters = db.session.query(Theater).all()
    for theater in all_theaters:
        print(theater.name)
