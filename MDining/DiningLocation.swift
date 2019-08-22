//
//  DiningLocation.swift
//  DiningMenus
//
//  Created by Maxim Aleksa on 3/13/17.
//  Copyright © 2017 Maxim Aleksa. All rights reserved.
//

import Foundation
import CoreLocation


// MARK: - DiningLocation class

/**
 This class represents a dining location on campus (e.g., Java Blue café in East Quad
 or East Quad Dining Hall).
 */
public class DiningLocation: NSObject, NSCoding {

    // MARK: Nested Types

    /**
     This enumeration represents the type of dining location, such as café, dining hall or market.
    */
    public enum DiningLocationType: Int {

        // MARK: Enumeration Cases

        /**
         A café, such as Bert's Café in the UGLi or JavaBlu.

         **See also**

         [dining.umich.edu/menus-locations/cafes/](http://dining.umich.edu/menus-locations/cafes/)
        */
        case cafe

        /**
         A dining hall, such as South Quad Dining Hall.

         **See also**

         [dining.umich.edu/menus-locations/dining-halls/](http://dining.umich.edu/menus-locations/dining-halls/)
        */
        case diningHall

        /**
         A market (convenience store), such as Blue Apple or U-GO's.

         **See also**

         [dining.umich.edu/menus-locations/markets/](http://dining.umich.edu/menus-locations/markets/)
        */
        case market
    }

    /**
     This struct represents the address of a dining location.
    */
    public struct Address: CustomStringConvertible {

        // MARK: Instance Properties

        /// Street component of the address.
        public let street: String
        /// City component of the address.
        public let city: String
        /// State component of the address.
        public let state: String
        /// ZIP code of the address.
        public let zip: String
        /// Full address string, such as `"701 East University Ann Arbor MI 48109"`.
        public var fullAddress: String {
            return "\(street) \(city) \(state) \(zip)"
        }
        /// A string representation of the dining location object, same as `fullName`.
        public var description: String {
            return fullAddress
        }
    }


    // MARK: Instance Properties

    /// Name of dining location (e.g., `"South Quad Dining Hall"`)
    public let name: String

    /// ID of dining location, used to uniquely identify it
    /// (e.g., in an API request or when saving favorites).
    public let id: String

    /// Address of dining location.
    public let address: Address

    /// Geographical coordinate of dining location.
    public let coordinate: CLLocationCoordinate2D

    /// Type of dining location (`.cafe`, `.diningHall` or `.market`).
    public let type: DiningLocationType

    /**
     Regular open hours of this dining location, represented as an array of strings,
     where each string is a new line of text.

     For example, the `hours` array could be

     ````
     [
         "Monday-Friday",
         "7:00 AM – 10:00 AM",
         "11:00 AM – 2:00 PM",
         "5:00 PM – 8:00 PM",
         "Saturday-Sunday",
         "Closed"
     ]
     ````

     - note: These are *regular* open hours of the dining location. In order to get
     actual hours that include special events and holidays,
     call one of the two `getHours` class functions of the `MenusAPIManager` class.
    */
    public let hours: [String]

    /**
     Regular open hours of this dining location, represented as an array of arrays of strings,
     where the outer array has elements that represent each day of the week
     (element at index 0 is dictionary corresponding to Sunday).

     Each element is an array that has hours for that specific day of the week.

     For example, the `hoursByWeekday` array of arrays of strings could be

     ````
     [
         [],
         [
             "Breakfast: 7:00 AM - 10:00 AM",
             "Lunch: 11:00 AM – 2:00 PM",
             "Dinner: 5:00 PM – 8:00 PM"
         ],
         [
             "Breakfast: 7:00 AM - 10:00 AM",
             "Lunch: 11:00 AM – 2:00 PM",
             "Dinner: 5:00 PM – 8:00 PM"
         ],
         ...
         [],
     ]
     ````

     - note: These are *regular* open hours of the dining location. In order to get
     actual hours that include special events and holidays,
     call one of the two `getHours` class functions of the `MenusAPIManager` class.
    */
    public let hoursByWeekday: [[String]]

    /// Contact phone number for this dining location.
    public let contactPhone: String?

    /// Contact email address for this dining location.
    public let contactEmail: String?

    /**
     Capacity of this dining location.

     - note: Not all dining locations have provide a capacity.
     In cases where this information is not available, `capacity` is `nil`.
    */
    public var capacity: Int?

    /**
     Current occupancy of this dining location.

     - note: Not all dining locations have provide a capacity,
     and it is usually available only when the dining location is open.
     In cases where this information is not available, `currentOccupancy` is `nil`.
    */
    public var currentOccupancy: Int?

    /// A string representation of the dining location object, same as `name`.
    override public var description: String {
        return self.name
    }


    // MARK: Initializers

    init(name: String, id: String, address: Address, coordinate: CLLocationCoordinate2D, type: DiningLocationType, hours: [String], hoursByWeekday: [[String]], contactPhone: String? = nil, contactEmail: String? = nil, capacity: Int? = nil, currentOccupancy: Int? = nil) {
        self.name = name
        self.id = id
        self.address = address
        self.coordinate = coordinate
        self.type = type
        self.hours = hours
        self.hoursByWeekday = hoursByWeekday
        self.contactPhone = contactPhone
        self.contactEmail = contactEmail
        self.capacity = capacity
        self.currentOccupancy = currentOccupancy

        super.init()
    }

    convenience init?(json: JSON) {
        if let name = json["name"].string,
            let id = json["id"].string,
            let state = json["address"]["state"].string,
            let city = json["address"]["city"].string,
            let street = json["address"]["street"].string,
            let zip = json["address"]["zip"].string,
            let latitude = json["coordinate"]["latitude"].double,
            let longitude = json["coordinate"]["longitude"].double,
            let typeString = json["type"].string {

            var type: DiningLocation.DiningLocationType
            if typeString == "cafe" {
                type = .cafe
            } else if typeString == "market" {
                type = .market
            } else {
                type = .diningHall
            }

            let address = DiningLocation.Address(street: street, city: city, state: state, zip: zip)
            let coordinate = CLLocationCoordinate2D(latitude: latitude, longitude: longitude)

            var hours = [String]()
            if let jsonHours = json["hours"].array {
                for jsonHour in jsonHours {
                    if let hourString = jsonHour.string {
                        hours.append(hourString)
                    }
                }
            }

            var hoursByWeekday = [[String]]()
            if let jsonDays = json["hoursByWeekday"].array {
                for jsonDay in jsonDays {
                    var hoursForDay = [String]()
                    for jsonHours in jsonDay.arrayValue {
                        if let hours = jsonHours.string {
                            hoursForDay.append(hours)
                        }
                    }
                    hoursByWeekday.append(hoursForDay)
                }
                // verify count
                if hoursByWeekday.count != 7 {
                    // if there are not seven entries, create 7 empty entries
                    hoursByWeekday = Array<Array<String>>(repeating: [], count: 7)
                }
            }

            let contactPhone = json["contact"]["phone"].string
            let contactEmail = json["contact"]["email"].string

            let capacity = json["capacity"].int

            self.init(name: name, id: id, address: address, coordinate: coordinate, type: type, hours: hours, hoursByWeekday: hoursByWeekday, contactPhone: contactPhone, contactEmail: contactEmail, capacity: capacity)
        } else {
            return nil
        }
    }


    // MARK: NSCoding

    private struct PropertyKey {
        static let name = "name"
        static let id = "id"
        static let addressStreet = "addressStreet"
        static let addressCity = "addressCity"
        static let addressState = "addressState"
        static let addressZip = "addressZip"
        static let latitude = "latitude"
        static let longitude = "longitude"
        static let type = "type"
        static let hours = "hours"
        static let hoursByWeekday = "hoursByWeekday"
        static let contactPhone = "contactPhone"
        static let contactEmail = "contactEmail"
        static let capacity = "capacity"
    }

    public func encode(with aCoder: NSCoder) {
        aCoder.encode(name, forKey: PropertyKey.name)
        aCoder.encode(id, forKey: PropertyKey.id)
        aCoder.encode(address.street, forKey: PropertyKey.addressStreet)
        aCoder.encode(address.city, forKey: PropertyKey.addressCity)
        aCoder.encode(address.state, forKey: PropertyKey.addressState)
        aCoder.encode(address.zip, forKey: PropertyKey.addressZip)
        aCoder.encode(coordinate.latitude, forKey: PropertyKey.latitude)
        aCoder.encode(coordinate.longitude, forKey: PropertyKey.longitude)
        aCoder.encode(type.rawValue, forKey: PropertyKey.type)
        aCoder.encode(hours, forKey: PropertyKey.hours)
        aCoder.encode(hoursByWeekday, forKey: PropertyKey.hoursByWeekday)
        aCoder.encode(contactPhone, forKey: PropertyKey.contactPhone)
        aCoder.encode(contactEmail, forKey: PropertyKey.contactEmail)
        aCoder.encode(capacity, forKey: PropertyKey.capacity)
    }

    required public convenience init?(coder aDecoder: NSCoder) {
        let typeRaw = aDecoder.decodeInteger(forKey: PropertyKey.type)

        guard let name = aDecoder.decodeObject(forKey: PropertyKey.name) as? String,
            let id = aDecoder.decodeObject(forKey: PropertyKey.id) as? String,
            let addressStreet = aDecoder.decodeObject(forKey: PropertyKey.addressStreet) as? String,
            let addressCity = aDecoder.decodeObject(forKey: PropertyKey.addressCity) as? String,
            let addressState = aDecoder.decodeObject(forKey: PropertyKey.addressState) as? String,
            let addressZip = aDecoder.decodeObject(forKey: PropertyKey.addressZip) as? String,
            let type = DiningLocationType.init(rawValue: typeRaw),
            let hours = aDecoder.decodeObject(forKey: PropertyKey.hours) as? [String],
            let hoursByWeekday = aDecoder.decodeObject(forKey: PropertyKey.hoursByWeekday) as? [[String]] else {
                return nil
        }

        let address = Address(street: addressStreet, city: addressCity, state: addressState, zip: addressZip)
        let latitude = aDecoder.decodeDouble(forKey: PropertyKey.latitude)
        let longitude = aDecoder.decodeDouble(forKey: PropertyKey.longitude)
        let coordinate = CLLocationCoordinate2D(latitude: latitude, longitude: longitude)

        let contactPhone = aDecoder.decodeObject(forKey: PropertyKey.contactPhone) as? String
        let contactEmail = aDecoder.decodeObject(forKey: PropertyKey.contactEmail) as? String
        
        let capacity = aDecoder.decodeObject(forKey: PropertyKey.capacity) as? Int

        self.init(name: name, id: id, address: address, coordinate: coordinate, type: type, hours: hours, hoursByWeekday: hoursByWeekday, contactPhone: contactPhone, contactEmail: contactEmail, capacity: capacity)
    }
}
