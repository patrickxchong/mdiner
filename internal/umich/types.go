package umich

type Result struct {
	Url      string   `json:"url"`
	Date     string   `json:"date"`
	Location string   `json:"location"`
	Traits   []string `json:"traits"`
	Meal     string   `json:"meal"`
	Name     string   `json:"name"`
}

// should have constructor function like NewMenu?
type Menu struct {
	Location string
	Date     string
	Filename string
	meals    string
}
