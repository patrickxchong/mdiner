package main

import (
	// "fmt"
	"go-diner/v0/drivers"
)

type Vertex struct {
	X int
	Y int
}

func main() {
	// arr := []int64{0, 1}
	// v:= Vertex{1, 2}
	// p := &v
	// fmt.Printf("%v %#v %T\n",p,p,p)
	// fmt.Printf("%v %#v %T\n",v,v,v)
	// fmt.Printf("%v %#v %T\n",v.X,v.X,v.X)
	// drivers.Cli()
	drivers.ConnectMongo()
	// drivers.FieldTest()
}
