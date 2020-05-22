# The MDiner

A simple web app built with Express.js that searches for food that the user desires from [MDining](https://dining.umich.edu/) dining halls within a specified date range.

The app works by getting data from the UMich Student Life API, and storing the food data in a remote MongoDB server for quick retrieval.

## Usage

- Go to the [MDiner](https://mdiner.now.sh)
- Type in what you would like to eat
- Select a date range (or use the default range)
- Click ✅ and I hope you find what you're looking for!

## Installation

To run the web app locally

- Install the following dependencies
  - Install Node.js
  - Run `npm install` or `yarn install` to install Express.js and other dependencies
- Run the app by running `npm run dev` or `yarn dev`

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

- 1.0.0
  - Migrated codebase from Flask on Python to Express.js on Node.js. Project deployed to https://mdiner.now.sh
- 0.3.2
  - Deployed code to Digital Ocean and linked to free domain https://www.mdiner.ml (for a year)
- 0.3.1
  - Made UI more responsive to screen sizes
- 0.3.0
  - Got inspiration from @wenhoong's School of Information project and implemented caching in MDiningScraper to avoid overloading the MDining server and to improve runtime
- 0.2.1
  - Revamped user interface with the help of a friend who did a mockup on Sketch
- 0.2.0
  - Succesfully built barebones user interface on Flask and deployed to Heroku
  - Reverted to non-threading algorithm because Heroku's free tier doesn't support threading well
- 0.1.1
  - Experimented with threading to speed up results
  - Threading drastically reduces runtime when running command line interface locally
- 0.1.0
  - Succesfully built a webscraper with Beautiful Soup to search dining halls for desired food and return results in a command line interface

## Buy me a coffee (or bubble tea)
[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/patrickxchong)


## License

This project is licensed under the GNU General Public License v3.0 or later - see the [COPYING](COPYING) file for details
