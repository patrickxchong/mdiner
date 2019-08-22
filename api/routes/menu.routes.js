const Menu = require("../models/menu.model.js");

const request = require("request-promise-native");

const diningLocations = [
  "Bursley Dining Hall",
  "East Quad Dining Hall",
  "Markley Dining Hall",
  "Martha Cook Dining Hall",
  "Mosher Jordan Dining Hall",
  "North Quad Dining Hall",
  "South Quad Dining Hall",
  "Twigs at Oxford"
];

module.exports = app => {
  app.get("/api/menu", async (req, res) => {
    let result = {};
    for (let location of diningLocations) {
      await request(
        `http://api.studentlife.umich.edu/menu/xml2print.php?controller=print&view=json&location=${location}`
      ).then(async body => {
        //   console.error("error:", error); // Print the error if one occurred
        //   console.log("statusCode:", response && response.statusCode); // Print the response status code if a response was received
        // Create a Menu
        const menuDB = await new Menu({
          content: body
        });

        // Save menu in the database
        await menuDB.save().catch(err => {
          res.status(500).send({
            message:
              err.message || "Some error occurred while creating the Menu."
          });
        });

        let menu = {};
        let meals = await JSON.parse(body)["menu"]["meal"];
        for (let meal of meals) {
          if (meal.course) {
            menu[meal.name] = [];
            for (let station of meal.course) {
              if (Array.isArray(station.menuitem)) {
                for (let food of station.menuitem) {
                  await menu[meal.name].push(food.name);
                }
              }
            }
          }
        }
        result[location] = menu;
      });
    }
    await res.json(result);
  });
};
