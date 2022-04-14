package api

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func RouteIndex(w http.ResponseWriter, r *http.Request) {
	url := "http://api.studentlife.umich.edu/menu/xml2print.php?controller=print&view=json&location=Bursley%20Dining%20Hall"
	resp, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("Response status:", resp.Status)

	responseData, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	var parsedJson map[string]interface{}

	json.Unmarshal([]byte(responseData), &parsedJson)
	fmt.Println(parsedJson["menu"])

	stringifiedJson, err := json.Marshal(parsedJson)
	if err != nil {
		log.Fatal(err)
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(stringifiedJson)
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
