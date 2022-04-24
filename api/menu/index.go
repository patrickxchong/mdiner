package menu

import (
	"encoding/json"
	// "fmt"
	"go-diner/v0/internal/umich"
	"log"
	"net/http"
	// "strings"
)

func respondStatusBadRequest(w http.ResponseWriter, errorMessage string) {
	w.WriteHeader(http.StatusBadRequest)
	w.Header().Set("Content-Type", "application/json")
	resp := make(map[string]string)
	resp["message"] = errorMessage
	jsonResp, err := json.Marshal(resp)
	if err != nil {
		log.Fatalf("Error happened in JSON marshal. Err: %s", err)
	}
	w.Write(jsonResp)
}

func respondStatusOK(w http.ResponseWriter, jsonString string) {
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(jsonString))

}

func RouteMenu(w http.ResponseWriter, r *http.Request) {

	location := r.URL.Query().Get("location")
	date := r.URL.Query().Get("date")
	item := r.URL.Query().Get("item")
	// alternative that returns in array format -> items := r.URL.Query()["item"]

	if location == "" {
		respondStatusBadRequest(w, "Location query is empty")
		return
	}
	if date == "" {
		respondStatusBadRequest(w, "Date query is empty")
		return
	}
	if item == "" {
		respondStatusBadRequest(w, "Item query is empty")
		return
	}

	menu := umich.Menu{Location: location, Date: date}
	results := menu.ExecuteOrder(item)

	respondStatusOK(w, results)
}
