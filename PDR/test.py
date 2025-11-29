import google.generativeai as genai

# API Key'i buraya yapıştıracaksın (terminalde soracak)
api_key = input("Lütfen API Key'inizi yapıştırıp Enter'a basın: ")
genai.configure(api_key=api_key)

print("\n--- ERİŞİLEBİLİR MODELLER LİSTESİ ---")
try:
    sayac = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            sayac += 1
    
    if sayac == 0:
        print("HİÇBİR MODEL BULUNAMADI! API Key hatalı veya yetkisiz.")
    else:
        print(f"\nToplam {sayac} model kullanabilirsiniz.")
        
except Exception as e:
    print("\nBİR HATA OLUŞTU:")
    print(e)
    print("\nOlası Sebep: API Key hatalı kopyalanmış olabilir.")

input("\nKapatmak için Enter'a bas...")