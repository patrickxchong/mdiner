package drivers

import (
	"encoding/json"
	"fmt"
)

type Employee struct {
	FirstName string `json:"firstname_string"`
	LastName  string `json:"lastname_string"`
	City      string `json:"city_string"`
}

func FieldTest() {
	json_string := `
    {
        "firstname_string": "Rocky",
        "lastname_string": "Sting",
        "city_string": "London"
    }`

	emp1 := new(Employee)
	json.Unmarshal([]byte(json_string), emp1)
	fmt.Println(emp1)

	emp2 := new(Employee)
	emp2.FirstName = "Ramesh"
	emp2.LastName = "Soni"
	emp2.City = "Mumbai"
	jsonStr, _ := json.Marshal(emp2)
	fmt.Printf("%s\n", jsonStr)
}
