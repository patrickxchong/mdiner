from flask import Flask, request, redirect
from thread import ribscraper
app = Flask(__name__)

@app.route('/')
def homepage():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="UTF-8">
        <title>Python Ribscraper</title>
    </head>
    <body>

    <h1>Hello World!</h1>
    <p> This ribscraper aims to tell you when the dining hall serves what you like! </p>
    <form action = "" method="POST">
        <p> Type of food: <input type="text" name="food_" value="Rib"> </p>
        <p> Starting date: <input type="date" id ='start' name="start"> </p> 
        <p> Number of days: <input type="number" name="numdays" min="1" max="15" value="2"> </p>
    <input type="submit">
    </form>
    <script type="text/javascript">
    
    var date = new Date();
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();
    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;
    var today = year + "-" + month + "-" + day;
    
    document.getElementById('start').value = today;
    </script>
    '''

@app.route('/', methods=['POST'])
def my_form_post():
    food_ = request.form.get('food_')
    start = request.form.get('start')
    numdays = request.form.get('numdays')
    return redirect("/{food_}/{start}/{numdays}".format(food_=food_,start=start,numdays=numdays))

@app.route('/<food_>/<start>/<numdays>')
def scraper(food_,start,numdays):
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Python Ribscraper</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="http://code.jquery.com/jquery-2.2.4.min.js" integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44=" crossorigin="anonymous"></script>
    </head>
    <body>
    <h1> Simple Python Ribscraper </h1>
    <p id="output"> Buffering ... </p>
    <input type="button" value="Go Back From Whence You Came!" onclick="history.back(-1)" />
    <script type="text/javascript">
    


    function postData(input) {{
        $.post("/find/{food_}/{start}/{numdays}",{{name: "Donald Duck",city: "Duckburg"}},
        function callbackFunc(response) {{document.getElementById("output").innerHTML = response;
        }})
    }}

    postData();

    </script>
    </body>
    </html>""".format(food_=food_,start=start,numdays=numdays)

@app.route('/find/<food_>/<start>/<numdays>', methods=['POST'])
def test(food_,start,numdays):
    return ribscraper(food_,start,numdays)

if __name__ == "__main__":
    app.run(use_reloader = True, debug = True)
