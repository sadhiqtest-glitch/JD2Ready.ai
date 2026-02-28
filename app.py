# ============================================================
# SkillScan AI — Main Application File
# app.py
# ============================================================

# 'import' means we're loading a tool/library into our program
import streamlit as st    # The tool that creates our web interface
import os                  # Tool to read environment variables (like secret keys)
from groq import Groq      # Tool to talk to the Groq AI service

# ============================================================
# PAGE CONFIGURATION
# This sets the title, icon, and layout of our web page
# ============================================================
st.set_page_config(
    page_title="SkillScan AI",          # Tab title in browser
    page_icon="🎯",                      # Tab icon
    layout="centered",                   # Layout style
    initial_sidebar_state="collapsed"    # Hide sidebar by default
)

# ============================================================
# CUSTOM STYLING
# This makes our app look better with custom colors
# st.markdown lets us inject CSS (styling code) into our page
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .score-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PAGE HEADER
# These display text on the webpage
# ============================================================
st.markdown('<div class="main-header">🎯 SkillScan AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Paste any job description. Know exactly where you stand.</div>', unsafe_allow_html=True)

st.divider()  # Draws a horizontal line on the page

# ============================================================
# INPUT SECTION
# These create input boxes where users type their information
# ============================================================

# st.text_area creates a large text input box
# The text in quotes is the label shown above the box
# 'placeholder' is the grey helper text inside the box
# 'height' controls how tall the box is (in pixels)
skills_input = st.text_area(
    "📝 Your Current Skills",
    placeholder="Example: Python basics, Excel, SQL queries, data visualization with Matplotlib, basic Linux commands...",
    height=150
)

job_description = st.text_area(
    "💼 Job Description (paste the full JD here)",
    placeholder="Paste the full job description from LinkedIn, Indeed, or any job portal...",
    height=250
)

# ============================================================
# ANALYZE BUTTON
# When the user clicks this button, the analysis runs
# ============================================================

# st.button creates a clickable button
# It returns True when clicked, False when not clicked
# The 'if' statement below only runs when button is clicked
if st.button("🚀 Analyze My Fit", use_container_width=True, type="primary"):
    
    # Check if user actually filled in both boxes
    # 'strip()' removes empty spaces before checking
    if not skills_input.strip() or not job_description.strip():
        # st.error shows a red error message
        st.error("⚠️ Please fill in both your skills and the job description before analyzing.")
    
    else:
        # st.spinner shows a spinning animation while we wait for AI response
        with st.spinner("🤖 AI is analyzing your profile... (this takes 5-10 seconds)"):
            
            try:
                # ============================================================
                # GROQ AI INTEGRATION
                # This is where we send data to the AI and get back analysis
                # ============================================================
                
                # os.environ.get reads a secret variable stored in the environment
                # We never type the actual API key in code — that's a security rule!
                api_key = os.environ.get("GROQ_API_KEY")
                
                # Create a connection to the Groq service using our key
                client = Groq(api_key=api_key)
                
                # This is the instruction we give to the AI
                # Think of it as a very detailed question
                prompt = f"""
You are a professional career coach and technical recruiter with 10 years of experience.

A candidate has provided their current skills and a job description. Your job is to analyze the fit and provide a detailed, actionable report.

CANDIDATE'S CURRENT SKILLS:
{skills_input}

JOB DESCRIPTION:
{job_description}

Please provide your analysis in the following EXACT format. Do not deviate from this format:

## 🎯 MATCH SCORE: [X]%
[Write 2-3 sentences explaining the score honestly]

## ✅ SKILLS YOU ALREADY HAVE
[List each matching skill on a new line with a checkmark ✅ and brief note on how it applies]

## ❌ SKILLS YOU NEED TO DEVELOP  
[List each missing/gap skill on a new line with ❌ and note the priority: HIGH/MEDIUM/LOW]

## 📅 YOUR 30-DAY LEARNING ROADMAP
Week 1: [Specific focus area and 2-3 free resources]
Week 2: [Specific focus area and 2-3 free resources]
Week 3: [Specific focus area and 2-3 free resources]
Week 4: [Specific focus area and project to build]

## 💡 APPLICATION TIPS
[3-4 specific, actionable tips for this exact role]

## ⚡ ONE THING TO DO TODAY
[Single most impactful action the candidate should take right now]

Be honest, specific, and encouraging. Use only free learning resources (YouTube, freeCodeCamp, official docs, etc.)
"""
                
                # Send the prompt to Groq AI and get a response
                # 'messages' is the conversation — we send one user message
                # 'model' is which AI brain to use — llama3-8b-8192 is free and fast
                # 'max_tokens' limits how long the response can be
                # 'temperature' controls creativity: 0=robotic, 1=very creative, 0.7=balanced
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",      # 'user' means this is our message to AI
                            "content": prompt     # The actual message content
                        }
                    ],
                    model="llama3-8b-8192",       # Free, fast model
                    max_tokens=2000,               # Maximum length of AI response
                    temperature=0.7                # Creativity level
                )
                
                # Extract the text from the AI response
                # response.choices[0] = the first (and only) response
                # .message.content = the actual text of the response
                result = response.choices[0].message.content
                
                # ============================================================
                # DISPLAY RESULTS
                # ============================================================
                
                st.success("✅ Analysis Complete!")
                st.divider()
                
                # st.markdown displays formatted text (supports markdown syntax)
                st.markdown(result)
                
                st.divider()
                
                # Share/download section
                st.caption("💾 Want to save this analysis? Select all text above and copy it.")
                
            except Exception as e:
                # This catches any error that occurs
                # str(e) converts the error to readable text
                st.error(f"❌ Something went wrong: {str(e)}")
                st.info("💡 Common fix: Check that your GROQ_API_KEY is set correctly in your Hugging Face Space secrets.")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("🔒 We don't store your data. | Built with Streamlit + Groq AI | 100% Free")
