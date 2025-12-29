# Contributing to Virtual Desktop Switcher

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs 🐛

If you find a bug, please open an issue with:
- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **System information** (Windows version, Python version)
- **Screenshots** if applicable

### Suggesting Features 💡

Feature requests are welcome! Please:
- Check if the feature has already been requested
- Explain the use case and why it would be useful
- Consider if it fits the "minimal and lightweight" philosophy

### Submitting Pull Requests 🔧

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly** on Windows 11
5. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
6. **Push to your fork** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Code Style Guidelines

- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and single-purpose
- Maintain the minimal dependency philosophy (no external packages)

### Testing Checklist

Before submitting, please verify:
- [ ] Works on Windows 11
- [ ] Desktop detection works correctly
- [ ] Desktop switching works in all directions
- [ ] Config saving/loading works
- [ ] Quit mode works as expected
- [ ] No errors in console output
- [ ] Window positioning persists correctly

## Development Setup

```bash
git clone https://github.com/yourusername/virtual-desktop-switcher.git
cd virtual-desktop-switcher
python desktop_switch.py
```

That's it! No dependencies to install.

## Ideas for Future Features

- Desktop naming/labels instead of just numbers
- Global hotkeys for switching
- Minimize to system tray
- Multiple monitor support optimization
- Themes/color schemes
- Desktop wallpaper preview on hover
- Integration with Windows 11 Snap Layouts

## Questions?

Feel free to open an issue for any questions about contributing!

---

**Note:** This is a personal project, so response times may vary. Please be patient! 😊