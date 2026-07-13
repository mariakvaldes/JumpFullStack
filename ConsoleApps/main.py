# Parent class for all users, stores common information shared by Admin and Customer

class User:

    # creates a new user with username and password
    def __init__(self, username, password):
        self.username = username
        self.password = password


    # returns the type of user, child classes will override this
    def get_user_type(self):
        return "User"



# Admin inherits from User, TODO: Admin will later manage customers
class Admin(User):

    # Returns Admin role
    def get_user_type(self):
        return "Admin"



# Customer inherits from User, customers can own multiple bank accounts
class Customer(User):

    # Creates a customer
    def __init__(self, username, password):

        # Initialize username/password from User
        super().__init__(username, password)

        # Store customer accounts
        self.accounts = []


    # Returns Customer role
    def get_user_type(self):
        return "Customer"



# bank account
class Account:

    # Used to automatically generate account numbers
    account_counter = 1000


    # Creates a new account
    def __init__(self, account_type):

        # Increase account number
        Account.account_counter += 1

        # Store account information
        self.account_number = Account.account_counter
        self.account_type = account_type
        self.balance = 0
        self.transactions = []



# Testing objects
if __name__ == "__main__":

    admin = Admin("admin", "admin123")

    customer = Customer("rohit", "rohit123")

    account = Account("Checking")


    print(admin.username)
    print(admin.get_user_type())

    print(customer.username)
    print(customer.get_user_type())

    print(account.account_number)
    print(account.account_type)
