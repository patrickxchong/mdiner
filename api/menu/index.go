package api

import (
	"fmt"
	"net/http"
)

func RouteMenu(w http.ResponseWriter, r *http.Request) {

	fmt.Fprintf(w, "<h1>Menu</h1>")
}
