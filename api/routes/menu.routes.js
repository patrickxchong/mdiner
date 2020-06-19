const Menu = require("../models/menu.model.js");

const request = require("request-promise-native");

const DINING_LOCATIONS = [
  "Bursley Dining Hall",
  "East Quad Dining Hall",
  "Mosher Jordan Dining Hall",
  "South Quad Dining Hall",
  "North Quad Dining Hall",
  "Markley Dining Hall",
  // "Martha Cook Dining Hall",
  "Twigs at Oxford"
];

const DINING_LOCATIONS_URLS = {
  "Bursley Dining Hall": "bursley",
  "East Quad Dining Hall": "east-quad",
  "Mosher Jordan Dining Hall": "mosher-jordan",
  "South Quad Dining Hall": "south-quad",
  "North Quad Dining Hall": "north-quad",
  "Markley Dining Hall": "markley",
  // "Martha Cook Dining Hall": "select-access/martha-cook",
  "Twigs at Oxford": "twigs-at-oxford"
};

const TRAITS = ['vegetarian', 'glutenfree', 'mhealthy', 'vegan', 'halal', 'spicy', 'kosher']

module.exports = app => {
  app.get("/api/menu", async (req, res) => {
    if (!req.query.date) {
      res.status(400).send({
        Error: "date query not defined."
      });
      return;
    }

    if (!req.query.item) {
      res.status(400).send({
        Error: "item query not defined."
      });
      return;
    }

    let diningLocations = Object.assign([], DINING_LOCATIONS);
    if (req.query.location) {
      diningLocations = [diningLocations[Number(req.query.location)]];
    }

    if (req.query.page) {
      if (req.query.page === "0") {
        diningLocations = diningLocations.slice(0, 4);
      } else if (req.query.page === "1") {
        diningLocations = diningLocations.slice(4, 7);
      }
    }
    // console.log(diningLocations);

    let results = [];
    for (let location of diningLocations) {
      let id = `${req.query.date},${location.replace(/\s/g, "")}`;
      // console.log(id);
      let meals = await Menu.findOne({ id }).exec();
      if (meals !== undefined && meals !== null) {
        // console.log("Found in DB");
        meals = JSON.parse(meals.meals);
      } else {
        // console.log("Not found in DB");
        let body = await request(
          `http://api.studentlife.umich.edu/menu/xml2print.php?controller=print&view=json&location=${location}&date=${req.query.date}"`
        );

        meals = JSON.parse(body)["menu"]["meal"];

        // Create a Menu
        const menuDB = new Menu({
          id,
          meals: JSON.stringify(meals)
        });

        // Save menu in the database
        await menuDB.save(function (err, menu) {
          if (err) {
            // console.log(err);
          }
          console.log(menu);
        });
      }
      // let menu = [];
      try {
        for (let meal of meals) {
          if (Array.isArray(meal.course)) {
            // menu[meal.name] = [];
            for (let station of meal.course) {
              if (Array.isArray(station.menuitem)) {
                for (let food of station.menuitem) {
                  // menu[meal.name].push(food.name);
                  let name = food.name;
                  if (food.trait) {
                    // console.log(Object.keys(food.trait));
                    name += "," + Object.keys(food.trait).join(",")
                  }
                  if (
                    name.search(new RegExp(req.query.item, "ig")) != -1
                  ) {
                    results.push({
                      url: `https://dining.umich.edu/menus-locations/dining-halls/${DINING_LOCATIONS_URLS[location]}/?menuDate=${req.query.date}`,
                      date: req.query.date,
                      location,
                      trait: food.trait,
                      meal: meal.name,
                      name: food.name
                    });
                  }
                }
              }
            }
          }
        }
      } catch (e) {
        console.log(meals);
        console.log(e);
      }
      // results[location] = menu; //menu;
    }
    res.json(results);
  });
};
