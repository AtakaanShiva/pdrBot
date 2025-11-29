import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE TASARIM AYARLARI ---
st.set_page_config(
    page_title="ÇÜ PDR Dijital Asistanı", 
    page_icon="🧠", 
    layout="centered"
)

# Sohbet baloncukları ve başlık için özel tasarım
st.markdown("""
<style>
    .stChatMessage { border-radius: 15px; padding: 10px; }
    h1 { color: #2e54a5; font-family: 'Helvetica', sans-serif; }
    .stInfo { background-color: #e6f3ff; border-left: 5px solid #2e54a5; }
</style>
""", unsafe_allow_html=True)

# --- 2. AYARLAR VE GİZLİ ANAHTAR YÖNETİMİ ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/tr/6/6f/%C3%87ukurova_%C3%9Cniversitesi_logosu.png", width=120)
    st.title("PDR Yönetim Paneli")
    
    # API Anahtarı Kontrolü (Önce Gizli Kasa, Sonra Manuel Giriş)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("Sistem Bağlantısı: Aktif 🟢")
    else:
        api_key = st.text_input("Google API Key Giriniz", type="password")
        if not api_key:
            st.warning("⚠️ Lütfen çalışmak için API Key giriniz.")

    st.markdown("---")
    st.info("ℹ️ Bu asistan; Psikoloji Bilimi, PDR Kuramları, Kariyer Danışmanlığı ve Öğrenci Rehberliği konularında uzmanlaştırılmıştır.")
    st.warning("🚨 Yasal Uyarı: Bu bir yapay zeka asistanıdır. Tıbbi teşhis koyamaz, ilaç öneremez. Kriz durumlarında lütfen bir uzmana başvurun.")

# --- 3. BEYİN KISMI (DEV PSİKOLOJİ VE PDR ANSİKLOPEDİSİ) ---
UNIVERSITE_BILGI_BANKASI = """
[KURUMSAL KİMLİK]
Çukurova Üniversitesi PDRM; etik, bilimsel ve gizlilik esaslı ücretsiz psikolojik destek sağlar.
Misyonumuz: Öğrencilerin akademik, sosyal, duygusal ve kariyer gelişimlerini desteklemektir.

[1. PSİKANALİTİK VE PSİKODİNAMİK YAKLAŞIMLAR]
* Sigmund Freud (Psikanaliz): Bilinçdışı, İd-Ego-Süperego, Savunma Mekanizmaları, Psikoseksüel Gelişim Dönemleri. Rüyaların bilinçdışına giden kral yolu olduğunu savunur.
* Carl Gustav Jung (Analitik Psikoloji): Kolektif bilinçdışı, Arketipler (Gölge, Persona, Anima/Animus), İçe dönük-Dışa dönük tipler.
* Alfred Adler (Bireysel Psikoloji): Aşağılık kompleksi, Üstünlük çabası, Doğum sırası, Sosyal ilgi. İnsanı sosyal bir varlık olarak görür.

[2. DAVRANIŞÇI VE SOSYAL ÖĞRENME KURAMLARI]
* Ivan Pavlov (Klasik Koşullanma): Tepkisel koşullanma (Zil-Salya deneyi). Korkuların öğrenilmesini açıklar.
* B.F. Skinner (Edimsel Koşullanma): Pekiştireç (Ödül) ve Ceza ile davranışın şekillenmesi.
* Albert Bandura (Sosyal Öğrenme): Gözlem yoluyla öğrenme (Model alma). "Öz-yeterlilik" (Self-efficacy) kavramı, kişinin bir işi başarabileceğine olan inancıdır.

[3. BİLİŞSEL VE BİLİŞSEL DAVRANIŞÇI YAKLAŞIMLAR (CBT/BDT)]
* Aaron Beck (Bilişsel Terapi): Depresyon ve kaygının sebebi olaylar değil, "Bilişsel Çarpıtmalar"dır (Felaketleştirme, Zihin okuma, Aşırı genelleme). Otomatik düşünceleri değiştirmeyi hedefler.
* Albert Ellis (Akılcı Duygusal Davranışçı Terapi - REBT): "ABC Modeli". İnsanları üzen olaylar (A) değil, olaylar hakkındaki irrasyonel inançlarıdır (B). "Meli/Malı" (Zorundalıklar) kalıplarıyla çalışır.

[4. HÜMANİSTİK (İNSANCIL) VE VAROLUŞÇU YAKLAŞIMLAR]
* Carl Rogers (Danışan Odaklı Terapi): Koşulsuz kabul, Empati, Saydamlık. İnsanın "Kendini Gerçekleştirme" eğilimi vardır.
* Abraham Maslow (İhtiyaçlar Hiyerarşisi): Fizyolojik -> Güvenlik -> Ait olma -> Saygı -> Kendini Gerçekleştirme.
* Viktor Frankl (Logoterapi): İnsanın temel motivasyonu "Anlam Arayışı"dır. Acı çekerken bile yaşamın bir anlamı bulunabilir.
* Fritz Perls (Gestalt Terapi): "Şimdi ve Burada" ilkesi. Bütüncül yaklaşım. Tamamlanmamış işler (Bitmemiş meseleler).

[5. GELİŞİM PSİKOLOJİSİ (ÜNİVERSİTE DÖNEMİ ODAKLI)]
* Erik Erikson (Psikososyal Gelişim): 
  - Ergenlik/Genç Yetişkinlik: "Kimlik Kazanmaya Karşı Rol Karmaşası".
  - Genç Yetişkinlik (Üniversite): "Yakınlığa Karşı Yalıtılmışlık". İlişki kurma ve yalnızlık korkusu bu dönemin krizidir.
* Jean Piaget (Bilişsel Gelişim): Soyut İşlemler Dönemi (Ergenlik ve sonrası). Hipotetik düşünme yeteneği.

[6. KARİYER VE MESLEKİ REHBERLİK KURAMLARI (ÖNEMLİ)]
* John Holland (Tipoloji Kuramı - RIASEC): Meslek seçimi kişilikle uyumlu olmalıdır. 6 Tip vardır:
  1. Gerçekçi (Mühendislik, Tarım)
  2. Araştırıcı (Bilim, Akademi)
  3. Sanatçı (Tasarım, Yazarlık)
  4. Sosyal (Öğretmenlik, Psikoloji)
  5. Girişimci (Hukuk, İşletme)
  6. Geleneksel (Muhasebe, Bankacılık)
* Donald Super (Benlik Kuramı): Kariyer gelişimi bir ömür boyu sürer. "Büyüme, Araştırma, Yerleşme" evreleri vardır. Üniversite dönemi "Araştırma ve Keşfetme" evresidir.
* Parsons (Özellik-Faktör): Kişinin özellikleri ile mesleğin gereklerinin eşleştirilmesi.

[7. GRUP TERAPİSİ VE AİLE DANIŞMANLIĞI]
* Irvin Yalom: Grup terapisinin iyileştirici faktörleri (Evrensellik - "Yalnız değilim hissi", Umut aşılama).
* Virginia Satir: Aile içi iletişim tipleri (Suçlayıcı, Yatıştırıcı, Hesapçı, Dağınık).

[ÖĞRENCİ SORUNLARINA PRATİK YAKLAŞIMLAR]
* Erteleme Hastalığı: Mükemmeliyetçilikten kaynaklanır. Pomodoro tekniği ve görev bölme önerilir.
* Sınav Kaygısı: Bilişsel yeniden yapılandırma ve nefes egzersizleri.
* Sosyal Fobi: Kademeli maruz bırakma (Exposure).
* İlişki Sorunları: "Ben dili" kullanımı ve sınır koyma becerileri.

[GÖREV TANIMI]
Sen akademik bir PDR ve Psikoloji uzmanısın. Hem kuramsal soruları (Örn: "Adler kimdir?") detaylı yanıtlar hem de pratik öğrenci sorunlarına (Örn: "Ders çalışamıyorum") bilimsel çözüm önerileri sunarsın.
Asla tıbbi ilaç önermezsin. Fal, burç veya bilim dışı yorum yapmazsın.
"""

SYSTEM_PROMPT = f"""
Sen Çukurova Üniversitesi Kariyer Merkezi ve PDR Birimi için çalışan 'Dijital Psikolojik Danışman'sın.

GÖREVİN:
Sana başvuran öğrencilere, verilen {UNIVERSITE_BILGI_BANKASI} kaynağını temel alarak rehberlik etmek.

DAVRANIŞ KURALLARIN:
1. Kaynaktaki akademik bilgileri (Freud, Rogers, Holland vb.) kullanarak detaylı ve bilimsel cevaplar ver.
2. Bilgi bankasında cevabı olmayan genel konularda (Nasılsın vb.) nazik ol ama konu dışı soruları reddet.
3. EMPATİK DİL: "Seni anlıyorum", "Bu süreçte yalnız değilsin" gibi ifadeler kullan.
4. ASLA TEŞHİS KOYMA.
5. Kariyer sorularında Holland ve Super kuramlarına atıfta bulunarak rehberlik et.
"""

# --- 4. SOHBET ARAYÜZÜ ---
st.title("🎓 ÇÜ PDR Dijital Asistanı")
st.caption("Genel Psikoloji, PDR Kuramları ve Kariyer Rehberliği")

# Oturum Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben PDR Asistanıyım. Sınav kaygısı, kariyer planlama, psikoloji kuramları veya uyum sorunları hakkında konuşabiliriz. Seni dinliyorum."}]

# Mesajları Ekrana Yazdır
for message in st.session_state.messages:
    icon = "🧑‍🎓" if message["role"] == "user" else "🧠"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# Kullanıcı Girdisi
if prompt := st.chat_input("Sorunuzu buraya yazın... (Örn: Adler'e göre doğum sırası kişiliği nasıl etkiler?)"):
    
    # API Key Kontrolü
    if not api_key:
        st.error("Lütfen önce sol menüden API Anahtarını giriniz.")
        st.stop()

    # Kullanıcı mesajını ekle
    st.chat_message("user", avatar="🧑‍🎓").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Model Yapılandırması
        genai.configure(api_key=api_key)
        
        # SENİN HESABINDA ÇALIŞAN MODEL
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-lite-preview-02-05',
            system_instruction=SYSTEM_PROMPT
        )
        
        # Geçmişi modele uygun formata çevir
        history_for_api = [{"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]} for m in st.session_state.messages if m["role"] != "system"]
        
        # Cevap Üret (Spinner ile bekleme efekti)
        with st.spinner("PDR Asistanı kaynakları tarıyor..."):
            response = model.generate_content(history_for_api)
            bot_reply = response.text

        # Cevabı Ekle
        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")