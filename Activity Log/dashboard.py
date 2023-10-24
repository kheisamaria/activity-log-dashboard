import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the data
activity_data = pd.read_csv('dataset/SELMA_Activity Log.csv')

# Filter data for sleep activities
sleep_data = activity_data[activity_data['Activity Description'] == 'Sleep']

# Calculate total hours of sleep
total_sleep_hours = sleep_data['Duration (hours)'].sum()

# Define a list of positive moods
positive_moods = ['Excited', 'Happy', 'Refreshed', 'Overjoyed', 'Chill', 'Satisfied', 'Great', 'Productive']

# Filter the DataFrame to include only rows with positive moods
positive_data = activity_data[activity_data['How I feel'].isin(positive_moods)]

# Calculate the sum of the duration for positive moods
sum_duration_positive = positive_data['Duration (hours)'].sum()

# Streamlit App
st.markdown("<h1 style='text-align: center;'>The Power of Data: How I Used a Dashboard to Monitor and Improve My Activities in Two Weeks", unsafe_allow_html=True)


# Display total hours of sleep at the top with border and shadow
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between;">
        <div style="flex: 1; margin-right: 10px; border: 2px solid #e4e4e4; border-radius: 5px; padding: 10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);">
            <h3>Total Sleeping Time</h3>
            <p style="margin-top: -10px;">{total_sleep_hours:.0f} hours</p>
        </div>
        <div style="flex: 1; border: 2px solid #e4e4e4; border-radius: 5px; padding: 10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);">
            <h3>Positive Moods</h3>
            <p style="margin-top: -10px;">{sum_duration_positive:.0f} hours</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



# Remove trailing spaces from the 'activity description' column
activity_data['Activity Description'] = activity_data['Activity Description'].str.strip()

# Define categories and their corresponding activities
categories = {
    'Study/Class (Academic)': ['Class', 'Study', 'Make assignment (ReactJS Code)', 'Assignment (Data Analytics)', 'Assignment (AppDev)', 'Assignment (PM)',
                               'Assignment (Data Analytics Regression Activity)', 'Assignment (Consultation for Techno)', 'Assignment', 'Process documents'],
    'Sleep': ['Sleep'],
    'Phone/Entertainment': ['Phone', 'Watch Youtube Videos', 'Watch Movie'],
    'Family Time': ['Family Time'],
    'Travel/Commute': ['Travel to School', 'Walk to Room', 'Travel to Home', 'Walk to Class', 'Travel', 'Walk to consultation', 'Walk to gate', 'Wait for transportation', 'Travel home'],
    'Meals': ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Buy coffee'],
    'Others': ['Personal Care/Preparation', 'Organization Work']
}

# Convert column names to lowercase for consistency
activity_data.columns = activity_data.columns.str.lower()

# Categorize each activity
activity_data['category'] = 'Others'
for category, activities in categories.items():
    activity_data.loc[activity_data['activity description'].isin(activities), 'category'] = category

# Move activities with the word "assignment" to 'Study/Class (Academic)'
activity_data.loc[activity_data['activity description'].str.contains('assignment', case=False), 'category'] = 'Study/Class (Academic)'

# Calculate total duration for each category
category_durations = activity_data.groupby('category')['duration (hours)'].sum().reset_index()

# Merge 'Others', 'Personal Care/Preparation', and 'Organization Work' into 'Others' for the pie chart
category_durations.loc[category_durations['category'].isin(['Personal Care/Preparation', 'Organization Work']), 'category'] = 'Others'

# Section 1: Pie Chart for Activity Distribution
# st.subheader('Activity Distribution Pie Chart')
# Plot Pie Chart
fig_pie = px.pie(category_durations, values='duration (hours)', names='category', title='A Slice of Life: A Pie Chart of My Activities for October 10-24',
                 hole=0.3, color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig_pie)

# Section 2: Daily Sleep Duration Visualization
# st.title('Activity Analysis')

# Section 2.1: Daily Sleep Duration Visualization
# st.subheader('Daily Sleep Duration Visualization')
# Convert the "Date" column to datetime format
activity_data['date'] = pd.to_datetime(activity_data['date'], format='%d/%m/%Y')

# Extract day from the "Date" column
activity_data['Day'] = activity_data['date'].dt.day

# Filter data for sleep activities
sleep_data = activity_data[activity_data['activity description'] == 'Sleep']

# Group by day and sum the sleep durations
daily_sleep = sleep_data.groupby('Day')['duration (hours)'].sum().reset_index()

# Plot the data using Plotly Express
fig_sleep = px.line(daily_sleep, x='Day', y='duration (hours)', markers=True,
                    labels={'Duration (hours)': 'Total Sleep Duration (hours)'})
fig_sleep.update_layout(title='My Sleep Patterns in Two Weeks: A Chart of My Daily Sleep Duration and Quality for October 10-24', xaxis_title='October',
                        yaxis_title='Total Sleep Duration (hours)')

# Streamlit plot for sleep
# st.subheader('Daily Sleep Duration for Two Weeks in October')
st.plotly_chart(fig_sleep)

# Section 3: Word Cloud for Activity Descriptions
# st.title('Word Cloud for Activity Descriptions')
st.write('<div style="text-align: center;"><h5>How I Felt in Two Weeks: A Word Cloud of My Emotions for October 10-24</h5></div>', unsafe_allow_html=True)

# Join all the activity descriptions into a single string
text = ' '.join(activity_data['how i feel'].dropna())

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the word cloud using Matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

# Section 4: Mood Tally Table
# st.title('Mood Tally Table')
mood_tally = activity_data['how i feel'].value_counts().reset_index()
mood_tally.columns = ['Mood', 'Count']

# Section 4: Mood Tally Table (Top 10)
# st.title('Top 10 Mood Tally Table')
top10_mood_tally = mood_tally.head(10)

# Section 5: Mood Tally Bar Chart (Top 10)
# st.title('Top 10 Mood Tally Bar Chart')
fig_bar_top10 = px.bar(top10_mood_tally, x='Mood', y='Count', title='Two Weeks of Emotions: A Bar Chart of My Top 10 Moods and Their Frequencies',
                       labels={'Mood': 'Mood', 'Count': 'Count'},
                       color='Mood')
st.plotly_chart(fig_bar_top10)