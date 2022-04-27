package main

import (
	// "fmt"
	// "go-diner/v0/api"
	// "go-diner/v0/api/menu"
	// "go-diner/v0/internal/demos"
	"fmt"
	"go-diner/v0/internal/umich"
	// "go-diner/v0/internal/mongo"
	// "log"
	// "net/http"
)

func main() {
	// demos.Cli()
	// demos.ConnectMongo()
	// demos.FieldTest()

	// http.HandleFunc("/api/menu", menu.RouteMenu)
	// http.HandleFunc("/api/demo", api.RouteDemo)
	// log.Fatal(http.ListenAndServe(":8080", nil))

	location, err := umich.GetDiningHall(1)
	if err != nil {
		fmt.Println(err)
	}
	menu := umich.Menu{Location: location, Date: "2022-04-19"}
	// menu := umich.Menu{Location: location, Date: "2022-04-19", Filename: "./internal/umich/menu_demo.json"}
	results := menu.ExecuteOrder("chicken")
	fmt.Println(results)

	// mongo.AddMenu()
	// fmt.Println(mongo.GetMenuById("id"))
	// fmt.Println(mongo.GetMenuById("id1"))
	// mongo.GetMenus()

}
