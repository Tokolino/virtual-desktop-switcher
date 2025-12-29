# Virtual Desktop Switcher

A lightweight, always-on-top overlay for Windows 11 that makes switching between virtual desktops fast and intuitive.

![Virtual Desktop Switcher Demo](screenshot.png)

## ✨ Features

- **🎯 Quick Desktop Switching** - Click numbered buttons to instantly switch between virtual desktops
- **👁️ Always Visible** - Stays on top of all windows, including RDP full-screen sessions
- **🔄 Auto-Detection** - Automatically detects desktop changes (keyboard shortcuts, taskbar, Teams calls)
- **📊 Dynamic Button Count** - Adapts to the number of virtual desktops you have
- **💾 Remembers Settings** - Saves window position and transparency between sessions
- **🎨 Customizable Transparency** - Set your preferred transparency level (0.1 - 1.0)
- **✋ Safe Quit Mode** - Two-step confirmation prevents accidental closure
- **🪶 Minimal & Lightweight** - Small footprint, no external dependencies

## 📋 Requirements

- **Windows 11** (with Virtual Desktops enabled)
- **Python 3.8+** (standard library only - no pip packages needed!)

## 🚀 Installation

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation

2. **Download the script**
   ```bash
   git clone https://github.com/Tokolino/virtual-desktop-switcher.git
   cd virtual-desktop-switcher
   ```

3. **Run the script**
   ```bash
   python desktop_switch.py
   ```

## 🎮 Usage

### Basic Controls
- **Click numbered buttons** - Switch to that desktop
- **Drag the window** - Move it anywhere on screen
- **Click red ✕** - Enter quit mode (button turns green ?)
- **Click green ?** - Confirm exit
- **Move window or click desktop button** - Cancel quit mode

### Keyboard Shortcuts Still Work
The overlay doesn't interfere with Windows native shortcuts:
- `Win + Ctrl + Left/Right` - Navigate between desktops
- `Win + Ctrl + 1-9` - Jump to specific desktop (if supported)
- `Win + Tab` - Open Task View

### Auto-Start on Windows Boot

**Method 1: Startup Folder (Recommended)**
1. Rename `desktop_switch.py` to `desktop_switch.pyw` (no console window)
2. Press `Win + R`, type `shell:startup`, press Enter
3. Create a shortcut to `desktop_switch.pyw` in this folder

**Method 2: Task Scheduler**
- For more control over startup delay, administrator privileges, etc.

## ⚙️ Configuration

Settings are automatically saved to `desktop_switch_config.json`:

```json
{
  "x": 1568,
  "y": 761,
  "alpha": 0.2
}
```

- **x, y** - Window position
- **alpha** - Transparency (0.1 = very transparent, 1.0 = fully opaque)

Edit this file manually to change transparency, or move the window to update position.

## 🛠️ How It Works

The tool uses Windows Registry to:
1. **Detect desktop count** - Reads `VirtualDesktopIDs` from Registry
2. **Track active desktop** - Monitors `CurrentVirtualDesktop` every 500ms
3. **Switch desktops** - Simulates `Win + Ctrl + Arrow` key combinations

No hooks, no admin rights required, no system modifications!

## 🐛 Troubleshooting

**"Desktop switching doesn't work"**
- Make sure you have multiple virtual desktops created (`Win + Tab` → New Desktop)
- Test if `Win + Ctrl + Left/Right` works manually

**"Active desktop not updating"**
- Your Windows version might not update `CurrentVirtualDesktop` in Registry
- This is a known limitation on some Windows 11 builds

**"Window disappears on startup"**
- Check `desktop_switch_config.json` - window position might be off-screen
- Delete the config file to reset to default position

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

## 🙏 Acknowledgments

Built with Python's tkinter and Windows Registry APIs.

## 📧 Contact

Have questions or suggestions? Open an issue on GitHub!

---

⭐ If you find this useful, please consider starring the repository!
