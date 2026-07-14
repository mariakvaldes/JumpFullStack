
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

//Admin credentials: admin, admin123
//User credentials: .....................
public class Runner {

    static Scanner sc = new Scanner(System.in);

    static List<User> users = new ArrayList<>();

    static {
        User admin = new Admin();
        admin.setUsername("admin");
        admin.setPassword("admin123");

        User customer1 = new Customer();
        customer1.setUsername("rohit");
        customer1.setPassword("rohit123");
        ((Customer)customer1).addAccount(new CheckingAccount(91));

        User customer2 = new Customer();
        customer2.setUsername("mohit");
        customer2.setPassword("mohit123");
        ((Customer)customer2).addAccount(new CheckingAccount(19));
        ((Customer)customer2).addAccount(new SavingsAccount(56));

        User customer3 = new Customer();
        customer3.setUsername("shobhit");
        customer3.setPassword("shobhit123");

        users.add(admin);
        users.add(customer1);
        users.add(customer2);
        users.add(customer3);

    }

    public static void main(String[] args) {
        printMessage("Welcome to ABC Digital Bank");

        boolean flag = true;
        while (flag) {
            String loginResult = login();

            if (loginResult.equals("invalid")) {
                //exception-handling
                System.out.println("Invalid Credentials");
            } else if (loginResult.equals("admin")) {
                adminDashboard(loginResult);
            } else {
                customerDashboard(loginResult);
            }

            System.out.println("Do you want to continue? Press y/n");
            String mainLoopUserResponse = sc.nextLine();
            if (mainLoopUserResponse.equalsIgnoreCase("n")) {
                flag = false;
            }
        }

    }

    private static void customerDashboard(String username) {
        // System.out.println("Welcome customer, " + username);
        //todo: using switch-case present customer options'
        //view his account or accounts, withdraw, transfer, deposit

        System.out.println("Welcome customer, " + username + "!");
        int userChoice = 0;

        Customer customer = findCustomerByUsername(username);

        do {
            System.out.println("\n===== Customer Dashboard =====");
            System.out.println("1. View My Account(s)");
            System.out.println("2. Deposit Money");
            System.out.println("3. Withdraw Money");
            System.out.println("4. Transfer Between My Accounts");
            System.out.println("5. Logout");
            System.out.print("Enter your choice: ");

            String input = sc.nextLine();

            try {
                userChoice = Integer.parseInt(input);
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
                continue;
            }

            switch (userChoice) {
                case 1:
                    viewMyAccounts(customer);
                    break;

                case 2:
                    depositMoney(customer);// Deposit money into one of the customer's accounts
                    break;

                case 3:
                    withdrawMoney(customer);// Withdraw money from one of the customer's accounts
                    break;

                case 4:
                    transferMoney(customer);// Transfer money between the customer's own accounts
                    break;

                case 5:
                    System.out.println("Logging out...");
                    break;

                default:
                    System.out.println("Invalid choice.");
            }

        } while (userChoice != 5);

    }

    private static void depositMoney(Customer customer) {
        System.out.print("Enter Account ID to deposit into: ");
        int id = Integer.parseInt(sc.nextLine());
        
        for (Account acc : customer.getAccounts()) {
            if (acc.getId() == id) {
                System.out.print("Enter amount to deposit: ");
                double amount = Double.parseDouble(sc.nextLine());
                acc.deposit(amount);
                System.out.println("Successfully deposited $" + amount + ". New balance: $" + acc.getBalance());
                return;
            }
        }
        System.out.println("Account not found.");
    }

    private static void withdrawMoney(Customer customer) {
        System.out.print("Enter Account ID to withdraw from: ");
        int id = Integer.parseInt(sc.nextLine());
        
        for (Account acc : customer.getAccounts()) {
            if (acc.getId() == id) {
                System.out.print("Enter amount to withdraw: ");
                double amount = Double.parseDouble(sc.nextLine());
                acc.withdraw(amount);
                System.out.println("Withdrawal attempted. New balance: $" + acc.getBalance());
                return;
            }
        }
        System.out.println("Account not found.");
    }

    private static void transferMoney(Customer customer) {
        System.out.print("Enter Source Account ID: ");
        int fromId = Integer.parseInt(sc.nextLine());
        System.out.print("Enter Destination Account ID: ");
        int toId = Integer.parseInt(sc.nextLine());
        
        Account source = null;
        Account dest = null;
        
        for (Account acc : customer.getAccounts()) {
            if (acc.getId() == fromId) source = acc;
            if (acc.getId() == toId) dest = acc;
        }
        
        if (source != null && dest != null) {
            System.out.print("Enter amount to transfer: ");
            double amount = Double.parseDouble(sc.nextLine());
            source.transfer(dest, amount);
            System.out.println("Transfer complete.");
        } else {
            System.out.println("One or both accounts not found.");
        }
    }

    private static void adminDashboard(String loginResult) {
        System.out.println("Welcome admin");
        int userChoice = 0;

        do {
            System.out.println("\n===== Admin Dashboard =====");
            System.out.println("1. View Customer(s)");
            System.out.println("2. View Customer Account(s)");
            System.out.println("3. Delete Customer(s)");
            System.out.println("4. Delete Accounts");
            System.out.println("5. Create Account");
            System.out.println("6. Logout");
            System.out.print("Enter your choice: ");

            String input = sc.nextLine();

            try {
                userChoice = Integer.parseInt(input);
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
                continue;
            }

            switch (userChoice) {
                case 1:
                    viewCustomers();
                    break;

                case 2:
                    viewAllCustomerAccounts();
                    break;

                case 3:
                    deleteCustomer();
                    break;

                case 4:
                    deleteAccount();
                    break;

                case 5:
                    createAccountForCustomer();
                    break;

                case 6:
                    System.out.println("Logging out...");
                    break;

                default:
                    System.out.println("Invalid choice.");
            }

        } while (userChoice != 6);
    }

    static String login() {
        String loginType = "invalid";
        System.out.println("Please enter your username and password separated by a space");//rohit rohit123
        //validation
        String enteredUsernamePassword = sc.nextLine();
        String[] parts = enteredUsernamePassword.split(" ");
        String enteredUsername = parts[0];
        String enteredPassword = parts[1];

        if (enteredUsername.equals("admin") && enteredPassword.equals("admin123")) {
            loginType = "admin";
        } else {
            Customer user = findCustomerByUsername(enteredUsername);
        
            if (user != null && enteredPassword.equals(user.getPassword())) {
                loginType = user.getUsername();
            }
        }

        return loginType;
    }

    private static Customer findCustomerByUsername(String username) {
        for (User u : users) {
            if (u instanceof Customer && u.getUsername().equalsIgnoreCase(username)) {
                return (Customer) u;
            }
        }
        return null; // Return null if not found
    }

    // 1. View all customers
    private static void viewCustomers() {
        System.out.println("\n--- All Customers ---");
        for (User u : users) {
            if (u instanceof Customer) {
                System.out.println("Username: " + u.getUsername());
            }
        }
    }

    // 2. View all customer accounts (only for those who have at least one)
    private static void viewAllCustomerAccounts() {
        System.out.println("\n--- All Customer Accounts ---");
        boolean anyAccountsFound = false;
    
        for (User u : users) {
            if (u instanceof Customer) {
                Customer c = (Customer) u;
                if (c.getAccounts() != null && !c.getAccounts().isEmpty()) {
                    anyAccountsFound = true;
                    System.out.println("Customer: " + c.getUsername());
                    printAccountList(c.getAccounts());
                }
            }
        }
    
        if (!anyAccountsFound) {
            System.out.println("No customer accounts found in the system.");
        }
    }

    private static void viewMyAccounts(Customer c) {
        System.out.println("\n--- My Accounts ---");
        List<Account> accounts = c.getAccounts();
        
        if (accounts == null || accounts.isEmpty()) {
            System.out.println("You currently have no accounts.");
        } else {
            printAccountList(accounts);
        }
    }

    private static void printAccountList(List<Account> accounts) {
        for (Account acc : accounts) {
            System.out.println("  - Account ID: " + acc.getId() + " | Balance: $" + acc.getBalance());
        }
    }

    // 3. Delete a customer
    private static void deleteCustomer() {
        System.out.print("Enter username to delete: ");
        String username = sc.nextLine();
        // Using the return value to confirm if the deletion was successful
        boolean wasRemoved = users.removeIf(u -> u.getUsername().equalsIgnoreCase(username));

        if (wasRemoved) {
            System.out.println("Customer '" + username + "' deleted successfully.");
        } else {
            System.out.println("Customer not found. No changes made.");
        }
    }

    // 4. Delete an account
    private static void deleteAccount() {
        System.out.print("Enter account ID to delete: ");
        String input = sc.nextLine();
        int id;

        try {
            id = Integer.parseInt(input);
        } catch (NumberFormatException e) {
            System.out.println("Invalid ID format.");
            return;
        }

        boolean foundAndDeleted = false;

        for (User u : users) {
            if (u instanceof Customer) {
                Customer customer = (Customer) u;

                // Check if accounts list is not null and not empty
                if (customer.getAccounts() != null && !customer.getAccounts().isEmpty()) {
                    // removeIf returns true if any element was removed
                    if (customer.getAccounts().removeIf(a -> a.getId() == id)) {
                        foundAndDeleted = true;
                        break; // Account IDs are unique, no need to keep searching
                    }
                }
            }
        }

        if (foundAndDeleted) {
            System.out.println("Account " + id + " deleted successfully.");
        } else {
            System.out.println("Account not found or customer has no accounts.");
        }
    }

    private static void createAccountForCustomer() {
        System.out.print("Enter existing customer username: ");
        String username = sc.nextLine();

        // 1. Locate the customer
        Customer targetCustomer = null;
        for (User u : users) {
            if (u instanceof Customer && u.getUsername().equalsIgnoreCase(username)) {
                targetCustomer = (Customer) u;
                break;
            }
        }

        // 2. Validate existence
        if (targetCustomer == null) {
            System.out.println("Error: Customer '" + username + "' not found. Cannot create account.");
            return;
        }

        // 3. Prompt for account details
        System.out.println("Select Account Type for " + targetCustomer.getUsername() + ":");
        System.out.println("1. Savings Account");
        System.out.println("2. Checking Account");
        System.out.print("Choice: ");
        String typeChoice = sc.nextLine();

        System.out.print("Enter Initial Deposit Amount: ");
        double amount;
        try {
            amount = Double.parseDouble(sc.nextLine());
        } catch (NumberFormatException e) {
            System.out.println("Invalid amount. Operation cancelled.");
            return;
        }

        // 4. Create the specific account
        if (typeChoice.equals("1")) {
            targetCustomer.addAccount(new SavingsAccount(amount));
            System.out.println("Savings Account created successfully.");
        } else if (typeChoice.equals("2")) {
            targetCustomer.addAccount(new CheckingAccount(amount));
            System.out.println("Checking Account created successfully.");
        } else {
            System.out.println("Invalid account type. Operation cancelled.");
        }
    }

    static void printMessage(String message) {
        System.out.println(message);
    }
}

class Bank {

    private int id;
    private String name;
    private List<Customer> customers = new ArrayList<>();

    public Bank(int id, String name, List<Customer> customers) {
        this.id = id;
        this.name = name;
        this.customers = customers;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<Customer> getCustomers() {
        return customers;
    }

    public void setCustomers(List<Customer> customers) {
        this.customers = customers;
    }
}

abstract class User {

    private String username;
    private String password;

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    abstract String getUserType();
}

class Admin extends User {

    String getUserType() {
        return "admin";
    }
}

class Customer extends User {

    // A customer has a list of accounts
    private List<Account> accounts = new ArrayList<>();

    String getUserType() {
        return "customer";
    }

    public List<Account> getAccounts() {
        return accounts;
    }

    public void addAccount(Account account) {
        this.accounts.add(account);
    }

}

abstract class Account {

    private static int idCounter = 1000; // Starting ID
    private int id;
    private double balance;

    public Account(double balance) {
        this.id = idCounter++; // Assign current counter and then increment
        this.balance = balance;
    }

    public int getId() {
        return id;
    }

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }

    public abstract void deposit(double amount);
    public abstract void withdraw(double amount);
    public abstract void transfer(Account target, double amount);
}

class CheckingAccount extends Account implements AccountOperations {

    public CheckingAccount(double balance) {
        super(balance);
    }

    @Override
    public void deposit(double amount) {
        setBalance(getBalance() + amount);
    }

    @Override
    public void withdraw(double amount) {
        if (getBalance() >= amount) {
            setBalance(getBalance() - amount);
        } else {
            System.out.println("Insufficient funds.");
        }
    }

    @Override
    public void transfer(Account target, double amount) {
        if (getBalance() >= amount) {
            withdraw(amount);
            target.deposit(amount);
        } else {
            System.out.println("Insufficient funds for transfer.");
        }
    }

    public double getInterestRate() {
        return 0.01; // 1%
    }
}

class SavingsAccount extends Account implements AccountOperations {

    public SavingsAccount(double balance) {
        super(balance);
    }

    @Override
    public void deposit(double amount) {
        setBalance(getBalance() + amount);
    }

    @Override
    public void withdraw(double amount) {
        // Example: Savings might require a minimum balance or have different rules
        if (getBalance() >= amount) {
            setBalance(getBalance() - amount);
        } else {
            System.out.println("Insufficient funds.");
        }
    }

    @Override
    public void transfer(Account target, double amount) {
        if (getBalance() >= amount) {
            withdraw(amount);
            target.deposit(amount);
        } else {
            System.out.println("Insufficient funds for transfer.");
        }
    }

    public double getInterestRate() {
        return 0.02; // 2%
    }
}

interface AccountOperations {
    void deposit(double amount);
    void withdraw(double amount);
    void transfer(Account target, double amount);
}
