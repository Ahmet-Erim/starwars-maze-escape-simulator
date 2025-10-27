# Labirent Oyunu (Pygame)

Bu proje, Pygame kullanılarak geliştirilmiş basit bir labirent oyunudur. Oyuncu, Master Yoda veya Luke Skywalker arasından birini seçerek haritada ilerler ve hedefe (kupa) ulaşmaya çalışır. Kötü karakterler (Darth Vader, Kylo Ren, Stormtrooper) oyuncuyu BFS tabanlı en kısa yol algoritmalarıyla kovalar.

## Özellikler
- Karakter seçimi: Master Yoda veya Luke Skywalker
- Kötü karakterler: Darth Vader (duvarları yok sayar), Kylo Ren (2 kare sıçrayabilir), Stormtrooper (1 kare)
- En kısa yol hesaplama: BFS (her kötü karakter için farklı kurallar)
- Can sistemi:
  - Master Yoda: 3 kalp = 6 birim (yarım kalpler desteklenir)
  - Luke Skywalker: 3 kalp
- Yakalanınca ses efekti ve respawn (iyi karakter başlangıca, kötüler kapılarına döner)
- Basit grid harita ve görsel göstergeler (kapılar A/B/C/D/E, ok yönleri, yol izleri)

## Ekran ve Kontroller
- Yön tuşları: Yukarı/Aşağı/Sol/Sağ hareket
- Hedef: Haritada (13, 9) koordinasyonundaki hücreye ulaşıp kupayı almak
- Oyun durumları: "KAZANDINIZ!" veya "GAME OVER!"

## Bağımlılıklar
- Python 3.8+
- Pygame 2.x

İsteğe bağlı olarak aşağıdaki dosyayı ekleyebilirsiniz:
```
requirements.txt
pygame>=2.1
```

## Kurulum (Windows - PowerShell)
1. Python'u kurun ve PATH'e ekleyin.
2. Proje klasöründe sanal ortam (önerilir) oluşturun ve etkinleştirin:
   ```powershell
   python -m venv .venv; .\.venv\Scripts\Activate.ps1
   ```
3. Bağımlılıkları kurun:
   ```powershell
   pip install pygame
   ```

## Çalıştırma
Proje kökünde aşağıdaki komutu çalıştırın:
```powershell
python .\app.py
```

İlk açılışta karakter seçimi penceresi gelir; seçimden sonra oyun ana pencereye döner.

## Varlıklar (Assets)
Aşağıdaki dosyalar `app.py` tarafından doğrudan kök dizinden yüklenir:
- Harita: `harita.txt`
- Görseller: `yoda.png`, `luke.png`, `vader.png`, `kylo.png`, `trooper.png`
- UI simgeleri: `kalp.png`, `yarim_kalp.png`, `bos_kalp.png`, `kupa.png`, `ok.png`
- Ses: `yakalanma.wav`

Dosyaların eksik olması durumunda oyun, ilgili görseller yerine basit şekiller çizer; ses yoksa sessiz devam eder.

## Harita Biçimi
`harita.txt` bir ızgara matrisi içerir:
- 0: Duvar
- 1: Yol (kupa hedefi için de kullanılır)
- 2: İyi karakter başlangıç noktası (koddaki varsayılan: (6, 5))
- 3: Kötü karakter kapıları (rastgele seçilip başlangıçları atanır)

Örnek (projedeki varsayılan harita):
```
0 0 0 0 3 0 0 0 0 0 0 0 3 0
0 1 1 1 1 0 1 1 1 1 1 1 1 0
0 1 0 1 1 1 1 0 1 0 0 0 1 0
0 1 0 1 1 0 1 0 1 1 0 1 1 0
0 1 0 1 0 0 1 0 1 1 0 1 1 0
3 1 0 1 1 1 2 0 1 0 0 0 1 3
0 1 0 0 1 0 1 0 1 0 1 1 1 0
0 1 0 1 1 1 1 1 1 0 0 0 1 0
0 1 0 1 0 0 0 0 1 0 0 1 1 0
0 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 3 0 0 0 0 0 0 0 0 0
```
Notlar:
- Kupa hedefi mantıksal olarak (13, 9) hücresindedir; görsel kupa simgesi bu hücrenin sağına çizilir.
- Kapı harfleri ve yön okları görsel amaçlıdır: A(0,5), B(4,0), C(12,0), D(13,5), E(4,10).

## Oyun Mekanikleri (Özet)
- Her iyi karakter hamlesinden sonra tüm kötü karakterler, oyuncunun mevcut konumuna doğru en kısa yolu hesaplar ve bir adım ilerler.
- Darth Vader, BFS ile sınır kontrolü yapar fakat duvarları yok sayarak en kısa yoldan gelir.
- Kylo Ren, önce 2 hücrelik sıçramaları dener; ara ve hedef hücrelerin duvar olmaması gerekir.
- Stormtrooper, sadece komşu hücrelere (duvar olmayan) ilerler.
- Çakışma (aynı hücre) yakalanma sayılır; can düşer ve herkes başlangıçlarına döner.

## Bilinen Sınırlamalar
- Pencere boyutu, harita boyutundan hesaplanır ve sabit ofsetlerle çizilir.
- Varlık dosyaları aynı klasörde değilse yüklenmez; dosya adları sabittir.
- Ses cihazı olmayan sistemlerde ses başlatma başarısız olabilir (oyun sessiz devam eder).

## Sorun Giderme
- Pygame ekranı açılmıyor: Python sürümünü ve `pygame` kurulumunu doğrulayın.
- Görseller yok: PNG dosyalarının isimlerini ve konumunu kontrol edin.
- Ses çalmıyor: `yakalanma.wav` mevcut mu ve sistemde ses aygıtı var mı kontrol edin.

## Lisans
Eğer aksi belirtilmediyse, bu proje eğitim amaçlıdır. Kullanılan görseller ve sesler telifli olabilir; kendi varlıklarınızı kullanmanız tavsiye edilir.
