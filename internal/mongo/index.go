package mongo

import (
	"context"
	"fmt"
	"github.com/joho/godotenv"
	"log"
	"os"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// Design with old mongo package (for reference)
// https://github.com/eamonnmcevoy/go_rest_api/tree/master/pkg/mongo

// https://levelup.gitconnected.com/build-a-todo-app-in-golang-mongodb-and-react-e1357b4690a6
// https://github.com/schadokar/go-to-do-app/blob/main/go-server/middleware/middleware.go
// https://dev.to/hackmamba/build-a-rest-api-with-golang-and-mongodb-fiber-version-4la0

var client *mongo.Client
var menuCollection *mongo.Collection
var timeout10s context.Context

func init() {
	godotenv.Load()
	connectionString := os.Getenv("MDINER_MONGO_CONNECTION_STRING")

	newClient, err := mongo.NewClient(options.Client().ApplyURI(connectionString))
	client = newClient
	if err != nil {
		log.Fatal(err)
	}

	menuCollection = client.Database("mdiner").Collection("menu")
}

func Connect() {
	timeout10s, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	err := client.Connect(timeout10s)
	if err != nil {
		log.Fatal(err)
	}

	// Check the connection - commented out to reduce latency
	// err = client.Ping(timeout10s, nil)
	// if err != nil {
	// 	log.Fatal(err)
	// }
}

func Disconnect() {
	client.Disconnect(timeout10s)
}

func CreateMenu(id string, meals string) {
	menu := MenuCache{
		Id:        id,
		Meals:     meals,
		CreatedAt: primitive.Timestamp{T: uint32(time.Now().Unix())},
		UpdatedAt: primitive.Timestamp{T: uint32(time.Now().Unix())},
	}

	_, insertErr := menuCollection.InsertOne(timeout10s, menu)
	if insertErr != nil {
		log.Fatal(insertErr)
	}
}

func GetMenuById(id string) (string, error) {
	menu, err := GetMenu(bson.D{primitive.E{Key: "id", Value: id}})
	if err != nil {
		return "", err
	}
	return menu.Meals, nil
}

func GetMenu(filter interface{}) (*MenuCache, error) {
	var menu MenuCache
	err := menuCollection.FindOne(timeout10s, filter).Decode(&menu)
	if err != nil {
		// ErrNoDocuments means that the filter did not match any documents in the collection
		if err == mongo.ErrNoDocuments {
			return nil, err
		}
		log.Fatal(err)
	}
	return &menu, err
}

func GetMenus(id string) {
	cur, currErr := menuCollection.Find(timeout10s, bson.D{})

	if currErr != nil {
		panic(currErr)
	}
	defer cur.Close(timeout10s)

	var posts []MenuCache
	if err := cur.All(timeout10s, &posts); err != nil {
		panic(err)
	}
	fmt.Println(posts)
}
