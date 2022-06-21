

import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime


title=[]
link=[]
price=[]
current_price=[]
cargo=[]
cargo_information=[]
seller=[]
seller_count=[]
seller_link=[]
point=[]
favorite=[]
assesment_count=[]

headers={"User-Agent":"Tarayıcınızda  user agent araması yaparak kendi user agent bilginizi buraya ekleyin"}

#Trendyolda ürünler scroll yaptıkça yükleniyor ürünler yüklendikçede linkin sonuna 1,2... şeklinde scroll  numaraları ekleniyor
# 1 ile 497 arasındaki ürünleri alamsı için bir döngü oluşturdum 

for sayfaNo in range(1,497):

   
    url=("https://www.trendyol.com/sr?wc=103700&attr=279%7C270492&pi=") + str(sayfaNo)
    #web sitesine istek atıp gitmek istediğimiz adresi belirttik 
    r=requests.get(url, headers=headers)
    #sitenin içeriğini alıp lxml ile parçaladık
    soup=BeautifulSoup(r.content,"lxml")
    # bütün ürünleri aldım 
    ürünler=soup.find_all("div", attrs={"class" :"p-card-chldrn-cntnr"})
    
   # ürünlerin içinde dolaşarak istediğim bilgileri çektim 
    for ürün in ürünler:
      # ürünlerin linki aldım ama adresin başı olmadığı için onu ekledim 
      sonu= ürün.a.get("href")
      başi="https://www.trendyol.com"
      adres=başi+sonu
      link.append(adres.strip())
     
      
      fiyat=ürün.find("div", attrs={"class":"prc-box-orgnl"})
      if fiyat is not None:
         price.append(fiyat.text.replace(".",",").strip())
      else:
         price.append("Önceki Fiyat Yok")

      şimdiki_fiyat=ürün.find("div",attrs={"class":"prc-box-dscntd"})
      current_price.append(şimdiki_fiyat.text.replace(".",",").strip())
     
      kargo=ürün.find("div",attrs={"class":"stmp fc"})
      if kargo is not None:
         cargo.append(kargo.text.strip())
      else:
         cargo.append("KARGO BEDAVA DEĞİL")
         #linklerin içine girdik 
      ürün_r=requests.get(adres, headers=headers)
       
      ürün_soup=BeautifulSoup(ürün_r.content)
      kargo_bilgisi=ürün_soup.find("div",attrs={"class":"pr-dd-rs-w"})
      if kargo_bilgisi is not None:
        cargo_information.append(kargo_bilgisi.text)
      else:
        cargo_information.append("Kargo Bilgisi Yok")
        
      başlık=ürün_soup.find("h1",attrs={"class":"pr-new-br"})
      if başlık is not None:
           title.append(başlık.text.capitalize())
      else:
             title.append("Başlık Yok")
      
      satıcı=ürün_soup.find("a", attrs={"class", "merchant-text"})
      if satıcı is not None:
       seller.append(satıcı.text.strip().upper())
      else:
       seller.append("Satıcı Yok")
     
      favori=ürün_soup.find("div",attrs={"class":"fv-dt"})
      if favori is not None:
              favorite.append(favori.text.replace("favori","").strip() )
      else:
              favorite.append("Favoriye Ekleyen Yok")
      degerlendirme=ürün_soup.find("a",attrs={"class":"rvw-cnt-tx"})
      if degerlendirme is not None:
          assesment_count.append(degerlendirme.text.replace("Değerlendirme","").strip())
      else:
          assesment_count.append("Değerlendirme Yok")
      bugün=datetime.date.today()

      satıcı_sayısı=ürün_soup.find("div",attrs={"class","pr-omc-tl title"})
      if satıcı_sayısı is not None:
       seller_count.append(satıcı_sayısı.text[25:-1].strip())
      else:
       seller_count.append("Başka Satıcı Yok")
      
     
     # satıcının sayfasınıa gitmek için adresini aldık linklerde yine adresin başı olmadığı
     #için adresin başını ekledim
      satıcı_bilgisi=ürün_soup.find("div",attrs={"class","merchant-box-wrapper"})
      link_sonu=(satıcı_bilgisi.a.get("href"))
         
      satıcı_linki=başi+link_sonu
      seller_link.append(satıcı_linki)
      #adreslerin içine girip satıcı puanını aldım
      ürün_r2=requests.get(satıcı_linki)
       
      ürün_soup2=BeautifulSoup(ürün_r2.content)
      satıcı_puanı=ürün_soup2.find("div",attrs={"class","seller-store__score score-actual"})
     
      if satıcı_puanı is not None:
        point.append(satıcı_puanı.text.replace(".",",").strip())
      else:
        point.append("Satıcı Puanı Yok")
        

veri={"Urun_Linki":link,
      "Urun_Adi":title,
      "Fiyat":price,
      "Mevcut_Fiyat":current_price,
      "Kargo":cargo,
      "Kargo_Bilgisi":cargo_information,
      "Satici":seller,
      "Satici_Linki":seller_link,
      "Satici_Puani":point,
      "Satici_Sayisi":seller_count,
      "Favori_Sayisi":favorite,
      "Degerlendirme_Sayisi":assesment_count,
      "Tarih":bugün}

df=pd.DataFrame(veri)        
df.to_excel(r'C:\\Users\\aysem\\Desktop\\Proje.xlsx',  encoding='utf-8-sig') 




