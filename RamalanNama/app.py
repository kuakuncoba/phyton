import google.generativeai as genai
import streamlit as st

# ===============================
# PENGATURAN API KEY DAN MODEL
# ===============================

API_KEY = st.secrets["AIzaSyC77hvhU75Z_iKzn-dV7GmnhiUTm7EpuZw"]  # API key sebaiknya disimpan di Streamlit Secrets
MODEL_NAME = 'gemini-1.5-flash'

# ===============================
# KONTEKS AWAL CHATBOT
# ===============================

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

# ===============================
# INISIALISASI MODEL
# ===============================

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=0.4,
            max_output_tokens=500
        )
    )
    chat = model.start_chat(history=INITIAL_CHATBOT_CONTEXT)
except Exception as e:
    st.error(f"Kesalahan konfigurasi: {e}")
    st.stop()

# ===============================
# STREAMLIT UI
# ===============================

st.set_page_config(page_title="Chatbot Nama", page_icon="🔮")
st.title("🔮 Chatbot Peramal Nama")
st.markdown("Masukkan nama dan biarkan aku mengungkap artinya serta kepribadianmu! 😊")

# Simpan sesi chat di state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Form input pengguna
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Masukkan Nama:")
    submitted = st.form_submit_button("Kirim")

if submitted and user_input:
    st.session_state.messages.append(("Anda", user_input))

    try:
        response = chat.send_message(user_input)
        chatbot_reply = response.text or "Maaf, saya tidak bisa memberikan balasan."
    except Exception as e:
        chatbot_reply = f"Terjadi kesalahan: {e}"

    st.session_state.messages.append(("Chatbot", chatbot_reply))

# Tampilkan riwayat chat
for sender, message in st.session_state.messages:
    st.markdown(f"**{sender}:** {message}")
