from django.shortcuts import render

from celery import Celery
from . import crawl

IS_CRAWLING = False		# Read-only!!

# Create your views here.
def index(requests):
	context = {"is_crawling": IS_CRAWLING}
	return render(requests, "crawling/index.html", context)

def players(requests):
	global IS_CRAWLING
	if IS_CRAWLING:
		return None

	IS_CRAWLING = True
	crawl.crawl_players()
	IS_CRAWLING = False
	return None
