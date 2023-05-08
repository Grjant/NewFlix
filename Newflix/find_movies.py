from models import app, db, Theater, Movie, StreamingService, Showings, Time
import requests

STREAMING_API_KEY = 'a61c974b28405c28cbc8e508d4854414'

STREAMING_API = "https://streaming-availability.p.rapidapi.com/v2/search/basic"

headers = {
    "X-RapidAPI-Key": "a54ebe8c18msh53adf323aaf817dp18f933jsnafd27041c503",
    "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}


def find_movies_in_services():  # parse through all movies in the database and add the link to streaming service
    with app.app_context():
        services = db.session.query(StreamingService).all()
        movies = db.session.query(Movie).all()
        for movie in movies:
            services_available = []
            for service in services:
                querystring = {"country": "us", "services": service.name,
                               "show_type": "movie", "keyword": movie.title}
                response = requests.request(
                    "GET", STREAMING_API, headers=headers, params=querystring)
                response_data = response.json()
                print(response_data)
                if not response_data["result"]:
                    continue
                else:
                    movie.streams.append(service)
                    db.session.commit()


# find_movies_in_services()
