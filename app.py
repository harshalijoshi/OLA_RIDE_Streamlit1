import streamlit as st
import pandas as pd

st.title("OLA Ride Analytics Dashboard")

uploaded_file = st.file_uploader("OLA ride.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of your data:")
    st.dataframe(df)
    st.write("Summary statistics:")
    st.write(df.describe())



import mysql.connector
# Connect to MySQL
conn = mysql.connector.connect(
    host=st.secrets["db_host"],
    port=st.secrets["db_port"],
    user=st.secrets["db_user"],
    password=st.secrets["db_password"],
    database=st.secrets["db_name"]

)

cursor = conn.cursor()
cursor.execute("SELECT * FROM ola_ride LIMIT 10")
rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
st.dataframe(df)

query = "SELECT * FROM ola_ride WHERE booking_status='success';"
#query = "SELECT * FROM ola_ride WHERE booking_status='success';"

# Button to run the query
if st.button("Retrieve Successful Bookings"):
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            # Convert to DataFrame
            df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
            st.subheader("Successful Bookings")
            st.dataframe(df)
        else:
            st.warning("No successful bookings found.")
    except Exception as e:
        st.error(f"Error running query: {e}")


# --- Query 1: Average ride distance per vehicle type ---
query_avg_distance = """
SELECT Vehicle_type, AVG(Ride_Distance) AS avg_distance
FROM ola_ride
GROUP BY Vehicle_type;
"""

if st.button("Find Average Ride Distance by Vehicle Type"):
    try:
        cursor.execute(query_avg_distance)
        rows = cursor.fetchall()
        df_avg = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Average Ride Distance per Vehicle Type")
        st.dataframe(df_avg)
    except Exception as e:
        st.error(f"Error running query: {e}")

# --- Query 2: Cancelled rides by customers ---
query_cancelled = """
SELECT * FROM ola_ride
WHERE booking_status='canceled by customer';
"""

if st.button("Get Cancelled Rides by Customers"):
    try:
        cursor.execute(query_cancelled)
        rows = cursor.fetchall()
        df_cancelled = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Cancelled Rides by Customers")
        st.dataframe(df_cancelled)
    except Exception as e:
        st.error(f"Error running query: {e}")

# --- Query 4: Top 5 customers with highest number of rides ---
query_top_customers = """
SELECT customer_id, COUNT(booking_ID) AS Total_ride
FROM ola_ride
GROUP BY customer_id
ORDER BY Total_ride DESC
LIMIT 5;
"""

if st.button("List Top 5 Customers by Number of Rides"):
    try:
        cursor.execute(query_top_customers)
        rows = cursor.fetchall()
        df_top = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Top 5 Customers by Number of Rides")
        st.dataframe(df_top)
    except Exception as e:
        st.error(f"Error running query: {e}")

# --- Query 5: Number of rides cancelled by drivers (personal & car issues) ---
query_driver_cancel = """
SELECT COUNT(*) AS cancelled_rides
FROM ola_ride
WHERE canceled_rides_by_driver='personal & car related issue';
"""

if st.button("Get Number of Rides Cancelled by Drivers (Personal & Car Issues)"):
    try:
        cursor.execute(query_driver_cancel)
        rows = cursor.fetchall()
        df_cancel_driver = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Cancelled Rides by Drivers (Personal & Car Issues)")
        st.dataframe(df_cancel_driver)
    except Exception as e:
        st.error(f"Error running query: {e}")


# --- Query 6: Max & Min driver ratings for Prime Sedan ---
query_driver_ratings = """
SELECT MAX(driver_ratings) AS max_rating,
       MIN(driver_ratings) AS min_rating
FROM ola_ride
WHERE vehicle_type='Prime Sedan';
"""

if st.button("Find Max & Min Driver Ratings (Prime Sedan)"):
    try:
        cursor.execute(query_driver_ratings)
        rows = cursor.fetchall()
        df_ratings = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Max & Min Driver Ratings for Prime Sedan")
        st.dataframe(df_ratings)
    except Exception as e:
        st.error(f"Error running query: {e}")


# --- Query 7: Rides paid using UPI ---
query_upi = """
SELECT * FROM ola_ride
WHERE payment_method='UPI';
"""

if st.button("Retrieve Rides Paid via UPI"):
    try:
        cursor.execute(query_upi)
        rows = cursor.fetchall()
        df_upi = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Rides Paid Using UPI")
        st.dataframe(df_upi)
    except Exception as e:
        st.error(f"Error running query: {e}")


# --- Query 8: Average customer rating per vehicle type ---
query_avg_rating = """
SELECT vehicle_type, AVG(customer_rating) AS avg_customer_rating
FROM ola_ride
GROUP BY vehicle_type;
"""

if st.button("Find Average Customer Rating per Vehicle Type"):
    try:
        cursor.execute(query_avg_rating)
        rows = cursor.fetchall()
        df_avg_rating = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Average Customer Rating per Vehicle Type")
        st.dataframe(df_avg_rating)
    except Exception as e:
        st.error(f"Error running query: {e}")


# --- Query 9: Total booking value of successful rides ---
query_total_success = """
SELECT SUM(booking_value) AS total_successfully_booking
FROM ola_ride
WHERE booking_status='success';
"""

if st.button("Calculate Total Booking Value of Successful Rides"):
    try:
        cursor.execute(query_total_success)
        rows = cursor.fetchall()
        df_total_success = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Total Booking Value of Successful Rides")
        st.dataframe(df_total_success)
    except Exception as e:
        st.error(f"Error running query: {e}")


# --- Query 10: Incomplete rides with reason ---
query_incomplete = """
SELECT booking_id, incomplete_rides_reason
FROM ola_ride
WHERE incomplete_rides='yes';
"""

if st.button("List Incomplete Rides with Reasons"):
    try:
        cursor.execute(query_incomplete)
        rows = cursor.fetchall()
        df_incomplete = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        st.subheader("Incomplete Rides with Reasons")
        st.dataframe(df_incomplete)
    except Exception as e:
        st.error(f"Error running query: {e}")





st.title("Power BI Dashboard")

# Your Publish to Web link
powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiOGY1Y2ZmNjItMTFjMS00ZDg2LTlhOTctM2E3ZDViYWM1ZGE4IiwidCI6ImI3OTIzZDJmLTdkOGMtNGFjNy05NWY0LTQ4ZjQzZDA1NWFmMyJ9"

st.components.v1.iframe(powerbi_url, width=1000, height=600)