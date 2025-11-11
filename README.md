# S.I.P.E.R. 🛡️

**System Internet Policy Enforcement Ruleset**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GTK 4](https://img.shields.io/badge/GTK-4.0-green.svg)](https://gtk.org/)
[![Made in Turkey](https://img.shields.io/badge/Made%20in-Turkey%20🇹🇷-red.svg)](https://github.com/cektor/S.I.P.E.R.)

A powerful, user-friendly website blocking and productivity application built with modern GTK 4 and Libadwaita. S.I.P.E.R. helps you maintain focus and productivity by blocking distracting websites with advanced features like Pomodoro focus mode, comprehensive statistics, and multi-language support.

![S.I.P.E.R. Screenshot](siperlo.png)

## ✨ Features

### 🛡️ **Advanced Website Blocking**
- **Secure hosts file management** with automatic backup and restore
- **Real-time blocking** without browser extensions or additional software
- **Bulk category blocking** with 12 predefined categories
- **Custom site addition** with intelligent URL parsing
- **Import/Export functionality** for sharing block lists

### 🍅 **Pomodoro Focus Mode**
- **Timed blocking sessions** (25, 60, 120 minutes or custom duration)
- **Automatic restoration** when focus time ends
- **Focus statistics tracking** with detailed session history
- **Motivational notifications** to keep you on track

### 📊 **Comprehensive Statistics**
- **Total focus time** tracking across all sessions
- **Weekly statistics** to monitor your progress
- **Session count** and duration analysis
- **Historical data** with persistent storage

### 🌍 **Multi-Language Support**
- **15 languages** including Turkish, English, Russian, German, French, Spanish, Japanese, Korean, and Turkic languages
- **Dynamic language switching** without restart
- **Localized interface** with proper RTL support where needed
- **Cultural adaptation** with appropriate flags and regional content

### 🎨 **Modern User Interface**
- **GTK 4 + Libadwaita** for native GNOME integration
- **Adaptive design** that works on different screen sizes
- **Dark/Light/Auto theme** support with system integration
- **Smooth animations** and modern visual feedback
- **Toast notifications** for user feedback

### 🔐 **Security & Privacy**
- **PolicyKit integration** for secure privilege management
- **No network dependencies** - works completely offline
- **Local data storage** with no cloud synchronization
- **Transparent operations** with detailed debug logging
- **Safe backup system** to prevent data loss

## 🚀 Quick Start

### Prerequisites

- **Linux** (Ubuntu 20.04+, Fedora 35+, Arch Linux, or any modern distribution)
- **Python 3.8+**
- **GTK 4.0+**
- **Libadwaita 1.0+**
- **PolicyKit** (usually pre-installed)

### Installation

#### Option 1: From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/cektor/S.I.P.E.R.git
cd S.I.P.E.R.

# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 polkit-1

# Install system dependencies (Fedora)
sudo dnf install python3-gobject gtk4-devel libadwaita-devel polkit

# Install system dependencies (Arch Linux)
sudo pacman -S python-gobject gtk4 libadwaita polkit

# Run the application
python3 siper.py
```

#### Option 2: System Installation

```bash
# Copy application files
sudo cp siper.py /usr/local/bin/siper
sudo chmod +x /usr/local/bin/siper

# Copy language files
sudo mkdir -p /usr/share/siper/languages/
sudo cp -r languages/* /usr/share/siper/languages/

# Copy icon
sudo cp siperlo.png /usr/share/pixmaps/

# Create desktop entry
cat > ~/.local/share/applications/siper.desktop << EOF
[Desktop Entry]
Name=S.I.P.E.R.
Comment=System Internet Policy Enforcement Ruleset
Exec=/usr/local/bin/siper
Icon=siperlo
Terminal=false
Type=Application
Categories=Utility;Network;
Keywords=website;blocker;productivity;focus;
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

### First Run

1. **Launch S.I.P.E.R.** from your application menu or run `python3 siper.py`
2. **Add websites** to block using the URL input field
3. **Choose quick categories** from the expandable menu (Social, Video, Gaming, etc.)
4. **Enable blocking** using the toggle button
5. **Start focus mode** for timed productivity sessions

## 📖 Usage Guide

### Basic Website Blocking

1. **Add Individual Sites:**
   - Enter a website URL in the input field (e.g., `facebook.com`)
   - Click "Add" or press Enter
   - The site will be added to your block list

2. **Use Quick Categories:**
   - Click on "Quick Actions" to expand the category menu
   - Select from 12 predefined categories:
     - 📱 **Social Media**: Facebook, Twitter, Instagram, TikTok, etc.
     - 🎥 **Video**: YouTube, Netflix, Twitch, etc.
     - 📰 **News**: CNN, BBC, local news sites
     - 🎮 **Gaming**: Steam, Epic Games, gaming platforms
     - 🛍️ **Shopping**: Amazon, eBay, e-commerce sites
     - 🔞 **Adult**: Adult content websites
     - ₿ **Crypto**: Cryptocurrency exchanges and trading platforms
     - 🌍 **Torrent**: BitTorrent and file sharing sites
     - 📚 **Education**: Online learning platforms
     - 💼 **Work**: Professional networking and job sites
     - 🎵 **Music**: Streaming and music platforms
     - 🏃 **Sports**: Sports news and streaming sites

3. **Enable/Disable Blocking:**
   - Use the main toggle button to activate or deactivate all blocks
   - When enabled, all sites in your list will be blocked system-wide
   - When disabled, all sites become accessible again

### Focus Mode (Pomodoro Technique)

1. **Quick Focus Sessions:**
   - Click on 25min, 60min, or 120min buttons for preset durations
   - Blocking will automatically activate for the selected time
   - A notification will appear when the session ends

2. **Custom Focus Sessions:**
   - Enter a custom duration in minutes in the text field
   - Click the play button (▶) to start
   - Perfect for personalized productivity schedules

3. **Focus Statistics:**
   - Click the statistics button (📊) to view your progress
   - See total focus time, weekly statistics, and session count
   - Track your productivity improvements over time

### Advanced Features

#### Import/Export Block Lists

- **Export:** Menu → Export → Save your block list as JSON
- **Import:** Menu → Import → Load a previously saved block list
- Share configurations between devices or with team members

#### Multi-Language Support

- Click the language button (🇹🇷 TR) in the header
- Choose from 15 available languages
- Interface will restart with the new language

#### Theme Customization

- Click the theme button (☀️/🌙/⚙️) to cycle through:
  - **Light Theme**: Bright, clean interface
  - **Dark Theme**: Easy on the eyes for low-light environments
  - **Auto Theme**: Follows your system preference

#### Statistics and Analytics

- **Total Time**: Cumulative focus time across all sessions
- **This Week**: Focus time for the current week
- **Session Count**: Number of completed focus sessions
- **Historical Data**: Persistent tracking of your productivity journey

## 🔧 Configuration

### Configuration Files

S.I.P.E.R. stores its configuration in `~/.config/siper/`:

```
~/.config/siper/
├── config.json          # Main configuration
├── stats.json           # Focus statistics
├── debug.log           # Debug information
├── hosts_backup        # Backup of original hosts file
└── languages/          # Language files (copied on first run)
    ├── english.ini
    ├── turkish.ini
    └── ...
```

### Configuration Options

The `config.json` file contains:

```json
{
  "blocked_sites": ["facebook.com", "youtube.com"],
  "is_active": false,
  "theme_mode": "auto",
  "language": "english"
}
```

### Custom Language Files

You can create custom language files by copying an existing `.ini` file from the `languages/` directory and translating the values. The file structure follows standard INI format:

```ini
[GENERAL]
app_name = S.I.P.E.R.
app_subtitle = System Internet Policy Enforcement Ruleset

[WINDOW]
title = S.I.P.E.R.
add_site_group = Add New Site
# ... more translations
```

## 🛠️ Technical Details

### Architecture

S.I.P.E.R. is built with a modern, modular architecture:

- **Frontend**: GTK 4 + Libadwaita for native Linux integration
- **Backend**: Python 3 with threading for non-blocking operations
- **Security**: PolicyKit (pkexec) for secure privilege escalation
- **Storage**: JSON-based configuration with atomic writes
- **Logging**: Comprehensive debug system with file and console output

### How It Works

1. **Hosts File Management**: S.I.P.E.R. modifies the system's `/etc/hosts` file to redirect blocked websites to `127.0.0.1` (localhost)
2. **Secure Operations**: All system-level changes require user authentication through PolicyKit
3. **Backup System**: Original hosts file is automatically backed up before any modifications
4. **Real-time Updates**: Changes take effect immediately without requiring browser restarts

### Security Considerations

- **Privilege Escalation**: Only occurs when explicitly requested by user actions
- **Backup Safety**: Original hosts file is always preserved
- **Atomic Operations**: File modifications are atomic to prevent corruption
- **User Control**: All operations can be reversed by the user

### Performance

- **Lightweight**: Minimal resource usage with efficient GTK 4 rendering
- **Fast Startup**: Optimized initialization and configuration loading
- **Responsive UI**: Non-blocking operations with proper threading
- **Memory Efficient**: Smart memory management with garbage collection

## 🐛 Troubleshooting

### Common Issues

#### "Permission Denied" Errors
```bash
# Ensure PolicyKit is installed and running
sudo systemctl status polkit

# Check if pkexec is available
which pkexec
```

#### GTK/Libadwaita Not Found
```bash
# Ubuntu/Debian
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1

# Fedora
sudo dnf install python3-gobject gtk4-devel libadwaita-devel

# Arch Linux
sudo pacman -S python-gobject gtk4 libadwaita
```

#### Application Won't Start
```bash
# Check Python version (3.8+ required)
python3 --version

# Install dependencies
pip install -r requirements.txt

# Run with debug output
python3 siper.py --debug
```

#### Hosts File Issues
```bash
# Check hosts file permissions
ls -la /etc/hosts

# Manually restore hosts file if needed
sudo cp ~/.config/siper/hosts_backup /etc/hosts
```

### Debug Mode

Run S.I.P.E.R. with debug output for troubleshooting:

```bash
python3 siper.py --debug
```

This will provide detailed logging information in both the terminal and `~/.config/siper/debug.log`.

### Getting Help

- **Check the logs**: `~/.config/siper/debug.log` contains detailed operation information
- **GitHub Issues**: Report bugs at [https://github.com/cektor/S.I.P.E.R./issues](https://github.com/cektor/S.I.P.E.R./issues)
- **Discussions**: Join community discussions on GitHub

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/S.I.P.E.R.git
cd S.I.P.E.R.

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Ways to Contribute

1. **🐛 Bug Reports**: Report issues with detailed reproduction steps
2. **💡 Feature Requests**: Suggest new features or improvements
3. **🌍 Translations**: Add support for new languages
4. **📝 Documentation**: Improve documentation and examples
5. **💻 Code**: Submit pull requests for bug fixes or new features
6. **🎨 Design**: Contribute UI/UX improvements
7. **🧪 Testing**: Help test new features and report feedback

### Translation Guidelines

To add a new language:

1. Copy `languages/english.ini` to `languages/yourlanguage.ini`
2. Translate all values (keep keys unchanged)
3. Add appropriate flag emoji and language code
4. Test the translation in the application
5. Submit a pull request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for public functions
- Include type hints where appropriate
- Write unit tests for new features

## 📄 License

S.I.P.E.R. is licensed under the **GNU General Public License v3.0**.

```
S.I.P.E.R. - System Internet Policy Enforcement Ruleset
Copyright (C) 2025 ALG Software Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

## 👨‍💻 Author & Credits

### Lead Developer
**Fatih ÖNDER (CekToR)** 🇹🇷
- GitHub: [@cektor](https://github.com/cektor)
- Company: ALG Software Inc.

### Technologies Used
- **GTK 4**: Modern user interface framework
- **Libadwaita**: GNOME design language and components
- **Python 3**: Main programming language
- **PolicyKit**: Secure privilege management system

### Acknowledgments
- GNOME Project for GTK 4 and Libadwaita
- Python Software Foundation
- The open-source community for inspiration and feedback
- All contributors and translators

## 🔗 Links

- **Homepage**: [https://github.com/cektor/S.I.P.E.R.](https://github.com/cektor/S.I.P.E.R.)
- **Issues**: [https://github.com/cektor/S.I.P.E.R./issues](https://github.com/cektor/S.I.P.E.R./issues)
- **Releases**: [https://github.com/cektor/S.I.P.E.R./releases](https://github.com/cektor/S.I.P.E.R./releases)
- **License**: [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)

---

**Made with ❤️ in Turkey 🇹🇷**

*S.I.P.E.R. - Taking control of your digital life, one blocked site at a time.*