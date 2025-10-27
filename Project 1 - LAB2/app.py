import pygame
import sys
import os
from typing import List, Tuple, Dict
import random
from collections import deque

# Pygame başlatma
pygame.init()

class Lokasyon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, yeniX):
        self.x = yeniX
    
    def setY(self, yeniY):
        self.y = yeniY


class Karakter:
    def __init__(self, ad, tur, konum):
        self.ad = ad
        self.tur = tur
        self.konum = konum
        self.hedef = None
        self.yol = []
    
    def getAd(self):
        return self.ad
    
    def setAd(self, yeniAd):
        self.ad = yeniAd
    
    def getTur(self):
        return self.tur
    
    def setTur(self, yeniTur):
        self.tur = yeniTur
    
    def getKonum(self):
        return self.konum
    
    def setKonum(self, konum):
        # Yeni bir Lokasyon nesnesi oluştur
        self.konum = Lokasyon(konum.getX(), konum.getY())
        # Yolu sıfırla
        self.yol = []
    
    def EnKısaYol(self, labirent, baslangic, hedef):
        pass # Bu metot alt sınıflarda ezilmelidir.

class DarthVader(Karakter):
    def __init__(self, konum):
        super().__init__("Darth Vader", "Kötü", konum)
        self.hiz = 1
    
    def EnKısaYol(self, labirent, baslangic, hedef):
        #*BFS ile yolu bulur ve duvarları yok sayarak ilk adımı atar.

        internal_baslangic = (self.konum.getX(), self.konum.getY())
        hedef_konum = hedef
        satir = len(labirent)
        sutun = len(labirent[0])
        
        # BFS için gerekli veri yapıları
        ziyaret = [[False] * sutun for _ in range(satir)]
        onceki = [[None] * sutun for _ in range(satir)]
        
        # BFS kuyruğu
        kuyruk = deque([(internal_baslangic[0], internal_baslangic[1])])
        ziyaret[internal_baslangic[1]][internal_baslangic[0]] = True
        
        # Dört yönlü hareket
        yonler = [
            (0, -1),  # yukarı
            (1, 0),   # sağa
            (0, 1),   # aşağı
            (-1, 0)   # sola
        ]
        
        path_found = False
        # BFS algoritması
        while kuyruk:
            x, y = kuyruk.popleft()
            
            if (x, y) == hedef_konum:
                path_found = True
                break
            
            # Dört yönü kontrol et
            for dx, dy in yonler:
                yeni_x, yeni_y = x + dx, y + dy
                
                # Labirent sınırları içinde mi? (Duvar kontrolü yok)
                if not (0 <= yeni_x < sutun and 0 <= yeni_y < satir):
                    continue
                    
                # Daha önce ziyaret edildi mi?
                if ziyaret[yeni_y][yeni_x]:
                    continue
                
                ziyaret[yeni_y][yeni_x] = True
                onceki[yeni_y][yeni_x] = (x, y)
                kuyruk.append((yeni_x, yeni_y))
        
        # En kısa yolu oluştur
        yol = []
        if path_found:
            simdiki = hedef_konum
            while simdiki is not None:
                yol.append(simdiki)
                if simdiki == internal_baslangic:
                    break
                simdiki = onceki[simdiki[1]][simdiki[0]]
            yol.reverse()

        # Yolu bulduysak ve hareket mümkünse ilk adımı at
        if yol and len(yol) > 1:
            yeni_konum_tuple = yol[1]
            yeni_x, yeni_y = yeni_konum_tuple
            
            # Darth Vader için sadece sınır kontrolü yeterli
            if (0 <= yeni_x < len(labirent[0]) and 0 <= yeni_y < len(labirent)):
                yeni_lokasyon = Lokasyon(yeni_x, yeni_y)
                self.setKonum(yeni_lokasyon)
                self.yol = yol
                return True

        # Hareket edilemedi veya yol bulunamadı
        self.yol = [] # Yolu temizle
        return False # Hareket başarısız

class KyloRen(Karakter):
    def __init__(self, konum):
        super().__init__("Kylo Ren", "Kötü", konum)
        self.hiz = 2  # İki kare birden hareket edebilir

    def EnKısaYol(self, labirent, baslangic, hedef):
        #*BFS ile 2 karelik adımları önceliklendirerek yolu bulur ve duvar kontrolü yaparak ilk adımı atar.

        internal_baslangic = (self.konum.getX(), self.konum.getY())
        hedef_konum = hedef
        satir = len(labirent)
        sutun = len(labirent[0])

        ziyaret = [[False] * sutun for _ in range(satir)]
        onceki = [[None] * sutun for _ in range(satir)]

        kuyruk = deque([(internal_baslangic[0], internal_baslangic[1])])
        ziyaret[internal_baslangic[1]][internal_baslangic[0]] = True

        # Öncelik: 2 karelik hareketler, sonra 1 karelik
        yonler = [
            (0, -2), (2, 0), (0, 2), (-2, 0), # 2 kare
            (0, -1), (1, 0), (0, 1), (-1, 0)  # 1 kare
        ]
        
        path_found = False
        while kuyruk:
            x, y = kuyruk.popleft()

            if (x, y) == hedef_konum:
                path_found = True
                break

            for dx, dy in yonler:
                yeni_x, yeni_y = x + dx, y + dy
                gecerli_hareket = False

                # 2 karelik hareket kontrolü
                if abs(dx) == 2 or abs(dy) == 2:
                    ara_x, ara_y = x + dx // 2, y + dy // 2
                    if (0 <= ara_x < sutun and 0 <= ara_y < satir and
                        0 <= yeni_x < sutun and 0 <= yeni_y < satir and
                        labirent[ara_y][ara_x] != 0 and labirent[yeni_y][yeni_x] != 0):
                        gecerli_hareket = True
                # 1 karelik hareket kontrolü
                elif abs(dx) <= 1 and abs(dy) <= 1:
                    if (0 <= yeni_x < sutun and 0 <= yeni_y < satir and
                        labirent[yeni_y][yeni_x] != 0):
                         gecerli_hareket = True

                if gecerli_hareket and not ziyaret[yeni_y][yeni_x]:
                    ziyaret[yeni_y][yeni_x] = True
                    onceki[yeni_y][yeni_x] = (x, y)
                    kuyruk.append((yeni_x, yeni_y))
        
        # En kısa yolu oluştur
        yol = []
        if path_found:
            simdiki = hedef_konum
            while simdiki is not None:
                yol.append(simdiki)
                if simdiki == internal_baslangic:
                    break
                simdiki = onceki[simdiki[1]][simdiki[0]]
            yol.reverse()

        # Yolu bulduysak ve hareket mümkünse ilk adımı at
        if yol and len(yol) > 1:
            yeni_konum_tuple = yol[1]
            yeni_x, yeni_y = yeni_konum_tuple
            
            # Kylo Ren duvar kontrolü yapar
            if (0 <= yeni_x < len(labirent[0]) and 0 <= yeni_y < len(labirent) and
                (labirent[yeni_y][yeni_x] == 1 or labirent[yeni_y][yeni_x] == 2)):
                
                yeni_lokasyon = Lokasyon(yeni_x, yeni_y)
                self.setKonum(yeni_lokasyon) # Konumu GÜNCELLE
                self.yol = yol # Yolu sakla (opsiyonel)
                return True # Hareket başarılı

        # Hareket edilemedi veya yol bulunamadı
        self.yol = [] # Yolu temizle
        return False # Hareket başarısız

class Stormtrooper(Karakter):
    def __init__(self, konum):
        super().__init__("Stormtrooper", "Kötü", konum)
        self.hiz = 1  # Sadece bir kare hareket edebilir

    def EnKısaYol(self, labirent, baslangic, hedef):
        #*BFS ile yolu bulur ve duvar kontrolü yaparak ilk adımı atar.

        internal_baslangic = (self.konum.getX(), self.konum.getY())
        hedef_konum = hedef
        satir = len(labirent)
        sutun = len(labirent[0])

        # BFS için gerekli veri yapıları
        ziyaret = [[False] * sutun for _ in range(satir)]
        onceki = [[None] * sutun for _ in range(satir)]

        # BFS kuyruğu
        kuyruk = deque([(internal_baslangic[0], internal_baslangic[1])])
        ziyaret[internal_baslangic[1]][internal_baslangic[0]] = True

        # Tek kare hareket için yönler
        yonler = [
            (0, -1), (1, 0), (0, 1), (-1, 0) 
        ]
        
        path_found = False
        # BFS algoritması
        while kuyruk:
            x, y = kuyruk.popleft()

            if (x, y) == hedef_konum:
                path_found = True
                break

            # Dört yönü kontrol et
            for dx, dy in yonler:
                yeni_x, yeni_y = x + dx, y + dy

                # Sınır ve duvar kontrolü (0 = duvar)
                if not (0 <= yeni_x < sutun and 0 <= yeni_y < satir and labirent[yeni_y][yeni_x] != 0):
                    continue

                # Ziyaret kontrolü
                if ziyaret[yeni_y][yeni_x]:
                    continue

                ziyaret[yeni_y][yeni_x] = True
                onceki[yeni_y][yeni_x] = (x, y)
                kuyruk.append((yeni_x, yeni_y))

        # En kısa yolu oluştur
        yol = []
        if path_found:
            simdiki = hedef_konum
            while simdiki is not None:
                yol.append(simdiki)
                if simdiki == internal_baslangic:
                    break
                simdiki = onceki[simdiki[1]][simdiki[0]]
            yol.reverse()
            
        # Yolu bulduysak ve hareket mümkünse ilk adımı at
        if yol and len(yol) > 1:
            yeni_konum_tuple = yol[1]
            yeni_x, yeni_y = yeni_konum_tuple
            
            # Stormtrooper duvar kontrolü yapar
            if (0 <= yeni_x < len(labirent[0]) and 0 <= yeni_y < len(labirent) and
                (labirent[yeni_y][yeni_x] == 1 or labirent[yeni_y][yeni_x] == 2)): # Sadece yol veya başlangıç noktası
                
                yeni_lokasyon = Lokasyon(yeni_x, yeni_y)
                self.setKonum(yeni_lokasyon) # Konumu GÜNCELLE
                self.yol = yol # Yolu sakla (opsiyonel)
                return True # Hareket başarılı

        # Hareket edilemedi veya yol bulunamadı
        self.yol = [] # Yolu temizle
        return False # Hareket başarısız

class MasterYoda(Karakter):
    def __init__(self, konum):
        super().__init__("Master Yoda", "İyi", konum)
        self.maksimum_kalp = 6  # 3 tam kalp (her kalp 2 birim)
        self.kalp = self.maksimum_kalp
        self.yakalanma_sayisi = 0
    
    def getKalp(self):
        return self.kalp / 2  # Kalp sayısını döndür (2 birim = 1 kalp)
    
    def yakalanma(self):
        # Yakalanma durumunda can kaybı

        self.yakalanma_sayisi += 1
        self.kalp -= 1  # Her yakalanmada 1 birim (yarım kalp) azalt
        
        # Canlar bittiyse oyun biter
        if self.kalp <= 0:
            return True
            
        return False

class LukeSkywalker(Karakter):
    def __init__(self, konum):
        super().__init__("Luke Skywalker", "İyi", konum)
        self.maksimum_kalp = 3
        self.kalp = self.maksimum_kalp
        self.yakalanma_sayisi = 0
    
    def getKalp(self):
        return self.kalp
    
    def yakalanma(self):
        # Yakalanma durumunda can kaybı

        self.yakalanma_sayisi += 1
        self.kalp -= 1
        
        # Canlar bittiyse oyun biter
        if self.kalp <= 0:
            return True
            
        return False


class OyunHarita:
    # Renkleri tanımla
    ARKAPLAN = (176, 224, 230)    # Açık mavi arkaplan
    SIYAH = (0, 0, 0)             # Duvarlar
    BEYAZ = (255, 255, 255)       # Yollar
    SARI = (255, 255, 0)          # Başlangıç noktası
    MAVI = (0, 0, 255)            # Kapılar
    ACIK_MAVI = (135, 206, 235)   # Açık mavi bölgeler
    KIRMIZI = (255, 0, 0)         # Kalpler için
    YESIL = (0, 255, 0)           # İyi karakterler için
    HUCRE_BOYUTU = 40             # Hücre boyutunu küçült
    OFFSET_X = 125                # Sağ ve soldan boşluğu artır
    OFFSET_Y = 75                # Üst ve alttan boşluğu artır
    FONT_BOYUT = 32

    def __init__(self):
        # Pygame başlatma kontrolü ve başlatma
        if not pygame.get_init():
            pygame.init()
        
        # Display modu ayarla
        self.screen = pygame.display.set_mode((1440, 960))
        
        # Müzik modülünü başlat
        pygame.mixer.init()
        
        self.labirent = []
        self.kotu_karakterler = []
        self.baslangic_konum = None
        self.kapi_konumlari = {}
        self.hedef_konum = None
        self.karakter_kapi_eslesmesi = {}
        
        self.WINDOW_WIDTH = None
        self.WINDOW_HEIGHT = None
        self.secilen_karakter = None
        self.font = pygame.font.Font(None, self.FONT_BOYUT)
        self.baslangic_koordinat = (6, 5)
        self.aktif_karakterler = []
        self.mesafe_font = None
        self.arkaplan = None
        self.oyun_bitti = False
        self.oyun_kazanildi = False
        self.aktif_karakter = None
        
        # Karakter resimlerini tutacak sözlük
        self.karakter_resimleri = {}
        
        # Resimleri yükle
        self.kalp_resmi = self.resim_yukle("kalp.png", (30, 30))
        self.yarim_kalp_resmi = self.resim_yukle("yarim_kalp.png", (30, 30))
        self.siyah_kalp_resmi = self.resim_yukle("bos_kalp.png", (30, 30))
        self.kupa_resmi = self.resim_yukle("kupa.png", (30, 30))
        self.ok_resmi = self.resim_yukle("ok.png", (30, 30))
        
        # Müziği yükle
        self.yakalanma_sesi = self.ses_yukle("yakalanma.wav")
        
        # Karakter resimlerini yükle
        self.resimleri_yukle()
    
    def resim_yukle(self, dosya_adi, boyut):
        # Belirtilen dosyadan resmi yükler ve boyutlandırır

        try:
            tam_yol = os.path.abspath(dosya_adi)
            if not os.path.exists(tam_yol):
                return None
                
            resim = pygame.image.load(tam_yol)
            if not resim:
                return None
                
            resim = resim.convert_alpha()
            resim = pygame.transform.scale(resim, boyut)
            return resim
            
        except Exception as e:
            return None
    
    def resimleri_yukle(self):
        # Tüm karakter resimlerini yükler

        karakter_boyutu = (self.HUCRE_BOYUTU - 10, self.HUCRE_BOYUTU - 10)
        
        karakterler = {
            "MasterYoda": "yoda.png",
            "LukeSkywalker": "luke.png",
            "DarthVader": "vader.png",
            "KyloRen": "kylo.png",
            "Stormtrooper": "trooper.png"
        }
        
        for karakter_adi, dosya_adi in karakterler.items():
            try:
                tam_yol = os.path.abspath(dosya_adi)
                if not os.path.exists(tam_yol):
                    continue
                    
                resim = pygame.image.load(tam_yol)
                if not resim:
                    continue
                    
                resim = resim.convert_alpha()
                resim = pygame.transform.scale(resim, karakter_boyutu)
                self.karakter_resimleri[karakter_adi] = resim
                
            except Exception:
                continue
    
    def harita_oku(self, dosya_adi):
        try:
            with open(dosya_adi, 'r', encoding='utf-8') as dosya:
                # Önce karakter bilgilerini oku
                satir = dosya.readline().strip()
                
                # Karakter bilgilerini oku
                while satir and satir.startswith('Karakter:'):
                    parcalar = satir.split(',')
                    karakter_tipi = parcalar[0].split(':')[1].strip()
                    kapi_ismi = parcalar[1].split(':')[1].strip()
                    self.kotu_karakterler.append((karakter_tipi, kapi_ismi))
                    satir = dosya.readline().strip()
                
                # Şimdi labirent verilerini okumaya başla
                # İlk labirent satırını işle
                self.labirent = []
                sayilar = [int(x) for x in satir.split()]
                self.labirent.append(sayilar)
                
                # Kalan labirent satırlarını oku
                for satir in dosya:
                    if satir.strip():  # Boş satır değilse
                        sayilar = [int(x) for x in satir.strip().split()]
                        self.labirent.append(sayilar)
                
                # Pencere boyutlarını ayarla
                satir_sayisi = len(self.labirent)
                sutun_sayisi = len(self.labirent[0])
                self.WINDOW_WIDTH = (sutun_sayisi * self.HUCRE_BOYUTU) + (self.OFFSET_X * 2)  # Her iki yandan offset
                self.WINDOW_HEIGHT = (satir_sayisi * self.HUCRE_BOYUTU) + (self.OFFSET_Y * 2)    # Üst ve alttan offset
                self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
                pygame.display.set_caption("Labirent Oyunu")
                
                self.konumlari_bul()
                return True
                
        except Exception as e:
            print(f"Hata: Harita dosyası okunamadı - {e}")
            return False
    
    def konumlari_bul(self):
        # Haritadaki özel konumları bulur

        self.hedef_konum = None
        self.kotu_karakterler = []
        self.kapi_konumlari = {}
        
        for y in range(len(self.labirent)):
            for x in range(len(self.labirent[y])):
                deger = self.labirent[y][x]
                
                if deger == 2:  # İyi karakter kapısı
                    self.baslangic_koordinat = Lokasyon(x, y)
                elif deger == 3:  # Kötü karakter kapısı
                    kapi_konum = Lokasyon(x, y)
                    self.kapi_konumlari[f"Kapi_{x}_{y}"] = kapi_konum
                elif deger == 1:  # Hedef/kupa konumu
                    if x == 13 and y == 9:
                        self.hedef_konum = Lokasyon(x, y)
    
    def karakter_olustur(self):
        # İyi ve kötü karakterleri oluşturur

        if self.secilen_karakter == "MasterYoda":
            self.aktif_karakter = MasterYoda(self.baslangic_koordinat)
        else:
            self.aktif_karakter = LukeSkywalker(self.baslangic_koordinat)
        
        self.aktif_karakterler = [self.aktif_karakter]
        
        kotu_karakter_sayisi = random.randint(2, 3)
        kapilar = list(self.kapi_konumlari.items())
        random.shuffle(kapilar)
        
        self.karakter_kapi_eslesmesi.clear()
        
        for i in range(kotu_karakter_sayisi):
            kapi_adi, konum = kapilar[i]
            karakter_tipi = random.choice(["DarthVader", "KyloRen", "Stormtrooper"])
            kotu_karakter = None
            
            if karakter_tipi == "DarthVader":
                kotu_karakter = DarthVader(konum)
            elif karakter_tipi == "KyloRen":
                kotu_karakter = KyloRen(konum)
            else:
                kotu_karakter = Stormtrooper(konum)
            
            self.karakter_kapi_eslesmesi[kotu_karakter] = konum
            self.aktif_karakterler.append(kotu_karakter)
    
    def harita_ciz(self):
        # Ekranı temizle
        self.screen.fill(self.ARKAPLAN)

        # Labirenti çiz
        for y in range(len(self.labirent)):
            for x in range(len(self.labirent[y])):
                rect = pygame.Rect(
                    self.OFFSET_X + (x * self.HUCRE_BOYUTU),
                    self.OFFSET_Y + (y * self.HUCRE_BOYUTU),
                    self.HUCRE_BOYUTU,
                    self.HUCRE_BOYUTU
                )

                # Hücreleri çiz
                if self.labirent[y][x] == 1:
                    pygame.draw.rect(self.screen, (173, 216, 230), rect)  # Yollar açık mavi
                elif self.labirent[y][x] == 2:
                    pygame.draw.rect(self.screen, self.SARI, rect)  # Başlangıç noktası sarı
                else:
                    pygame.draw.rect(self.screen, self.BEYAZ, rect)  # Duvarlar beyaz

                # Hücre çerçeveleri
                pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)

        # Kötü karakterlerin en kısa yollarını çiz
        if self.aktif_karakterler and not self.oyun_bitti:
            # Yarı şeffaf kırmızı yüzey oluştur
            yol_yuzey = pygame.Surface((self.HUCRE_BOYUTU, self.HUCRE_BOYUTU), pygame.SRCALPHA)
            pygame.draw.rect(yol_yuzey, (255, 0, 0, 128), yol_yuzey.get_rect())

            for karakter in self.aktif_karakterler:
                if karakter.getTur() == "Kötü":
                    yol = karakter.yol
                    karakter_mevcut_konum = (karakter.konum.getX(), karakter.konum.getY())
                    
                    try:
                        # Karakterin yol listesindeki mevcut indeksini bul
                        current_index = yol.index(karakter_mevcut_konum)
                    except ValueError:
                        # Karakterin konumu yolda bulunamazsa (beklenmedik durum), çizim yapma
                        continue 
                        
                    # Mevcut konumdan sonraki yolu ve ara adımları çiz
                    if yol and len(yol) > current_index + 1:
                        for i in range(current_index + 1, len(yol)):
                            konum_to_draw = yol[i]
                            prev_konum_in_path = yol[i-1]
                            
                            # Bir sonraki hedef kareyi çiz
                            rect = pygame.Rect(
                                self.OFFSET_X + (konum_to_draw[0] * self.HUCRE_BOYUTU),
                                self.OFFSET_Y + (konum_to_draw[1] * self.HUCRE_BOYUTU),
                                self.HUCRE_BOYUTU,
                                self.HUCRE_BOYUTU
                            )
                            self.screen.blit(yol_yuzey, rect)

                            # Eğer 2 karelik bir zıplama ise, aradaki kareyi de çiz 
                            # (Bu ara kare karakterin mevcut konumu olamaz çünkü i > current_index)
                            dx = konum_to_draw[0] - prev_konum_in_path[0]
                            dy = konum_to_draw[1] - prev_konum_in_path[1]
                            if abs(dx) == 2 or abs(dy) == 2:
                                ara_x = prev_konum_in_path[0] + dx // 2
                                ara_y = prev_konum_in_path[1] + dy // 2
                                ara_rect = pygame.Rect(
                                    self.OFFSET_X + (ara_x * self.HUCRE_BOYUTU),
                                    self.OFFSET_Y + (ara_y * self.HUCRE_BOYUTU),
                                    self.HUCRE_BOYUTU,
                                    self.HUCRE_BOYUTU
                                )
                                self.screen.blit(yol_yuzey, ara_rect)

        # Hücre değerlerini çiz
        for y in range(len(self.labirent)):
            for x in range(len(self.labirent[y])):
                rect = pygame.Rect(
                    self.OFFSET_X + (x * self.HUCRE_BOYUTU),
                    self.OFFSET_Y + (y * self.HUCRE_BOYUTU),
                    self.HUCRE_BOYUTU,
                    self.HUCRE_BOYUTU
                )
                deger = self.labirent[y][x]
                font = pygame.font.Font(None, 16)
                text = font.render(str(deger), True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.bottomright = (rect.right - 2, rect.bottom - 2)
                self.screen.blit(text, text_rect)

        # Giriş ve çıkış noktalarını ekle
        giris_cikis = {'A': (0, 5), 'B': (4, 0), 'C': (12, 0), 'D': (13, 5), 'E': (4, 10)}
        ok_yonleri = {
            'A': (1, 0), 
            'B': (0, -1), 
            'C': (0, -1),  
            'D': (-1, 0), 
            'E': (0, 1)   
        }
        
        for harf, (gx, gy) in giris_cikis.items():
            # Kapı hücresini çiz
            rect = pygame.Rect(
                self.OFFSET_X + (gx * self.HUCRE_BOYUTU),
                self.OFFSET_Y + (gy * self.HUCRE_BOYUTU),
                self.HUCRE_BOYUTU,
                self.HUCRE_BOYUTU
            )
            pygame.draw.rect(self.screen, (0, 0, 139), rect)  # Koyu mavi giriş alanı
            
            # Harfi çiz
            font = pygame.font.Font(None, 30)
            text = font.render(harf, True, (255, 255, 255))
            self.screen.blit(text, rect.move(10, 10))
            
            # Ok resmini çiz
            if self.ok_resmi:
                # Ok yönüne göre döndürme açısını belirle
                yon = ok_yonleri[harf]
                if yon == (1, 0):  
                    aci = 0
                elif yon == (-1, 0): 
                    aci = 180
                elif yon == (0, 1): 
                    aci = 90
                else:                
                    aci = -90
                
                # Ok resmini döndür
                donmus_ok = pygame.transform.rotate(self.ok_resmi, aci)
                
                # Ok pozisyonunu ayarla (labirentin dışında)
                ok_rect = donmus_ok.get_rect()
                if yon == (1, 0): 
                    ok_rect.midright = (self.OFFSET_X + (gx * self.HUCRE_BOYUTU) - 10, rect.centery)
                elif yon == (-1, 0):  
                    ok_rect.midleft = (self.OFFSET_X + ((gx + 1) * self.HUCRE_BOYUTU) + 10, rect.centery)
                elif yon == (0, 1):   
                    ok_rect.midtop = (rect.centerx, self.OFFSET_Y + ((gy + 1) * self.HUCRE_BOYUTU) + 10)
                else:          
                    ok_rect.midbottom = (rect.centerx, self.OFFSET_Y + (gy * self.HUCRE_BOYUTU) - 10)
                
                self.screen.blit(donmus_ok, ok_rect)

        # Karakterleri çiz
        if self.aktif_karakterler:
            for karakter in self.aktif_karakterler:
                x = self.OFFSET_X + (karakter.konum.getX() * self.HUCRE_BOYUTU)
                y = self.OFFSET_Y + (karakter.konum.getY() * self.HUCRE_BOYUTU)
                karakter_resmi = self.karakter_resimleri.get(karakter.__class__.__name__)
                
                if karakter_resmi:
                    resim_rect = karakter_resmi.get_rect()
                    resim_rect.center = (x + self.HUCRE_BOYUTU // 2, y + self.HUCRE_BOYUTU // 2)
                    self.screen.blit(karakter_resmi, resim_rect)
                else:
                    renk = self.YESIL if karakter.getTur() == "İyi" else self.KIRMIZI
                    boyut = self.HUCRE_BOYUTU // 2 if karakter.getTur() == "İyi" else self.HUCRE_BOYUTU // 3
                    pygame.draw.circle(self.screen, renk, (x + self.HUCRE_BOYUTU // 2, y + self.HUCRE_BOYUTU // 2), boyut)

        # Canları çiz
        self.canlari_ciz()

        # Kupayı çiz
        if self.kupa_resmi:
            # Çıkış noktasının koordinatlarını hesapla
            kupa_x = self.OFFSET_X + ((13 + 1) * self.HUCRE_BOYUTU)  # 13 + 1 çünkü sağına yerleştiriyoruz
            kupa_y = self.OFFSET_Y + (9 * self.HUCRE_BOYUTU)  # 9. satır
            kupa_rect = self.kupa_resmi.get_rect()
            kupa_rect.midleft = (kupa_x, kupa_y + self.HUCRE_BOYUTU // 2)  # Hücrenin orta sol noktasına hizala
            self.screen.blit(self.kupa_resmi, kupa_rect)

        # Oyun durumu mesajları
        if self.oyun_bitti:
            self.mesaj_goster("GAME OVER!")
        elif self.oyun_kazanildi:
            self.mesaj_goster("KAZANDINIZ!")

        # Ekranı güncelle
        pygame.display.flip()
        
    def canlari_ciz(self):
        # "Canlar:" yazısı için font ve konum ayarla
        font = pygame.font.Font(None, 36)  
        text = font.render("Canlar:", True, self.SIYAH)
        text_rect = text.get_rect()
        text_rect.topright = (self.WINDOW_WIDTH - 150, 2)  # Y koordinatını yukarıda tut
        self.screen.blit(text, text_rect)
        
        # Kalpleri çiz
        if self.kalp_resmi and self.yarim_kalp_resmi and self.siyah_kalp_resmi:
            for i in range(3):  # 3 tam kalp pozisyonu
                kalp_x = self.WINDOW_WIDTH - 120 + (i * 40)  # Kalpler arası mesafeyi koru
                kalp_y = 2  # Y koordinatını yukarıda tut
                kalp_rect = self.kalp_resmi.get_rect()
                kalp_rect.topleft = (kalp_x, kalp_y)
                
                if isinstance(self.aktif_karakter, MasterYoda):
                    # MasterYoda için özel kalp çizimi (6 birimlik sistem)
                    kalan_kalp = self.aktif_karakter.kalp - (i * 2)  # Her pozisyon için kalan kalp miktarı
                    if kalan_kalp >= 2:
                        # Tam kalp (2 birim veya daha fazla)
                        self.screen.blit(self.kalp_resmi, kalp_rect)
                    elif kalan_kalp == 1:
                        # Yarım kalp (1 birim)
                        self.screen.blit(self.yarim_kalp_resmi, kalp_rect)
                    else:
                        # Boş kalp (0 birim)
                        self.screen.blit(self.siyah_kalp_resmi, kalp_rect)
                else:
                    # Diğer karakterler için normal kalp çizimi
                    if i < self.aktif_karakter.kalp:
                        self.screen.blit(self.kalp_resmi, kalp_rect)
                    else:
                        self.screen.blit(self.siyah_kalp_resmi, kalp_rect)

    def karakter_hareket(self, yon):
        # İyi karakteri hareket ettirir ve sonrasında kötü karakterleri hareket ettirir

        if self.aktif_karakter and not self.oyun_bitti:
            yeni_x = self.aktif_karakter.konum.getX() + yon[0]
            yeni_y = self.aktif_karakter.konum.getY() + yon[1]
            
            # Hareket geçerliyse
            if (0 <= yeni_x < len(self.labirent[0]) and 
                0 <= yeni_y < len(self.labirent) and 
                (self.labirent[yeni_y][yeni_x] == 1 or self.labirent[yeni_y][yeni_x] == 2)):
                
                # İyi karakteri hareket ettir
                self.aktif_karakter.konum.setX(yeni_x)
                self.aktif_karakter.konum.setY(yeni_y)
                
                # Kupaya ulaşma kontrolü
                if (yeni_x == self.hedef_konum.getX() and 
                    yeni_y == self.hedef_konum.getY()):
                    self.oyun_kazanildi = True
                    return
                
                # Kötü karakterleri hareket ettir
                self.kotu_karakterleri_hareket_ettir()
                
                # Yakalanma kontrolü
                for kotu_karakter in self.aktif_karakterler:
                    if (kotu_karakter.getTur() == "Kötü" and
                        kotu_karakter.konum.getX() == self.aktif_karakter.konum.getX() and
                        kotu_karakter.konum.getY() == self.aktif_karakter.konum.getY()):
                        
                        # Yakalanma durumunda can kaybı ve konumları sıfırla
                        oyun_bitti = self.karakter_yakalandi()
                        
                        # Yakalanma sonrası tüm karakterlerin hedeflerini sıfırla
                        for karakter in self.aktif_karakterler:
                            if karakter.getTur() == "Kötü":
                                karakter.hedef = None
                                karakter.yol = []
                        
                        if oyun_bitti:
                            self.oyun_bitti = True
                        return

    def kotu_karakterleri_hareket_ettir(self):
        # Her kötü karakterin EnKisaYol metodunu çağırarak hareket etmesini sağlar.
        
        for kotu_karakter in self.aktif_karakterler:
            if kotu_karakter.getTur() == "Kötü":
                # Hedefi belirle
                hedef_tuple = (self.aktif_karakter.konum.getX(), 
                               self.aktif_karakter.konum.getY())
                baslangic_tuple = (kotu_karakter.konum.getX(), kotu_karakter.konum.getY())
                
                # EnKisaYol'u çağır (hareket bu metodun içinde gerçekleşir)
                kotu_karakter.EnKısaYol(self.labirent, baslangic_tuple, hedef_tuple)

    def karakter_yakalandi(self):
        # Karakterin yakalanma durumunu yönetir
       
        # Can kaybını yönet
        oyun_bitti = self.aktif_karakter.yakalanma()
        
        # Yakalanma sesini çal
        if self.yakalanma_sesi:
            self.yakalanma_sesi.play()
        
        # Eğer can bittiyse oyun biter
        if oyun_bitti:
            return True
        
        # İyi karakteri başlangıç konumuna döndür
        yeni_konum = Lokasyon(6, 5)
        self.aktif_karakter.konum = yeni_konum
        
        # Kötü karakterleri kendi başlangıç kapılarına döndür
        for karakter in self.aktif_karakterler:
            if karakter.getTur() == "Kötü":
                # Karakterin kayıtlı başlangıç kapısını al
                baslangic_kapisi = self.karakter_kapi_eslesmesi.get(karakter)
                if baslangic_kapisi:
                    karakter.konum.setX(baslangic_kapisi.getX())
                    karakter.konum.setY(baslangic_kapisi.getY())
        
        return False

    def mesaj_goster(self, mesaj):
        # Ekrana mesaj gösterir

        font = pygame.font.Font(None, 74)
        text = font.render(mesaj, True, self.KIRMIZI)
        text_rect = text.get_rect()
        text_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
        self.screen.blit(text, text_rect)

    def karakter_secim_ekrani(self):
        # Karakter seçim ekranını gösterir ve seçilen karakteri döndürür
        
        # Karakter seçim ekranı için sabit boyut
        SECIM_GENISLIK = 600
        SECIM_YUKSEKLIK = 200
        
        # Karakter seçim ekranı için yeni pencere
        secim_ekrani = pygame.display.set_mode((SECIM_GENISLIK, SECIM_YUKSEKLIK))
        pygame.display.set_caption("Karakter Seçimi")
        
        # Font ayarla
        self.font = pygame.font.Font(None, 36)
        
        # Butonlar için dikdörtgenler
        yoda_button = pygame.Rect(50, 50, 200, 100)
        luke_button = pygame.Rect(350, 50, 200, 100)
        
        secim_yapildi = False
        while not secim_yapildi:
            secim_ekrani.fill(self.BEYAZ)
            
            # Butonları çiz
            pygame.draw.rect(secim_ekrani, (0, 255, 0), yoda_button)  # Yeşil
            pygame.draw.rect(secim_ekrani, (0, 0, 255), luke_button)  # Mavi
            
            # Buton yazıları
            yoda_text = self.font.render("Master Yoda", True, self.SIYAH)
            luke_text = self.font.render("Luke Skywalker", True, self.SIYAH)
            
            # Yazıları ortala
            secim_ekrani.blit(yoda_text, (yoda_button.centerx - yoda_text.get_width()//2,
                                        yoda_button.centery - yoda_text.get_height()//2))
            secim_ekrani.blit(luke_text, (luke_button.centerx - luke_text.get_width()//2,
                                        luke_button.centery - luke_text.get_height()//2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if yoda_button.collidepoint(mouse_pos):
                        self.secilen_karakter = "MasterYoda"
                        secim_yapildi = True
                    elif luke_button.collidepoint(mouse_pos):
                        self.secilen_karakter = "LukeSkywalker"
                        secim_yapildi = True
            
            pygame.display.flip()
        
        return self.secilen_karakter

    def ses_yukle(self, dosya_adi):
        # Belirtilen dosyadan sesi yükler
        
        try:
            tam_yol = os.path.abspath(dosya_adi)
            if not os.path.exists(tam_yol):
                return None
                
            ses = pygame.mixer.Sound(tam_yol)
            return ses
            
        except Exception:
            return None

def main():
    pygame.init()
    clock = pygame.time.Clock()
    oyun_harita = OyunHarita()
    
    # Haritayı oku
    if not oyun_harita.harita_oku("harita.txt"):
        return
    
    # Karakter seçimi yap
    secilen_karakter = oyun_harita.karakter_secim_ekrani()
    
    # Oyun ekranını oluştur
    oyun_harita.screen = pygame.display.set_mode((oyun_harita.WINDOW_WIDTH, oyun_harita.WINDOW_HEIGHT))
    pygame.display.set_caption("Labirent Oyunu - " + secilen_karakter)
    
    # Karakterleri oluştur
    oyun_harita.karakter_olustur()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not oyun_harita.oyun_bitti:
                # Klavye kontrolleri
                if event.key == pygame.K_UP:
                    oyun_harita.karakter_hareket((0, -1))
                elif event.key == pygame.K_DOWN:
                    oyun_harita.karakter_hareket((0, 1))
                elif event.key == pygame.K_LEFT:
                    oyun_harita.karakter_hareket((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    oyun_harita.karakter_hareket((1, 0))
        
        # Haritayı çiz
        oyun_harita.harita_ciz()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()