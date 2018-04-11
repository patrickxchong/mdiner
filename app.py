from flask import Flask, request, redirect
from flask import render_template
from thread import ribscraper
import os

app = Flask(__name__, static_url_path="/static")

# # to solve browser cache problem
# @app.url_defaults
# def hashed_url_for_static_file(endpoint, values):
#     if 'static' == endpoint or endpoint.endswith('.static'):
#         filename = values.get('filename')
#         if filename:
#             if '.' in endpoint:  # has higher priority
#                 blueprint = endpoint.rsplit('.', 1)[0]
#             else:
#                 blueprint = request.blueprint  # can be None too

#             if blueprint:
#                 static_folder = app.blueprints[blueprint].static_folder
#             else:
#                 static_folder = app.static_folder

#             param_name = 'h'
#             while param_name in values:
#                 param_name = '_' + param_name
#             values[param_name] = static_file_hash(os.path.join(static_folder, filename))
            
# def static_file_hash(filename):
#   return int(os.stat(filename).st_mtime)


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/', methods=['POST'])
def my_form_post():
    food_ = request.form.get('food_')
    start = request.form.get('start')
    numdays = request.form.get('numdays')
    return redirect("/{food_}/{start}/{numdays}".format(food_=food_,start=start,numdays=numdays))

@app.route('/<food_>/<start>/<numdays>')
def search(food_,start,numdays):
    return render_template("search.html", food_=food_,start=start,numdays=numdays)

@app.route('/find/<food_>/<start>/<numdays>', methods=['POST'])
def scraper(food_,start,numdays):
    return ribscraper(food_,start,numdays)

if __name__ == "__main__":
    app.run(use_reloader = True, debug = True)

