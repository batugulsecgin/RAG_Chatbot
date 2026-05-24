# 🤖 Local RAG Chatbot (Veritabanı Destekli AI Asistan)

Bu proje, tamamen yerel ortamda çalışan, gizlilik odaklı ve **RAG (Retrieval-Augmented Generation)** mimarisiyle geliştirilmiş bir sohbet botudur. Kullanıcıların sisteme yüklediği PDF ve TXT belgelerini okuyarak, **yalnızca bu belgelerdeki bilgilere dayanarak** soruları yanıtlar. 

Sistem, dışarıdan bilgi uydurmasını (hallucination) engelleyen sıkı bir prompt mühendisliği ve önceki sohbetleri hatırlamasını sağlayan bağlamsal hafıza (contextual memory) ile donatılmıştır.

## 🚀 Özellikler

- **%100 Yerel ve Ücretsiz:** Ollama altyapısı sayesinde hiçbir bulut servisine veri gönderilmez, API ücreti ödenmez.
- **Sıkı Sınırlandırma (Strict Grounding):** Chatbot genel kültürünü kullanmaz. Cevap veritabanında yoksa "Bilmiyorum" der.
- **Dinamik Dosya Yükleme:** Arayüz üzerinden kolayca PDF veya TXT dosyası yüklenebilir.
- **Otomatik Metin Parçalama (Chunking):** Yüklenen büyük belgeler, anlam bütünlüğü korunarak parçalara bölünür ve hızlı arama için optimize edilir.
- **Sohbet Hafızası:** Önceki soruları ve bağlamı hatırlar (Örn: "Peki bu oyunda kaç zar var?" sorusundaki 'bu oyun' referansını anlar).
- **Hafif Veritabanı:** Vektör veritabanları yerine SQLite FTS5 (Tam Metin Arama) kullanılarak yüksek performans elde edilmiştir.

## 🛠️ Kullanılan Teknolojiler

- **Dil:** Python
- **Arayüz:** Streamlit
- **LLM Sağlayıcısı:** Ollama (Llama 3.1)
- **Veritabanı:** SQLite (FTS5)
- **Belge İşleme:** PyPDF2

## 📦 Kurulum ve Çalıştırma

Projenin yerel bilgisayarınızda çalışabilmesi için aşağıdaki adımları izleyin.

### 1. Ollama Kurulumu
Bilgisayarınıza [Ollama](https://ollama.com/)'yı kurun ve terminalden kullanacağınız dil modelini indirin:
```bash
ollama run llama3.1
```

### 2. Projeyi Klonlayın
```bash
git clone https://github.com/KULLANICI_ADINIZ/rag-chatbot.git
cd rag-chatbot
```

### 3. Sanal Ortam Oluşturun ve Gereksinimleri Yükleyin
```bash
python -m venv venv
# Windows için:
venv\Scripts\activate

pip install streamlit ollama PyPDF2
```

### 4. Uygulamayı Başlatın
```bash
streamlit run app.py
```

## 📂 Proje Yapısı
- **app.py:** Streamlit arayüzü ve uygulamanın ana başlangıç noktası.

- **database.py:** SQLite veritabanı bağlantısı, tablo oluşturma, veri kaydetme ve arama fonksiyonları.

- **llm_handler.py:** Ollama API entegrasyonu, prompt oluşturma ve sohbet hafızası yönetimi.