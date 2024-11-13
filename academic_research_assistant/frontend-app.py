import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Configure API endpoint
API_BASE_URL = "http://localhost:8000"

def init_session_state():
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None
    if 'papers' not in st.session_state:
        st.session_state.papers = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def main():
    st.title("Academic Research Paper Assistant")
    init_session_state()

    # Sidebar for topic search
    with st.sidebar:
        st.header("Search Papers")
        topic = st.text_input("Enter research topic")
        if st.button("Search"):
            with st.spinner("Searching papers..."):
                response = requests.post(f"{API_BASE_URL}/search/{topic}")
                if response.status_code == 200:
                    st.session_state.papers = response.json()
                    st.session_state.current_topic = topic
                    st.success("Papers found!")

        # Year filter
        if st.session_state.current_topic:
            st.header("Filter by Year")
            years = list(range(2019, datetime.now().year + 1))
            start_year, end_year = st.select_slider(
                "Select year range",
                options=years,
                value=(years[0], years[-1])
            )

            if st.button("Apply Filter"):
                response = requests.get(
                    f"{API_BASE_URL}/papers/{st.session_state.current_topic}",
                    params={"start_year": start_year, "end_year": end_year}
                )
                if response.status_code == 200:
                    st.session_state.papers = response.json()

    # Main content area
    if st.session_state.current_topic:
        # Display papers in timeline
        st.header(f"Papers on {st.session_state.current_topic}")
        if st.session_state.papers:
            df = pd.DataFrame(st.session_state.papers)
            df['published_date'] = pd.to_datetime(df['published_date'])
            df = df.sort_values('published_date', ascending=False)
            
            for _, paper in df.iterrows():
                with st.expander(f"{paper['title']} ({paper['published_date'].strftime('%Y-%m-%d')})"):
                    st.write(f"**Abstract:** {paper['abstract']}")
                    st.write(f"**URL:** {paper['url']}")

        # Chat interface
        st.header("Ask Questions")
        user_question = st.text_input("Ask a question about the papers")
        if st.button("Send"):
            if user_question:
                # Add user question to chat history
                st.session_state.chat_history.append(("user", user_question))
                
                # Get answer from API
                response = requests.post(
                    f"{API_BASE_URL}/qa",
                    json={
                        "topic": st.session_state.current_topic,
                        "question": user_question,
                        "paper_ids": [p["id"] for p in st.session_state.papers]
                    }
                )
                
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.session_state.chat_history.append(("assistant", answer))

        # Display chat history
        st.header("Chat History")
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.write(f"🧑 **You:** {message}")
            else:
                st.write(f"🤖 **Assistant:** {message}")

        # Generate Review Paper
        if st.button("Generate Review Paper"):
            with st.spinner("Generating review paper..."):
                response = requests.post(f"{API_BASE_URL}/generate-review/{st.session_state.current_topic}")
                if response.status_code == 200:
                    review = response.json()["review"]
                    st.download_button(
                        "Download Review Paper",
                        review,
                        file_name=f"{st.session_state.current_topic}_review.md",
                        mime="text/markdown"
                    )

if __name__ == "__main__":
    main()
