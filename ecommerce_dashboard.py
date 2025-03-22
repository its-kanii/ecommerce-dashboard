import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Database Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Kanimozhi@20",  # Replace with your MySQL password
        database="EcommerceDB"
    )

# Fetch data from MySQL
def fetch_data(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    data = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    cursor.close()
    conn.close()
    return data

# Streamlit UI
st.title("📊 E-commerce Sales Dashboard")

# Total Revenue
total_sales = fetch_data("SELECT SUM(TotalAmount) AS Total_Revenue FROM Orders;")
st.metric("💰 Total Revenue", f"${total_sales.iloc[0, 0]:,.2f}")

# Top Selling Products
st.subheader("🏆 Top 5 Selling Products")
top_products = fetch_data("""
    SELECT p.Name, SUM(od.Quantity) AS Total_Sold 
    FROM OrderDetails od 
    JOIN Products p ON od.ProductID = p.ProductID 
    GROUP BY p.Name 
    ORDER BY Total_Sold DESC 
    LIMIT 5;
""")

fig, ax = plt.subplots()
sns.barplot(x="Total_Sold", y="Name", data=top_products, palette="viridis", ax=ax)
ax.set_xlabel("Total Sold")
ax.set_ylabel("Product Name")
st.pyplot(fig)

# Top Customers by Spending
st.subheader("💎 Top 5 Customers by Spending")
top_customers = fetch_data("""
    SELECT c.Name, SUM(o.TotalAmount) AS Total_Spent 
    FROM Orders o 
    JOIN Customers c ON o.CustomerID = c.CustomerID 
    GROUP BY c.Name 
    ORDER BY Total_Spent DESC 
    LIMIT 5;
""")

fig, ax = plt.subplots()
sns.barplot(x="Total_Spent", y="Name", data=top_customers, palette="coolwarm", ax=ax)
ax.set_xlabel("Total Spent ($)")
ax.set_ylabel("Customer Name")
st.pyplot(fig)

# Sales Trends Over Time
st.subheader("📈 Sales Over Time")
sales_trends = fetch_data("""
    SELECT OrderDate, SUM(TotalAmount) AS Sales 
    FROM Orders 
    GROUP BY OrderDate 
    ORDER BY OrderDate;
""")

fig, ax = plt.subplots()
ax.plot(sales_trends["OrderDate"], sales_trends["Sales"], marker='o', linestyle='-')
ax.set_xlabel("Date")
ax.set_ylabel("Sales ($)")
ax.set_title("Sales Trend Over Time")
plt.xticks(rotation=45)
st.pyplot(fig)

# Footer
st.markdown("🚀 **Built with Streamlit & MySQL**")

