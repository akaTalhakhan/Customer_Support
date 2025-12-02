import streamlit as st
from crewai import Task, Crew, Agent
from crewai_tools.tools import ScrapeWebsiteTool
from bs4 import BeautifulSoup
import requests, os, time


class ProgressTracker:
    def __init__(self):
        self.steps = []

    def add_step(self, message):
        self.steps.append(message)

    def render(self):
        with st.expander("📋 Agent Step-by-Step Progress", expanded=False):
            for i, step in enumerate(self.steps[-15:], 1):
                st.markdown(f"**{i}.** {step}")


# Custom CSS for better styling
st.markdown("""
<style>
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom title styling */
    .main-title {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Custom input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Warning and success styling */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 10px;
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #667eea;
    }
    
    /* Custom card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-ready { background-color: #28a745; }
    .status-working { background-color: #ffc107; }
    .status-error { background-color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Page configuration with custom styling
st.set_page_config(
    page_title="CrewAI Chatbot", 
    layout="centered",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# Enhanced title section
st.markdown('<h1 class="main-title">🤖 AI Support Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by CrewAI • Get instant answers from any website</p>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions only using the provided website documentation."
        }
    ]

# Enhanced sidebar
with st.sidebar:
    st.markdown("### 🔐 Configuration")
    
    # API Key section with better styling
    st.markdown("**OpenAI API Key**")
    openai_key = st.text_input(
        "Enter your API key", 
        type="password",
        placeholder="sk-...",
        help="Your OpenAI API key is required to power the AI agents"
    )
    
    if openai_key:
        st.markdown('<span class="status-indicator status-ready"></span>**API Key Connected**', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-indicator status-error"></span>**API Key Required**', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Website URL section
    st.markdown("**Website to Analyze**")
    website_url = st.text_input(
        "Enter website URL", 
        placeholder="https://example.com",
        help="The website that will be scraped for information"
    )
    
    if website_url:
        st.markdown('<span class="status-indicator status-ready"></span>**Website Ready**', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-indicator status-error"></span>**Website URL Required**', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info section
    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown("""
        1. **Enter** your OpenAI API key
        2. **Provide** a website URL to scrape
        3. **Ask** your support questions
        4. **Get** AI-powered answers based on the website content
        """)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]  # Keep system message
        st.rerun()

# Main content area
if not openai_key:
    st.markdown("""
    <div class="info-card">
        <h3>🔑 API Key Required</h3>
        <p>Please enter your OpenAI API key in the sidebar to get started. Your key is used securely and not stored.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if not website_url:
    st.markdown("""
    <div class="info-card">
        <h3>🌐 Website URL Needed</h3>
        <p>Enter a website URL in the sidebar. The AI will scrape this website to answer your questions accurately.</p>
    </div>
    """, unsafe_allow_html=True)

# Set environment variables
os.environ["OPENAI_API_KEY"] = openai_key
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

# Display chat messages with enhanced styling
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
inquiry = st.chat_input("💬 Ask your support question here...")

if inquiry and website_url:
    st.session_state.messages.append({"role": "user", "content": inquiry})

    with st.chat_message("user"):
        st.markdown(inquiry)

    progress = ProgressTracker()

    # Enhanced spinner with custom text
    with st.spinner("🛠️ AI agents are analyzing and preparing your response..."):
        try:
            progress.add_step("🌐 Fetching website content...")
            soup = BeautifulSoup(requests.get(website_url, timeout=10).text, 'html.parser')
            text_content = soup.get_text(separator=' ', strip=True)
            preview = text_content[:1000] + "..."
            progress.add_step("✅ Website content retrieved successfully!")

            progress.add_step("🧠 Preparing context from chat messages...")
            context_block = "\n".join(
                f"<|{msg['role']}|> {msg['content']}"
                for msg in st.session_state.messages
                if msg["role"] in ["user", "assistant"]
            )

            progress.add_step("🛠️ Initializing support and QA agents...")
            support_agent = Agent(
                role="Senior Support Representative",
                goal="Answer user questions using only provided website documentation.",
                backstory="You're a helpful support agent. Use the scraped website to assist users. Don't hallucinate.",
                allow_delegation=False,
                verbose=True,
                model_parameters={"temperature": 0.5, "max_tokens": 500}
            )
            qa_agent = Agent(
                role="Support QA Reviewer",
                goal="Ensure support quality and accuracy based strictly on website content.",
                backstory="You review support responses to make sure they are helpful and accurate.",
                allow_delegation=False,
                verbose=True,
                model_parameters={"temperature": 0.5, "max_tokens": 300}
            )
            progress.add_step("🤖 Agents initialized and ready!")

            progress.add_step("📝 Creating tasks for support and QA agents...")
            docs_scrape_tool = ScrapeWebsiteTool(website_url=website_url)

            inquiry_resolution = Task(
                description=(
                    f"You are a support assistant responding only using information from a scraped website.\n\n"
                    f"Previous conversation:\n{context_block or 'None'}\n\n"
                    f"<|user|> {inquiry}\n\n"
                    f"Respond with a clear and complete answer in plain text, based only on the website content."
                ),
                expected_output="Plain text answer only.",
                tools=[docs_scrape_tool],
                agent=support_agent
            )

            qa_review = Task(
                description=(
                    f"Review the support agent's answer for accuracy and clarity based only on website content.\n\n"
                    f"Question:\n<|user|> {inquiry}\n\n"
                    f"Return a final improved plain text answer. No extra formatting."
                ),
                expected_output="Plain text final answer only.",
                agent=qa_agent
            )

            progress.add_step("📋 Tasks created successfully!")

            progress.add_step("🚀 Executing the CrewAI workflow...")
            crew = Crew(
                agents=[support_agent, qa_agent],
                tasks=[inquiry_resolution, qa_review],
                memory=True,
                verbose=True
            )

            for msg in [
                "🔍 Support agent is analyzing website content...",
                "✍️ Support agent is crafting your response...",
                "🧐 QA agent is reviewing for accuracy..."
            ]:
                progress.add_step(msg)
                time.sleep(0.6)

            result = crew.kickoff(inputs={"inquiry": inquiry})
            final_response = result.output if hasattr(result, "output") else str(result)

            st.session_state.messages.append({
                "role": "assistant",
                "content": final_response
            })

            with st.chat_message("assistant"):
                st.markdown(final_response)

            progress.add_step("✅ Response generated successfully!")

        except Exception as e:
            error_msg = f"❌ **Error occurred:** {str(e)}"
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
            with st.chat_message("assistant"):
                st.markdown(error_msg)
            progress.add_step(error_msg)

    # Render progress with enhanced styling
    progress.render()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #6c757d; font-size: 0.9rem;">Made with ❤️ using Streamlit & CrewAI</p>', 
    unsafe_allow_html=True
)