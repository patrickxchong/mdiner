package mongodb

import (
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

type MongoClient struct {
	client         *mongo.Client
	menuCollection *mongo.Collection
}

type MenuCache struct {
	Id        string              `bson:"id,omitempty"`
	Meals     string              `bson:"meals,omitempty"`
	CreatedAt primitive.Timestamp `bson:"createdAt,omitempty"`
	UpdatedAt primitive.Timestamp `bson:"updatedAt,omitempty"`
}
