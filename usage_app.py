import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("UsageApp - Electrical Usage Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your utility CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:")
    st.write(df.head())
    
    # Ensure correct column name
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df['Start Datetime'] = pd.to_datetime(df['Start Datetime'])
    
    # Extract time components
    df['Month'] = df['Start Datetime'].dt.month
    df['Day'] = df['Start Datetime'].dt.day
    df['Hour'] = df['Start Datetime'].dt.hour
    
    # Monthly analysis
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthly_analysis = []

    for month in range(1, 13):
        month_df = df[df['Month'] == month]
        
        # Calculate total usage for each month
        total_usage = month_df['Net Usage'].sum()
        
        # Average 24-hour usage (Total usage divided by the number of days in the month)
        num_days_in_month = len(month_df['Day'].unique())
        avg_24hr_usage = total_usage / num_days_in_month
        
        # Daytime and nighttime usage
        total_daytime_usage = month_df[(month_df['Hour'] >= 6) & (month_df['Hour'] < 18)]['Net Usage'].sum()
        total_nighttime_usage = month_df[(month_df['Hour'] < 6) | (month_df['Hour'] >= 18)]['Net Usage'].sum()
        
        avg_daytime_usage = total_daytime_usage / num_days_in_month
        avg_nighttime_usage = total_nighttime_usage / num_days_in_month
        
        # Add results to list
        monthly_analysis.append({
            'Month': months[month-1],
            'Total Usage': total_usage,
            'Average 24 Hour Usage': avg_24hr_usage,
            'Average Daytime Usage': avg_daytime_usage,
            'Average Nighttime Usage': avg_nighttime_usage
        })
    
    # Display Monthly Analysis
    st.subheader("Monthly Analysis")
    monthly_df = pd.DataFrame(monthly_analysis)
    st.write(monthly_df)
    
    # Yearly analysis (average of the 12 months)
    yearly_24hr_usage = sum([entry['Average 24 Hour Usage'] for entry in monthly_analysis]) / 12
    yearly_daytime_usage = sum([entry['Average Daytime Usage'] for entry in monthly_analysis]) / 12
    yearly_nighttime_usage = sum([entry['Average Nighttime Usage'] for entry in monthly_analysis]) / 12
    
    st.subheader("Yearly Analysis")
    st.write(f"**Average 24 Hour Usage for the Year:** {yearly_24hr_usage:.2f} kWh")
    st.write(f"**Average Daytime Usage for the Year:** {yearly_daytime_usage:.2f} kWh")
    st.write(f"**Average Nighttime Usage for the Year:** {yearly_nighttime_usage:.2f} kWh")

    # Create an interactive bar graph for monthly total usage
    st.subheader("Monthly Usage Bar Graph")
    
    # Prepare the data for the monthly bar graph (showing total usage per month)
    monthly_usage_data = pd.DataFrame(monthly_analysis)
    fig = go.Figure(go.Bar(
        x=monthly_usage_data['Month'],
        y=monthly_usage_data['Total Usage'],
        hovertemplate='Month: %{x}<br>Total Usage: %{y} kWh',
        name='Total Usage'
    ))
    
    # Update layout for interactivity
    fig.update_layout(
        title="Monthly Electrical Usage",
        xaxis_title="Month",
        yaxis_title="Total Usage (kWh)",
        clickmode='event+select'
    )
    
    # Display the monthly graph
    st.plotly_chart(fig)
