from flask import Flask, request, redirect
from test import ribscraper

app = Flask(__name__)

@app.route('/')
def homepage():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Python Ribscraper</title>

    </head>
    <body>


    <h1>Hello World!</h1>
    <form method="POST">
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

    var tday = date.getDate() + 1;
    var tmonth = date.getMonth() + 1;
    var tyear = date.getFullYear();
    if (tmonth < 10) tmonth = "0" + tmonth;
    if (tday < 10) tday = "0" + tday;

    
    var tomorrow = tyear + "-" + tmonth + "-" + tday;
    document.getElementById('start').value = today;
    document.getElementById('tomorrow').value = tomorrow;
    </script>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def my_form_post():
    food_ = request.form.get('food_')
    start = request.form.get('start')
    numdays = request.form.get('numdays')
    #end = request.form.get('end')
    return redirect("/{food_}/{start}/{numdays}".format(food_=food_,start=start,numdays=numdays))

@app.route('/<food_>/<start>/<numdays>')
def scraper(food_,start,numdays):
    output = ribscraper(food_,start,numdays)
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Python Ribscraper</title>
    </head>
    <body>
    <h1> Simple Python Ribscraper </h1>
    <p> {output} </p>
    <input type="button" value="Go Back From Whence You Came!" onclick="history.back(-1)" />
    </body>
    </html>
    """.format(output = output)

if __name__ == "__main__":
    app.run(use_reloader = True, debug = True)
