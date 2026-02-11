# Apriori Analizi
Excel verileri üzerinde Apriori algoritması kullanarak support, confidence ve lift analizi yapan Streamlit tabanlı bir veri madenciliği uygulaması.

Bu proje, Excel veri setleri üzerinde **Apriori birliktelik kuralı analizi**
yapmak için geliştirilmiş **Streamlit tabanlı bir veri madenciliği uygulamasıdır**.

Uygulama; verileri 0-1 formatına dönüştürerek Apriori algoritmasını uygular ve
elde edilen kuralları support, confidence  ve
lift  değerleri ile analiz eder.Ayrıca analiz sonuçları
grafiksel olarak görselleştirilir.




## Özellikler
- Excel dosyası yükleme
- Verilerin 0-1 formatına dönüştürülmesi
- Apriori algoritmasının uygulanması
- Birliktelik kurallarının çıkarılması
- Support, confidence ve lift değerlerinin gösterimi
- Analiz sonuçlarının grafiklerle görselleştirilmesi
- Streamlit ile etkileşimli arayüz


## Grafikler ve Görselleştirme
Uygulama içerisinde elde edilen birliktelik kuralları, kullanıcıların sonuçları
daha kolay yorumlayabilmesi için çeşitli grafikler ile sunulmaktadır:


-  **Histogram Grafiği**
-  **Support-Confidence Grafiği**  
-  **Ağ (Network) Grafiği**

## Kullanılan Kütüphaneler
- pandas: Veri okuma ve işleme
- streamlit: Web arayüzü ve kullanıcı etkileşimi
- mlxtend: Apriori algoritması ve birliktelik kuralları
- matplotlib: Histogram ve saçılım grafikleri
- networkx: Birliktelik kurallarının ağ grafiği ile gösterimi





  

## Kurulum ve Çalıştırma

Gerekli kütüphaneleri yükleyin:
```bash
pip install streamlit pandas mlxtend matplotlib
