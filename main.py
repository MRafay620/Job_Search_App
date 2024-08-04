import streamlit as st
import requests

# Your Adzuna API credentials
API_ID = "e0b00986"
API_KEY = "d1def8e80d7f8aff5b1512cff4a7b60e"

def fetch_jobs(what, where, results_per_page=10):
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={API_ID}&app_key={API_KEY}&what={what}&where={where}&results_per_page={results_per_page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_jobs(jobs):
    for job in jobs['results']:
        st.markdown(f"### {job['title']}")
        st.markdown(f"**Company:** {job['company']['display_name']}")
        st.markdown(f"**Location:** {job['location']['display_name']}")
        st.markdown(f"**Description:** {job['description'][:200]}...")  # Displaying the first 200 characters
        st.markdown(f"[Read more]({job['redirect_url']})", unsafe_allow_html=True)
        st.markdown("---")

def main():
    st.markdown("""
        <style>
        .main {font-family: 'Helvetica';}
        .st-bb, .st-at, .css-2trqyj {background-color: rgba(30, 130, 230, 0.8);}
        h1, .st-af {color: rgba(30, 130, 230, 1);}
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔍 Job Search Portal")
    
    # Inputs for job search
    cols = st.columns(2)
    what = cols[0].text_input("What job are you looking for?", "software developer")
    where = cols[1].text_input("Where?", "London")
    search_button = st.button("Search Jobs")
    
    if search_button:
        st.subheader("Job Listings")
        jobs = fetch_jobs(what, where)
        if jobs and jobs.get('results'):
            display_jobs(jobs)
        else:
            st.error("No jobs found or failed to retrieve jobs.")

if __name__ == '__main__':
    main()
