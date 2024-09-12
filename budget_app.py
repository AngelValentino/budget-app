import math

class Category:
    def __init__(self, type):
        # Initialize a Category with a given type (e.g., 'Food', 'Entertainment')
        self.type = type
        # List to store ledger entries {'amount': amount, 'description': description}
        self.ledger = []
        # Total category balance
        self.balance = 0
        # Total category spend
        self.total_spend = 0

    def __str__(self):
        # Center categroy title between asterisks at max 30 characters
        title = f'{self.type:*^30}\n' 
        assets = ''

        # Format each entry in the ledger
        for asset in self.ledger:
            # Format the description (max 23 characters) and amount 
            # right-aligned (max 7 character) with 2 decimal places
            assets += f"{asset['description'][0:23]:23}" + f"{asset['amount']:>7.2f}\n"

        # Append the total balance to the formatted output
        formatted_balance = title + assets + f'Total: {self.get_balance()}'

        return formatted_balance

    def deposit(self, amount, description = ''):
        # Add a record of the transaction to the ledger
        self.ledger.append({'amount': amount, 'description': description})
        # Add the amount to the the current balance
        self.balance += amount

    def withdraw(self, amount, description = ''):
        # Attempt to withdraw funds; return False if insufficient funds
        if not self.check_funds(amount):
            print('insufficent funds')
            return False
        
        # Add a record of the transaction to the ledger
        self.ledger.append({'amount': -amount, 'description': description})
        # Deduct the amount from the current balance
        self.balance -= amount
        # Add to the amount to the total_spend variable
        self.total_spend += amount
     
        return True

    def get_balance(self):
        # Return the current balance rounded to 2 decimal places
        return round(self.balance, 2)

    def check_funds(self, amount):
        # Check if there are sufficient funds to cover the requested amount
        if amount > self.get_balance():
            return False
        return True

    def transfer(self, amount, target_category):
        # Attempt to transfer funds to another category
        if not self.check_funds(amount):
            # Rturnn false if there are not enough funds
            print('insufficent funds')
            return False
        # Withdraw the amount from the current category
        self.withdraw(amount, f'Transfer to {target_category.type}')
        # Deposit the amount into the target category
        target_category.deposit(amount, f'Transfer from {self.type}')
        
        return True

    def get_withdraws(self):
        return round(self.total_spend, 2)
        

food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
print(food, food.get_withdraws())

clothing = Category('Clothing')
clothing.deposit(1000, 'deposit')
clothing.withdraw(70, 'Polo shirt')
clothing.withdraw(120, 'Sports jacket')
clothing.transfer(20, food)
print(clothing, clothing.get_withdraws())

auto = Category('Auto')
auto.deposit(20000, 'deposit')
auto.withdraw(400, 'Custom Cafe Racer Motorcycle parts')
print(auto, auto.get_withdraws())

def create_spend_chart(categories):
    total_sepend = 0
    category_spend = {}

    # Get the total spend in all categories
    for category in categories:
        total_sepend += category.get_withdraws()

    # Get what each cateogoty has spend compared to the others
    # (single category amount spent) / (total spent across all categories)
    for category in categories:
        # Make a dicitionary entry containing the ammount in percentatge the cateogry has spent
        # floored to the nearrest 10 => 58 becomes 50
        category_spend[category.type] = math.floor(int((category.get_withdraws() / total_sepend) * 100) / 10) * 10

    print(category_spend)

    #TODO Create spend chart


create_spend_chart([food, clothing, auto])