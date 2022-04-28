package umich

import (
	"encoding/json"
	"errors"
	"fmt"
	"go-diner/v0/internal/mongo"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strings"
)

var DINING_LOCATIONS = []string{
	"Bursley Dining Hall",
	"East Quad Dining Hall",
	"Mosher Jordan Dining Hall",
	"South Quad Dining Hall",
	"North Quad Dining Hall",
	"Markley Dining Hall",
	"Twigs at Oxford",
	// "Martha Cook Dining Hall",
}

var DINING_LOCATION_URLS = map[string]string{
	"Bursley Dining Hall":       "bursley",
	"East Quad Dining Hall":     "east-quad",
	"Mosher Jordan Dining Hall": "mosher-jordan",
	"South Quad Dining Hall":    "south-quad",
	"North Quad Dining Hall":    "north-quad",
	"Markley Dining Hall":       "markley",
	"Twigs at Oxford":           "twigs-at-oxford",
	// "Martha Cook Dining Hall": "select-access/martha-cook",
}

func GetDiningHall(index int) (string, error) {
	if index > len(DINING_LOCATIONS) {
		return "", errors.New("index > len(DINING_LOCATIONS)")
	}
	return DINING_LOCATIONS[index], nil
}

func GetRandomDiningHall() (string, error) {
	i := rand.Intn(len(DINING_LOCATION_URLS))
	return GetDiningHall(i)
}

func (m *Menu) ExecuteOrder(item string) string {
	if m.Location == "" || m.Date == "" {
		log.Fatal("Menu Location and Date must be set.")
	}

	if m.Filename != "" {
		// "./internal/umich/menu_demo.json"
		m.GetMenuByFile(m.Filename)
	} else {
		removeWhitespaceRegex := regexp.MustCompile(`\s`)
		id := m.Date + "," + removeWhitespaceRegex.ReplaceAllString(m.Location, "")
		// alternative to remove whitespace that is less efficient -> id := strings.Join(strings.Fields(m.Location), "")

		mongo.Connect()
		defer mongo.Disconnect()
		meals, err := mongo.GetMenuById(id)
		if err != nil {
			meals = m.GetMenuByUrl(m.BuildApiUrl())
			mongo.CreateMenu(id, meals)
		}
		m.meals = meals
	}
	results := m.FilterMenu(item)
	return results
}

func (m *Menu) GetMenuByFile(filename string) string {
	jsonFile, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	} else {
		fmt.Printf("Successfully opened %v\n", filename)
	}
	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)
	m.meals = string(byteValue[:])
	return m.meals
}

func (m *Menu) BuildApiUrl() string {
	url_template := `https://api.studentlife.umich.edu/menu/xml2print.php?controller=print&view=json&location=%s&date=%s`
	url := fmt.Sprintf(url_template, url.QueryEscape(m.Location), m.Date)
	return url
}

func (m *Menu) BuildPageUrl() string {
	url_template := `https://dining.umich.edu/menus-locations/dining-halls/%s/?menuDate=%s`
	url := fmt.Sprintf(url_template, DINING_LOCATION_URLS[m.Location], m.Date)
	return url
}

func (m *Menu) GetMenuByUrl(url string) string {
	if url == "" {
		// default for testing
		url = "https://api.studentlife.umich.edu/menu/xml2print.php?controller=print&view=json&location=Bursley%20Dining%20Hall"
	}
	resp, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	responseData, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	meals := string(responseData[:])
	return meals
}

func (m *Menu) FilterMenu(foodQuery string) string {
	results := []Result{}
	var parsedJson map[string]interface{}

	json.Unmarshal([]byte(m.meals), &parsedJson)

	menuMap := parsedJson["menu"].(map[string]interface{})
	meals := menuMap["meal"].([]interface{})
	for _, meal := range meals {
		if course, ok := meal.(map[string]interface{})["course"]; ok {
			for _, station := range course.([]interface{}) {
				menuitem := station.(map[string]interface{})["menuitem"]

				menuitems, _ := menuitem.([]interface{})
				for _, food := range menuitems {
					foodMap := food.(map[string]interface{})
					searchableString := foodMap["name"].(string)

					var traits []string
					if traitsMap, ok := foodMap["trait"].(map[string]interface{}); ok {
						for k := range traitsMap {
							traits = append(traits, k)
						}
						foodMap["traits"] = traits
						searchableString += "," + strings.Join(traits[:], ",")
					}

					if match := strings.Contains(strings.ToLower(searchableString), strings.ToLower(foodQuery)); match {

						result := Result{
							Url:      m.BuildPageUrl(),
							Date:     m.Date,
							Location: m.Location,
							Traits:   traits,
							Meal:     meal.(map[string]interface{})["name"].(string),
							Name:     foodMap["name"].(string),
						}

						results = append(results, result)
					}
				}

			}
		}
	}

	stringifiedJson, err := json.Marshal(results)
	if err != nil {
		log.Fatal(err)
	}
	return string(stringifiedJson[:])
}
