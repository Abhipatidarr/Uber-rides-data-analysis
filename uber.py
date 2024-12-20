import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load  the dataset
@st.cache_data
def load_data():
    
    data = pd.read_csv("uber-rides-dataset.csv")
    
    # Convert pickup and dropoff times to datetime
    data['pickup'] = pd.to_datetime(data['pickup'], errors='coerce')
    data['dropoff'] = pd.to_datetime(data['dropoff'], errors='coerce')
    
    # Extract time-related features
    data['pickup_hour'] = data['pickup'].dt.hour
    data['pickup_day'] = data['pickup'].dt.day_name()
    data['pickup_month'] = data['pickup'].dt.month
    
    # Handle missing values
    data['payment'] = data['payment'].fillna('Unknown')
    data['pickup_zone'] = data['pickup_zone'].fillna('Unknown')
    data['dropoff_zone'] = data['dropoff_zone'].fillna('Unknown')
    
    return data

data = load_data()
 
st.sidebar.title("Uber Dataset Analysis")
questions = [
    "Total number of trips",
    "Average trip distance",
    "Average trip fare",
    "Total revenue generated",
    "Trips per day of the week",
    "Trips per hour of the day",
    "Trips per month",
    "Average trip fare by day of the week",
    "Average trip distance by hour of the day",
    "Top 10 busiest pickup zones",
    "Top 10 busiest dropoff zones",
    "Most common pickup-dropoff zone pairs",
    "Average fare by pickup zone",
    "Average fare by dropoff zone",
    "Distribution of the number of passengers",
    "Average fare per passenger count",
    "Distribution of payment methods",
    "Average fare by payment method",
    "Distribution of trip distances",
    "Outliers in trip distances and their characteristics",
]
selected_question = st.sidebar.selectbox("Choose a question to analyze", questions)


st.title(f"Analysis: {selected_question}")


if selected_question == "Total number of trips":
    total_trips = len(data)
    st.write(f"Total number of trips: {total_trips}")

elif selected_question == "Average trip distance":
    avg_distance = data['distance'].mean()
    st.write(f"Average trip distance: {avg_distance:.2f} miles")

elif selected_question == "Average trip fare":
    avg_fare = data['fare'].mean()
    st.write(f"Average trip fare: ${avg_fare:.2f}")

elif selected_question == "Total revenue generated":
    total_revenue = data['fare'].sum()
    st.write(f"Total revenue generated: ${total_revenue:.2f}")

elif selected_question == "Trips per day of the week":
    trips_by_day = data['pickup_day'].value_counts()
    st.bar_chart(trips_by_day)

elif selected_question == "Trips per hour of the day":
    trips_by_hour = data['pickup_hour'].value_counts().sort_index()
    st.bar_chart(trips_by_hour)

elif selected_question == "Trips per month":
    trips_by_month = data['pickup_month'].value_counts().sort_index()
    st.bar_chart(trips_by_month)

elif selected_question == "Average trip fare by day of the week":
    avg_fare_by_day = data.groupby('pickup_day')['fare'].mean().sort_values()
    st.bar_chart(avg_fare_by_day)

elif selected_question == "Average trip distance by hour of the day":
    avg_distance_by_hour = data.groupby('pickup_hour')['distance'].mean()
    st.line_chart(avg_distance_by_hour)

elif selected_question == "Top 10 busiest pickup zones":
    top_pickup_zones = data['pickup_zone'].value_counts().head(10)
    st.bar_chart(top_pickup_zones)

elif selected_question == "Top 10 busiest dropoff zones":
    top_dropoff_zones = data['dropoff_zone'].value_counts().head(10)
    st.bar_chart(top_dropoff_zones)

elif selected_question == "Most common pickup-dropoff zone pairs":
    common_pairs = data.groupby(['pickup_zone', 'dropoff_zone']).size().sort_values(ascending=False).head(10)
    st.write(common_pairs)

elif selected_question == "Average fare by pickup zone":
    avg_fare_pickup = data.groupby('pickup_zone')['fare'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_fare_pickup)

elif selected_question == "Average fare by dropoff zone":
    avg_fare_dropoff = data.groupby('dropoff_zone')['fare'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_fare_dropoff)

elif selected_question == "Distribution of the number of passengers":
    passenger_distribution = data['passengers'].value_counts()
    st.bar_chart(passenger_distribution)

elif selected_question == "Average fare per passenger count":
    avg_fare_per_passenger = data.groupby('passengers')['fare'].mean()
    st.line_chart(avg_fare_per_passenger)

elif selected_question == "Distribution of payment methods":
    payment_distribution = data['payment'].value_counts()
    st.bar_chart(payment_distribution)

elif selected_question == "Average fare by payment method":
    avg_fare_payment = data.groupby('payment')['fare'].mean()
    st.bar_chart(avg_fare_payment)

elif selected_question == "Distribution of trip distances":
    plt.figure(figsize=(10, 6))
    sns.histplot(data['distance'], bins=30, kde=True)
    st.pyplot(plt)

elif selected_question == "Outliers in trip distances and their characteristics":
    outliers = data[data['distance'] > data['distance'].quantile(0.95)]
    st.write(f"Outliers (top 5% of trip distances): {len(outliers)} trips")
    st.write(outliers[['pickup_zone', 'dropoff_zone', 'distance', 'fare']].head(10))
