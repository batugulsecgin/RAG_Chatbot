import ollama
from database import search_knowledge

MODEL_NAME = "llama3.1"


def generate_response(user_query, chat_history):
    """
    Kullanıcı sorgusunu ve sohbet geçmişini alarak RAG tabanlı hafızalı cevap üretir.
    """
    # 1. SORGU ZENGİNLEŞTİRME: SQLite aramasının zamirlerden etkilenmemesi için
    # eğer geçmişte bir kullanıcı sorusu varsa mevcut soruyla birleştiriyoruz.
    search_query = user_query
    user_messages = [msg["content"] for msg in chat_history if msg["role"] == "user"]

    if user_messages:
        # Son kullanıcı sorusunu mevcut soruya ekleyerek bağlamı (context) koruyoruz
        search_query = f"{user_messages[-1]} {user_query}"

    # 2. Veritabanında zenginleştirilmiş sorgu ile ara
    db_results = search_knowledge(search_query, limit=3)

    # 3. Bağlam metnini oluştur
    if db_results:
        context_text = "\n\n".join([f"Belge Başlığı: {title}\nİçerik: {content}" for title, content in db_results])
    else:
        context_text = "Veritabanında bu konuyla ilgili hiçbir kayıt bulunamadı."

    # 4. Sıkı Sistem Promptu
    system_prompt = f"""
    Sen bir şirket asistanısın ve sadece aşağıda sana sağlanan 'VERİTABANI KAYITLARI'nı kullanarak sorulara cevap vermelisin.
    Sohbet geçmişine dikkat et ve kullanıcının 'o oyun', 'bu kural' gibi atıflarını geçmişe göre anlamlandır.

    KURALLAR:
    1. Kullanıcının sorusunun cevabı kayıtlarda yoksa veya kayıtlar yetersizse, kesinlikle kendi genel kültürünü, internet bilgilerini veya yorumlarını kullanma.
    2. Bilgi yoksa SADECE şunu söyle: "Bu konu hakkında veritabanımda bilgi bulunmuyor."

    --- VERİTABANI KAYITLARI ---
    {context_text}
    ----------------------------
    """

    # 5. OLLAMA MESAJ DİZİSİNİ OLUŞTURMA
    # Yapı: [System Prompt] + [Eski Konuşmalar] + [Mevcut Kullanıcı Sorusu]
    messages = [{'role': 'system', 'content': system_prompt}]

    # Geçmiş mesajları aynen Ollama formatına aktar
    for msg in chat_history:
        messages.append({'role': msg['role'], 'content': msg['content']})

    # En son sorulan soruyu ekle
    messages.append({'role': 'user', 'content': user_query})

    # 6. Ollama'ya istek gönder
    try:
        response = ollama.chat(model=MODEL_NAME, messages=messages)
        return response['message']['content']
    except Exception as e:
        return f"LLM ile iletişim kurulurken bir hata oluştu: {str(e)}"