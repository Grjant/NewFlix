from serpapi import GoogleSearch

theaters_api = 'https://serpapi.com/search.json?q={theater}&location=Austin,+Texas,+United+States&hl=en&gl=us'


def get_showings():  # manually add theaters in Austin; TODO: expand using MovieGlu api to pull nearby theaters and automate theater database population
    params1 = {
        "q": "AMC Barton Creek Square 14",
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params2 = {
        "q": "Alamo Drafthouse Cinema South Lamar",
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params3 = {
        "q": "Cinemark Southpark Meadows",
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params4 = {
        "q": "Alamo Drafthouse Cinema Mueller",
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params5 = {
        "q": "Galaxy Theatres",
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params6 = {
        "q": "Regal Westgate",
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params7 = {
        "q": "Alamo Drafthouse Cinema Village",
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params8 = {
        "q": "Santikos Entertainment Palladium",
        "location": "San Antonio, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params9 = {
        "q": "Alamo Drafthouse Cinema Park North",
        "location": "San Antonio, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params10 = {
        "q": "Cinemark San Antonio 16",
        "location": "San Antonio, Texas, United States",
        "hl": "en",
        "gl": "us",
        "api_key": "506ef892bcfe29f1e395784f0aa4733a28b25897d6cf3099817754dd3f1b3d9b"
    }
    params = [params1, params2, params3, params4, params5,
              params6, params7, params8, params9, params10]
    #params = [params1, params2]
    theaters_list = []
    for param in params:

        search = GoogleSearch(param)
        results = search.get_dict()
        if "showtimes" not in results:
            continue
        r = {
            "name": param["q"],
            "location": param["location"],
            "showtimes": results["showtimes"],
            "map": results["search_information"]["menu_items"][1]["link"]
        }
        theaters_list.append(r)

    theaters_list[0]["img"] = "../static/imgs/amcbarton.jpg"
    theaters_list[1]["img"] = "../static/imgs/alamolamar.jpg"
    theaters_list[2]["img"] = "../static/imgs/cinemarksouthpark.jpg"
    theaters_list[3]["img"] = "../static/imgs/alamomueller.jpg"
    theaters_list[4]["img"] = "../static/imgs/galaxy.jpg"
    theaters_list[5]["img"] = "../static/imgs/regalwestgate.jpg"
    theaters_list[6]["img"] = "../static/imgs/alamovillage.jpg"
    theaters_list[7]["img"] = "../static/imgs/santikos.jpg"
    theaters_list[8]["img"] = "../static/imgs/alamoparknorth.jpg"
    theaters_list[9]["img"] = "../static/imgs/cinemark16.jpg"
    return theaters_list


get_showings()
