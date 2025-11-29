import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="ÇÜ PDR Dijital Asistanı", 
    page_icon="🧠", 
    layout="centered"
)

# --- 2. GÖRÜNÜM AYARLARI (DARK MODE DÜZELTME) ---
st.markdown("""
<style>
    /* 1. ARKA PLANI ZORLA AÇIK RENK YAP */
    [data-testid="stAppViewContainer"] {
        background-color: #f4f6f9; /* Çok açık gri-mavi */
    }
    
    /* 2. TÜM YAZILARI ZORLA KOYU RENK YAP (Dark Mode engelleme) */
    h1, h2, h3, h4, h5, h6, p, li, div {
        color: #1f2937 !important; /* Koyu Gri/Siyah */
    }
    
    /* 3. SOHBET BALONCUKLARI */
    .stChatMessage {
        background-color: #ffffff !important; /* Baloncuk içi beyaz */
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }
    
    /* 4. GİRİŞ KUTUSU (INPUT) DÜZELTMESİ */
    .stTextInput input {
        color: #000000 !important; /* Yazılan yazı siyah olsun */
        background-color: #ffffff !important; /* Kutu içi beyaz olsun */
    }
    /* Placeholder (ipucu yazısı) rengi */
    ::placeholder {
        color: #6b7280 !important;
        opacity: 1;
    }

    /* 5. BAŞLIK RENGİ */
    h1 {
        color: #1e3a8a !important; /* Çukurova Mavisi */
    }
    
    /* 6. SIDEBAR (Sol Menü) */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    [data-testid="stSidebar"] * {
        color: #1f2937 !important; /* Sidebar yazıları siyah */
    }
</style>
""", unsafe_allow_html=True)

# --- 3. KENAR ÇUBUĞU VE AYARLAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/tr/6/6f/%C3%87ukurova_%C3%9Cniversitesi_logosu.png", width=120)
    st.title("Yönetim Paneli")
    
    # API Anahtarı Kontrolü (Secrets Öncelikli)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("Sistem Bağlantısı: Aktif 🟢")
    else:
        api_key = st.text_input("Google API Key", type="password")
        if not api_key:
            st.warning("⚠️ Lütfen API Key giriniz.")

    st.markdown("---")
    st.info("ℹ️ Bu asistan; Psikoloji Bilimi, PDR Kuramları ve Kariyer Rehberliği konularında uzmanlaştırılmıştır.")

# --- 4. BAŞLIK VE LOGO ALANI ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/tr/6/6f/%C3%87ukurova_%C3%9Cniversitesi_logosu.png", width=70)
with col2:
    st.title("ÇÜ PDR Dijital Asistanı")
    st.caption("Çukurova Üniversitesi Kariyer Merkezi & PDR Birimi Yapay Zeka Desteği")

st.markdown("---")

# --- 5. BEYİN KISMI (DEV BİLGİ BANKASI) ---
UNIVERSITE_BILGI_BANKASI = """
[KURUMSAL KİMLİK]
Çukurova Üniversitesi PDRM; etik, bilimsel ve gizlilik esaslı ücretsiz psikolojik destek sağlar.

[1. PSİKANALİTİK VE PSİKODİNAMİK YAKLAŞIMLAR]
* Sigmund Freud: Bilinçdışı, İd-Ego-Süperego, Savunma Mekanizmaları.
* Carl Gustav Jung: Kolektif bilinçdışı, Arketipler (Gölge, Persona, Anima/Animus).
* Alfred Adler: Aşağılık kompleksi, Üstünlük çabası, Doğum sırası, Sosyal ilgi.

[2. DAVRANIŞÇI VE SOSYAL ÖĞRENME]
* Ivan Pavlov: Klasik Koşullanma.
* B.F. Skinner: Edimsel Koşullanma (Ödül/Ceza).
* Albert Bandura: Sosyal Öğrenme (Model alma), Öz-yeterlilik.

[3. BİLİŞSEL VE BDT YAKLAŞIMLARI]
* Aaron Beck: Bilişsel Çarpıtmalar (Felaketleştirme, Zihin okuma).
* Albert Ellis: Akılcı Duygusal Terapi (ABC Modeli - İrrasyonel inançlar).

[4. HÜMANİSTİK VE VAROLUŞÇU]
* Carl Rogers: Koşulsuz kabul, Empati, Saydamlık.
* Abraham Maslow: İhtiyaçlar Hiyerarşisi.
* Viktor Frankl: Logoterapi (Anlam arayışı).

[5. KARİYER VE GELİŞİM]
* Erik Erikson: Psikososyal Gelişim (Kimlik kazanımı, Yakınlık kurma).
* John Holland (Kariyer): RIASEC Tipleri (Gerçekçi, Araştırıcı, Sanatçı, Sosyal, Girişimci, Geleneksel).

[GÖREV TANIMI]
Sen akademik bir PDR uzmanısın. Kuramsal soruları detaylı açıkla. Öğrenci sorunlarına (Sınav kaygısı, Erteleme vb.) bilimsel ve empatik yaklaş. Asla tıbbi teşhis koyma.
"""

SYSTEM_PROMPT = f"""
Sen Çukurova Üniversitesi PDR Asistanısın.
Görevin: {UNIVERSITE_BILGI_BANKASI} kaynağını kullanarak rehberlik etmek.
Kurallar:
1. Akademik ve bilimsel konuş.
2. Empatik ol ("Seni anlıyorum" de).
3. Kaynak dışına çıkma ama genel psikoloji sorularını yanıtla.
4. Asla teşhis koyma.
"""

# --- 6. SOHBET MANTIĞI ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben PDR Asistanıyım. Sınav kaygısı, kariyer planlama veya psikoloji kuramları hakkında konuşabiliriz."}]

for message in st.session_state.messages:
    # İkon seçimi
    icon = "🧑‍🎓" if message["role"] == "user" else "🧠"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    if not api_key:
        st.error("Lütfen önce API Anahtarını giriniz.")
        st.stop()

    st.chat_message("user", avatar="🧑‍🎓").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-lite-preview-02-05',
            system_instruction=SYSTEM_PROMPT
        )
        
        history_for_api = [{"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]} for m in st.session_state.messages if m["role"] != "system"]
        
        with st.spinner("PDR Asistanı kaynakları tarıyor..."):
            response = model.generate_content(history_for_api)
            bot_reply = response.text

        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
