from flask import Flask, request, redirect
from flask import render_template
from MDiningScraper import scraper
import os

app = Flask(__name__, static_url_path="/static")

# to solve browser cache problem
@app.url_defaults
def hashed_url_for_static_file(endpoint, values):
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            if '.' in endpoint:  # has higher priority
                blueprint = endpoint.rsplit('.', 1)[0]
            else:
                blueprint = request.blueprint  # can be None too

            if blueprint:
                static_folder = app.blueprints[blueprint].static_folder
            else:
                static_folder = app.static_folder

            param_name = 'h'
            while param_name in values:
                param_name = '_' + param_name
            values[param_name] = static_file_hash(os.path.join(static_folder, filename))
            
def static_file_hash(filename):
  return int(os.stat(filename).st_mtime)

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def my_form_post():
    search = request.form.get('search')
    start = request.form.get('start')
    end = request.form.get('end')
    return redirect("/{search}/{start}/{end}".format(search=search,start=start,end=end))

@app.route('/<search>/<start>/<end>')
def search(search,start,end):
    return render_template("search.html", search=search,start=start,end=end)

@app.route('/find/<search>/<start>/<end>', methods=['POST'])
def python_scraper(search,start,end):
    return scraper(search,start,end)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', use_reloader = True, threaded = True, debug = False)
