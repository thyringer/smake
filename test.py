# Start all unit tests with: python -m unittest
# Or just this file: python -m test

import sys
import unittest

from importlib.machinery import SourceFileLoader

smake = SourceFileLoader("smake", "./smake").load_module()


#

_sql_script = """
/* Create the Customers table

*/
CREATE TABLE Customers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	email TEXT UNIQUE NOT NULL
);

-- Create the Orders table (linked to Customers)
CREATE TABLE Orders (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER,
	product TEXT NOT NULL,
	amount INTEGER NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES Customers(id) ON DELETE CASCADE
);

-- Begin transaction
BEGIN TRANSACTION;

-- Insert sample customers
INSERT INTO Customers (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO Customers (name, email) VALUES ('Bob', 'bob@example.com');

-- Insert orders for Alice (customer_id = 1) and Bob (customer_id = 2)
INSERT INTO Orders (customer_id, product, amount) VALUES (1, 'Laptop', 1200);
INSERT INTO Orders (customer_id, product, amount) VALUES (1, 'Mouse', 25);
INSERT INTO Orders (customer_id, product, amount) VALUES (2, 'Keyboard', 45);

-- Commit the transaction
COMMIT;

-- Update Bob's email
UPDATE Customers SET email = 'bob.new@example.com' WHERE name = 'Bob';

-- Delete Alice's orders
DELETE FROM Orders WHERE customer_id = 1;

-- Show remaining data
SELECT * FROM Customers;
/*
SELECT * FROM Orders;
*/

-- Begin a new transaction to demonstrate rollback
BEGIN TRANSACTION;

-- Try to insert an order for a non-existing customer (should fail)
INSERT INTO Orders (customer_id, product, amount) VALUES (99, 'Monitor', 200);

-- Rollback because the customer does not exist
ROLLBACK;

-- Check tables after rollback
SELECT * FROM Customers;
SELECT * FROM Orders;
"""


class TestSMake(unittest.TestCase):

	def test_sql_parser(self):
		statements = smake.parse_sql(_sql_script)

		for stmt in statements:
			print(f"{stmt.line_from}:{stmt.line_to}\n    {stmt.code}")

		for stmt in statements:
			print(smake.extract_beginning(stmt.code))

		self.assertEqual(len(statements), 17, "SQL statements were not parsed correctly.")


if __name__ == '__main__':
	unittest.main()