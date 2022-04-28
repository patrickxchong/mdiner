package mongodb

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

var ctxBackground context.Context = context.Background()

func init() {
	godotenv.Load()
}

func NewClient() MongoClient {
	var mongoClient MongoClient
	// timeout10s, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	// defer cancel()

	connectionString := os.Getenv("MDINER_MONGO_CONNECTION_STRING")
	newClient, err := mongo.NewClient(options.Client().ApplyURI(connectionString))
	if err != nil {
		log.Fatal(err)
	}
	mongoClient.client = newClient
	return mongoClient
}

func (mongoClient *MongoClient) Connect() {
	err := mongoClient.client.Connect(ctxBackground)
	if err != nil {
		log.Fatal(err)
	}

	// Check the connection - commented out to reduce latency and it's not required (?)
	// err = client.Ping(ctxBackground, nil)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	mongoClient.menuCollection = mongoClient.client.Database("mdiner").Collection("menu")
}

func (mongoClient *MongoClient) Disconnect() {
	mongoClient.client.Disconnect(ctxBackground)
}

func (mongoClient *MongoClient) CreateMenu(id string, meals string) {
	menu := MenuCache{
		Id:        id,
		Meals:     meals,
		CreatedAt: primitive.Timestamp{T: uint32(time.Now().Unix())},
		UpdatedAt: primitive.Timestamp{T: uint32(time.Now().Unix())},
	}

	_, insertErr := mongoClient.menuCollection.InsertOne(ctxBackground, menu)
	if insertErr != nil {
		log.Fatal(insertErr)
	}
}

func (mongoClient *MongoClient) GetMenuById(id string) (string, error) {
	menu, err := mongoClient.GetMenu(bson.D{primitive.E{Key: "id", Value: id}})
	if err != nil {
		return "", err
	}
	return menu.Meals, nil
}

func (mongoClient *MongoClient) GetMenu(filter interface{}) (*MenuCache, error) {
	var menu MenuCache
	err := mongoClient.menuCollection.FindOne(ctxBackground, filter).Decode(&menu)
	if err != nil {
		// ErrNoDocuments means that the filter did not match any documents in the collection
		if err == mongo.ErrNoDocuments {
			return nil, err
		}
		log.Fatal(err)
	}
	return &menu, err
}

func (mongoClient *MongoClient) GetMenus(id string) {
	cur, currErr := mongoClient.menuCollection.Find(ctxBackground, bson.D{})

	if currErr != nil {
		panic(currErr)
	}
	defer cur.Close(ctxBackground)

	var posts []MenuCache
	if err := cur.All(ctxBackground, &posts); err != nil {
		panic(err)
	}
	fmt.Println(posts)
}
