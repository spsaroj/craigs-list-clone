from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
import requests
from . import models


BASE_CRAIGSLIST_URL = "https://sacramento.craigslist.org/search/sss?query={}"
BASE_IMAGE_URL = "https://images.craigslist.org/{}_600x450.jpg"


# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)   #This is to add all the history of searches to the database
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))  #quote_plus is used to create URLs based on the text
    response = requests.get(final_url)
    data = response.text
    #print(final_url)


    soup = BeautifulSoup(data, features='html.parser')      #Beautiful soup object
    # post_titles = soup.find_all('a', {'class': 'result-title'})     #this will select all the 'a' tags with class name result-title
    # print(post_titles)    This will print in list format. post_title is a list.
    # print(post_titles[0])
    post_listings = soup.find_all('li', {'class': 'result-row'})

    '''post_title = post_listings[0].find(class_="result-title").text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_="result-price").text

    print(post_title)
    print(post_url)
    print(post_price)'''

    postings_list = []

    for post in post_listings:
        post_title = post.find(class_="result-title").text
        post_url = post.find('a').get('href')
        if post.find(class_="result-price"):
            post_price = post.find(class_="result-price").text    
        else:
            post_price = 'N/A'

        if post.find(class_="result-image").get('data-ids'):
            #need to change this to get all the images instead the first one only.
            #So need to remove [0] as it only gets the first image and use loop
            post_image_id = post.find(class_="result-image").get('data-ids').split(",")[0][2:]

            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = "https://craigslist.org/images/peace.jpg"

        postings_list.append((post_title, post_url, post_price, post_image_url))

    

    # This will include all the things that needs to be passed to the frontend. Look at the return command down below.
    to_send_to_frontend = {
        'search': search,
        'final_postings': postings_list,
    }

    return render(request, 'my_app/new_search.html', to_send_to_frontend)       # by attaching to_send_to_frontend, we are sending it to the views.    