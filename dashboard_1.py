import streamlit as st #important 
import pandas as pd
import matplotlib.pyplot as plt #graph
import plotly.express as px

st.image('obesity_2.jpg')

st.date_input("Select a date")

st.title("""Welcome to my Dashboard
This is my first time using streamlit.""")

#upload data
#upload_file = st.file_uploader("Please upload here:", type = 'csv')


#df = pd.read_csv(r"C:\Users\welcome\Desktop\BSMS1306\streamlit\Tips.csv")
df = pd.read_csv("obesity_level_rawdata.csv")
#df = pd.read_csv(upload_file)

#show data
st.subheader("Raw Data")
st.write(df)

#histogram
st.subheader("Histogram")
column = st.selectbox("Choose a column",df.columns)
fig, ax = plt.subplots(figsize = (10,6))
df[column].plot(kind = 'hist', ax =ax)
st.pyplot(fig)
#fig = px.histogram(df, x=column)
#fig.update_traces( marker = {"color":"purple", "line":{"color":"black","width":2}})
#st.plotly_chart(fig)

#Scatter chart
st.subheader("Scatter Chart")
x_column = st.selectbox("Choose x-axis column",df.columns)
y_column = st.selectbox("Choose y-axis column",df.columns)
fig, ax = plt.subplots(figsize = (10,6))
df.plot(kind = 'scatter', x=x_column, y=y_column, ax =ax)
st.pyplot(fig)

#fig = px.scatter(df, x=x_column, y = y_column,color ='sex' , color_discrete_sequence= ['yellow', 'red'])
#st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Data Preparation ---
# (Make sure 'df' is the name of your loaded DataFrame)

# Calculate BMI if it doesn't already exist
if 'BMI' not in df.columns and 'Weight' in df.columns and 'Height' in df.columns:
    df['BMI'] = df['Weight'] / (df['Height'] ** 2)

# Create Age Groups
if 'Age' in df.columns:
    # Define the boundaries and names for your age groups
    bins = [0, 29, 39, 49, 59, 100]
    labels = ['Under 30', '30-39', '40-49', '50-59', '60+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

    # --- 2. Interactive Bar Chart Section ---
    st.header("📊 Age Group vs. Average BMI")
    st.write("This interactive chart displays the calculated average Body Mass Index (BMI) across different age demographics.")

    # Calculate the average BMI for each age group
    df_avg_bmi = df.groupby('Age Group', as_index=False)['BMI'].mean()

    # Build the interactive bar chart using Plotly Express
    fig = px.bar(
        df_avg_bmi,
        x='Age Group',
        y='BMI',
        title='Average BMI by Age Group',
        labels={'BMI': 'Average BMI', 'Age Group': 'Age Cohort'},
        color='Age Group',             # Colors each bar differently
        text_auto='.2f',               # Displays the exact BMI value on top of each bar
        template='plotly_dark'         # Matches your dark theme dashboard
    )

    # Clean up layout appearance
    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Average BMI",
        showlegend=False               # Disables redundant legend since X-axis has labels
    )

    # Display the chart dynamically inside Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Could not find the 'Age' column in your dataset to generate age groups.")

import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Data Preparation & Classification ---
# (Assumes 'df' is your existing DataFrame)

# Ensure BMI is calculated
if 'BMI' not in df.columns and 'Weight' in df.columns and 'Height' in df.columns:
    df['BMI'] = df['Weight'] / (df['Height'] ** 2)

# Create Age Groups
if 'Age Group' not in df.columns and 'Age' in df.columns:
    bins = [0, 29, 39, 49, 59, 100]
    labels = ['Under 30', '30-39', '40-49', '50-59', '60+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

# Create Obesity Categories
if 'BMI' in df.columns and 'Age Group' in df.columns:
    bmi_bins = [0, 18.5, 24.9, 29.9, float('inf')]
    bmi_labels = ['Underweight', 'Normal weight', 'Overweight', 'Obese']
    df['Obesity Category'] = pd.cut(df['BMI'], bins=bmi_bins, labels=bmi_labels, right=True)

    # --- 2. Aggregating the Data ---
    df_counts = df.groupby(['Obesity Category', 'Age Group'], as_index=False).size()
    df_counts.rename(columns={'size': 'Count'}, inplace=True)

    # --- 3. Interactive Grouped Bar Chart ---
    st.header("📊 Obesity Categories vs. Age Distribution (Grouped)")
    st.write("This interactive grouped bar chart displays age groups side-by-side within each weight status category for easier direct comparison.")

    fig = px.bar(
        df_counts,
        x='Obesity Category',   
        y='Count',
        color='Age Group',       
        title='Age Group Comparison across Obesity Categories',
        labels={'Count': 'Number of People', 'Age Group': 'Age Cohort', 'Obesity Category': 'Weight Category'},
        category_orders={'Obesity Category': ['Underweight', 'Normal weight', 'Overweight', 'Obese']},
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Set2  
    )

    # Customize layout settings
    fig.update_layout(
        barmode='group',              # <--- CHANGED THIS FROM 'stack' TO 'group'
        xaxis_title="Obesity Category",
        yaxis_title="Number of Individuals",
        legend_title="Age Cohort",
        hovermode="x unified"         
    )

    # Render inside Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Required data columns are missing from the dataset.")

import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Data Validation ---
# (Assumes 'df' is your existing DataFrame)
# Adjust column names ('Technology Use', 'Physical Activity', 'Commute Type') 
# to match your exact dataset columns.

required_columns = ['Technology Use', 'Physical Activity', 'Commute Type']
if all(col in df.columns for col in required_columns):

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Interactive Scatter Plot Section ---
# Checking if the correct abbreviated columns exist in your DataFrame (df)
required_cols = ['FAF', 'TUE']

if all(col in df.columns for col in required_cols):
    st.header("📊 Technology Use vs. Physical Activity (FAF vs. TUE)")
    st.write("This interactive scatter plot explores the correlation between Time Using Technology Devices (TUE) and Physical Activity Frequency (FAF).")

    # Use 'MTRANS' for commute type if it exists, otherwise plot without color grouping
    color_col = 'MTRANS' if 'MTRANS' in df.columns else None

    fig = px.scatter(
        df,
        x='FAF',                         # Physical Activity Frequency on X-axis
        y='TUE',                         # Technology Use on Y-axis
        color=color_col,                 # Groups and colors points by Transportation Mode
        title='Correlation Between Technology Use (TUE) and Physical Activity (FAF)',
        labels={
            'FAF': 'Physical Activity Frequency (FAF)',
            'TUE': 'Time Using Technology Devices (TUE)',
            'MTRANS': 'Commute Type (MTRANS)'
        },
        opacity=0.7,                     # Helps visualize overlapping data points
        template='plotly_dark',          # Matches your dark dashboard theme
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    # Customize the appearance of the scatter plot markers
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
    
    fig.update_layout(
        xaxis_title="Physical Activity Frequency (FAF)",
        yaxis_title="Time Using Technology (TUE)",
        legend_title="Commute Type",
        hovermode="closest"
    )

    # Render inside Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Missing required columns. Please ensure 'FAF' and 'TUE' exist in your dataset.")