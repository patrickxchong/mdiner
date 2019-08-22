//
//  MenusAPIManager.swift
//  DiningMenus
//
//  Created by Maxim Aleksa on 2/25/17.
//  Copyright © 2017 Maxim Aleksa. All rights reserved.
//

import Foundation
import CoreLocation


// MARK: - MenusAPIManager Class


/**
 This class communicates with the API over the network to get dining information.

 All of the functions in this class are *class* functions, which means that
 they must be called on the `MenusAPIManager` class, and not on an instance of the class:

 ````
 MenusAPIManager.getDiningLocations { diningLocationsFromAPI in
     print(diningLocationsFromAPI.count)
 }
 ````

 Since the functions in this class communicate with the API over the network,
 which takes some time, the functions are *asynchronous*. This means that they
 "return" before they finish executing, so that they do not block the main thread
 and the entire UI (e.g., scrolling) while the data is loading.

 Once the data finishes loading, these functions will call `completionHandler`,
 which is provided as the last argument.
 */
public class MenusAPIManager {

    // MARK: Class methods

    /**
     Gets dining locations from the API.

     This is a *class* function that must be called on the `MenusAPIManager` class,
     and not on an instance of the class (see example below).

     - important:
     This is an *asynchronous* function that calls `completionHandler`
     when data is fetched from the API.

     - parameter completionHandler: a function that will execute once the data is
     retrieved from the API.
     This function will be called with one argument, an array of `DiningLocation` objects.


     **Example**

     This example shows how to retrieve the dining locations from the API, and then
     print the number of dining locations in the array.

     ````
     MenusAPIManager.getDiningLocations { diningLocationsFromAPI in
         print(diningLocationsFromAPI.count)
     }
     ````
    */
    public class func getDiningLocations(completionHandler: @escaping (([DiningLocation]) -> Void)) {

        // dictionary that maps dining location IDs to occupancies
        var occupancies = [String: Int]()

        var diningLocations = [DiningLocation]()

        var didLoadDiningLocations = false
        var didLoadOccupancies = false

        func matchOccupancies() {
            if didLoadDiningLocations && didLoadOccupancies {
                // match occupancies
                for diningLocation in diningLocations {
                    if let currentOccupancy = occupancies[diningLocation.id] {
                        diningLocation.currentOccupancy = currentOccupancy
                    }
                }
                // ensure we are on the main queue
                DispatchQueue.main.async {
                    completionHandler(diningLocations)
                }
            }
        }

        // get dining hall data
        let url = APIURLs.diningLocations
        fetch(url: url) { (json) in
            if let locationsJSON = json?.array {
                let locations = locationsJSON.map { DiningLocation(json: $0) }
                diningLocations = locations.removeNils()
            }
            didLoadDiningLocations = true
            matchOccupancies()
        }

        // get occupancy data
        let occupancyURL = APIURLs.occupancy
        fetch(url: occupancyURL) { (json) in
            if let jsonArray = json?["diningHallGroup"].array {
                for group in jsonArray {
                    for diningLocationJSON in group["diningHall"].arrayValue {
                        if let id = diningLocationJSON["name"].string, let currentOccupancy = diningLocationJSON["hallCapacity"]["currentOccupancy"].int {

                            occupancies[id] = currentOccupancy
                        }
                    }
                }
            }
            didLoadOccupancies = true
            matchOccupancies()
        }
    }


    /**
     Gets meals for specified dining location and date (that defaults to
     today's date) from the API.

     This is a *class* function that must be called on the `MenusAPIManager` class,
     and not on an instance of the class (see example below).

     - important:
     This is an *asynchronous* function that calls `completionHandler`
     when data is fetched from the API.

     - parameter diningLocation: an instance of `DiningLocation` class for which
     this function should get the meals.

     - parameter date: an instance of `Date` for which this function should get
     the meals. This argument is optional, and if not provided, this function will
     get the meals for today's date.

     - parameter completionHandler: a function that will execute once the data is
     retrieved from the API.
     This function will be called with one argument, an array of `Meal` objects.


     **Example**

     This example shows how to retrieve the meals for some dining location (`aDiningHall`)
     for today from the API, and then print the number of meals in the array.
     
     ````
     let aDiningHall: DiningLocation = ...
     MenusAPIManager.getMeals(for: aDiningHall) { mealsFromAPI in
        print(meals.count)
     }
     ````
     */
    public class func getMeals(for diningLocation: DiningLocation, on date: Date = Date(), completionHandler: @escaping (([Meal]) -> Void)) {

        let url = APIURLs.menusURL(for: diningLocation, on: date)
        fetch(url: url) { (json) in
            if let mealsJSON = json?["menu"]["meal"].array {
                var meals = mealsJSON.map({ (json) -> Meal? in
                    if let name = json["name"].string {
                        var type: Meal.MealType!

                        if name == "BREAKFAST" {
                            type = .breakfast
                        } else if name == "LUNCH TRANSITION" {
                            type = .lunchTransition
                        } else if name == "LUNCH" {
                            type = .lunch
                        } else if name == "DINNER TRANSITION" {
                            type = .dinnerTransition
                        } else if name == "DINNER" {
                            type = .dinner
                        } else if name == "PARSTOCKS" || name == "SMART TEMPS" {
                            type = .other
                        }

                        if type != nil {

                            var coursesJSONArray: [JSON]?
                            if let jsonArray = json["course"].array {
                                coursesJSONArray = jsonArray
                            } else if json["course"].dictionary != nil {
                                coursesJSONArray = [json["course"]]
                            }
                            let courses = coursesJSONArray?.map({ (json) -> Course? in
                                if let name = json["name"].string {
                                    var menuItems = [MenuItem?]()
                                    func jsonToMenuItem(json: JSON) -> MenuItem? {
                                        return MenuItem(json: json)
                                    }
                                    if let _ = json["menuitem"].dictionary {
                                        menuItems = [jsonToMenuItem(json: json["menuitem"])]
                                    } else if let menuItemArray = json["menuitem"].array {
                                        menuItems = menuItemArray.map(jsonToMenuItem)
                                    }
                                    return Course(name: name.trimmingCharacters(in: CharacterSet.whitespaces), menuItems: menuItems.removeNils())
                                }
                                return nil
                            })
                            let message = json["message"]["content"].string
                            return Meal(type: type, courses: courses?.removeNils(), message: message)
                        }
                    }
                    return nil
                })

                // combine "other" meals and remove nils
                var newMeals = [Meal]()
                var otherMeal: Meal?
                for meal in meals {
                    if meal != nil {
                        if meal?.type == .other {
                            if otherMeal == nil {
                                otherMeal = meal
                            } else {
                                // add courses
                                if meal?.courses != nil {
                                    let otherCourses = otherMeal?.courses ?? []
                                    let newCourses = otherCourses + meal!.courses!
                                    otherMeal = Meal(type: .other, courses: newCourses)
                                }
                            }
                        } else {
                            newMeals.append(meal!)
                        }
                    }
                }
                if otherMeal != nil {
                    newMeals.append(otherMeal!)
                }

                // ensure we are on the main queue
                DispatchQueue.main.async {
                    completionHandler(newMeals)
                }
            } else {

                // ensure we are on the main queue
                DispatchQueue.main.async {
                    completionHandler([])
                }
            }
        }
    }


    /**
     Gets current occupancy of the specified dining location, if available.

     - note:
     Only dining halls support occupancy (excluding Martha Cook and Lawyers Club).

     If occupancy is currently not available for the specified dining location, the
     `completionHandler` function is called with `nil`.

     This is a *class* function that must be called on the `MenusAPIManager` class,
     and not on an instance of the class (see example below).

     - important:
     This is an *asynchronous* function that calls `completionHandler`
     when data is fetched from the API.

     - parameter diningLocation: an instance of `DiningLocation` class for which
     this function should get the meals.

     - parameter completionHandler: a function that will execute once the data is
     retrieved from the API.
     This function will be called with one argument, an optional `Int`,
     which will be `nil` if current occupancy is currently not available
     for the specified dining location.


     **Example**

     This example shows how to get the occupancy for some dining location (`aDiningHall`)
     from the API, and then print the occupancy if it is available.
     
     ````
     let aDiningHall: DiningLocation = ...
     MenusAPIManager.getCurrentOccupancy(for: aDiningHall) { currentOccupancy in
         if let occupancy = currentOccupancy {
             print(occupancy)
         } else {
             print("Occupancy information is not available.")
         }
     }
     ````
     */
    public class func getCurrentOccupancy(for diningLocation: DiningLocation, completionHandler: @escaping ((_ currentOccupancy: Int?) -> Void)) {
        // get occupancy data
        let occupancyURL = APIURLs.occupancy
        fetch(url: occupancyURL) { (json) in
            var occupancy: Int? = nil
            if let jsonArray = json?["diningHallGroup"].array {
                for group in jsonArray {
                    for diningLocationJSON in group["diningHall"].arrayValue {
                        if let id = diningLocationJSON["name"].string, let currentOccupancy = diningLocationJSON["hallCapacity"]["currentOccupancy"].int {

                            if id == diningLocation.id {
                                occupancy = currentOccupancy
                                break
                            }
                        }
                    }
                }
            }
            // ensure we are on the main queue
            DispatchQueue.main.async {
                completionHandler(occupancy)
            }
        }
    }


    /**
     Gets actual hours (including holiday and special event hours)
     for the specified dining location is open on the specified date.

     Hours are provided as an array of
     [tuples](https://developer.apple.com/library/content/documentation/Swift/Conceptual/Swift_Programming_Language/TheBasics.html#//apple_ref/doc/uid/TP40014097-CH5-ID329),
     where each tuple is composed of...

     * `eventTitle`, a string such as `"Brunch"`, `"Dinner"` or `"Open"`
     * `hours`, a string representing hours for that event (e.g., `"7:00 AM – 2:00 PM"`).

     This is a *class* function that must be called on the `MenusAPIManager` class,
     and not on an instance of the class (see example below).

     - important:
     This is an *asynchronous* function that calls `completionHandler`
     when data is fetched from the API.

     - note:
     Since there exists another function of the same name, you must specify
     the type of the argument of completion handler when calling `getHours`.
     So it should be similar to `events: [(eventTitle: String, hours: String)]`
     instead of just `events`. See example below.

     - parameter diningLocation: an instance of `DiningLocation` class for which
     this function should get the hours

     - parameter date: an instance of `Date` for which this function should get
     the hours.

     - parameter completionHandler: a function that will execute once the data is
     retrieved from the API.
     This function will be called with one argument, an array of tuples
     describing the hours (see above).


     **Example**

     This example shows how to get the hours for some dining location (`aDiningHall`)
     from the API, and then print the hours in the format

     ````
     Breakfast and Lunch: 7:00 AM – 2:00 PM
     Dinner: 5:00 PM – 8:00 PM
     ````

     ````
     let aDiningHall: DiningLocation = ...
     let someDate: Date = ...
     MenusAPIManager.getHours(for: aDiningHall, on: someDate) { events: [(eventTitle: String, hours: String)] in
         for eventTitle, hours in events {
             print("\(eventTitle): \(hours)")
         }
     }
     ````


     **See also**

     [Tuples](https://developer.apple.com/library/content/documentation/Swift/Conceptual/Swift_Programming_Language/TheBasics.html#//apple_ref/doc/uid/TP40014097-CH5-ID329)
     */
    public class func getHours(for diningLocation: DiningLocation, on date: Date, completionHandler: @escaping (([(eventTitle: String, hours: String)]) -> Void)) {

        MenusAPIManager.getHours(for: diningLocation, on: date) { (events: [(eventTitle: String, hours: (start: Date, end: Date))]) in
            var result = [(String, String)]()
            for (eventTitle, (start: startDate, end: endDate)) in events {
                let formatter = DateFormatter()
                formatter.dateStyle = .none
                formatter.timeStyle = .short
                let hours = "\(formatter.string(from: startDate)) – \(formatter.string(from: endDate))"
                result.append((eventTitle, hours))
            }
            completionHandler(result)
        }
    }


    /**
     Gets actual hours (including holiday and special event hours)
     for the specified dining location is open on the specified date.

     Hours are provided as an array of
     [tuples](https://developer.apple.com/library/content/documentation/Swift/Conceptual/Swift_Programming_Language/TheBasics.html#//apple_ref/doc/uid/TP40014097-CH5-ID329),
     where each tuple is composed of...

     * `eventTitle`, a string such as `"Brunch"`, `"Dinner"` or `"Open"`
     * `hours`, another tuple, composed of...
         * `start`, a date representing the start of the event
         * `end`, a date representing the end of the event

     This is a *class* function that must be called on the `MenusAPIManager` class,
     and not on an instance of the class (see example below).

     - important:
     This is an *asynchronous* function that calls `completionHandler`
     when data is fetched from the API.

     - note:
     Since there exists another function of the same name, you must specify
     the type of the argument of completion handler when calling `getHours`.
     So it should be similar to `events: [(eventTitle: String, hours: (start: Date, end: Date))]`
     instead of just `events`. See example below.

     - note:
     You can use a `DateFormatter` to format a `Date` as a string.
     See the example in the implementation of the other `getHours` function.

     - parameter diningLocation: an instance of `DiningLocation` class for which
     this function should get the hours.

     - parameter date: an instance of `Date` for which this function should get
     the hours.

     - parameter completionHandler: a function that will execute once the data is
     retrieved from the API.
     This function will be called with one argument, an array of tuples
     describing the hours (see above).


     **Example**

     This example shows how to get the hours for some dining location (`aDiningHall`)
     from the API, and then print the hours in the format

     ````
     Breakfast and Lunch: 2017-03-27 11:00:00 +0000 – 2017-03-27 18:00:00 +0000
     Dinner: 2017-03-27 21:00:00 +0000 – 2017-03-28 00:00:00 +0000
     ````

     ````
     let aDiningHall: DiningLocation = ...
     let someDate: Date = ...
     MenusAPIManager.getHours(for: aDiningHall, on: someDate) { events: [(eventTitle: String, hours: (start: Date, end: Date))] in
         for eventTitle, hours in events {
             print("\(eventTitle): \(hours.start) – \(hours.end)")
         }
     }
     ````


     **See also**

     [Tuples](https://developer.apple.com/library/content/documentation/Swift/Conceptual/Swift_Programming_Language/TheBasics.html#//apple_ref/doc/uid/TP40014097-CH5-ID329)

     [Date - Foundation](https://developer.apple.com/reference/foundation/date)
     */
    public class func getHours(for diningLocation: DiningLocation, on date: Date, completionHandler: @escaping (([(eventTitle: String, hours: (start: Date, end: Date))]) -> Void)) {
        let url = APIURLs.menusURL(for: diningLocation, on: date)
        fetch(url: url) { (json) in
            let jsonArray: [JSON]
            if json?["hours"]["calendar_event"].array != nil {
                jsonArray = json!["hours"]["calendar_event"].array!
            } else if json?["hours"]["calendar_event"].dictionary != nil {
                jsonArray = [json!["hours"]["calendar_event"]]
            } else {
                jsonArray = []
            }

            var events = [(eventTitle: String, (start: Date, end: Date))]()
            for eventJSON in jsonArray {
                if let eventTitle = eventJSON["event_title"].string, let startString = eventJSON["event_time_start"].string, let endString = eventJSON["event_time_end"].string {
                    if let startDate = startString.dateFromISO8601, let endDate = endString.dateFromISO8601 {
                        events.append((eventTitle, (startDate, endDate)))
                    }
                }
            }
            // ensure we are on the main queue
            DispatchQueue.main.async {
                completionHandler(events)
            }
        }
    }


    /**
     Checks if the specified dining locaiton is open at the specified time and date.

     This is a *class* function that must be called on the `MenusAPIManager` class,
     and not on an instance of the class (see example below).

     - important:
     This is an *asynchronous* function that calls `completionHandler`
     when data is fetched from the API.

     - parameter diningLocation: an instance of `DiningLocation` class that
     the function is checking.

     - parameter date: an instance of `Date` for which this function should check
     if the specified dining location is opened or closed.

     - parameter completionHandler: a function that will execute once the data is
     retrieved from the API.
     This function will be called with one argument, a Bool, which will be
     `true` if the dining location is open and `false` otherwise.


     **Example**

     This example shows how to check if a dining location is open on some date.

     ````
     let aDiningHall: DiningLocation = ...
     let someDate: Date = ...
     MenusAPIManager.isOpen(aDiningHall, on: someDate) { open in
         if open {
             print("\(aDiningHall) is open")
         } else {
             print("\(aDiningHall) is closed")
         }
     }
     ````


     **See also**

     [Date - Foundation](https://developer.apple.com/reference/foundation/date)
     */
    public class func isOpen(_ diningLocation: DiningLocation, on date: Date, completionHandler: @escaping ((Bool) -> Void)) {
        MenusAPIManager.getHours(for: diningLocation, on: date, completionHandler: { (events: [(eventTitle: String, hours: (start: Date, end: Date))]) in

            var isOpen = false
            for (_, hours) in events {
                if (hours.start...hours.end).contains(date) {
                    isOpen = true
                }
            }
            completionHandler(isOpen)
        })
    }

    /// URLs for APIs
    private struct APIURLs {
        /// URL for getting static information about dining location
        static let diningLocations = URL(string: "https://eecs183.org/api/menus/v1/diningLocations.json")!
        /// URL for getting occupancy information about dining locations
        static let occupancy = URL(string: "https://mobile.its.umich.edu/michigan/services/dining/shallowDiningHallGroups?_type=json")!
        /// Returns URL for getting menus for specified dining location on a given date
        static func menusURL(for diningLocation: DiningLocation, on date: Date) -> URL {
            let baseURLString = "http://api.studentlife.umich.edu/menu/xml2print.php"

            let escapedID = diningLocation.id.addingPercentEncoding(withAllowedCharacters: CharacterSet.urlQueryAllowed)!

            let formatter = DateFormatter()
            formatter.dateFormat = "YYYY-MM-dd"
            let stringDate = formatter.string(from: date)

            let urlString = "\(baseURLString)?controller=print&view=json&location=\(escapedID)&date=\(stringDate)"
            return URL(string: urlString)!
        }
    }


    /**
     Simplifies access to APIs.

     Gets data at the specified `url` and converts it to `JSON`,
     /// calling `completionHandler` when finished.

     This is a *class* function that must be called on the `MenusAPIManager` class,
     and not on an instance of the class.

     - important:
     This is an *asynchronous* function that calls `completionHandler`
     when data is fetched from the API.

     - note:
     This function calls `completionHandler` from a non-main thread.

     - parameter url: a URL that will be used to get the data.

     - parameter completionHandler: a function that will execute once the data is
     retrieved from the API.
     This function will be called with one argument of type `JSON`.


     **See also**

     [SwiftyJSON](https://github.com/SwiftyJSON/SwiftyJSON)
     */
    private class func fetch(url: URL, completionHandler: @escaping ((JSON?) -> Void)) {

        // get off the main queue to avoid blocking rendering of UI
        DispatchQueue.global(qos: .default).async {
            // let request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: 60.0)
            // let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            let task = URLSession.shared.dataTask(with: url) { (data, response, error) in
                if error != nil {
                    print(error!)
                    completionHandler(nil)
                } else {
                    if data != nil {
                        let json = JSON(data: data!)
                        completionHandler(json)
                    } else {
                        completionHandler(nil)
                    }
                }
            }
            task.resume()
        }
    }
}


// MARK: - Extensions

// filtering out nil values
// http://stackoverflow.com/questions/28190631/creating-an-extension-to-filter-nils-from-an-array-in-swift
protocol OptionalType {
    associatedtype Wrapped
    func map<U>(_ f: (Wrapped) throws -> U) rethrows -> U?
}

extension Optional: OptionalType {}

extension Sequence where Iterator.Element: OptionalType {
    func removeNils() -> [Iterator.Element.Wrapped] {
        var result: [Iterator.Element.Wrapped] = []
        for element in self {
            if let element = element.map({ $0 }) {
                result.append(element)
            }
        }
        return result
    }
}

// dates
// based on http://stackoverflow.com/questions/28016578/swift-how-to-create-a-date-time-stamp-and-format-as-iso-8601-rfc-3339-utc-tim
extension Date {
    static let iso8601Formatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.calendar = Calendar(identifier: .iso8601)
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.timeZone = TimeZone(secondsFromGMT: 0)
        formatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ssXXXXX"
        return formatter
    }()
    var iso8601: String {
        return Date.iso8601Formatter.string(from: self)
    }
}

extension String {
    var dateFromISO8601: Date? {
        return Date.iso8601Formatter.date(from: self)
    }
}
