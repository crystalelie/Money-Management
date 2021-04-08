# Money-Management

Implementation of a finance tracker built using Python and MySQL. Able to enter and view data through the command line in PyCharm.

Python takes your MySQL credentials to create a connection. Once the connection is created, it will check to see if the four tables already exist, if they don't, it will create these tables in MySQL. Once they're created, it brings the user to the main menu, where they can opt to view, write, or read data.

Writing the data will allow them to choose the table they would like to write data to. Once chosen, it will ask for some information, then will send the data to the table in MySQL. They are able to add as much data as they would like to each of the tables. 

Reading the data will allow them to choose how they would like to sum the data. They can sum credits minus debits, sum all of their debits, sum debits for each month or sum debits for each category. This runs queries to pull the data and present the data in PyCharm.

Viewing the data will allow them to choose if they would like to see a pie graph, which includes a section for the totals for each of their tables, or if they would like to see a bar graph, which creates bars for the totals for each category.
