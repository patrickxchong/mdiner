require("dotenv").config();

const consola = require("consola");
const express = require("express");
const helmet = require("helmet");
const request = require("request");

const app = express();

app.use(helmet());

// ==== Mongoose ====
const mongoose = require("mongoose");
mongoose.set("useCreateIndex", true);
mongoose.Promise = global.Promise;
// Connecting to the database
mongoose
  .connect(process.env.MDINER_MONGO_CONNECTION_STRING, {
    useNewUrlParser: true
  })
  .then(() => {
    consola.info("Successfully connected to the database");
  })
  .catch(err => {
    consola.info(`Could not connect to the database. Exiting now... ${err}`);
    process.exit();
  });

app.get("/api", (req, res) => {
  request(
    "http://api.studentlife.umich.edu/menu/xml2print.php?controller=print&view=json&location=Bursley%20Dining%20Hall",
    function(error, response, body) {
      console.error("error:", error); // Print the error if one occurred
      console.log("statusCode:", response && response.statusCode); // Print the response status code if a response was received

      let result = {};

      let meals = JSON.parse(body)["menu"]["meal"];
      meals.forEach(meal => {
        if (meal.course) {
          result[meal.name] = [];
          meal.course.forEach(station => {
            if (Array.isArray(station.menuitem)) {
              station.menuitem.forEach(food => {
                result[meal.name].push(food.name);
              });
            }
          });
        }
      });
      res.json(JSON.parse(body));
    }
  );
});

require("./routes/menu.routes")(app);

module.exports = app;
