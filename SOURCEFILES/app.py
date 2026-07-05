import sys
import os
# Ensure SOURCEFILES directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import html
import json
from datetime import datetime, timezone
from dotenv import load_dotenv

# Reorganized custom imports
from assets.styles import apply_styles
from backend.ai.gemini_client import configure_gemini, transcribe_audio, evaluate_explanation
from backend.config.settings import CONCEPTS_FILE_PATH

# Load local environment variables
load_dotenv(override=True)
load_dotenv(".env.local", override=True)

# Setup Streamlit App configuration
st.set_page_config(
    page_title="VBCUA | Formative Knowledge Evaluator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_styles()

# Load reference academic concepts data from database
try:
    with open(CONCEPTS_FILE_PATH, "r", encoding="utf-8") as f:
        REFERENCE_CONCEPTS = json.load(f)
except Exception as e:
    st.error(f"Failed to load reference concepts database: {str(e)}")
    REFERENCE_CONCEPTS = []

# Session state initialization for history and audio
if "history" not in st.session_state:
    st.session_state.history = []
if "active_record" not in st.session_state:
    st.session_state.active_record = None
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "mime_type" not in st.session_state:
    st.session_state.mime_type = "audio/wav"
if "audio_source" not in st.session_state:
    st.session_state.audio_source = None
if "uploader_id" not in st.session_state:
    st.session_state.uploader_id = 0

def handle_upload():
    uploaded_file = st.session_state.get(f"uploader_{st.session_state.uploader_id}")
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        st.session_state.audio_bytes = file_bytes
        st.session_state.audio_source = 'upload'
        file_name_lower = uploaded_file.name.lower()
        if file_name_lower.endswith(".mp3"):
            st.session_state.mime_type = "audio/mp3"
        elif file_name_lower.endswith(".m4a"):
            st.session_state.mime_type = "audio/m4a"
        elif file_name_lower.endswith(".wav"):
            st.session_state.mime_type = "audio/wav"
        elif file_name_lower.endswith(".ogg"):
            st.session_state.mime_type = "audio/ogg"
        elif file_name_lower.endswith(".mpeg") or file_name_lower.endswith(".mpg"):
            st.session_state.mime_type = "audio/mpeg"
        else:
            st.session_state.mime_type = "audio/wav"
    else:
        st.session_state.audio_bytes = None
        st.session_state.audio_source = None

def handle_record():
    audio_record = st.session_state.get(f"recorder_{st.session_state.uploader_id}")
    if audio_record is not None:
        rec_bytes = audio_record.getvalue()
        st.session_state.audio_bytes = rec_bytes
        st.session_state.audio_source = 'record'
        st.session_state.mime_type = audio_record.type if hasattr(audio_record, 'type') else "audio/wav"
    else:
        st.session_state.audio_bytes = None
        st.session_state.audio_source = None

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067260.png", width=60)
    st.markdown("### VBCUA Settings")
    
    student_name = st.text_input("Candidate Name", value="Alexander Vance")
    student_grade = st.selectbox("Grade / Level", ["Undergraduate", "High School", "Graduate School", "Professional"])
    student_subject = st.text_input("Subject Area", value="Computer Science")
    
    st.markdown("---")
    if st.session_state.history:
        st.markdown("### Past Evaluations")
        for idx, rec in enumerate(st.session_state.history):
            if st.button(f"{rec['concept_title']} ({rec['score']}/100)", key=f"hist-{idx}"):
                st.session_state.active_record = rec
                st.rerun()
        st.markdown("---")
        if st.button("🗑️ Clear History", key="clear_history_btn", use_container_width=True):
            st.session_state.history = []
            st.session_state.active_record = None
            st.rerun()

# --- MAIN APP LAYOUT ---
st.markdown("<div class='main-title'>🧠 VBCUA | Formative Knowledge Evaluator</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Voice-Based Concept Understanding & Speech Evaluation Suite</div>", unsafe_allow_html=True)

# Select Category and Concept
col1, col2 = st.columns(2)
with col1:
    categories = sorted(list(set(c['category'] for c in REFERENCE_CONCEPTS))) if REFERENCE_CONCEPTS else []
    selected_category = st.selectbox("Select Subject Category", categories) if categories else None
with col2:
    category_concepts = [c for c in REFERENCE_CONCEPTS if c['category'] == selected_category] if selected_category else []
    concept_titles = [c['title'] for c in category_concepts]
    selected_concept_title = st.selectbox("Select Assessment Topic", concept_titles) if concept_titles else None

if selected_category and selected_concept_title:
    try:
        selected_concept = next(c for c in category_concepts if c['title'] == selected_concept_title)
    except StopIteration:
        st.error("Selected concept not found. Please try selecting another topic.")
        st.stop()

    # Display reference concept details card
    st.markdown(f"""
    <div class='custom-card'>
        <h4 style='margin-top:0; color:#f8fafc;'>Reference Description: {selected_concept['title']}</h4>
        <p style='font-size:13px; line-height:1.6; color:#94a3b8;'>{selected_concept['description']}</p>
        <div style='margin-top:12px;'>
            <strong style='font-size:11px; text-transform:uppercase; color:#94a3b8; display:block; margin-bottom:6px;'>Expected Topic Keywords</strong>
            {"".join(f"<span class='accent-badge'>{kw}</span>" for kw in selected_concept['keywords'])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Deliver Explanation")
    upload_tab, record_tab = st.tabs(["📤 Upload Audio File", "🎤 Record Audio"], key="active_tab")

    with upload_tab:
        uploaded_file = st.file_uploader(
            "Upload wav/mp3/m4a/mpeg audio file", 
            type=["wav", "mp3", "m4a", "ogg", "mpeg"], 
            key=f"uploader_{st.session_state.uploader_id}",
            on_change=handle_upload
        )
        # Display playback preview inside upload tab if uploaded
        if st.session_state.audio_source == 'upload' and st.session_state.audio_bytes is not None:
            st.markdown("#### Uploaded Audio Preview")
            st.audio(st.session_state.audio_bytes, format=st.session_state.mime_type)

    with record_tab:
        st.markdown("Click the microphone icon below to record your voice explanation.")
        audio_record = st.audio_input(
            "Record Audio",
            label_visibility="collapsed",
            key=f"recorder_{st.session_state.uploader_id}",
            on_change=handle_record
        )
        if st.session_state.audio_source == 'record' and st.session_state.audio_bytes is not None:
            st.markdown("#### Recorded Audio Preview")
            st.audio(st.session_state.audio_bytes, format=st.session_state.mime_type)

    # Perform evaluation triggers
    if st.session_state.audio_bytes is not None:
        st.markdown("---")
        col_eval, col_clear = st.columns([4, 1])
        with col_clear:
            if st.button("🗑️ Clear Audio", use_container_width=True):
                st.session_state.audio_bytes = None
                st.session_state.audio_source = None
                st.session_state.uploader_id += 1
                st.rerun()
                
        with col_eval:
            evaluate_clicked = st.button("Evaluate Explanation", type="primary", use_container_width=True)
            
        if evaluate_clicked:
            audio_size_mb = len(st.session_state.audio_bytes) / (1024 * 1024)
            if audio_size_mb > 25:
                st.error(f"Audio file is too large ({audio_size_mb:.1f} MB). Maximum supported size is 25 MB. Please upload a shorter recording.")
            elif not student_name.strip():
                st.error("Please enter your name in the sidebar before evaluating.")
            else:
                api_key = os.environ.get("GEMINI_API_KEY", "")
                if not api_key:
                    st.error("GEMINI_API_KEY environment variable is not configured. Please add your key to the .env or .env.local file in the project folder.")
                else:
                    # Configure Gemini API
                    configure_gemini(api_key)
                
                    with st.status("Analyzing explanation...", expanded=True) as status:
                        try:
                            # Step 1: Transcribe Audio File
                            status.update(label="Transcribing audio with Gemini...", state="running")
                            transcript = transcribe_audio(st.session_state.audio_bytes, st.session_state.mime_type)
                            
                            if not transcript:
                                status.update(label="Transcription failed", state="error")
                                st.error("Failed to generate voice transcript. The audio was empty, silent, or blocked by safety settings. Please try again with a clearer recording.")
                            else:
                                # Step 2: Semantic evaluation
                                status.update(label="Running conceptual analysis...", state="running")
                                result_json = evaluate_explanation(
                                    selected_concept['title'],
                                    selected_concept['description'],
                                    selected_concept['keywords'],
                                    transcript
                                )
                                
                                if not result_json:
                                    status.update(label="Analysis failed", state="error")
                                    st.error("Failed to parse evaluation result. The model response was empty, blocked by safety settings, or returned invalid JSON.")
                                else:
                                    # Package assessment record
                                    record = {
                                        "id": f"rec-{int(datetime.now(timezone.utc).timestamp())}",
                                        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                                        "studentName": student_name,
                                        "grade": student_grade,
                                        "subject": student_subject,
                                        "concept_title": selected_concept['title'],
                                        "transcript": transcript,
                                        "score": result_json.get("semanticSimilarity", 0),
                                        "level": result_json.get("difficultyLevel", "Beginner"),
                                        "summary": result_json.get("summary", ""),
                                        "strengths": result_json.get("strengths", []),
                                        "weaknesses": result_json.get("weaknesses", []),
                                        "missingIdeas": result_json.get("missingIdeas", []),
                                        "wrongStatements": result_json.get("wrongStatements", []),
                                        "suggestions": result_json.get("suggestions", []),
                                        "learningAdvice": result_json.get("learningAdvice", ""),
                                        "coveredKeywords": result_json.get("coveredKeywords", []),
                                        "missedKeywords": result_json.get("missedKeywords", [])
                                    }
                                    
                                    # Cap history to 15 items to prevent session state memory bloat
                                    st.session_state.history.insert(0, record)
                                    if len(st.session_state.history) > 15:
                                        st.session_state.history = st.session_state.history[:15]
                                        
                                    st.session_state.active_record = record
                                    
                                    status.update(label="Analysis complete!", state="complete")
                                    st.rerun()
                                    
                        except Exception as e:
                            status.update(label="Evaluation failed", state="error")
                            st.error(f"Failed to process evaluation. Error details: {str(e)}")

    # --- RESULTS REPORT CARD ---
    if st.session_state.active_record:
        rec = st.session_state.active_record
        
        st.markdown("---")
        st.markdown("### Academic Assessment Report")
        
        # Header Banner Info
        level_color = "#34d399" # Green for Advanced
        if rec['score'] < 60:
            level_color = "#f87171" # Red for Beginner
        elif rec['score'] < 85:
            level_color = "#fbbf24" # Orange for Intermediate
            
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%); border: 1px solid rgba(255, 255, 255, 0.08); padding: 24px; border-radius: 20px; display: flex; flex-direction: row; align-items: center; gap: 20px; backdrop-filter: blur(16px); box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);'>
            <div style='background: {level_color}15; border: 2px solid {level_color}; width: 85px; height: 85px; border-radius: 16px; display: flex; flex-direction: column; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 0 15px {level_color}30;'>
                <span style='font-size: 10px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;'>SCORE</span>
                <span style='font-size: 28px; color: {level_color}; font-weight: 800; line-height: 1;'>{rec['score']}</span>
            </div>
            <div>
                <span style='font-size: 11px; font-weight: 700; color: {level_color}; text-transform: uppercase; letter-spacing: 0.1em;'>{html.escape(str(rec['level']))} LEVEL</span>
                <h3 style='margin: 4px 0 0 0; color: #f8fafc; font-size: 20px;'>{html.escape(rec['concept_title'])} Understanding Report</h3>
                <p style='margin: 4px 0 0 0; font-size: 13px; color: #94a3b8;'>Candidate: <strong style="color: #e2e8f0;">{html.escape(rec['studentName'])}</strong> • Grade: {html.escape(rec['grade'])} • Date: {rec['date']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Columns for Transcript and Narrative Summary
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("""
            <div class='custom-card' style='height: 100%;'>
                <h4 style='margin-top:0; color:#f8fafc;'>Verbatim Audio Transcript</h4>
                <p style='font-size:13px; line-height:1.6; color:#e2e8f0; font-style:italic;'>"{}"</p>
            </div>
            """.format(html.escape(rec['transcript'])), unsafe_allow_html=True)
            
        with col_right:
            st.markdown("""
            <div class='custom-card' style='height: 100%;'>
                <h4 style='margin-top:0; color:#f8fafc;'>Assessment Narrative</h4>
                <p style='font-size:13px; line-height:1.6; color:#e2e8f0;'>{}</p>
            </div>
            """.format(html.escape(rec['summary'])), unsafe_allow_html=True)
            
        # Keywords Covered / Missed
        st.markdown("""
        <div class='custom-card'>
            <h4 style='margin-top:0; color:#f8fafc; margin-bottom:12px;'>Expected Keywords Coverage</h4>
            <div style='margin-bottom:12px;'>
                <strong style='font-size:10px; color:#34d399; text-transform:uppercase; display:block; margin-bottom:6px;'>Covered Keywords ({})</strong>
                {}
            </div>
            <div>
                <strong style='font-size:10px; color:#f87171; text-transform:uppercase; display:block; margin-bottom:6px;'>Omitted Keywords ({})</strong>
                {}
            </div>
        </div>
        """.format(
            len(rec['coveredKeywords']),
            "".join(f"<span class='accent-badge keyword-covered'>{html.escape(kw)}</span>" for kw in rec['coveredKeywords']) if rec['coveredKeywords'] else "<span style='font-size:13px; color:#94a3b8;'>None</span>",
            len(rec['missedKeywords']),
            "".join(f"<span class='accent-badge keyword-missed'>{html.escape(kw)}</span>" for kw in rec['missedKeywords']) if rec['missedKeywords'] else "<span style='font-size:13px; color:#94a3b8;'>None</span>"
        ), unsafe_allow_html=True)
        
        # Strengths, Gaps, Recommendations
        col_str, col_gap = st.columns(2)
        with col_str:
            st.markdown("<div class='custom-card' style='height: 100%;'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top:0; color:#f8fafc;'>Demonstrated Strengths</h4>", unsafe_allow_html=True)
            if rec['strengths']:
                for s in rec['strengths']:
                    st.markdown(f"<div style='font-size:13px; color:#e2e8f0; margin-bottom:6px;'>✨ {html.escape(s)}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='font-size:13px; color:#94a3b8;'>None recorded.</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_gap:
            st.markdown("<div class='custom-card' style='height: 100%;'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top:0; color:#f8fafc;'>Conceptual Gaps Detected</h4>", unsafe_allow_html=True)
            gaps_list = []
            if rec['weaknesses']:
                gaps_list.extend([f"Gap: {html.escape(w)}" for w in rec['weaknesses']])
            if rec['wrongStatements']:
                gaps_list.extend([f"Incorrect Statement: {html.escape(ws)}" for ws in rec['wrongStatements']])
            if rec['missingIdeas']:
                gaps_list.extend([f"Missing Concept: {html.escape(mi)}" for mi in rec['missingIdeas']])
                
            if gaps_list:
                for g in gaps_list:
                    st.markdown(f"<div style='font-size:13px; color:#f87171; margin-bottom:6px;'>⚠️ {g}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='font-size:13px; color:#34d399;'>No logical gaps or deviations detected. Good job!</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Recommendations and Study Advice
        st.markdown(f"""
        <div class='custom-card'>
            <h4 style='margin-top:0; color:#f8fafc;'>Improvement Recommendations</h4>
            <div style='margin-top:8px;'>
                {"".join(f"<div style='font-size:13px; color:#e2e8f0; margin-bottom:8px;'>✦ {html.escape(sug)}</div>" for sug in rec['suggestions'])}
            </div>
            <div style='margin-top:16px; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top:16px;'>
                <strong style='font-size:13px; color:#f8fafc; display:block; margin-bottom:6px;'>Personalized Study Advice</strong>
                <p style='font-size:13px; line-height:1.6; color:#94a3b8; margin:0;'>{html.escape(rec['learningAdvice'])}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Download Report Button
        report_json = json.dumps(rec, indent=4)
        st.download_button(
            label="📥 Download Assessment Report (JSON)",
            data=report_json,
            file_name=f"VBCUA_Report_{rec['studentName'].replace(' ', '_')}_{rec['concept_title'].replace(' ', '_')}.json",
            mime="application/json",
            type="secondary",
            use_container_width=True
        )
else:
    st.info("No concepts available. Please verify your concepts database is correctly loaded.")
