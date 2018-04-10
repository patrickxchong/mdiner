from flask import Flask, request, redirect
from flask import render_template
from thread import ribscraper
app = Flask(__name__, static_url_path="/static")


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
