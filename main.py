# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
SELECT firstName, lastName, jobTitle
    FROM employees
    JOIN offices
        USING(officeCode)
    WHERE city = 'Boston';
    """, conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
SELECT officeCode, city
    FROM offices
    LEFT JOIN employees
        USING(officeCode)
    WHERE employeeNumber IS NULL;
""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
SELECT firstName, lastName, city, State
    FROM employees
    LEFT JOIN offices
        USING(officeCode)
    ORDER BY firstName ASC, lastName ASC;
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
    FROM customers
    LEFT JOIN orders
        USING(customerNumber)
    WHERE orderNumber IS NULL
    ORDER BY contactLastName ASC;
""", conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
SELECT contactFirstName, contactLastName, amount, paymentDate
    FROM customers
    JOIN payments
        USING(customerNumber)
    ORDER BY CAST(amount AS REAL) DESC;
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
SELECT  employeeNumber, firstName, lastName, COUNT(customerNumber) AS number_of_customers
    FROM employees
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY employeeNumber, firstName, lastName
    HAVING AVG(creditLimit) > 90000
    ORDER BY number_of_customers DESC;
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
SELECT productName, COUNT(*) AS numorders, SUM(quantityOrdered) AS totalunits
    FROM products
    JOIN orderdetails
        USING(productCode)
    GROUP BY productCode, productName
    ORDER BY totalunits DESC;
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
SELECT productName, productCode, COUNT(DISTINCT customerNumber) AS numpurchasers
    FROM products
    JOIN orderdetails
        USING(productCode)
    JOIN orders
        USING(orderNumber)
    GROUP BY productCode, productName
    ORDER BY numpurchasers DESC;
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
SELECT COUNT(customerNumber) AS n_customers, o.officeCode, o.city
    FROM offices AS o
    LEFT JOIN employees AS e
        USING(officeCode)
    LEFT JOIN customers AS c
       ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY officeCode, o.city;
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
SELECT DISTINCT
    employeeNumber, firstName, lastName, o.city, o.officeCode
    FROM employees AS e
    JOIN offices AS o
        USING(officeCode)
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders
        USING(customerNumber)
    JOIN orderdetails
        USING(orderNumber)
    WHERE orderdetails.productCode IN (
        SELECT od2.productCode
            FROM orderdetails AS od2
            JOIN orders AS ord2
                USING(orderNumber)
            GROUP BY od2.productCode
            HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.employeeNumber;
""", conn)

conn.close()