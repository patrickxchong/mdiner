from flask import render_template, request, redirect, Response
from app import app
import os

from MDiningScraper import scraper

@app.route('/')
def homepage():
    return render_template("home.html")

def stream_template(template_name, **context):      
    with app.app_context():                  
        with app.test_request_context():                                                                                                                      
            app.update_template_context(context)                                                                                                                                                       
            t = app.jinja_env.get_template(template_name)                                                                                                                                              
            rv = t.stream(context)                                                                                                                                                                     
            rv.disable_buffering()                                                                                                                                                                     
            return rv

@app.route('/', methods=['POST'])
def my_form_post():
    search = request.form.get('search')
    start = request.form.get('start')
    end = request.form.get('end')
    results = scraper(search,start,end)
    return Response(stream_template('search.html', results=results))
    # return render_template("search.html", search=search,start=start,end=end)
    # return redirect("/search?q={search}&start={start}&end={end}".format(search=search,start=start,end=end))

@app.route('/search', methods=['POST'])
def searcher():
    search = request.args.get('q', default = '*', type = str)
    start = request.args.get('start', default = '*', type = str)
    end = request.args.get('end', default = '*', type = str)
    return scraper(search,start,end)
    # return app.response_class(scraper(search,start,end), mimetype='application/json')
    # return render_template("search.html", search=search,start=start,end=end)

# @app.route('/find/<search>/<start>/<end>', methods=['POST'])
# def python_scraper(search,start,end):
#     return scraper(search,start,end)

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