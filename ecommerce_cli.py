"""
Nekruz Ashrapov
E-commerce Database CLI Application
CS4092 Database Design and Development Final Project
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
import sys
from decimal import Decimal

class ECommerceDB:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self, host='localhost', database='ecommerce_db', user='root', password=''):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print(" Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f" Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print(" Database connection closed")
    
    def display_customers(self):
        """Display all customers"""
        try:
            query = """
            SELECT customer_id, CONCAT(first_name, ' ', last_name) as name, 
                   email, phone, city, state, registration_date
            FROM CUSTOMER
            ORDER BY registration_date DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            print("\n" + "="*80)
            print("                           CUSTOMER LIST")
            print("="*80)
            print(f"{'ID':<4} {'Name':<20} {'Email':<25} {'Phone':<15} {'Location':<20}")
            print("-"*80)
            
            for row in results:
                location = f"{row[4]}, {row[5]}" if row[4] and row[5] else "N/A"
                print(f"{row[0]:<4} {row[1]:<20} {row[2]:<25} {row[3] or 'N/A':<15} {location:<20}")
            
            print(f"\nTotal customers: {len(results)}")
            
        except Error as e:
            print(f" Error fetching customers: {e}")
    
    def display_products(self):
        """Display all products with stock information"""
        try:
            query = """
            SELECT product_id, product_name, category, price, stock_quantity, 
                   CASE 
                       WHEN stock_quantity = 0 THEN 'Out of Stock'
                       WHEN stock_quantity < 10 THEN 'Low Stock'
                       ELSE 'In Stock'
                   END as status
            FROM PRODUCT
            ORDER BY category, product_name
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            print("\n" + "="*90)
            print("                              PRODUCT CATALOG")
            print("="*90)
            print(f"{'ID':<4} {'Product Name':<25} {'Category':<15} {'Price':<10} {'Stock':<8} {'Status':<12}")
            print("-"*90)
            
            for row in results:
                print(f"{row[0]:<4} {row[1]:<25} {row[2] or 'N/A':<15} ${row[3]:<9.2f} {row[4]:<8} {row[5]:<12}")
            
            print(f"\nTotal products: {len(results)}")
            
        except Error as e:
            print(f" Error fetching products: {e}")
    
    def add_product(self):
        """Add a new product to inventory"""
        try:
            print("\n" + "="*50)
            print("           ADD NEW PRODUCT")
            print("="*50)
            
            name = input("Product name: ").strip()
            if not name:
                print(" Product name cannot be empty")
                return
            
            description = input("Description (optional): ").strip()
            
            try:
                price = float(input("Price: $"))
                if price < 0:
                    print(" Price cannot be negative")
                    return
            except ValueError:
                print(" Invalid price format")
                return
            
            try:
                stock = int(input("Initial stock quantity: "))
                if stock < 0:
                    print(" Stock quantity cannot be negative")
                    return
            except ValueError:
                print(" Invalid stock quantity")
                return
            
            category = input("Category (optional): ").strip()
            
            query = """
            INSERT INTO PRODUCT (product_name, description, price, stock_quantity, category)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (name, description or None, price, stock, category or None)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            product_id = self.cursor.lastrowid
            print(f" Product '{name}' added successfully with ID: {product_id}")
            
        except Error as e:
            print(f" Error adding product: {e}")
            self.connection.rollback()
    
    def update_product_stock(self):
        """Update stock quantity for a product"""
        try:
            self.display_products()
            
            try:
                product_id = int(input("\nEnter Product ID to update stock: "))
            except ValueError:
                print(" Invalid Product ID")
                return
            
            # Check if product exists
            check_query = "SELECT product_name, stock_quantity FROM PRODUCT WHERE product_id = %s"
            self.cursor.execute(check_query, (product_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(" Product not found")
                return
            
            product_name, current_stock = result
            print(f"\nProduct: {product_name}")
            print(f"Current stock: {current_stock}")
            
            try:
                new_stock = int(input("New stock quantity: "))
                if new_stock < 0:
                    print(" Stock quantity cannot be negative")
                    return
            except ValueError:
                print(" Invalid stock quantity")
                return
            
            update_query = "UPDATE PRODUCT SET stock_quantity = %s WHERE product_id = %s"
            self.cursor.execute(update_query, (new_stock, product_id))
            self.connection.commit()
            
            print(f" Stock updated for '{product_name}': {current_stock} → {new_stock}")
            
        except Error as e:
            print(f" Error updating stock: {e}")
            self.connection.rollback()
    
    def view_customer_purchases(self):
        """View purchases for a specific customer"""
        try:
            self.display_customers()
            
            try:
                customer_id = int(input("\nEnter Customer ID to view purchases: "))
            except ValueError:
                print(" Invalid Customer ID")
                return
            
            query = """
            SELECT c.first_name, c.last_name, p.purchase_id, p.purchase_date, 
                   p.total_amount, p.status, cc.card_type,
                   CONCAT('****', RIGHT(cc.card_number, 4)) as masked_card
            FROM CUSTOMER c
                JOIN PURCHASE p ON c.customer_id = p.customer_id
                JOIN CREDIT_CARD cc ON p.card_id = cc.card_id
            WHERE c.customer_id = %s
            ORDER BY p.purchase_date DESC
            """
            
            self.cursor.execute(query, (customer_id,))
            results = self.cursor.fetchall()
            
            if not results:
                print(" No purchases found for this customer")
                return
            
            customer_name = f"{results[0][0]} {results[0][1]}"
            print(f"\n" + "="*80)
            print(f"              PURCHASE HISTORY FOR {customer_name.upper()}")
            print("="*80)
            print(f"{'Purchase ID':<12} {'Date':<12} {'Amount':<10} {'Status':<12} {'Payment':<15}")
            print("-"*80)
            
            total_spent = 0
            for row in results:
                purchase_date = row[3].strftime('%Y-%m-%d')
                payment_info = f"{row[6]} {row[7]}"
                print(f"{row[2]:<12} {purchase_date:<12} ${row[4]:<9.2f} {row[5]:<12} {payment_info:<15}")
                total_spent += row[4]
            
            print("-"*80)
            print(f"Total purchases: {len(results)}")
            print(f"Total amount spent: ${total_spent:.2f}")
            
        except Error as e:
            print(f" Error fetching customer purchases: {e}")
    
    def search_products_by_category(self):
        """Search products by category"""
        try:
            # Get available categories
            category_query = "SELECT DISTINCT category FROM PRODUCT WHERE category IS NOT NULL ORDER BY category"
            self.cursor.execute(category_query)
            categories = self.cursor.fetchall()
            
            if not categories:
                print(" No categories found")
                return
            
            print("\nAvailable categories:")
            for i, (category,) in enumerate(categories, 1):
                print(f"{i}. {category}")
            
            try:
                choice = int(input("\nSelect category number (or 0 to enter custom): "))
                if choice == 0:
                    search_category = input("Enter category name: ").strip()
                elif 1 <= choice <= len(categories):
                    search_category = categories[choice-1][0]
                else:
                    print(" Invalid choice")
                    return
            except ValueError:
                print(" Invalid input")
                return
            
            query = """
            SELECT product_id, product_name, description, price, stock_quantity
            FROM PRODUCT
            WHERE category LIKE %s
            ORDER BY product_name
            """
            
            self.cursor.execute(query, (f"%{search_category}%",))
            results = self.cursor.fetchall()
            
            if not results:
                print(f" No products found in category '{search_category}'")
                return
            
            print(f"\n" + "="*80)
            print(f"              PRODUCTS IN CATEGORY: {search_category.upper()}")
            print("="*80)
            print(f"{'ID':<4} {'Name':<30} {'Price':<10} {'Stock':<8} {'Description':<20}")
            print("-"*80)
            
            for row in results:
                desc = (row[2][:20] + "...") if row[2] and len(row[2]) > 20 else (row[2] or "N/A")
                print(f"{row[0]:<4} {row[1]:<30} ${row[3]:<9.2f} {row[4]:<8} {desc:<20}")
            
            print(f"\nFound {len(results)} products in '{search_category}' category")
            
        except Error as e:
            print(f" Error searching products: {e}")
    
    def add_customer(self):
        """Add a new customer"""
        try:
            print("\n" + "="*50)
            print("         REGISTER NEW CUSTOMER")
            print("="*50)
            
            first_name = input("First name: ").strip()
            if not first_name:
                print(" First name cannot be empty")
                return
            
            last_name = input("Last name: ").strip()
            if not last_name:
                print(" Last name cannot be empty")
                return
            
            email = input("Email: ").strip()
            if not email or '@' not in email:
                print(" Valid email is required")
                return
            
            # Check if email already exists
            check_query = "SELECT customer_id FROM CUSTOMER WHERE email = %s"
            self.cursor.execute(check_query, (email,))
            if self.cursor.fetchone():
                print(" Email already registered")
                return
            
            phone = input("Phone (optional): ").strip()
            address = input("Address (optional): ").strip()
            city = input("City (optional): ").strip()
            state = input("State (optional): ").strip()
            zip_code = input("ZIP code (optional): ").strip()
            
            query = """
            INSERT INTO CUSTOMER (first_name, last_name, email, phone, address, city, state, zip_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, email, 
                     phone or None, address or None, city or None, state or None, zip_code or None)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            customer_id = self.cursor.lastrowid
            print(f" Customer '{first_name} {last_name}' registered successfully with ID: {customer_id}")
            
        except Error as e:
            print(f" Error adding customer: {e}")
            self.connection.rollback()
    
    def sales_report(self):
        """Generate sales report"""
        try:
            query = """
            SELECT 
                COUNT(DISTINCT pur.purchase_id) as total_orders,
                COUNT(DISTINCT pur.customer_id) as unique_customers,
                SUM(pur.total_amount) as total_revenue,
                AVG(pur.total_amount) as avg_order_value,
                MAX(pur.purchase_date) as latest_order,
                MIN(pur.purchase_date) as first_order
            FROM PURCHASE pur
            """
            
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            
            print("\n" + "="*60)
            print("                    SALES REPORT")
            print("="*60)
            print(f"Total Orders: {result[0]}")
            print(f"Unique Customers: {result[1]}")
            print(f"Total Revenue: ${result[2]:.2f}")
            print(f"Average Order Value: ${result[3]:.2f}")
            print(f"Latest Order: {result[4]}")
            print(f"First Order: {result[5]}")
            
            # Top selling products
            top_products_query = """
            SELECT p.product_name, SUM(pi.quantity) as total_sold, SUM(pi.subtotal) as revenue
            FROM PRODUCT p
                JOIN PURCHASE_ITEM pi ON p.product_id = pi.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY total_sold DESC
            LIMIT 5
            """
            
            self.cursor.execute(top_products_query)
            top_products = self.cursor.fetchall()
            
            print("\n" + "-"*60)
            print("TOP 5 SELLING PRODUCTS:")
            print("-"*60)
            print(f"{'Product':<30} {'Qty Sold':<10} {'Revenue':<10}")
            print("-"*60)
            
            for product in top_products:
                print(f"{product[0]:<30} {product[1]:<10} ${product[2]:<9.2f}")
            
        except Error as e:
            print(f" Error generating sales report: {e}")


def main():
    """Main application loop"""
    db = ECommerceDB()
    
    print(" E-commerce Database Management System")
    print("="*50)
    
    # Get database connection details
    print("Database Connection Setup:")
    host = input("MySQL host (default: localhost): ").strip() or 'localhost'
    database = input("Database name (default: ecommerce_db): ").strip() or 'ecommerce_db'
    user = input("MySQL username (default: root): ").strip() or 'root'
    password = input("MySQL password: ")
    
    if not db.connect(host, database, user, password):
        print(" Failed to connect to database. Exiting...")
        return
    
    while True:
        print("\n" + "="*50)
        print("           MAIN MENU")
        print("="*50)
        print("1. View All Customers")
        print("2. View All Products")
        print("3. Add New Product")
        print("4. Update Product Stock")
        print("5. Add New Customer")
        print("6. View Customer Purchase History")
        print("7. Search Products by Category")
        print("8. Generate Sales Report")
        print("9. Exit")
        print("="*50)
        
        try:
            choice = input("Select an option (1-9): ").strip()
            
            if choice == '1':
                db.display_customers()
            elif choice == '2':
                db.display_products()
            elif choice == '3':
                db.add_product()
            elif choice == '4':
                db.update_product_stock()
            elif choice == '5':
                db.add_customer()
            elif choice == '6':
                db.view_customer_purchases()
            elif choice == '7':
                db.search_products_by_category()
            elif choice == '8':
                db.sales_report()
            elif choice == '9':
                print(" Thank you for using the E-commerce Database Management System!")
                break
            else:
                print(" Invalid option. Please select 1-9.")
                
        except KeyboardInterrupt:
            print("\n\n Goodbye!")
            break
        except Exception as e:
            print(f" An unexpected error occurred: {e}")
    
    db.disconnect()

if __name__ == "__main__":
    main()