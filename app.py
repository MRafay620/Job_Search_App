import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def main():
    st.markdown("""
        <style>
        .main {font-family: 'Helvetica';}
        .st-bb, .st-at, .css-2trqyj {background-color: rgba(30, 130, 230, 0.8);}
        h1, .st-af {color: rgba(30, 130, 230, 1);}
        </style>
    """, unsafe_allow_html=True)

    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.title("🔍 Job Search Portal")
        with st.form(key='searchform'):
            cols = st.columns(2)
            search_term = cols[0].text_input("Search Job", placeholder="Enter Job Title or Keyword")
            location = cols[1].text_input("Location", placeholder="Enter Location")
            submit_search = st.form_submit_button(label='Search')

        if submit_search:
            formatted_search_term = quote_plus(search_term)
            formatted_location = quote_plus(location)
            job_url = f"https://uk.indeed.com/jobs?q={formatted_search_term}&l={formatted_location}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            response = requests.get(job_url, headers=headers)
            if response.status_code == 200:
                html_jobs = response.text
                soup_jobs = BeautifulSoup(html_jobs, "html.parser")
                jobs = soup_jobs.find_all("div", class_="jobsearch-SerpJobCard")
                if jobs:
                    for job in jobs:
                        job_title = job.find("h2", class_="title").a.get('title')
                        company_name = job.find("span", class_="company").text.strip()
                        location = job.find("div", class_="recJobLoc")["data-rc-loc"]
                        summary = job.find("div", class_="summary").text.strip()

                        st.markdown("---")
                        st.subheader(job_title)
                        st.write("Company:", company_name)
                        st.write("Location:", location)
                        st.write("Summary:", summary)
                        st.markdown(f"[More Info](https://uk.indeed.com{job.find('a')['href']})", unsafe_allow_html=True)
                        st.markdown("---")
                else:
                    st.error("No jobs found. Please refine your search criteria.")
            else:
                st.error(f"Failed to retrieve job listings. Status code: {response.status_code}")

    else:
        st.subheader("About")
        st.info("This is a job search application created to simplify your job hunting process. Enter keywords and locations to find your desired job listings in the UK.")

if __name__ == '__main__':
    main()
