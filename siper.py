#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

import os
import json
import subprocess
import threading
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import configparser
import glob
import logging
import traceback
import sys
from functools import wraps

class DebugLogger:
    def __init__(self):
        self.debug_enabled = True
        # Config dizinini oluştur
        config_dir = os.path.expanduser('~/.config/siper')
        os.makedirs(config_dir, exist_ok=True)
        self.log_file = os.path.join(config_dir, 'debug.log')
        self.setup_logging()
        self.operation_counter = 0
    
   
        # Handlers ekle
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self.info("🚀 SIPER Debug Sistemi Başlatıldı")
        self.info(f"📁 Log dosyası: {self.log_file}")
    
    def debug(self, message, operation_id=None):
        if self.debug_enabled:
            prefix = f"[OP-{operation_id}]" if operation_id else ""
            self.logger.debug(f"🔍 {prefix} {message}")
    
    def info(self, message, operation_id=None):
        prefix = f"[OP-{operation_id}]" if operation_id else ""
        self.logger.info(f"ℹ️  {prefix} {message}")
    
    def warning(self, message, operation_id=None):
        prefix = f"[OP-{operation_id}]" if operation_id else ""
   
    def step(self, step_num, total_steps, message, operation_id=None):
        prefix = f"[OP-{operation_id}]" if operation_id else ""
        progress = f"({step_num}/{total_steps})"
        self.logger.info(f"🔄 {prefix} {progress} {message}")
    
    def operation_start(self, operation_name):
        self.operation_counter += 1
        op_id = self.operation_counter
        self.info(f"🎯 İşlem Başlatıldı: {operation_name}", op_id)
        return op_id
    
    
    
    def permission_request(self, reason, operation_id=None):
        self.warning(f"🔐 Yetki İsteği: {reason}", operation_id)
    
    def config_change(self, key, old_value, new_value, operation_id=None):
        self.debug(f"⚙️  Yapılandırma Değişikliği: {key} = {old_value} -> {new_value}", operation_id)
    
    def network_operation(self, operation, details, operation_id=None):
        self.debug(f"🌐 Ağ İşlemi: {operation} - {details}", operation_id)

class ColoredFormatter(logging.Formatter):
    """Renkli terminal çıktısı için formatter"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green  
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        return formatter.format(record)

def debug_operation(operation_name):
    """İşlemleri otomatik debug eden decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, 'debug') or hasattr(self.app, 'debug'):
                debug = getattr(self, 'debug', None) or getattr(self.app, 'debug', None)
                op_id = debug.operation_start(f"{operation_name} - {func.__name__}")
                try:
                    result = func(self, *args, **kwargs)
                    debug.operation_end(op_id, True, "İşlem başarıyla tamamlandı 🇹🇷")
                    return result
                except Exception as e:
                    debug.operation_end(op_id, False, f"Hata: {str(e)}")
                    debug.error(f"İşlem hatası: {func.__name__}", op_id, e)
                    raise
            else:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator

class Language:
    def __init__(self):
        self.current_language = 'english'
        self.translations = {}
        self.available_languages = {}
        self.load_available_languages()
        self.load_language(self.current_language)
               
    def load_language(self, language):
        if language in self.available_languages:
            config = configparser.ConfigParser()
            config.read(self.available_languages[language], encoding='utf-8')
            self.translations = {}
            for section in config.sections():
                self.translations[section.lower()] = dict(config.items(section))
            self.current_language = language
    
    def get(self, section, key, default=""):
        return self.translations.get(section, {}).get(key, default)
    
    def get_available_languages(self):
        return list(self.available_languages.keys())

class SiperApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.siper.app')
        
        # Varsayılan pencere ikonunu ayarla
        if os.path.exists('/usr/share/pixmaps/siperlo.png'):
            Gtk.Window.set_default_icon_name('siperlo')
            print("[DEBUG] Varsayılan pencere ikonu ayarlandı: siperlo")
        
        self.debug = DebugLogger()
        self.blocked_sites = set()
        self.is_blocking_active = False
        self.theme_mode = 'auto'  # auto, light, dark
        self.hosts_file = '/etc/hosts'
        
        # Config dizinini oluştur
        self.config_dir = os.path.expanduser('~/.config/siper')
        os.makedirs(self.config_dir, exist_ok=True)
        
       
    def do_activate(self):
        self.window = SiperWindow(application=self)
        self.window.present()
    
    @debug_operation("Hosts Senkronizasyonu")
    def check_hosts_sync(self):
        """Hosts dosyasını kontrol ederek gerçek durumu tespit et"""
        op_id = self.debug.operation_start("Hosts dosyası senkronizasyon kontrolü")
        try:
            self.debug.file_operation("READ", self.hosts_file, op_id)
            with open(self.hosts_file, 'r') as f:
                content = f.read()
            
            has_siper = '# siper' in content
            self.debug.debug(f"Hosts dosyasında SIPER girişi bulundu: {has_siper}", op_id)
            self.debug.debug(f"Mevcut engelleme durumu: {self.is_blocking_active}", op_id)
            
            if has_siper and not self.is_blocking_active:
                self.debug.config_change("is_blocking_active", False, True, op_id)
                self.is_blocking_active = True
                self.save_config()
                self.debug.success("Engelleme durumu aktif olarak güncellendi", op_id)
            elif not has_siper and self.is_blocking_active:
                self.debug.config_change("is_blocking_active", True, False, op_id)
                self.is_blocking_active = False
                self.save_config()
                self.debug.success("Engelleme durumu pasif olarak güncellendi", op_id)
            else:
                self.debug.success("Hosts dosyası ve yapılandırma senkronize", op_id)
            
            self.debug.operation_end(op_id, True)
        except Exception as e:
            self.debug.error(f"Hosts senkronizasyon hatası: {str(e)}", op_id, e)
            self.debug.operation_end(op_id, False)

    @debug_operation("Yapılandırma Yükleme")
    def load_config(self):
        op_id = self.debug.operation_start("Yapılandırma dosyası yükleme")
        try:
            if os.path.exists(self.config_file):
                self.debug.file_operation("READ", self.config_file, op_id)
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    
                old_sites_count = len(self.blocked_sites)
                self.blocked_sites = set(data.get('blocked_sites', []))
                self.debug.config_change("blocked_sites_count", old_sites_count, len(self.blocked_sites), op_id)
                
                old_active = self.is_blocking_active
                self.is_blocking_active = data.get('is_active', False)
                self.debug.config_change("is_blocking_active", old_active, self.is_blocking_active, op_id)
                
                old_theme = self.theme_mode
                self.theme_mode = data.get('theme_mode', 'auto')
                self.debug.config_change("theme_mode", old_theme, self.theme_mode, op_id)
                
                saved_language = data.get('language', 'turkish')
                if saved_language in self.language.get_available_languages():
                    self.language.load_language(saved_language)
                    self.debug.success(f"Dil yüklendi: {saved_language}", op_id)
                
                self.debug.success(f"Yapılandırma başarıyla yüklendi - {len(self.blocked_sites)} site", op_id)
            else:
                self.debug.warning("Yapılandırma dosyası bulunamadı, varsayılan değerler kullanılıyor", op_id)
            
            self.debug.operation_end(op_id, True)
        except Exception as e:
            self.debug.error(f"Yapılandırma yüklenirken hata: {str(e)}", op_id, e)
            self.debug.operation_end(op_id, False)

    
    @debug_operation("Yapılandırma Kaydetme")
    def save_config(self):
        def save_in_thread():
            op_id = self.debug.operation_start("Yapılandırma dosyası kaydetme")
            try:
                config_data = {
                    'blocked_sites': list(self.blocked_sites),
                    'is_active': self.is_blocking_active,
                    'theme_mode': self.theme_mode,
                    'language': self.language.current_language
                }
                
                self.debug.file_operation("WRITE", self.config_file, op_id)
                self.debug.debug(f"Kaydedilecek veri: {len(self.blocked_sites)} site, aktif: {self.is_blocking_active}", op_id)
                
                with open(self.config_file, 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                self.debug.success("Yapılandırma başarıyla kaydedildi", op_id)
                self.debug.operation_end(op_id, True)
            except Exception as e:
                self.debug.error(f"Yapılandırma kaydedilirken hata: {str(e)}", op_id, e)
                self.debug.operation_end(op_id, False)
        
        threading.Thread(target=save_in_thread, daemon=True).start()
    
    def apply_theme(self):
        style_manager = Adw.StyleManager.get_default()
        if self.theme_mode == 'light':
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        elif self.theme_mode == 'dark':
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)

class SiperWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = self.get_application()
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        self.set_title("SiPER")
        self.set_default_size(650, 750)
        
        # Pencere ikonunu ayarla
        if os.path.exists('/usr/share/pixmaps/siperlo.png'):
            self.set_icon_name('siperlo')
            print("[DEBUG] Pencere ikonu ayarlandı: siperlo")
        else:
            print("[DEBUG] İkon dosyası bulunamadı")

        # Main container
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Header Bar
        header = Adw.HeaderBar()
        
        # Theme toggle button
        self.theme_button = Gtk.Button()
        self.theme_button.add_css_class("flat")
        self.theme_button.connect('clicked', self.toggle_theme)
        header.pack_start(self.theme_button)
        
        # Language menu button
        self.lang_menu_button = Gtk.MenuButton()
        self.lang_menu_button.set_icon_name("preferences-desktop-locale-symbolic")
        self.lang_menu_button.add_css_class("flat")
        self.create_language_menu()
        header.pack_start(self.lang_menu_button)
        
        # About button
        about_button = Gtk.Button()
        about_button.set_icon_name("help-about-symbolic")
        about_button.add_css_class("flat")
        about_button.connect('clicked', self.show_about)
        header.pack_end(about_button)
        
        # Stats button
        stats_button = Gtk.Button()
        stats_button.set_icon_name("view-list-symbolic")
        stats_button.add_css_class("flat")
        stats_button.connect('clicked', self.show_stats)
        header.pack_end(stats_button)
        
        # Menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()
        menu.append(self.app.language.get('dialogs', 'export_title'), "app.export")
        menu.append(self.app.language.get('dialogs', 'import_title'), "app.import")
        menu_button.set_menu_model(menu)
        header.pack_end(menu_button)
        
        self.update_theme_button()
        self.update_language_button()
        
        main_container.append(header)

        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.set_margin_top(12)
        main_box.set_margin_bottom(12)
        main_box.set_margin_start(12)
        main_box.set_margin_end(12)
        main_container.append(main_box)

        # Title
        title = Gtk.Label(label="S.I.P.E.R.")
        title.add_css_class("title-1")
        main_box.append(title)
        
        # Subtitle with bold first letters
        subtitle = Gtk.Label()
        subtitle.set_markup("<b>S</b>ystem <b>I</b>nternet <b>P</b>olicy <b>E</b>nforcement <b>R</b>uleset")
        subtitle.set_tooltip_text("🇹🇷")
        subtitle.add_css_class("dim-label")
        subtitle.set_margin_bottom(6)
        main_box.append(subtitle)

        # Add Site Section
        self.add_group = Adw.PreferencesGroup()
        self.add_group.set_title(self.app.language.get('window', 'add_site_group'))

        self.add_row = Adw.ActionRow()
        self.add_row.set_title(self.app.language.get('window', 'add_site_title'))

        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text(self.app.language.get('window', 'add_site_placeholder'))
        self.url_entry.set_hexpand(True)
        self.url_entry.connect('activate', self.on_add_site)

        self.add_button = Gtk.Button(label=self.app.language.get('window', 'add_button'))
        self.add_button.add_css_class("suggested-action")
        self.add_button.connect('clicked', self.on_add_site)

        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        entry_box.append(self.url_entry)
        entry_box.append(self.add_button)

        self.add_row.add_suffix(entry_box)
        self.add_group.add(self.add_row)
        
        # Quick categories - Expandable
        self.categories_row = Adw.ExpanderRow()
        self.categories_row.set_title(self.app.language.get('window', 'quick_actions'))
        self.categories_row.set_expanded(False)
        
        # Grid for compact layout
        grid = Gtk.Grid()
        grid.set_row_spacing(6)
        grid.set_column_spacing(6)
        grid.set_column_homogeneous(True)
        grid.set_margin_top(6)
        grid.set_margin_bottom(6)
        grid.set_margin_start(12)
        grid.set_margin_end(12)
        
        # Category buttons with icons and compact style
        lang = self.app.language
        categories = [
            (f"📱 {lang.get('categories', 'social')}", self.add_social_sites),
            (f"🎥 {lang.get('categories', 'video')}", self.add_video_sites),
            (f"📰 {lang.get('categories', 'news')}", self.add_news_sites),
            (f"🎮 {lang.get('categories', 'gaming')}", self.add_gaming_sites),
            (f"🛍 {lang.get('categories', 'shopping')}", self.add_shopping_sites),
            (f"🔞 {lang.get('categories', 'adult')}", self.add_adult_sites),
            (f"₿ {lang.get('categories', 'crypto')}", self.add_crypto_sites),
            (f"🌍 {lang.get('categories', 'torrent')}", self.add_torrent_sites),
            (f"📚 {lang.get('categories', 'education')}", self.add_education_sites),
            (f"💼 {lang.get('categories', 'work')}", self.add_work_sites),
            (f"🎵 {lang.get('categories', 'music')}", self.add_music_sites),
            (f"🏃 {lang.get('categories', 'sports')}", self.add_sports_sites)
        ]
        
        for i, (label, callback) in enumerate(categories):
            btn = Gtk.Button(label=label)
            btn.add_css_class("flat")
            btn.set_size_request(80, 32)
            btn.connect('clicked', lambda w, cb: (cb(w), self.categories_row.set_expanded(False)), callback)
            grid.attach(btn, i % 4, i // 4, 1, 1)
        
        self.categories_row.add_row(grid)
        self.add_group.add(self.categories_row)
        
        main_box.append(self.add_group)

        # Blocked Sites List
        self.list_group = Adw.PreferencesGroup()
        self.list_group.set_title(self.app.language.get('window', 'blocked_sites'))
        
        # Clear all button row
        self.clear_row = Adw.ActionRow()
        self.clear_row.set_title(self.app.language.get('window', 'clear_all_title'))
        self.clear_row.set_subtitle(self.app.language.get('window', 'clear_all_subtitle'))
        
        self.clear_button = Gtk.Button(label=self.app.language.get('window', 'clear_button'))
        self.clear_button.add_css_class("destructive-action")
        self.clear_button.connect('clicked', self.on_clear_all)
        self.clear_row.add_suffix(self.clear_button)
        
        self.list_group.add(self.clear_row)
        
        # Add spacing between clear button and list
        spacing_box = Gtk.Box()
        spacing_box.set_size_request(-1, 6)
        self.list_group.add(spacing_box)

        # Container for list and empty state
        self.list_container = Gtk.Stack()
        
        # ScrolledWindow for the list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)

        self.sites_listbox = Gtk.ListBox()
        self.sites_listbox.add_css_class("boxed-list")
        scrolled.set_child(self.sites_listbox)
        
        # Empty state
        self.empty_page = Adw.StatusPage()
        self.empty_page.set_title(self.app.language.get('empty_state', 'title'))
        self.empty_page.set_description(self.app.language.get('empty_state', 'description'))
        self.empty_page.set_icon_name("document-new-symbolic")
        
        # Küçük ikon ve yazı için CSS
        self.empty_page.add_css_class("compact")
        
        # CSS provider ekle
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
        .compact .status-page-icon {
            -gtk-icon-size: 48px;
        }
        .compact .title-1 {
            font-size: 18px;
        }
        .compact .body {
            font-size: 12px;
        }
        """)
        
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        self.list_container.add_named(scrolled, "list")
        self.list_container.add_named(self.empty_page, "empty")
        
        self.list_group.add(self.list_container)
        main_box.append(self.list_group)

        # Control Buttons
        button_group = Adw.PreferencesGroup()
        
        # Regular toggle
        self.toggle_row = Adw.ActionRow()
        self.toggle_button = Gtk.Button()
        self.toggle_button.connect('clicked', self.on_toggle_blocking)
        self.toggle_row.add_suffix(self.toggle_button)
        button_group.add(self.toggle_row)
        
        # Focus mode
        self.focus_row = Adw.ActionRow()
        self.focus_row.set_title(self.app.language.get('buttons', 'focus_mode'))
        self.focus_row.set_subtitle(self.app.language.get('buttons', 'focus_subtitle'))
        
        focus_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Quick time buttons
        lang = self.app.language
        time_buttons = [
            (25, lang.get('time', '25min')),
            (60, lang.get('time', '60min')),
            (120, lang.get('time', '120min'))
        ]
        for minutes, label in time_buttons:
            btn = Gtk.Button(label=label)
            btn.add_css_class("flat")
            btn.connect('clicked', self.on_focus_mode, minutes)
            focus_box.append(btn)
        
        # Custom time input
        custom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.custom_time_entry = Gtk.Entry()
        self.custom_time_entry.set_placeholder_text(lang.get('time', 'custom_time'))
        self.custom_time_entry.set_width_chars(4)
        self.custom_time_entry.set_max_width_chars(4)
        self.custom_time_entry.set_input_purpose(Gtk.InputPurpose.DIGITS)
        self.custom_time_entry.connect('activate', self.on_custom_focus_mode)
        custom_box.append(self.custom_time_entry)
        
        time_label = Gtk.Label(label=lang.get('time', 'minutes_short'))
        custom_box.append(time_label)
        
        custom_btn = Gtk.Button(label="▶")
        custom_btn.add_css_class("flat")
        custom_btn.connect('clicked', self.on_custom_focus_mode)
        custom_box.append(custom_btn)
        
        focus_box.append(custom_box)
        
        self.focus_row.add_suffix(focus_box)
        button_group.add(self.focus_row)
        
        main_box.append(button_group)

        # Status
        self.status_label = Gtk.Label()
        self.status_label.add_css_class("dim-label")
        main_box.append(self.status_label)
        
        # Made in TURKIYE label
        made_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        made_box.set_halign(Gtk.Align.END)
        made_label = Gtk.Label(label="Made in TURKIYE 🇹🇷")
        made_label.set_opacity(0.3)
        made_label.add_css_class("caption")
        made_box.append(made_label)
        main_box.append(made_box)

        self.set_content(main_container)
        self.setup_actions()
        self.update_toggle_button()
        self.update_status()
    
    def toggle_theme(self, widget):
        if self.app.theme_mode == 'auto':
            self.app.theme_mode = 'light'
        elif self.app.theme_mode == 'light':
            self.app.theme_mode = 'dark'
        else:
            self.app.theme_mode = 'auto'
        
        self.app.apply_theme()
        self.app.save_config()
        self.update_theme_button()
    
    def create_language_menu(self):
        """Dil seçim menüsünü oluştur"""
        lang_names = {
            'turkish': '🇹🇷 Türkçe',
            'azerbaijani': '🇦🇿 Azərbaycanca',
            'kazakh': '🇰🇿 Қазақша',
            'uzbek': '🇺🇿 O\'zbekcha',
            'turkmen': '🇹🇲 Türkmençe',
            'kyrgyz': '🇰🇬 Кыргызча',
            'tatar': '🏴 Татарча',
            'uyghur': '🏴 ئۇيغۇرچە',
            'english': '🇬🇧 English',
            'russian': '🇷🇺 Русский',
           'german': '🇩🇪 Deutsch',
            'french': '🇫🇷 Français',
            'spanish': '🇪🇸 Español',
            'japanese': '🇯🇵 日本語',
            'korean': '🇰🇷 한국어'
        }
        
        menu = Gio.Menu()
        langs = self.app.language.get_available_languages()
        
        for lang in sorted(langs):
            display_name = lang_names.get(lang, lang.capitalize())
            menu.append(display_name, f"app.change_language::{lang}")
        
        self.lang_menu_button.set_menu_model(menu)
        self.update_language_button()
    
 
    def restart_application(self):
        """Uygulamayı yeniden başlat - artık kullanılmıyor"""
        pass
    
    def update_language_button(self):
        lang_names = {
            'turkish': '🇹🇷 TR',
            'azerbaijani': '🇦🇿 AZ',
            'kazakh': '🇰🇿 KZ',
            'uzbek': '🇺🇿 UZ',
            'turkmen': '🇹🇲 TM',
            'kyrgyz': '🇰🇬 KG',
            'tatar': '🏴 TT',
            'uyghur': '🏴 UG',
            'english': '🇬🇧 EN',
            'russian': '🇷🇺 RU',
            'arabic': '🇸🇦 AR',
            'persian': '🇮🇷 FA',
            'german': '🇩🇪 DE',
            'french': '🇫🇷 FR',
            'spanish': '🇪🇸 ES',
            'chinese': '🇨🇳 ZH',
            'japanese': '🇯🇵 JA',
            'korean': '🇰🇷 KO'
        }
        current = self.app.language.current_language
        self.lang_menu_button.set_label(lang_names.get(current, current.upper()[:2]))
        self.lang_menu_button.set_tooltip_text(self.app.language.get('tooltips', 'language'))
    
    def update_ui_texts(self):
        # Tüm UI metinlerini güncelle
        lang = self.app.language
        
        # Header butonları
        self.update_theme_button()
        
        # Grup başlıkları
        self.add_group.set_title(lang.get('window', 'add_site_group'))
        self.add_row.set_title(lang.get('window', 'add_site_title'))
        self.url_entry.set_placeholder_text(lang.get('window', 'add_site_placeholder'))
        self.add_button.set_label(lang.get('window', 'add_button'))
        
        self.categories_row.set_title(lang.get('window', 'quick_actions'))
        
        self.list_group.set_title(lang.get('window', 'blocked_sites'))
        self.clear_row.set_title(lang.get('window', 'clear_all_title'))
        self.clear_row.set_subtitle(lang.get('window', 'clear_all_subtitle'))
        self.clear_button.set_label(lang.get('window', 'clear_button'))
        
        self.empty_page.set_title(lang.get('empty_state', 'title'))
        self.empty_page.set_description(lang.get('empty_state', 'description'))
        
        self.focus_row.set_title(lang.get('buttons', 'focus_mode'))
        self.focus_row.set_subtitle(lang.get('buttons', 'focus_subtitle'))
        
        self.refresh_list()
        self.update_toggle_button()
        self.update_status()
    
    def update_theme_button(self):
        if self.app.theme_mode == 'light':
            self.theme_button.set_icon_name("weather-clear-symbolic")
            self.theme_button.set_tooltip_text(self.app.language.get('tooltips', 'theme_light'))
        elif self.app.theme_mode == 'dark':
            self.theme_button.set_icon_name("weather-clear-night-symbolic")
            self.theme_button.set_tooltip_text(self.app.language.get('tooltips', 'theme_dark'))
        else:
            self.theme_button.set_icon_name("applications-system-symbolic")
            self.theme_button.set_tooltip_text(self.app.language.get('tooltips', 'theme_system'))

    @debug_operation("Site Ekleme")
    def on_add_site(self, widget):
        op_id = self.app.debug.operation_start("Manuel site ekleme")
        url = self.url_entry.get_text().strip()
        lang = self.app.language
        
        if url:
            self.app.debug.debug(f"Ham URL girişi: '{url}'", op_id)
            
            # Clean URL
            original_url = url
            url = url.replace('http://', '').replace('https://', '').replace('www.', '')
            if '/' in url:
                url = url.split('/')[0]
            
            self.app.debug.debug(f"Temizlenmiş URL: '{original_url}' -> '{url}'", op_id)
            
            if url:
                if url in self.app.blocked_sites:
                    self.app.debug.warning(f"Site zaten listede: {url}", op_id)
                    self.show_toast(f"{url} {lang.get('messages', 'site_exists')}")
                    self.app.debug.operation_end(op_id, False, "Site zaten mevcut")
                else:
                    self.app.debug.step(1, 3, f"Site ekleniyor: {url}", op_id)
                    self.app.blocked_sites.add(url)
                    
                    self.app.debug.step(2, 3, "Yapılandırma kaydediliyor", op_id)
                    self.app.save_config()
                    
                    self.app.debug.step(3, 3, "Arayüz güncelleniyor", op_id)
                    self.refresh_list()
                    self.url_entry.set_text("")
                    
                    self.app.debug.success(f"Site başarıyla eklendi: {url}", op_id)
                    self.show_toast(f"{url} {lang.get('messages', 'site_added')}")
                    self.app.debug.operation_end(op_id, True, f"Toplam site sayısı: {len(self.app.blocked_sites)}")
            else:
                self.app.debug.error("Geçersiz URL formatı", op_id)
                self.app.debug.operation_end(op_id, False, "Geçersiz URL")
        else:
            self.app.debug.warning("Boş URL girişi", op_id)
            self.app.debug.operation_end(op_id, False, "Boş giriş")

   

        # Show empty state or list
        if len(self.app.blocked_sites) == 0:
            self.list_container.set_visible_child_name("empty")
            self.clear_row.set_visible(False)
        else:
            self.list_container.set_visible_child_name("list")
            # Add sites
            for site in sorted(self.app.blocked_sites):
                row = Adw.ActionRow()
                row.set_title(site)
                
                remove_button = Gtk.Button()
                remove_button.set_icon_name("user-trash-symbolic")
                remove_button.add_css_class("flat")
                remove_button.connect('clicked', self.on_remove_site, site)
                
                row.add_suffix(remove_button)
                self.sites_listbox.append(row)
            
            # Show/hide clear all button based on site count
            self.clear_row.set_visible(len(self.app.blocked_sites) > 1)

    def on_toggle_blocking(self, widget):
        if self.app.is_blocking_active:
            self.on_disable_blocking()
        else:
            self.on_enable_blocking()
    
    
        threading.Thread(target=enable_in_thread, daemon=True).start()

    def on_disable_blocking(self):
        def disable_in_thread():
            try:
                success = self.restore_hosts()
                if success:
                    self.app.is_blocking_active = False
                    self.app.save_config()
                    lang = self.app.language
                    GLib.idle_add(lambda: self.show_toast(lang.get('messages', 'blocking_disabled')))
                    GLib.idle_add(self.update_toggle_button)
                    GLib.idle_add(self.update_status)
                else:
                    lang = self.app.language
                    GLib.idle_add(lambda: self.show_toast(lang.get('messages', 'restore_cancelled')))
            except Exception as e:
                lang = self.app.language
                GLib.idle_add(lambda: self.show_toast(f"{lang.get('messages', 'error')}: {str(e)}"))

        threading.Thread(target=disable_in_thread, daemon=True).start()
    
    def update_toggle_button(self):
        lang = self.app.language
        if self.app.is_blocking_active:
            self.toggle_row.set_title(lang.get('buttons', 'disable_blocking'))
            self.toggle_row.set_subtitle(lang.get('buttons', 'disable_subtitle'))
            self.toggle_button.set_label(lang.get('buttons', 'disable_button'))
            self.toggle_button.remove_css_class("suggested-action")
            self.toggle_button.add_css_class("destructive-action")
            self.focus_row.set_sensitive(False)
        else:
            self.toggle_row.set_title(lang.get('buttons', 'enable_blocking'))
            self.toggle_row.set_subtitle(lang.get('buttons', 'enable_subtitle'))
            self.toggle_button.set_label(lang.get('buttons', 'enable_button'))
            self.toggle_button.remove_css_class("destructive-action")
            self.toggle_button.add_css_class("suggested-action")
            self.focus_row.set_sensitive(True)

    @debug_operation("Hosts Engelleme Uygulama")
    def backup_and_apply_blocking(self):
        op_id = self.app.debug.operation_start("Hosts dosyası yedekleme ve engelleme uygulama")
        
        # Step 1: Read current hosts file
        self.app.debug.step(1, 6, "Mevcut hosts dosyasını okuma", op_id)
        try:
            self.app.debug.file_operation("READ", self.app.hosts_file, op_id)
            with open(self.app.hosts_file, 'r') as f:
                content = f.read()
            self.app.debug.success(f"Hosts dosyası okundu - {len(content)} karakter", op_id)
        except PermissionError:
            self.app.debug.permission_request("Hosts dosyası okuma için yetki gerekli", op_id)
            self.app.debug.command_execution(['pkexec', 'cat', self.app.hosts_file], op_id)
            result = subprocess.run(['pkexec', 'cat', self.app.hosts_file], 
                                  capture_output=True, text=True)
            content = result.stdout if result.returncode == 0 else ""
            if result.returncode == 0:
                self.app.debug.success("Hosts dosyası pkexec ile okundu", op_id)
            else:
                self.app.debug.error(f"pkexec okuma hatası: {result.stderr}", op_id)
        except Exception as e:
            self.app.debug.error(f"Hosts dosyası okuma hatası: {str(e)}", op_id, e)
            content = ""

        # Step 2: Remove old entries
        self.app.debug.step(2, 6, "Eski SIPER girişlerini temizleme", op_id)
        lines = content.split('\n')
        old_line_count = len(lines)
        filtered_lines = [line for line in lines if '# siper' not in line]
        removed_count = old_line_count - len(filtered_lines)
        self.app.debug.debug(f"Temizlenen eski giriş sayısı: {removed_count}", op_id)

        # Step 3: Add new entries
        self.app.debug.step(3, 6, f"{len(self.app.blocked_sites)} site için yeni girişler ekleme", op_id)
        added_entries = 0
        for site in self.app.blocked_sites:
            filtered_lines.append(f"127.0.0.1 {site} # siper")
            filtered_lines.append(f"127.0.0.1 www.{site} # siper")
            added_entries += 2
        
        self.app.debug.success(f"Eklenen giriş sayısı: {added_entries}", op_id)
        new_content = '\n'.join(filtered_lines)
        
        # Step 4: Create temporary files
        self.app.debug.step(4, 6, "Geçici dosyalar oluşturma", op_id)
        hosts_temp = None
        script_temp = None
        
        try:
            # Secure temporary hosts file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(new_content)
                hosts_temp = f.name
            self.app.debug.file_operation("CREATE_TEMP", hosts_temp, op_id)
            
            # Secure temporary script file
            script_content = f'''#!/bin/bash
echo "SIPER: Hosts dosyası yedekleniyor..."
cp {self.app.hosts_file} {self.app.backup_file}
chown {os.getlogin()} {self.app.backup_file}
echo "SIPER: Yeni hosts dosyası uygulanıyor..."
cp {hosts_temp} {self.app.hosts_file}
echo "SIPER: İşlem tamamlandı!"
'''
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(script_content)
                script_temp = f.name
            
            os.chmod(script_temp, 0o755)
            self.app.debug.file_operation("CREATE_SCRIPT", script_temp, op_id)
            
            # Step 5: Execute with pkexec
            self.app.debug.step(5, 6, "pkexec ile yetki isteme ve uygulama", op_id)
            self.app.debug.permission_request("Hosts dosyası değiştirme için root yetki", op_id)
            self.app.debug.command_execution(['pkexec', 'bash', script_temp], op_id)
            
            result = subprocess.run(['pkexec', 'bash', script_temp], 
                                  capture_output=True, text=True, check=True)
            
            self.app.debug.success("pkexec komutu başarıyla çalıştırıldı", op_id)
            if result.stdout:
                self.app.debug.debug(f"Komut çıktısı: {result.stdout.strip()}", op_id)
            
            # Step 6: Cleanup
            self.app.debug.step(6, 6, "Geçici dosyaları temizleme", op_id)
            self.app.debug.operation_end(op_id, True, f"{len(self.app.blocked_sites)} site engellendi")
            return True
            
        except subprocess.CalledProcessError as e:
            self.app.debug.error(f"pkexec komutu başarısız: {e.stderr if e.stderr else 'Kullanıcı iptal etti'}", op_id, e)
            self.app.debug.operation_end(op_id, False, "Kullanıcı işlemi iptal etti")
            return False
        except Exception as e:
            self.app.debug.error(f"Beklenmeyen hata: {str(e)}", op_id, e)
            self.app.debug.operation_end(op_id, False, f"Hata: {str(e)}")
            return False
        finally:
            # Cleanup
            if hosts_temp and os.path.exists(hosts_temp):
                os.remove(hosts_temp)
                self.app.debug.file_operation("DELETE_TEMP", hosts_temp, op_id)
            if script_temp and os.path.exists(script_temp):
                os.remove(script_temp)
                self.app.debug.file_operation("DELETE_TEMP", script_temp, op_id)

    @debug_operation("Hosts Geri Yükleme")
    def restore_hosts(self):
        op_id = self.app.debug.operation_start("Hosts dosyası geri yükleme")
        
        try:
            # Mevcut hosts dosyasını oku
            self.app.debug.step(1, 3, "Mevcut hosts dosyasını okuma", op_id)
            with open(self.app.hosts_file, 'r') as f:
                content = f.read()
            
            # SIPER girişlerini temizle
            self.app.debug.step(2, 3, "SIPER girişlerini temizleme", op_id)
            lines = content.split('\n')
            filtered_lines = [line for line in lines if '# siper' not in line]
            new_content = '\n'.join(filtered_lines)
            
            # Geçici dosya oluştur
            hosts_temp = None
            script_temp = None
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(new_content)
                hosts_temp = f.name
            
            # Script oluştur
            script_content = f'''#!/bin/bash
cp {hosts_temp} {self.app.hosts_file}
'''
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(script_content)
                script_temp = f.name
            
            os.chmod(script_temp, 0o755)
            
            # pkexec ile çalıştır
            self.app.debug.step(3, 3, "Temizlenmiş hosts dosyasını uygulama", op_id)
            result = subprocess.run(['pkexec', 'bash', script_temp], 
                                  capture_output=True, text=True, check=True)
            
            # Cleanup
            if hosts_temp and os.path.exists(hosts_temp):
                os.remove(hosts_temp)
            if script_temp and os.path.exists(script_temp):
                os.remove(script_temp)
            
            self.app.debug.success("Tüm engeller kaldırıldı", op_id)
            self.app.debug.operation_end(op_id, True, "Geri yükleme başarılı")
            return True
            
        except subprocess.CalledProcessError as e:
            self.app.debug.error(f"Geri yükleme başarısız: {e.stderr if e.stderr else 'Kullanıcı iptal etti'}", op_id, e)
            self.app.debug.operation_end(op_id, False, "Kullanıcı işlemi iptal etti")
            return False
        except Exception as e:
            self.app.debug.error(f"Beklenmeyen hata: {str(e)}", op_id, e)
            self.app.debug.operation_end(op_id, False, f"Hata: {str(e)}")
            return False

    def on_custom_focus_mode(self, widget):
        try:
            minutes = int(self.custom_time_entry.get_text().strip())
            if minutes > 0:
                self.custom_time_entry.set_text("")
                self.on_focus_mode(widget, minutes)
            else:
                lang = self.app.language
                self.show_toast(f"{lang.get('messages', 'error')}: Invalid time")
        except ValueError:
            lang = self.app.language
            self.show_toast(f"{lang.get('messages', 'error')}: Invalid number")
    
    def on_focus_mode(self, widget, minutes):
        def focus_in_thread():
            try:
                success = self.backup_and_apply_blocking()
                if success:
                    self.app.is_blocking_active = True
                    self.app.current_focus_start = datetime.now()
                    self.app.save_config()
                    
                    # Timer başlat
                    self.app.focus_timer_id = GLib.timeout_add_seconds(
                        minutes * 60, self.on_focus_timer_end
                    )
                    
                    lang = self.app.language
                    GLib.idle_add(lambda: self.show_toast(f"{lang.get('messages', 'focus_started')} - {minutes} {lang.get('statistics', 'minutes')}"))
                    GLib.idle_add(self.update_toggle_button)
                    GLib.idle_add(self.update_status)
                else:
                    lang = self.app.language
                    GLib.idle_add(lambda: self.show_toast(lang.get('messages', 'operation_cancelled')))
            except Exception as e:
                lang = self.app.language
                GLib.idle_add(lambda: self.show_toast(f"{lang.get('messages', 'error')}: {str(e)}"))
        
        threading.Thread(target=focus_in_thread, daemon=True).start()
                       
                    self.app.is_blocking_active = False
                    self.app.current_focus_start = None
                    self.app.save_config()
                    self.app.focus_timer_id = None
                    lang = self.app.language
                    GLib.idle_add(lambda: self.show_toast(lang.get('messages', 'focus_ended')))
                    GLib.idle_add(self.update_toggle_button)
                    GLib.idle_add(self.update_status)
            except Exception as e:
                lang = self.app.language
                GLib.idle_add(lambda: self.show_toast(f"{lang.get('messages', 'error')}: {str(e)}"))
        
        threading.Thread(target=restore_in_thread, daemon=True).start()
        return False  # Timer'ı durdur
    
    def update_status(self):
        lang = self.app.language
        count = len(self.app.blocked_sites)
        if self.app.is_blocking_active:
            if self.app.focus_timer_id:
                status_text = lang.get('status', 'focus_mode')
            else:
                status_text = lang.get('status', 'active')
        else:
            status_text = lang.get('status', 'inactive')
        sites_text = lang.get('status', 'sites_in_list')
        self.status_label.set_text(f"{status_text} • {count} {sites_text}")

    def setup_actions(self):
        export_action = Gio.SimpleAction.new("export", None)
        export_action.connect("activate", self.on_export)
        self.app.add_action(export_action)
        
        import_action = Gio.SimpleAction.new("import", None)
        import_action.connect("activate", self.on_import)
        self.app.add_action(import_action)
        
        # Dil değiştirme action
        lang_action = Gio.SimpleAction.new("change_language", GLib.VariantType.new("s"))
        lang_action.connect("activate", self.on_language_selected)
        self.app.add_action(lang_action)
    
    def add_social_sites(self, widget):
        sites = ["facebook.com", "twitter.com", "x.com", "instagram.com", "tiktok.com", "linkedin.com", 
                "snapchat.com", "pinterest.com", "reddit.com", "discord.com", "telegram.org",
                "whatsapp.com", "messenger.com", "clubhouse.com", "mastodon.social", "threads.net",
                "vk.com", "weibo.com", "tumblr.com", "flickr.com", "meetup.com"]
        self._add_sites_from_list(sites, "sosyal medya")
    
    def add_video_sites(self, widget):
        sites = ["youtube.com", "netflix.com", "twitch.tv", "vimeo.com", "dailymotion.com",
                "hulu.com", "disneyplus.com", "primevideo.com", "hbomax.com", "crunchyroll.com",
                "peacocktv.com", "paramountplus.com", "appletv.com", "funimation.com", "vrv.co",
                "puhutv.com", "exxen.com", "blutv.com", "gain.tv", "tabii.com", "netflix.com.tr"]
        self._add_sites_from_list(sites, "video")
    
    def add_news_sites(self, widget):
        sites = ["cnn.com", "bbc.com", "hurriyet.com.tr", "sabah.com.tr", "milliyet.com.tr",
                "sozcu.com.tr", "haberturk.com", "ntv.com.tr", "cnnturk.com", "aa.com.tr",
                "reuters.com", "ap.org", "nytimes.com", "washingtonpost.com", "theguardian.com",
                "dw.com", "euronews.com", "aljazeera.com", "ensonhaber.com", "mynet.com",
                "gazetevatan.com", "star.com.tr", "aksam.com.tr", "cumhuriyet.com.tr"]
        self._add_sites_from_list(sites, "haber")
    
    def add_gaming_sites(self, widget):
        sites = ["store.steampowered.com", "epicgames.com", "origin.com", "battle.net", "riotgames.com",
                "minecraft.net", "roblox.com", "fortnite.com", "leagueoflegends.com", "valorant.com",
                "ubisoft.com", "ea.com", "rockstargames.com", "bethesda.net", "gog.com",
                "itch.io", "gamepass.com", "playstation.com", "xbox.com", "nintendo.com",
                "twitch.tv", "mixer.com", "youtube.com/gaming", "discord.gg"]
        self._add_sites_from_list(sites, "oyun")
    
    def add_shopping_sites(self, widget):
        sites = ["amazon.com", "amazon.com.tr", "ebay.com", "aliexpress.com", "trendyol.com", "hepsiburada.com",
                "n11.com", "ciceksepeti.com", "morhipo.com", "koton.com", "lcwaikiki.com",
                "defacto.com.tr", "boyner.com.tr", "migros.com.tr", "carrefoursa.com", "bim.com.tr",
                "a101.com.tr", "sok.com.tr", "teknosa.com", "vatan.com", "mediamarkt.com.tr",
                "gittigidiyor.com", "sahibinden.com", "letgo.com", "dolap.com", "modanisa.com"]
        self._add_sites_from_list(sites, "alışveriş")
    
    def add_adult_sites(self, widget):
        sites = ["pornhub.com", "xvideos.com", "xnxx.com", "redtube.com", "youporn.com",
                "tube8.com", "spankbang.com", "xhamster.com", "beeg.com", "sex.com",
                "chaturbate.com", "cam4.com", "livejasmin.com", "stripchat.com", "bongacams.com",
                "onlyfans.com", "manyvids.com", "clips4sale.com", "iwantclips.com", "adultwork.com",
                "brazzers.com", "realitykings.com", "bangbros.com", "naughtyamerica.com", "digitalplayground.com",
                "twistys.com", "babes.com", "mofos.com", "teamskeet.com", "familystrokes.com",
                "pornpics.com", "sex.com", "sexstories.com", "literotica.com", "asstr.org",
                "motherless.com", "heavy-r.com", "empflix.com", "slutload.com", "drtuber.com",
                "porntrex.com", "txxx.com", "hqporner.com", "eporner.com", "upornia.com",
                "4tube.com", "porntube.com", "xtube.com", "tnaflix.com", "sunporno.com",
                "perfectgirls.net", "freeones.com", "iafd.com", "adultdvdempire.com", "aebn.com",
                "flirt4free.com", "myfreecams.com", "camsoda.com", "cam4.com", "jerkmate.com",
                "adultfriendfinder.com", "ashley-madison.com", "seeking.com", "benaughty.com", "fuckbook.com"]
        self._add_sites_from_list(sites, "yetişkin")
    
    def add_crypto_sites(self, widget):
        sites = ["binance.com", "coinbase.com", "kraken.com", "bitfinex.com", "huobi.com",
                "kucoin.com", "gate.io", "bybit.com", "okx.com", "crypto.com",
                "gemini.com", "bitstamp.net", "bittrex.com", "poloniex.com", "ftx.com",
                "pancakeswap.org", "uniswap.org", "sushiswap.org", "1inch.io", "compound.finance",
                "btcturk.com", "paribu.com", "bitexen.com", "thodex.com", "icrypex.com"]
        self._add_sites_from_list(sites, "kripto")
    
    def add_torrent_sites(self, widget):
        sites = ["thepiratebay.org", "1337x.to", "rarbg.to", "yts.mx", "eztv.re",
                "torrentz2.eu", "limetorrents.info", "zooqle.com", "torlock.com", "kickasstorrents.to",
                "nyaa.si", "rutracker.org", "torrentgalaxy.to", "glodls.to", "torrentdownloads.me",
                "seedpeer.me", "torrenthound.com", "demonoid.is", "extratorrent.cc", "isohunt.to"]
        self._add_sites_from_list(sites, "torrent")
    
    def add_education_sites(self, widget):
        sites = ["coursera.org", "udemy.com", "edx.org", "khanacademy.org", "codecademy.com",
                "pluralsight.com", "lynda.com", "skillshare.com", "masterclass.com", "brilliant.org",
                "duolingo.com", "babbel.com", "memrise.com", "quizlet.com", "chegg.com",
                "studyblue.com", "coursehero.com", "scribd.com", "academia.edu", "researchgate.net",
                "acikders.ankara.edu.tr", "uzaktan.istanbul.edu.tr", "auzef.istanbul.edu.tr"]
        self._add_sites_from_list(sites, "eğitim")
    
    def add_work_sites(self, widget):
        sites = ["linkedin.com", "indeed.com", "glassdoor.com", "monster.com", "ziprecruiter.com",
                "careerbuilder.com", "upwork.com", "freelancer.com", "fiverr.com", "99designs.com",
                "slack.com", "teams.microsoft.com", "zoom.us", "meet.google.com", "webex.com",
                "trello.com", "asana.com", "notion.so", "monday.com", "basecamp.com",
                "kariyer.net", "yenibiris.com", "secretcv.com", "elemanonline.com", "randstad.com.tr"]
        self._add_sites_from_list(sites, "iş")
    
    def add_music_sites(self, widget):
        sites = ["spotify.com", "apple.com/music", "music.youtube.com", "soundcloud.com", "pandora.com",
                "deezer.com", "tidal.com", "amazon.com/music", "last.fm", "bandcamp.com",
                "mixcloud.com", "8tracks.com", "audiomack.com", "reverbnation.com", "genius.com",
                "shazam.com", "musixmatch.com", "songkick.com", "setlist.fm", "discogs.com",
                "muud.com", "fizy.com", "musicmax.com", "radyodinle.fm", "powertürk.com"]
        self._add_sites_from_list(sites, "müzik")
    
    def add_sports_sites(self, widget):
        sites = ["espn.com", "bleacherreport.com", "sbnation.com", "thescore.com", "cbssports.com",
                "foxsports.com", "skysports.com", "bbc.com/sport", "eurosport.com", "goal.com",
                "transfermarkt.com", "whoscored.com", "flashscore.com", "livescore.com", "sofascore.com",
                "fanatik.com.tr", "fotomac.com.tr", "aspor.com.tr", "sporx.com", "ntvspor.net",
                "trtspor.com.tr", "beinsports.com.tr", "spor.com", "mackolik.com", "nesine.com"]
        self._add_sites_from_list(sites, "spor")
    
    @debug_operation("Kategori Site Ekleme")
    def _add_sites_from_list(self, sites, category_name):
        op_id = self.app.debug.operation_start(f"{category_name} kategorisi site ekleme")
        
        self.app.debug.debug(f"Kategori: {category_name}, Toplam site: {len(sites)}", op_id)
        
        added = []
        skipped = 0
        
        for i, site in enumerate(sites):
            if site not in self.app.blocked_sites:
                self.app.blocked_sites.add(site)
                added.append(site)
                self.app.debug.debug(f"Eklendi ({i+1}/{len(sites)}): {site}", op_id)
            else:
                skipped += 1
        
        self.app.debug.debug(f"Eklenen: {len(added)}, Atlanan: {skipped}", op_id)
        
        if added:
            self.app.debug.step(1, 2, "Yapılandırma kaydediliyor", op_id)
            self.app.save_config()
            
            self.app.debug.step(2, 2, "Arayüz güncelleniyor", op_id)
            self.refresh_list()
            
            self.app.debug.success(f"{len(added)} {category_name} sitesi eklendi", op_id)
            lang = self.app.language
            self.show_toast(f"{len(added)} {category_name} {lang.get('messages', 'sites_added')}")
            self.app.debug.operation_end(op_id, True, f"Toplam site: {len(self.app.blocked_sites)}")
        else:
            self.app.debug.warning(f"Tüm {category_name} siteleri zaten listede", op_id)
            lang = self.app.language
            self.show_toast(f"{lang.get('messages', 'all_sites_exist')} {category_name} {lang.get('messages', 'sites_already_in_list')}")
            self.app.debug.operation_end(op_id, False, "Hiçbir yeni site eklenmedi")
    
    def on_export(self, action, param):
        lang = self.app.language
        dialog = Gtk.FileChooserDialog(
            title=lang.get('dialogs', 'export_title'),
            transient_for=self,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            lang.get('dialogs', 'cancel'), Gtk.ResponseType.CANCEL,
            lang.get('dialogs', 'save'), Gtk.ResponseType.ACCEPT
        )
        dialog.set_current_name("blocked_sites.json")
        dialog.connect("response", self.on_export_response)
        dialog.present()
    
    def on_import(self, action, param):
        lang = self.app.language
        dialog = Gtk.FileChooserDialog(
            title=lang.get('dialogs', 'import_title'),
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            lang.get('dialogs', 'cancel'), Gtk.ResponseType.CANCEL,
            lang.get('dialogs', 'open'), Gtk.ResponseType.ACCEPT
        )
        dialog.connect("response", self.on_import_response)
        dialog.present()
    
    def on_import_response(self, dialog, response):
        lang = self.app.language
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            try:
                with open(file.get_path(), 'r') as f:
                    sites = json.load(f)
                added = 0
                for site in sites:
                    if site not in self.app.blocked_sites:
                        self.app.blocked_sites.add(site)
                        added += 1
                if added > 0:
                    self.app.save_config()
                    self.refresh_list()
                self.show_toast(f"{added} {lang.get('messages', 'import_success')}")
            except Exception as e:
                self.show_toast(f"{lang.get('messages', 'error')}: {str(e)}")
        dialog.destroy()
     
    def show_stats(self, widget):
        lang = self.app.language
        dialog = Adw.Window()
        dialog.set_title(lang.get('dialogs', 'statistics_title'))
        dialog.set_default_size(400, 300)
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        
        # Calculate stats
        total_minutes = sum(session['duration_minutes'] for session in self.app.focus_history)
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60
        
        # This week stats
        week_ago = datetime.now() - timedelta(days=7)
        week_sessions = [s for s in self.app.focus_history 
                        if datetime.fromisoformat(s['start']) > week_ago]
        week_minutes = sum(session['duration_minutes'] for session in week_sessions)
        week_hours = week_minutes // 60
        week_remaining = week_minutes % 60
        
        # Content
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(24)
        content.set_margin_bottom(24)
        content.set_margin_start(24)
        content.set_margin_end(24)
        
        # Header
        header = Adw.HeaderBar()
        content.append(header)
        
        # Stats
        stats_group = Adw.PreferencesGroup()
        stats_group.set_title(lang.get('statistics', 'focus_statistics'))
        
        # Total time
        total_row = Adw.ActionRow()
        total_row.set_title(lang.get('statistics', 'total_time'))
        total_row.set_subtitle(f"{total_hours} {lang.get('statistics', 'hours')} {remaining_minutes} {lang.get('statistics', 'minutes')}")
        stats_group.add(total_row)
        
        # This week
        week_row = Adw.ActionRow()
        week_row.set_title(lang.get('statistics', 'this_week'))
        week_row.set_subtitle(f"{week_hours} {lang.get('statistics', 'hours')} {week_remaining} {lang.get('statistics', 'minutes')}")
        stats_group.add(week_row)
        
        # Session count
        session_row = Adw.ActionRow()
        session_row.set_title(lang.get('statistics', 'total_sessions'))
        session_row.set_subtitle(f"{len(self.app.focus_history)} {lang.get('statistics', 'sessions')}")
        stats_group.add(session_row)
        
        content.append(stats_group)
        dialog.set_content(content)
        dialog.present()
    
    def show_about(self, widget):
        from gi.repository import GdkPixbuf
        
        lang = self.app.language
        about = Adw.AboutWindow()
        about.set_transient_for(self)
        about.set_modal(True)
        
        about.set_application_name("S.I.P.E.R.")
        # Önce özel ikonu dene, yoksa varsayılanı kullan
        if os.path.exists('/usr/share/pixmaps/siperlo.png'):
            about.set_application_icon('siperlo')
        else:
            about.set_application_icon('applications-internet')
        about.set_version("1.0.0")
        about.set_developer_name("Fatih ÖNDER (CekToR) 🇹🇷")
        about.set_copyright(lang.get('about', 'copyright'))
        about.set_comments(f"{lang.get('general', 'app_subtitle')}\n\n{lang.get('general', 'app_description')}")
        
        about.set_website("https://github.com/cektor/S.I.P.E.R.")
        about.set_issue_url("https://github.com/cektor/S.I.P.E.R./issues")
        
        about.add_credit_section(lang.get('about', 'features_title'), [
            lang.get('about', 'feature_1'),
            lang.get('about', 'feature_2'),
            lang.get('about', 'feature_3'),
            lang.get('about', 'feature_4'),
            lang.get('about', 'feature_5'),
            lang.get('about', 'feature_6'),
            lang.get('about', 'feature_7')
        ])
        
        about.add_credit_section(lang.get('about', 'developer_title'), [
            lang.get('about', 'developer_name'),
            lang.get('about', 'company')
        ])
        
        about.add_credit_section(lang.get('about', 'technologies_title'), [
            lang.get('about', 'tech_1'),
            lang.get('about', 'tech_2'),
            lang.get('about', 'tech_3'),
            lang.get('about', 'tech_4')
        ])
        
        about.set_license_type(Gtk.License.GPL_3_0)
        about.present()

def main():
    import sys
    import platform
    
    # İşletim sistemi bilgisi
    os_name = platform.system()
    print(f"İşletim Sistemi: {os_name}")
    print(f"Platform: {platform.platform()}")
    print(f"Python Sürümü: {platform.python_version()}")
    
    # Terminal argümanları kontrolü
    if len(sys.argv) > 1:
        if '--help' in sys.argv or '-h' in sys.argv:
            print("\nS.I.P.E.R. - Site ve İçerik Engelleyici")
            print("Kullanım: python siper.py [seçenekler]")
            print("Seçenekler:")
            print("  -h, --help     Bu yardım mesajını göster")
            print("  --version      Sürüm bilgisini göster")
            print("  --debug        Debug modunda çalıştır")
            return 0
        
        if '--version' in sys.argv:
            print("S.I.P.E.R. v1.0.0")
            return 0

if __name__ == '__main__':
    sys.exit(main())
