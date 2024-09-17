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
        

food = Category('Business')
food.deposit(1000, 'deposit')
food.withdraw(5, 'groceries')

clothing = Category('Food')
clothing.deposit(1000, 'deposit')
clothing.withdraw(140, 'Polo shirt')

auto = Category('Entertainment')
auto.deposit(20000, 'deposit')
auto.withdraw(40, 'Custom Cafe Racer Motorcycle parts')


def create_spend_chart(categories):
    total_sepend = 0
    category_spend = {}
    formatted_chart = 'Percentage spent by category\n'

    def check_category_bar(category_bar, current_bar):
        # If the category bar is larger or equal to the current bar print 'o'
        if category_bar >= current_bar:
            return 'o'
        # Else return a space
        return ' '
        
    def check_categories_bar_chart(bar):
        formatted_categories_bars = ''

        for category in category_spend:
            # Print 'o' character as bars
            formatted_categories_bars += check_category_bar(category_spend[category], bar) + '  '
        
        return formatted_categories_bars
    
    def format_horizontal_line():
        # Number of spaces form the current bar + the pipe "|" symbol
        bar_spaces = 4
        # First space after the current bar
        starter_space = 1
        category_bar_spaces = 0
        # Add two spaces after the last bar
        final_spaces = 2

        # Calculate how many categories are and add a space for each one
        for _ in categories:
            category_bar_spaces += 1

        # Calculate the number of spaces between category bars
        category_bar_between_spaces = (category_bar_spaces - 1) * 2
        # Calculate the total width of the horizontal line
        horizontal_line_width = starter_space + category_bar_spaces + category_bar_between_spaces + final_spaces
        # Create the horizontal line consisting of hyphens
        total_line_hypens = "-" * horizontal_line_width

        # Right-align the horizontal line within a total width that includes the additional bar spaces
        return f'{total_line_hypens:>{bar_spaces + horizontal_line_width}}\n'

    # Get the total spend in all categories
    for category in categories:
        total_sepend += category.get_withdraws()

    # Get what each cateogory has spend compared to the others
    # (single category amount spent) / (total spent across all categories)
    for category in categories:
        # Make a dicitionary entry containing the ammount in percentatge the cateogry has spent
        # floored to the nearrest 10 => 58 becomes 50
        category_spend[category.type] = math.floor(int((category.get_withdraws() / total_sepend) * 100) / 10) * 10

    # Generate bar chart
    for i in range(10, -1, -1):
        bar = i * 10
        formatted_chart += f'{bar:3}| {check_categories_bar_chart(bar)}\n'

    # Generate horizonatl line    
    formatted_chart += format_horizontal_line()


    #TODO Add category names




    print(category_spend)
    return formatted_chart


print(create_spend_chart([food, clothing, auto]))