package project;

import java.util.*;

public class Start {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean running = true;

        while(running) {
            printMenu();

            String userInput = scanner.nextLine();
            switch (userInput) {
                case "1":
                    // Call function to read intput
                    Catalog.readCatalog();
                    break;
                case "2":
                    System.out.println("Enter item element");
                    String itemElement = scanner.nextLine();
                    System.out.println("Enter item elements name");
                    String itemName = scanner.nextLine();

                    // Call function to read intput
                    Catalog.selectItem(itemElement, itemName);
                    break;
                case "3":
                    // Call function to read intput
                    Catalog.addToCatalog();
                    break;
                case "4":
                    break;

                case "5":
                    running = false;
                    System.out.println("Exiting program.");
                    break;
                default:
                    System.out.println("Invalid choice. Enter a correct option.");
            }
        }


    }

    static void printMenu() {
        System.out.println("---Main Menu---");
        System.out.println("1: Display Catalog");
        System.out.println("2: Select Item From Catalog");
        System.out.println("3: Add to Database");
        System.out.println("4: Edit Database");
        System.out.println("5: Save and Exit");
        System.out.print("Choose an Option: ");
    }
}
