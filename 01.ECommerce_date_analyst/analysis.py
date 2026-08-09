#%%
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="olist"
)
query = """
SELECT 
    *
FROM mart_monthly_revenue
ORDER BY month
"""

df = pd.read_sql(query, conn)
conn.close()

df.head()


df['month'] = pd.to_datetime(df['month'])

plt.figure()
plt.plot(df['month'], df['revenue'])
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(df['month'], df['growth_rate'])
plt.title("Monthly Growth Rate")
plt.xlabel("Month")
plt.ylabel("Growth Rate")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



fig, ax1 = plt.subplots()

ax1.plot(df['order_month'], df['revenue'])
ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue")

ax2 = ax1.twinx()
ax2.plot(df['order_month'], df['growth_rate'])
ax2.set_ylabel("Growth Rate")

plt.title("Revenue & Growth Rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# %%
