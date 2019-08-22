//
//  Course.swift
//  DiningMenus
//
//  Created by Maxim Aleksa on 3/13/17.
//  Copyright © 2017 Maxim Aleksa. All rights reserved.
//

import Foundation


// MARK: - Course class

/**
 This class represents a category of menu items or a food station (e.g., 24 Carrots).
 */
public class Course: CustomStringConvertible {

    // MARK: Instance Properties

    /// Name of the course (e.g., `"24 Carrots"`).
    public let name: String

    /// Array of menu items for this course.
    public let menuItems: [MenuItem]

    /// A string representation of the course location object, same as `name`.
    public var description: String {
        return self.name
    }


    // MARK: Initializers

    init(name: String, menuItems: [MenuItem]) {
        self.name = name
        self.menuItems = menuItems
    }
}
