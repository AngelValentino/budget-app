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
        # Center category title between asterisks at max 30 characters
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
        # Add the amount to the current balance
        self.balance += amount

    def withdraw(self, amount, description = ''):
        # Attempt to withdraw funds; return False if insufficient funds
        if not self.check_funds(amount):
            print('insufficient funds')
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
        return amount <= self.get_balance()

    def transfer(self, amount, target_category):
        # Attempt to transfer funds to another category
        if not self.check_funds(amount):
            # Return false if there are not enough funds
            print('insufficient funds')
            return False
        # Withdraw the amount from the current category
        self.withdraw(amount, f'Transfer to {target_category.type}')
        # Deposit the amount into the target category
        target_category.deposit(amount, f'Transfer from {self.type}')
        
        return True

    def get_withdrawals(self):
        return round(self.total_spend, 2)
        
def create_spend_chart(categories):
    bar_spaces = 4 # Number of spaces form the current bar + the pipe "|" symbol
    spaces_between_categories = 2 # Number of spaces between bars between category bar or name
    total_spend = 0 # Total amount spent across all categories
    category_spend = {} # Dictionary to store the percentage spent per category
    category_names = [] # List to store names of categories
    longest_category_name = 0 # Length of the longest category name
    formatted_chart = 'Percentage spent by category\n' # Initialize the chart with a header

    # Determine if a category bar should be represented with 'o' or a space based on the current bar level
    def check_category_bar(category_bar, current_bar):
        return 'o' if category_bar >= current_bar else ' '
    
    # Create the visual representation of the bar chart for all categories with their specific spending
    def check_categories_bar_chart(bar):
        formatted_categories_bars = ''

        for category in category_spend:
            # Print the bars or spaces
            formatted_categories_bars += check_category_bar(category_spend[category], bar) + ' ' * spaces_between_categories
        
        return formatted_categories_bars
    
    # Format the horizontal line at the bottom of the chart
    def format_horizontal_line():
        # First space after the current bar
        starter_space = 1
        # Spaces after the last bar
        final_spaces = 2
        # Variable to keep track of spaces between bars
        category_bar_spaces = len(categories)

        # Calculate the number of spaces between category bars
        category_bar_between_spaces = (category_bar_spaces - 1) * spaces_between_categories
        # Calculate the total width of the horizontal line
        horizontal_line_width = starter_space + category_bar_spaces + category_bar_between_spaces + final_spaces

        # Return the formatted horizontal line with leading spaces
        return ' ' * bar_spaces + '-' * horizontal_line_width + '\n'

    # Format the category names to align them with the bars in the chart
    def get_formatted_names():
        # Variable to keep track of the formatted names
        formatted_names = ''

        # Create a line for each character position in the category names
        for i in range(0, longest_category_name):
            # Initial spaces before names
            formatted_names += ' ' * (bar_spaces + 1)

            # Add characters line
            for name in category_names:
                try:
                    # If the character has been found add it to the formatted line
                    formatted_names +=  name[i]
                except IndexError:
                    # Else add a space
                    formatted_names += ' '
                # Add spaces between category name characters
                formatted_names += ' ' * spaces_between_categories
            
            # If is the last character do not add a new line
            if i < longest_category_name - 1:
                formatted_names += '\n'
        
        # Return formatted names
        return formatted_names
    
    # Calculate total spending and store category names
    for category in categories:
        category_names.append(category.type)
        total_spend += category.get_withdrawals()

    # Determine the length of the longest category name
    for name in category_names:
        if len(name) > longest_category_name:
            longest_category_name = len(name)

    # Calculate percentage spent per category
    # (single category amount spent) / (total spent across all categories)
    if total_spend > 0:
        for category in categories:
            # Make a dictionary entry containing the amount in percentage the category has spent
            # floored to the nearest 10 => 58 becomes 50
            percentage_spent = (category.get_withdrawals() / total_spend) * 100
            category_spend[category.type] = math.floor(percentage_spent / 10) * 10
    else:
        # Handle case where total_spend is zero to avoid division by zero
        for category in categories:
            category_spend[category.type] = 0

    # Add the bar chart to the formatted string (from 0% to 100%)
    for i in range(10, -1, -1):
        # Calculate the bar percentage
        bar = i * 10
        # Add the bar percentage with the available spending bars for all the available categories
        formatted_chart += f'{bar:3}| {check_categories_bar_chart(bar)}\n'

    # Add horizontal line to the formatted string 
    formatted_chart += format_horizontal_line()

    # Add the categories names to the formatted string
    formatted_chart +=  get_formatted_names()

    return formatted_chart

# Example usage of the Category class and create_spend_chart function
business = Category('Business')
business.deposit(1000, 'deposit')
business.withdraw(300, 'stock')

food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
entertainment = Category('Entertainment')
food.transfer(50, entertainment)

# Print the food category details and the formatted spend chart
print(food)
print(create_spend_chart([business, food, entertainment]))