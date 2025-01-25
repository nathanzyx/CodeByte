package com.microsoft.azure;

import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
// Import the Scanner class to read text files
import java.util.*;

class Catalog {
    static List<Map<String, String>> list = new ArrayList<>();

    public static void selectItem(String itemElement, String itemName) {
        // Iterate through each map in the list
        for (Map<String, String> map : list) {
            // Check if the map contains the specific element (key)
            if (map.containsKey(itemElement)) {
                // If the value associated with the key matches the itemName, print the map
                if (map.get(itemElement).equals(itemName)) {
                    System.out.println(map);
                }
            }
        }
    }

    public static void readCatalog() {
        System.out.println("Working directory: " + System.getProperty("user.dir"));
        readContents("info.csv", list);

        // Print out each read element
        for (Map<String, String> map : list) {
            System.out.println(map);
        }

    }

    static boolean firstRead = true;

    public static void readContents(String fileName, List<Map<String, String>> list) {
        int lineNum = 1; // Current line being read
        String[] elements = {}; // Array for element names (ex. name, id, age)

        if (!firstRead) {
            return;
        } else {
            firstRead = false;
        }

        try {
            File file = new File(fileName);
            Scanner reader = new Scanner(file);
            while (reader.hasNextLine()) {
                // Each 'data' represents a line in the csv file
                String data = reader.nextLine();

                //Parse Line into a string
                String[] parsedData = data.split(",");

                if (lineNum == 1) { // First line is saved as elements
                    elements = parsedData;

                } else {
                    Map<String, String> map = new HashMap<>();
                    // Add each parsed element to the map
                    for (int i = 0; i < parsedData.length; i++) {
                        map.put(elements[i], parsedData[i]);
                    }
                    // Add map to list
                    list.add(map);
                }
                //Store data into usable format (list of dictionaries)
                lineNum++;
            }
            reader.close();
//            firstRead = false;
        } catch (FileNotFoundException e) {
            System.out.println("Error in reading file");
            e.printStackTrace();
        }
    }

    public static void addToCatalog() {
        Scanner scanner = new Scanner(System.in);
        Map<String, String> newItem = new HashMap<>();

        // Get field names from the first item in the list
        if (list.isEmpty()) {
            System.out.println("Catalog is empty. Cannot determine fields for the new item.");
            return;
        }
        String[] fields = list.get(0).keySet().toArray(new String[0]);

        // Prompt user for each field
        for (String field : fields) {
            System.out.print("Enter " + field + ": ");
            String value = scanner.nextLine().trim();

            // Basic validation to ensure the field is not empty
            if (value.isEmpty()) {
                System.out.println(field + " cannot be empty. Aborting item addition.");
                return;
            }
            newItem.put(field, value);
        }

        // Add the new item to the catalog list
        list.add(newItem);
        System.out.println("Item added successfully!");
    }

}

//    private static void appendToCSV(Map<String, String> newItem) {
//
//    }
//}