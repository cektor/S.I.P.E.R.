# S.I.P.E.R. - Site ve İçerik Engelleyici

<div align="center">
  <img src="siperlo.png" alt="S.I.P.E.R. Logo" width="128" height="128">
  
  **Modern ve Kullanıcı Dostu Site Engelleyici**
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
  [![GTK4](https://img.shields.io/badge/GTK-4.0-green.svg)](https://gtk.org)
  [![Libadwaita](https://img.shields.io/badge/Libadwaita-1.0-purple.svg)](https://gnome.pages.gitlab.gnome.org/libadwaita/)
  [![Lisans](https://img.shields.io/badge/Lisans-GPL%20v3-red.svg)](LICENSE)
</div>

## 📋 İçindekiler

- [Hakkında](#-hakkında)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Yapılandırma](#-yapılandırma)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)
- [İletişim](#-i̇letişim)

## 🎯 Hakkında

S.I.P.E.R. (Site ve İçerik Engelleyici), Linux sistemler için geliştirilmiş modern bir site engelleyici uygulamasıdır. GTK4 ve Libadwaita kullanılarak oluşturulan bu uygulama, kullanıcıların dikkatini dağıtan web sitelerini engelleyerek odaklanmalarına yardımcı olur.

### Neden S.I.P.E.R.?

- 🎨 **Modern Arayüz**: GTK4 ve Libadwaita ile native GNOME deneyimi
- 🚀 **Hızlı ve Hafif**: Minimal kaynak kullanımı
- 🔒 **Güvenli**: Sistem hosts dosyasını güvenli şekilde yönetir
- 🌍 **Çok Dilli**: Türkçe ve İngilizce dil desteği
- 📊 **İstatistikler**: Odaklanma sürelerinizi takip edin
- ⏰ **Zamanlayıcı**: Pomodoro tekniği ile çalışın

## ✨ Özellikler

### 🔧 Temel Özellikler
- **Site Engelleme**: Belirli web sitelerini sistem seviyesinde engelleme
- **Kategori Desteği**: Sosyal medya, oyun, haber gibi kategorilerde toplu engelleme
- **Zamanlayıcı**: Belirli süre boyunca odaklanma modu
- **İstatistikler**: Odaklanma sürelerinizi görüntüleme
- **İçe/Dışa Aktarma**: Site listelerinizi JSON formatında kaydetme/yükleme

### 🎨 Arayüz Özellikleri
- **Modern Tasarım**: GNOME HIG uyumlu arayüz
- **Karanlık/Açık Tema**: Sistem temasını otomatik takip
- **Toast Bildirimleri**: Kullanıcı dostu geri bildirimler
- **Responsive Tasarım**: Farklı ekran boyutlarına uyum
- **Erişilebilirlik**: Klavye navigasyonu ve ekran okuyucu desteği

### 🛡️ Güvenlik Özellikleri
- **Güvenli Hosts Yönetimi**: Sistem dosyalarını güvenli şekilde düzenleme
- **Yedekleme**: Otomatik hosts dosyası yedekleme
- **Geri Alma**: Değişiklikleri kolayca geri alma
- **İzin Kontrolü**: Gerekli sistem izinlerini kontrol etme

## 🚀 Kurulum

### Sistem Gereksinimleri

- **İşletim Sistemi**: Linux (Ubuntu 20.04+, Fedora 35+, Arch Linux)
- **Python**: 3.8 veya üzeri
- **GTK**: 4.0 veya üzeri
- **Libadwaita**: 1.0 veya üzeri

### Otomatik Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/cektor/S.I.P.E.R.git
cd S.I.P.E.R

# Kurulum scriptini çalıştırın
chmod +x install.sh
sudo ./install.sh
```

### Manuel Kurulum

#### Ubuntu/Debian

```bash
# Gerekli paketleri yükleyin
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1

# Uygulamayı indirin
git clone https://github.com/cektor/S.I.P.E.R.git
cd S.I.P.E.R

# Uygulamayı çalıştırın
python3 siper.py
```

#### Fedora

```bash
# Gerekli paketleri yükleyin
sudo dnf install python3 python3-pip python3-gobject gtk4-devel libadwaita-devel

# Uygulamayı indirin
git clone https://github.com/cektor/S.I.P.E.R.git
cd S.I.P.E.R

# Uygulamayı çalıştırın
python3 siper.py
```

#### Arch Linux

```bash
# Gerekli paketleri yükleyin
sudo pacman -S python python-pip python-gobject gtk4 libadwaita

# Uygulamayı indirin
git clone https://github.com/cektor/S.I.P.E.R.git
cd S.I.P.E.R

# Uygulamayı çalıştırın
python3 siper.py
```

## 📖 Kullanım

### İlk Çalıştırma

1. Uygulamayı başlatın:
   ```bash
   python3 siper.py
   ```

2. İlk çalıştırmada uygulama gerekli yapılandırma dosyalarını oluşturacaktır.

3. Sistem hosts dosyasını düzenlemek için sudo yetkisi gerekebilir.

### Temel Kullanım

#### Site Ekleme
1. Ana ekranda "Site Ekle" butonuna tıklayın
2. Engellemek istediğiniz site adresini girin (örn: facebook.com)
3. "Ekle" butonuna tıklayın

#### Kategori Ekleme
1. "Kategori Ekle" menüsünden istediğiniz kategoriyi seçin:
   - 📱 Sosyal Medya
   - 🎮 Oyun Siteleri
   - 📰 Haber Siteleri
   - 🛒 Alışveriş Siteleri
   - 📺 Video Platformları

#### Zamanlayıcı Kullanımı
1. "Odaklanma Başlat" butonuna tıklayın
2. Süreyi dakika cinsinden girin
3. Zamanlayıcı çalışırken tüm engellenen siteler erişilemez olacaktır

#### İstatistikleri Görüntüleme
1. Menüden "İstatistikler" seçeneğini tıklayın
2. Toplam odaklanma sürenizi ve haftalık istatistiklerinizi görün

### Gelişmiş Özellikler

#### İçe/Dışa Aktarma
```bash
# Site listesini dışa aktarma
Menü → Dışa Aktar → blocked_sites.json

# Site listesini içe aktarma
Menü → İçe Aktar → JSON dosyasını seçin
```

#### Komut Satırı Seçenekleri
```bash
# Yardım mesajını görüntüle
python3 siper.py --help

# Sürüm bilgisini göster
python3 siper.py --version

# Debug modunda çalıştır
python3 siper.py --debug
```

## ⚙️ Yapılandırma

### Yapılandırma Dosyaları

Uygulama yapılandırma dosyalarını `~/.config/siper/` dizininde saklar:

```
~/.config/siper/
├── config.json          # Ana yapılandırma
├── blocked_sites.json   # Engellenen siteler
├── focus_history.json   # Odaklanma geçmişi
└── hosts_backup        # Hosts dosyası yedeği
```

### config.json Yapısı

```json
{
  "language": "tr",
  "theme": "auto",
  "blocked_sites": [],
  "focus_history": [],
  "auto_backup": true,
  "notification_sound": true
}
```

### Dil Değiştirme

Dil ayarını değiştirmek için:

1. `~/.config/siper/config.json` dosyasını açın
2. `"language"` değerini `"tr"` (Türkçe) veya `"en"` (İngilizce) olarak değiştirin
3. Uygulamayı yeniden başlatın

## 📸 Ekran Görüntüleri

### Ana Ekran
![Ana Ekran](screenshots/main_window.png)

### Site Ekleme
![Site Ekleme](screenshots/add_site.png)

### Zamanlayıcı
![Zamanlayıcı](screenshots/timer.png)

### İstatistikler
![İstatistikler](screenshots/statistics.png)

## 🤝 Katkıda Bulunma

S.I.P.E.R. projesine katkıda bulunmak isterseniz:

1. **Fork** edin
2. **Feature branch** oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi **commit** edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi **push** edin (`git push origin feature/AmazingFeature`)
5. **Pull Request** açın

### Geliştirme Ortamı Kurulumu

```bash
# Geliştirme bağımlılıklarını yükleyin
pip3 install -r requirements-dev.txt

# Pre-commit hook'larını kurun
pre-commit install

# Testleri çalıştırın
python3 -m pytest tests/
```

### Kod Standartları

- **PEP 8** Python kod standardını takip edin
- **Type hints** kullanın
- **Docstring** ekleyin
- **Unit test** yazın

## 🐛 Hata Bildirimi

Hata bulduğunuzda lütfen [GitHub Issues](https://github.com/cektor/S.I.P.E.R./issues) sayfasından bildirin.

Hata bildirirken şunları ekleyin:
- İşletim sistemi bilgisi
- Python sürümü
- Hata mesajı
- Hatayı tekrarlama adımları

## 📝 Lisans

Bu proje [GPL v3](LICENSE) lisansı altında lisanslanmıştır.

```
S.I.P.E.R. - Site ve İçerik Engelleyici
Copyright (C) 2024 Fatih ÖNDER (CekToR)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

## 📞 İletişim

**Geliştirici**: Fatih ÖNDER (CekToR) 🇹🇷

- **GitHub**: [@cektor](https://github.com/cektor)
- **E-posta**: [fatih@onder.web.tr](mailto:fatih@onder.web.tr)
- **Web**: [https://onder.web.tr](https://onder.web.tr)

## 🙏 Teşekkürler

- **GNOME Projesi** - GTK4 ve Libadwaita için
- **Python Topluluğu** - Harika Python ekosistemi için
- **Açık Kaynak Topluluğu** - İlham ve destek için

---

<div align="center">
  <p>⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!</p>
  <p>Made with ❤️ in Turkey 🇹🇷</p>
</div>