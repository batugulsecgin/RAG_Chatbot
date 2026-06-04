import streamlit as st
import PyPDF2
from database import insert_knowledge, init_db
from llm_handler import generate_response

# Uygulama başlarken veritabanının var olduğundan emin ol
init_db()


def get_chunks(text, chunk_size=1500, overlap=200):
    """Metni anlam bütünlüğünü koruyarak parçalara böler."""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks


def extract_text_from_pdf(uploaded_file):
    """PDF dosyasının sayfalarını okuyup metne çevirir."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Veritabanı Destekli Chatbot")

# --- YAN MENÜ (SIDEBAR): DOSYA YÜKLEME ---
with st.sidebar:
    st.header("📂 Yeni Belge Yükle")
    st.write("Veritabanına PDF veya TXT formatında dosya yükleyebilirsiniz.")

    # Streamlit dosya yükleyici bileşeni
    uploaded_file = st.file_uploader("Bir dosya seçin", type=["pdf", "txt"])

    if uploaded_file is not None:
        # Kaydet butonu sadece dosya seçildiğinde görünür
        if st.button("Veritabanına Kaydet", use_container_width=True):
            with st.spinner("Dosya okunuyor ve veritabanına işleniyor..."):
                doc_title = uploaded_file.name
                doc_content = ""

                # Dosya türüne göre okuma işlemi
                if uploaded_file.type == "application/pdf":
                    doc_content = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    doc_content = uploaded_file.read().decode("utf-8")

                # İçerik başarıyla okunduysa parçala ve kaydet
                if doc_content.strip():
                    chunks = get_chunks(doc_content)
                    for i, chunk in enumerate(chunks):
                        insert_knowledge(f"{doc_title} (Bölüm {i + 1})", chunk)
                    st.success(f"'{doc_title}' başarıyla {len(chunks)} parça halinde eklendi!")
                else:
                    st.error("Dosya boş veya içerik okunamadı.")

    st.divider()
    st.info("💡 Sadece buraya eklediğiniz belgeler kullanılarak cevap üretilecektir.")
    st.info("💡 Chatbot'a yüklenmiş belge yabancı dilde ise sorunuzu yüklemiş olduğunuz belge ile aynı dilde sormak faydalı olabilir.")
    st.info("   Denediğiniz için teşekkürler... (Batu Gülseçgin)")

# --- ANA EKRAN: SOHBET ARAYÜZÜ (Hafızalı) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Veritabanındaki bilgilere dair bir soru sorun..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Düşünüyor ve geçmişi hatırlıyor..."):
            response = generate_response(prompt, st.session_state.messages)
            st.markdown(response)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})