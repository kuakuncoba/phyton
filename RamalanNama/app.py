import streamlit as st
import google.generativeai as genai
import os

# =====================================================================
# SETUP API KEY via environment variable (lebih aman untuk GitHub!)
# =====================================================================
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("API Key belum disetel. Harap tambahkan environment variable 'GEMINI_API_KEY'.")
    st.stop()

# Nama model Gemini
MODEL_NAME = 'gemini-1.5-flash'

# Konfigurasi API
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=0.4,
            max_output_tokens=500
        )
    )
except Exception as e:
    st.error(f"Terjadi kesalahan saat mengonfigurasi model: {e}")
    st.stop()

# Konteks awal chatbot
INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": ["Kamu adalah ahli penerjemah dan peramal nama. Ketika user memberi nama, jawab dengan: arti nama secara umum, asal bahasanya, dan tebakan kepribadian yang cocok berdasarkan nama tersebut. Jawaban harus ringkas, positif, dan menyenangkan. Abaikan input selain nama orang."]
    },
    {
        "role": "model",
        "parts": ["Hai! Kirimkan namamu atau nama temanmu, dan aku akan ungkap artinya serta ramalan kepribadiannya. 😊"]
    }
]

# Inisialisasi chat hanya sekali (menghindari reset)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=INITIAL_CHATBOT_CONTEXT)
    st.session_state.messages = []

# UI Streamlit
st.title("🔮 Penerjemah & Peramal Nama AI")
st.markdown("_Powered by Gemini API_")

# Riwayat Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Pengguna
prompt = st.chat_input("Ketik nama yang ingin diterjemahkan...")

if prompt:
    # Tampilkan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tanggapan chatbot
    with st.chat_message("assistant"):
        with st.spinner("Meramal nama..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                result = response.text
            except Exception as e:
                result = f"⚠️ Terjadi kesalahan: {e}"

        st.markdown(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
