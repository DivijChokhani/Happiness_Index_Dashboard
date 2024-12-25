import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Load data files
file_paths = ["C:\\Users\\Nivedita\\Downloads\\2015.csv", "C:\\Users\\Nivedita\\Downloads\\2016.csv", "C:\\Users\\Nivedita\\Downloads\\2017.csv", "C:\\Users\\Nivedita\\Downloads\\2018.csv", "C:\\Users\\Nivedita\\Downloads\\2019.csv"]
data_frames = []

# Load all datasets
for file in file_paths:
    try:
        df = pd.read_csv(file)
        data_frames.append(df)
    except Exception as e:
        st.error(f"Error loading file {file}: {e}")

# Combine datasets
data_combined = pd.concat(data_frames, keys=["2015", "2016", "2017", "2018", "2019"], names=["Year", "RowID"])
data_combined.reset_index(level=0, inplace=True)

# Streamlit dashboard setup
st.title("Interactive Data Dashboard")
st.sidebar.title("Options")

# Sidebar options
data_option = st.sidebar.selectbox("Choose a dataset:", ["2015", "2016", "2017", "2018", "2019", "All Combined"])

if data_option == "All Combined":
    selected_data = data_combined
else:
    selected_data = data_combined[data_combined["Year"] == data_option]

# Display dataset
st.subheader(f"Dataset: {data_option}")
st.write(selected_data.head())

# Visualizations
st.sidebar.subheader("Visualizations")
chart_type = st.sidebar.selectbox("Choose a chart type:", ["Bar Chart", "Line Chart", "Scatter Plot"])

if chart_type and not selected_data.empty:
    column_options = list(selected_data.columns)
    x_axis = st.sidebar.selectbox("Select X-axis:", column_options)
    y_axis = st.sidebar.selectbox("Select Y-axis:", column_options)

    if x_axis and y_axis:
        if chart_type == "Bar Chart":
            fig = px.bar(selected_data, x=x_axis, y=y_axis, color=y_axis)
        elif chart_type == "Line Chart":
            fig = px.line(selected_data, x=x_axis, y=y_axis, color=y_axis)
        elif chart_type == "Scatter Plot":
            fig = px.scatter(selected_data, x=x_axis, y=y_axis, color=y_axis)
        st.plotly_chart(fig)

# Filter section
st.sidebar.subheader("Filters")
columns_to_filter = st.sidebar.multiselect("Choose columns to filter:", list(selected_data.columns))
filters = {}

for column in columns_to_filter:
    unique_values = selected_data[column].unique()
    selected_values = st.sidebar.multiselect(f"Filter {column}:", unique_values)
    if selected_values:
        filters[column] = selected_values

# Apply filters
if filters:
    for column, values in filters.items():
        selected_data = selected_data[selected_data[column].isin(values)]

st.subheader("Filtered Data")
st.write(selected_data)

# Download option
st.sidebar.subheader("Download")
st.sidebar.download_button(
    label="Download Data as CSV",
    data=selected_data.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)
