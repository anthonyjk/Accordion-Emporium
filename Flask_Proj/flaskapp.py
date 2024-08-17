import sys
from flask import Flask, render_template, request, redirect, url_for
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread

sys.path.append('C:\\Users\\ajtru\\Music\\Accordion-Emporium\\accordionscraper\\spiders')
import database
from  accordionspider import AccordionSpider, crawl_to_json

app = Flask(__name__)

# bash cmds
# RUN ON GIT BASH!!!!

# export FLASK_APP=flaskapp.py
# sets file location for flask

# flask run
# runs flask at localhost:5000

# export FLASK_DEBUG=1
# debug mode

@app.route("/")
def home():

	json_data = database.load_json('accordion.json')
	database.update_database(json_data, True, push=True)

	data = database.get_sql_data()

	return render_template('home.html', data = data)

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/sort_price", methods=['POST'])
def sort_price():
	#database.sort_price()
	return redirect(url_for("home"))

@app.route('/refresh_list', methods=['POST'])
def refresh_list():
	recrawl()
	return redirect(url_for("home"))

def recrawl():
	thread = Thread(target=crawl_to_json())
	thread.start()

	data = database.load_json('accordion.json')
	database.update_database(data, True, push=True)

# Runs in debug mode when called directly (python flaskapp.py)
if __name__ == '__main__':
	app.run(debug=True)
