package api

import (
	"go-diner/v0/internal/umich"
	"net/http"
)

func RouteIndex(w http.ResponseWriter, r *http.Request) {
	location, _ := umich.GetRandomDiningHall()
	menu := umich.Menu{Location: location, Date: "2022-04-19"}
	results := menu.ExecuteOrder("chicken")
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(results))
}

/*
app.get("/api", (req, res) => {
  request(
    "http://api.studentlife.umich.edu/menu/xml2print.php?controller=print&view=json&location=Bursley%20Dining%20Hall",
    function (error, response, body) {
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
*/
