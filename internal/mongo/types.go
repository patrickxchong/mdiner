package mongo

import (
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type MenuCache struct {
	Id        string              `bson:"id,omitempty"`
	Meals     string              `bson:"meals,omitempty"`
	CreatedAt primitive.Timestamp `bson:"createdAt,omitempty"`
	UpdatedAt primitive.Timestamp `bson:"updatedAt,omitempty"`
}
