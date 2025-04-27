
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Training Monitoring Dashboard", layout="wide")

training_records = pd.DataFrame({
    'ID': [1,2,3,4],
    'Phase': ['Creation', 'Approval', 'Completed', 'Completed'],
    'CompletionDate': ['2025-04-10', '2025-04-12', '2025-04-15', '2025-04-18'],
    'AccountabilityCode': ['OII', 'OIE', 'OIE', 'OIE']
})

sme_data = pd.DataFrame({
    'ID': [1,2,3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Availability': ['Available', 'Unavailable', 'Available'],
    'Expertise': ['Budgeting', 'Compliance', 'Training']
})

feedback_data = pd.DataFrame({
    'ID': [1,2,3,4],
    'Score': [4.5, 3.2, 4.8, 4.0],
    'Comments': ['Good session', 'Needs improvement', 'Excellent!', 'Well done'],
    'Trainee': ['John', 'Mike', 'Sara', 'Anna'],
    'LinkedRecord': [1,2,3,4]
})

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Training Records", "SME Status", "Feedback Analysis"])

st.title("Training Monitoring Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Trainings", value=len(training_records))
col2.metric("SMEs Available", value=sme_data[sme_data['Availability'] == 'Available'].shape[0])
col3.metric("Average Feedback Score", value=round(feedback_data['Score'].mean(),2))

st.markdown("---")

if page == "Overview":
    st.header("Quick Summary")
    overdue_trainings = training_records[training_records['Phase'] != 'Completed']
    if not overdue_trainings.empty:
        st.error(f"⚠️ {len(overdue_trainings)} training(s) delayed or still pending completion!")
    else:
        st.success("✅ All trainings completed on time!")

elif page == "Training Records":
    st.header("Training Records")
    phase_filter = st.selectbox("Filter by Phase", options=["All"] + training_records['Phase'].unique().tolist())

    if phase_filter != "All":
        filtered_data = training_records[training_records['Phase'] == phase_filter]
    else:
        filtered_data = training_records

    st.dataframe(filtered_data)

elif page == "SME Status":
    st.header("Subject Matter Experts (SMEs)")
    avail_filter = st.radio("Show SMEs who are:", ["All", "Available", "Unavailable"])

    if avail_filter == "Available":
        filtered_smes = sme_data[sme_data['Availability'] == 'Available']
    elif avail_filter == "Unavailable":
        filtered_smes = sme_data[sme_data['Availability'] == 'Unavailable']
    else:
        filtered_smes = sme_data

    st.dataframe(filtered_smes)

elif page == "Feedback Analysis":
    st.header("Training Feedback")
    st.subheader("Feedback Table")
    st.dataframe(feedback_data)

    st.subheader("Feedback Score Distribution")
    fig, ax = plt.subplots()
    ax.hist(feedback_data['Score'], bins=[0,2,3,4,5], color='skyblue', edgecolor='black')
    plt.title("Feedback Scores")
    plt.xlabel("Score")
    plt.ylabel("Number of Trainees")
    st.pyplot(fig)

    st.subheader("Top Training Sessions")
    top_feedback = feedback_data.sort_values('Score', ascending=False).head(3)
    st.dataframe(top_feedback)
    