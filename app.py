import streamlit as st
import google.generativeai as genai

# === Internal Model Setup ===
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# === Streamlit UI ===
st.set_page_config(page_title="Network Anomaly Detector")
st.title("Network Anomaly Detector")
st.write("Paste traffic summaries, NetFlow fields, or system-level network logs. The system will evaluate for unusual behavior or threats.")

# === Text input for logs or traffic summary
input_text = st.text_area(
    "Paste Network Features / Log Sample",
    height=250,
    placeholder="""
Example:
SrcIP: 192.168.1.10, DstIP: 8.8.8.8, Bytes: 429496, Packets: 4, Duration: 3s
Connection rate: 42/min, Protocol: TCP, SYN rate spike observed
""")

# === Analyze button
if st.button("Analyze for Anomalies"):
    if not input_text.strip():
        st.warning("Please paste network traffic summary or logs.")
    else:
        with st.spinner("Running anomaly analysis..."):
            prompt = f"""
You are a network behavior analysis engine trained on packet flow summaries and anomaly detection signals.

Analyze the following input and output:
1. Verdict: Normal / Suspicious / Malicious  
2. Anomaly Type: e.g. DDoS, Port Scan, Exfiltration, None  
3. Confidence Score: (0–95%)  
4. Reason: Technical summary in ≤ 2 lines

Input:
\"\"\"{input_text}\"\"\"

Output format:
Verdict: <...>  
Anomaly Type: <...>  
Confidence: <...>%  
Reason: <...>
"""

            response = model.generate_content(prompt)
            result = response.text.strip()

            st.subheader("🚨 Anomaly Analysis Result")
            st.text(result)
