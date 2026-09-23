import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AutoGen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="AI Manual Testing Interviewer",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ROBUST LIGHT THEME & VISIBILITY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Force Pure White Background and Dark Slate Text Globally */
    .stApp {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Main Container Centering */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 6rem;
        max-width: 750px;
    }

    /* Custom Header Card */
    .header-card {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        border: 1px solid #e2e8f0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.4rem;
    }
    
    .header-subtitle {
        font-size: 14px;
        color: #64748b;
        font-weight: 400;
    }

    /* Force Visibility on Chat Messages and Paragraphs */
    [data-testid="stChatMessage"] {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }

    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stChatMessage"] div {
        color: #0f172a !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    /* Fix Chat Input Box Text Visibility */
    [data-testid="stChatInput"] textarea {
        color: #0f172a !important;
        background-color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
    }

    /* Spinner Text Visibility */
    .stSpinner div {
        color: #475569 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div class="header-card">
        <div class="header-title">🧪 AI Manual Testing Interviewer</div>
        <div class="header-subtitle">QA Engineer Technical Screening Panel (5-Question Flow)</div>
    </div>
""", unsafe_allow_html=True)

# --- AUTOGEN SETUP ---
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

evaluator_agent = AssistantAgent(
    name="qa_evaluator",
    model_client=model_client,
    system_message=(
        "You are a professional technical interviewer for a Junior Manual Testing / QA position. "
        "When the candidate provides an answer, you must start your response by saying 'Nice explanation!' "
        "followed by a very brief assessment or tip about their answer."
    ),
)

# --- INTERVIEW QUESTIONS LIST (5 QUESTIONS) ---
INTERVIEW_QUESTIONS = [
    "Question 1: Can you explain the main difference between black-box testing and white-box testing?",
    "Question 2: What is the difference between a bug, a defect, and a failure in software testing?",
    "Question 3: How would you design test cases for a standard e-commerce login page?",
    "Question 4: What is regression testing, and why is it crucial during software updates?",
    "Question 5: What is the difference between Smoke Testing and Sanity Testing?"
]

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.question_index = 0
    
    # Start with Question 1
    initial_greeting = f"Hello! Welcome to your technical interview for the Junior Manual Testing (QA) position. We will go through 5 core manual testing questions today.\n\nLet's start with **{INTERVIEW_QUESTIONS[0]}**"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Display Chat History with ChatGPT-style message components
for message in st.session_state.messages:
    avatar_icon = "💻" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# Only show chat input if interview is not finished
if st.session_state.question_index < len(INTERVIEW_QUESTIONS):
    # Watermark text embedded inside placeholder
    user_input = st.chat_input("Write your answer here...")

    if user_input:
        # 1. Append User Answer
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # 2. Evaluate current answer via AutoGen
        current_q = INTERVIEW_QUESTIONS[st.session_state.question_index]
        prompt = f"The question was: '{current_q}'. The candidate answered: '{user_input}'. Start your response with 'Nice explanation!' and add brief feedback."

        async def evaluate_answer():
            result = await evaluator_agent.run(task=prompt)
            return result.messages[-1].content

        with st.spinner("AI QA Interviewer is evaluating your answer..."):
            evaluation = asyncio.run(evaluate_answer())

        # 3. Advance to next question or finish
        st.session_state.question_index += 1

        if st.session_state.question_index < len(INTERVIEW_QUESTIONS):
            next_q = INTERVIEW_QUESTIONS[st.session_state.question_index]
            response_content = f"{evaluation}\n\n--- \n\nNow, let's move to the next question:\n\n**{next_q}**"
        else:
            # Final closing summary after 5th question
            response_content = f"{evaluation}\n\n--- \n\n🎉 **END OF INTERVIEW.** \n\nThank you for completing the technical screening panel for the Junior Manual Testing position! You have successfully answered all 5 questions."

        # Append Assistant Response
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        with st.chat_message("assistant", avatar="💻"):
            st.markdown(response_content)
        
        # Rerun to update state and lock input if finished
        st.rerun()
else:
    st.info("Interview session has concluded. Refresh the page if you'd like to restart.")