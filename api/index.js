const express = require("express");
const helmet = require("helmet");
const request = require("request");

const app = express();

app.use(helmet());

let isObject = function(a) {
  return (!!a) && (a.constructor === Object);
};

app.get("*", (req, res) => {
  request(
    "http://api.studentlife.umich.edu/menu/xml2print.php?controller=print&view=json&location=Bursley%20Dining%20Hall",
    function(error, response, body) {
      console.error("error:", error); // Print the error if one occurred
      console.log("statusCode:", response && response.statusCode); // Print the response status code if a response was received
      
      let result = {}
      
      let meals = JSON.parse(body)["menu"]["meal"]
      meals.forEach(meal => {
        if (meal.course) {
          result[meal.name] = [];
          (meal.course).forEach((station)=> {
            if (Array.isArray(station.menuitem)) {
              station.menuitem.forEach((food)=> {
                result[meal.name].push(food.name)
              })
            }
          })
        }
      })
      res.json(result);
    }
  );
});

module.exports = app;
