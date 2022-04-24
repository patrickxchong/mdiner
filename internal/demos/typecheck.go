package drivers

import (
	"reflect"
)

func TypeCheck1(variable interface{}) string {
	switch variable.(type) {
	case string:
		return "string"
	case int:
		return "int"
	case []interface{}:
		return "slice"
	case map[string]interface{}:
		return "map"
	default:
		return "nil"
	}

}

func TypeCheck2(variable interface{}) string {
	rt := reflect.TypeOf(variable)
	switch rt.Kind() {
	case reflect.Slice:
		return "slice"
	case reflect.Array:
		return "array"
	case reflect.Map:
		return "map"
	default:
		return "nil"
	}
}
