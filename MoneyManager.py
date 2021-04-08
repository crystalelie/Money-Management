import datetime
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error


def create_server_connection(host_name, user_name, user_password, user_database, connection=None):
    """
    Function is to set up the connection between Python and MySQL. It takes the host,
    user, password and database from the user to establish the connection. If connected,
    it will jump to the Create Tables Function, otherwise, it will notify the user of the
    error that is not allowing them to connect.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=user_database
        )
        create_tables(connection)
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def create_tables(connection):
    """
    Function to create the skeletons of the tables in MySQL. If the tables already exist, it will
    continue to call the next function. Otherwise, it will create the new tables.
    """
    # Creating a cursor object
    cur = connection.cursor()

    # Creates the tables, Finance, Income, Rent_Expenses and Entertainment_Other, if they don't already exist
    cur.execute('''CREATE TABLE IF NOT EXISTS Finances (date DATE, item TEXT, cost FLOAT, detail TEXT, category TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Income (date DATE, value FLOAT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Rent_Expenses (date DATE, details TEXT, cost FLOAT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Entertainment_Other (date DATE, details TEXT, cost FLOAT)''')

    print("Welcome to the Money Manager. \n \
          ")
    choices(cur, connection)


def choices(cur, connection):
    """
    This function acts as the homepage of the program. It takes the parameters cur and connection, since
    those are needed to keep the connection with MySQL. This function asks what the user would like to do.
    It continues through the prompts until the user selects a number, then it will launch the applicable
    function
    """

    print("Please enter Read, View, Write or Exit. \n \
           ")
    prompt = input('>>> ')

    while prompt == "write".lower():
        print("Please enter the number of one of the following choices. \n \
              1. Income \n \
              2. Rent/Expenses \n \
              3. Other \n \
              To go back to the prior screen, enter 'back'")
        action = input('>>> ')
        if action == '1':
            write_income(cur, connection)
        if action == '2':
            write_expenses(cur, connection)
        if action == '3':
            write_other(cur, connection)
        if action == 'back'.lower():
            choices(cur, connection)
        else:
            choices(cur, connection)

    while prompt == "read".lower():
        print("Please enter the number of one of the following choices. \n \
              1. Print All (Income minus Debits) \n \
              2. Sum All (Debits) \n \
              3. Sum by Month \n \
              4. Sum by Category \n \
              To go back to the prior screen, enter 'back'")
        action = input('>>> ')
        if action == '1':
            print_all(cur)
            choices(cur, connection)
        if action == '2':
            sum_all(cur)
            choices(cur, connection)
        if action == '3':
            sum_by_month(cur)
            choices(cur, connection)
        if action == '4':
            sum_by_category(cur)
            choices(cur, connection)
        if action == 'back'.lower():
            choices(cur, connection)
        else:
            choices(cur, connection)

    while prompt == "view".lower():
        print("Please enter the number of one of the following choices. \n \
                     1. Pie Graph for All Income/Expenses \n \
                     2. Bar Graph by Category \n \
                     To go back to the prior screen, enter 'back'")
        action = input('>>> ')
        if action == '1':
            all_graph(cur, connection)
        if action == '2':
            category_graph(cur, connection)
        if action == 'back'.lower():
            choices(cur, connection)
        else:
            choices(cur, connection)

    while prompt == "exit".lower():
        exit_program(cur, connection)


def write_income(cur, connection):
    """
    This function asks the user for the date they want to record and the amount of income they want to record. If either
    of these are in the wrong format, it will provide them with an error message and re-prompt them for a date. It will
    submit the date and income to the Income table in MySQL, then will ask if they would like to enter more income or
    to go back to the main screen.
    """
    try:
        user_input = input("Please enter the date in YYYY-MM-DD format. ")
        date = datetime.datetime.strptime(user_input, '%Y-%m-%d').date()
        value = input("Enter Income: ").rstrip()
        cur.execute('INSERT INTO Income(date, value) VALUES (%s, %s)', (date, value))
        connection.commit()

    except:
        print("Incorrect date or value format.")
        write_income(cur, connection)

    print("Would you like to enter more income?")
    answer = input('>>> ')
    if answer.lower() == "yes":
        write_income(cur, connection)
    else:
        choices(cur, connection)


def write_expenses(cur, connection):
    """
    This function asks the user for the date, the cost, the item, the category and the details they want to record. If any
    of these are in the wrong format, it will provide them with an error message and re-prompt them for the details. It will
    submit the info to both the Rent_Expenses table and the Finances table then will ask if they would like to enter more
    expenses or to go back to the main screen.
    """
    try:
        user_input = input("Please enter the date in YYYY-MM-DD format. ")
        date = datetime.datetime.strptime(user_input, '%Y-%m-%d').date()
        cost = input('Please enter the cost of the expense: ').rstrip()
        item = input('Please enter the item name: ').rstrip()
        cat = input('Please enter the category: ').rstrip()
        detail = input('Please enter details: ').rstrip()

        cur.execute('INSERT INTO Rent_Expenses(date, details, cost) VALUES(%s, %s, %s)', (date, item, cost))
        cur.execute('INSERT INTO Finances(date, item, cost, detail, category) VALUES(%s, %s, %s, %s, %s)',
                    (date, item, cost, detail, cat))
        connection.commit()

    except:
        print("Incorrect date or cost format.")
        write_expenses(cur, connection)

    print("Would you like to enter more rent/expenses?")
    answer = input('>>> ')
    if answer.lower() == "yes":
        write_expenses(cur, connection)
    else:
        choices(cur, connection)


def write_other(cur, connection):
    """
    This function asks the user for the date, the cost, the item, the category and the details they want to record. If any
    of these are in the wrong format, it will provide them with an error message and re-prompt them for the details. It will
    submit the info to both the Entertainment_Other table and the Finances table then will ask if they would like to enter more
    other expenses or to go back to the main screen.
    """
    try:
        user_input = input("Please enter the date in YYYY-MM-DD format. ")
        date = datetime.datetime.strptime(user_input, '%Y-%m-%d').date()
        cost = input('Please enter the cost of the expense: ').rstrip()
        item = input('Please enter the item or press enter: ').rstrip()
        cat = input('Please enter the category or press enter: ').rstrip()
        detail = input('Please enter details or press enter: ').rstrip()

        cur.execute('INSERT INTO Entertainment_Other(date, details, cost) VALUES(%s, %s, %s)', (date, item, cost))
        cur.execute('INSERT INTO Finances(date, item, cost, detail, category) VALUES(%s, %s, %s, %s, %s)',
                    (date, item, cost, detail, cat))
        connection.commit()

    except:
        print("Incorrect date or value format.")
        write_other(cur, connection)

    print("Would you like to enter more entertainment/other?")
    answer = input('>>> ')
    if answer.lower() == "yes":
        write_expenses(cur, connection)
    else:
        choices(cur, connection)


def print_all(cur):
    """
    Runs a query in MySQL to sum the cost from Finances and to sum the values from Income. It subtracts the costs from
    the income to give the resulting total.
    """
    total_cost = cur.execute('SELECT sum(cost) FROM Finances')
    data = cur.fetchall()
    total_cost = 0
    for row in data:
        total_cost += row[0]

    total_income = cur.execute('SELECT sum(value) FROM Income')
    data1 = cur.fetchall()
    total_income = 0
    for row in data1:
        total_income += row[0]

    total = total_income - total_cost
    print("The total sum of your income minus your debits: " + str(total))


def sum_all(cur):
    """
    Runs a query in MySQL to sum the cost from Finances. It returns the total sum of the debits.
    """
    total = cur.execute('SELECT sum(cost) FROM Finances')
    data = cur.fetchall()
    total = 0
    for row in data:
        total += row[0]

    print("The total sum of your debits: " + str(total))


def sum_by_month(cur):
    """
    Runs a query in MySQL to sum the cost from Finances per month and sorts the findings by year and month. It returns
    the total cost for each month.
    """
    query = cur.execute("SELECT MONTHNAME(date), sum(cost) FROM Finances GROUP BY Year(date), Month(date)")
    data = cur.fetchall()

    print("The total sum of debits for each month is : ", str(data))


def sum_by_category(cur):
    """
    Runs a query in MySQL to sum the cost from Finances per category. It returns the total cost for each category.
    """

    total = cur.execute('SELECT category, sum(cost) FROM Finances GROUP BY category')
    data = cur.fetchall()

    print("The total sum of your debits: " + str(data))


def all_graph(cur, connection):
    """
    Creates a pie graph to compare each of the three graphs, Income, Rent/Expenses and Entertainment/Other. It runs
    queries to sum the total cost/value for all items in each of the tables and presents a labelled pie graph.
    """

    sections = 'Income', 'Rent/Expenses', 'Entertainment/Other'
    sizes = []

    # Total income
    total = cur.execute('SELECT sum(value) FROM Income')
    data = cur.fetchall()
    total = 0
    for row in data:
        total += row[0]
    sizes.append(total)

    # Total Rent/Expenses
    total = cur.execute('SELECT sum(cost) FROM Rent_Expenses')
    data = cur.fetchall()
    total = 0
    for row in data:
        total += row[0]
    sizes.append(total)

    # Total Entertainment/Other
    total = cur.execute('SELECT sum(cost) FROM Entertainment_Other')
    data = cur.fetchall()
    total = 0
    for row in data:
        total += row[0]
    sizes.append(total)

    # Explode only the income section
    explode = (0.1, 0, 0)

    plt.pie(sizes, explode=explode, autopct='%1.1f%%', labels=sections, shadow=True, startangle=90)
    plt.title("Total Money Movement")
    plt.show()


def category_graph(cur, connection):
    """
    Creates a bar graph to compare all of the different categories that are recorded in the Finances table. Runs queries
    to sum the total cost for each category
    """
    classes = []
    total = cur.execute('SELECT category, sum(cost) FROM Finances GROUP BY category')
    data = cur.fetchall()

    # Breaking the tuples apart into two lists for the labels and the data
    for i in range(len(data)):
        classes.append(data[i])
    labels, numbers = map(list,zip(*classes))

    plt.bar(labels, numbers, width=.5)
    plt.title("Total Expenses Per Category")
    plt.show()


def exit_program(cur, connection):
    """
    Function to end the program. If they answer with no, then it will bring them back to the choices function, otherwise,
    if they answer with yes, it will say goodbye, close the connection and exit the program.
    """
    print("Would you like to exit the program? \n \
          ")
    answer = input('<<< ')

    if answer == "No" or answer == "no":
        choices(cur, connection)
    if answer == "Yes" or answer == "yes":
        print("Thank you for using the Money Manager. Goodbye.")
        cur.close()
        exit()



