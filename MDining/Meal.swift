//
//  Meal.swift
//  DiningMenus
//
//  Created by Maxim Aleksa on 3/13/17.
//  Copyright © 2017 Maxim Aleksa. All rights reserved.
//

import Foundation


// MARK: - Meal class

/**
 This class represents a meal of the day (breakfast, lunch, dinner).
 */
public class Meal: CustomStringConvertible {

    // MARK: Nested Types

    /**
     This enumeration represents type of meal (breakfast, lunch transition,
     lunch, dinner transition, dinner or other).
    */
    public enum MealType: String {

        // MARK: Enumeration Cases

        /// Represents breakfast.
        case breakfast = "Breakfast"
        /// Represents lunch transition, served by some dining halls between breakfast and lunch.
        case lunchTransition = "Lunch Transition"
        /// Represents lunch or brunch.
        case lunch = "Lunch"
        /// Represents dinner transition, served by some dining halls between lunch and dinner.
        case dinnerTransition = "Dinner Transition"
        /// Represents dinner.
        case dinner = "Dinner"
        /// This meal type groups menu items that are not directly related
        /// to other meals (e.g., salad bar).
        case other = "Other"
    }


    // MARK: Instance properties

    /// Type of meal (e.g., breakfast, dinner, etc.).
    public let type: MealType

    /// Array of courses for this meal.
    /// `courses` is `nil` if this meal is not served.
    public let courses: [Course]?

    /// A notice message informing the user about this meal
    /// (e.g., that this meal is not being served today).
    /// `message` is `nil` if there is no notice message for this meal.
    public let message: String?

    /// A string representation of the meal object,
    /// same as the string associated with the `type`.
    public var description: String {
        return self.type.rawValue
    }

    // MARK: Initializers

    init(type: MealType, courses: [Course]?, message: String? = nil) {
        self.type = type
        self.courses = courses
        self.message = message
    }
}
