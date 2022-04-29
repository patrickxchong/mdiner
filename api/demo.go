package api

import (
	// "encoding/json"
	"fmt"
	"net/http"
)

func RouteDemo(w http.ResponseWriter, r *http.Request) {

	// w.Header().Set("Content-Type", "application/json")

	fmt.Fprintf(w, `{"status":"OK1"}`)
	// w.Write([]byte(`{"status":"OK2"}`))
	// json.NewEncoder(w).Encode(map[string]string{"status": "OK3"})
}
