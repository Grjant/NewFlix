from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import requests
import sys
from serpapi import GoogleSearch

params = {
    "q": "AMC Barton Creek Square 14",
    "location": "Austin, Texas, United States",
    "hl": "en",
    "gl": "us",
    "api_key": "c226bc4b8d8bf01993a185e0d04287898b59ded4d0e14de453c8ef8744fc6d0f"
}

search = GoogleSearch(params)
results = search.get_dict()
showtimes = results["showtimes"]
print(showtimes)
