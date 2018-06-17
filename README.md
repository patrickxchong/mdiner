# The MDiner

A simple web app built with Flask on Python that searches for food that the user desires from [MDining](https://dining.umich.edu/) dining halls within a specified date range.

The app works on the principle of webscraping the 6 dining hall sites (Mosher Jordan, Bursley, North Quad, South Quad, East Quad and West Quad). The results are cached locally in [dining_sites.json](dining_sites.json) to prevent too many requests to the MDining website as well as to reduce the time required to return the result to the user.

## Installation

To run the web app locally
* Install the following dependencies
    * Python 3.5/3.6
    * Flask 1.0.1
* Run the app by running `python app.py`

## Usage

* Go to the [MDiner](https://www.mdiner.ml)
* Type in what you would like to eat
* Select a date range (or use the default range)
* Click ✅ and I hope you find what you're looking for!

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## File Descriptions

As I have experimented with deploying this repo to both Heroku and Digital Ocean, this repo contains a few files that is not necessary to run the program locally.

* Core files to run app locally
    * [app.py](app.py) - Flask Server
    * [MDiningScraper.py](MDiningScraper.py) - Webscraping library
    * [dining_sites.json](dining_sites.json) - Dining Hall results are cached here for faster retrieval
    * Files in the `templates` and `static` folder

* Files for Heroku deployment
    * [Procfile](Procfile)
    * [Procfile.windows](Procfile.windows)
    * [runtime.txt](runtime.txt)

* Files for Digital Ocean deployment (uWSGI and Nginx on Ubuntu 16.04)
    * [wsgi.py](wsgi.py)
    * [myproject.ini](myproject.ini)

## History
* 0.3.2
    * Deployed code to Digital Ocean and linked to free domain https://www.mdiner.ml (for a year)
* 0.3.1
    * Made UI more responsive to screen sizes
* 0.3.0
    * Got inspiration from @wenhoong's School of Information project and implemented caching in MDiningScraper to avoid overloading the MDining server and to improve runtime
* 0.2.1
    * Revamped user interface with the help of a friend who did a mockup on Sketch
* 0.2.0
    * Succesfully built barebones user interface on Flask and deployed to Heroku
    * Reverted to non-threading algorithm because Heroku's free tier doesn't support threading well
* 0.1.1 
    * Experimented with threading to speed up results
    * Threading drastically reduces runtime when running command line interface locally
* 0.1.0
    * Succesfully built a webscraper with Beautiful Soup to search dining halls for desired food and return results in a command line interface


## Credits

* Flask documentation
* Guide on how to [deploy a Python app on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* Guide on how to [host a Flask app via Nginx on Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04) 
* @wenhoong's SI 206 Project 2

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details