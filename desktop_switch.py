"""
Virtual Desktop Switcher for Windows 11
A lightweight overlay tool for quick switching between virtual desktops.
"""

import tkinter as tk
from tkinter import ttk
import ctypes
import ctypes.wintypes as wintypes
import time
import winreg
import json
import os


class VirtualDesktopOverlay:
    """Main application class for the Virtual Desktop Switcher overlay."""
    
    def __init__(self):
        """Initialize the overlay window and load configuration."""
        self.config_file = "desktop_switch_config.json"
        self.mode = "work"  # Modes: "work" or "inQuit"
        self.saved_alpha = 0.9  # Saved transparency for work mode
        
        self.root = tk.Tk()
        self.root.title("Virtual Desktops")
        
        # Window settings for overlay
        self.root.attributes('-topmost', True)  # Always on top
        self.root.overrideredirect(True)  # No window frame
        
        # Load position and transparency from config
        config = self.load_config()
        if config and 'alpha' in config:
            alpha = config['alpha']
            self.saved_alpha = alpha
            print(f"Loaded saved transparency: {alpha}")
        else:
            alpha = 0.9  # Default transparency
            self.saved_alpha = alpha
        
        self.root.attributes('-alpha', alpha)  # Set transparency
        
        # Automatically detect number of virtual desktops
        self.desktop_count = self.get_desktop_count()
        self.last_desktop_count = self.desktop_count
        print(f"Detected desktops: {self.desktop_count}")
        
        # Calculate width dynamically (10px margin left + right)
        width = 20 + (self.desktop_count * 43) + 20  # 43px per desktop button + 20px for close button
        height = 50
        screen_width = self.root.winfo_screenwidth()
        
        # Load position or use default
        if config and 'x' in config and 'y' in config:
            x = config['x']
            y = config['y']
            print(f"Loaded saved position: {x}, {y}")
        else:
            x = screen_width - width - 20
            y = 20
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Background color
        self.root.configure(bg='#1e1e1e')
        
        # Drag & drop functionality
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.on_drag)
        self.root.bind('<ButtonRelease-1>', self.end_drag)
        
        self.current_desktop = 0
        self.buttons = []
        self.close_button = None  # Reference to close button
        
        self.create_ui()
        self.update_current_desktop()
        
        # Auto-refresh every 500ms (checks desktop count and active desktop)
        self.auto_update()
    
    def get_desktop_count(self):
        """
        Determines the number of virtual desktops by reading Windows Registry.
        
        Returns:
            int: Number of virtual desktops, minimum 1
        """
        try:
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VirtualDesktops"
            
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
                desktop_ids, _ = winreg.QueryValueEx(key, "VirtualDesktopIDs")
                winreg.CloseKey(key)
                
                # Each desktop has a 16-byte GUID
                count = len(desktop_ids) // 16
                if count > 0:
                    return count
            except:
                pass
            
            # Fallback: At least 1 desktop always exists
            return 1
            
        except Exception as e:
            print(f"Error determining desktop count: {e}")
            return 2  # Fallback to 2 desktops
    
    def get_current_desktop_index(self):
        """
        Determines the index of the currently active desktop from Windows Registry.
        
        Returns:
            int: Index of current desktop (0-based)
        """
        try:
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VirtualDesktops"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
            
            # Read current desktop GUID
            try:
                current_desktop, _ = winreg.QueryValueEx(key, "CurrentVirtualDesktop")
            except:
                winreg.CloseKey(key)
                return 0  # Fallback to first desktop
            
            # Read all desktop IDs
            desktop_ids, _ = winreg.QueryValueEx(key, "VirtualDesktopIDs")
            winreg.CloseKey(key)
            
            # Find index by matching GUID
            for i in range(0, len(desktop_ids), 16):
                if desktop_ids[i:i+16] == current_desktop:
                    return i // 16
            
            return 0  # Fallback
            
        except Exception as e:
            print(f"Error determining current desktop: {e}")
            return self.current_desktop  # Keep current value
    
    def load_config(self):
        """
        Loads the saved configuration from JSON file.
        
        Returns:
            dict: Configuration dictionary or None if file doesn't exist
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        return None
    
    def save_config(self):
        """Saves current position and transparency to JSON file."""
        try:
            config = {
                'x': self.root.winfo_x(),
                'y': self.root.winfo_y(),
                'alpha': self.root.attributes('-alpha')
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            print(f"Position and transparency saved: x={config['x']}, y={config['y']}, alpha={config['alpha']}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def create_ui(self):
        """Creates the user interface with desktop buttons and close button."""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Desktop buttons
        button_frame = tk.Frame(main_frame, bg='#1e1e1e')
        button_frame.pack(side=tk.LEFT)
        
        for i in range(self.desktop_count):
            btn = tk.Button(button_frame, 
                          text=str(i + 1),
                          width=3,
                          height=1,
                          bg='#3c3c3c',
                          fg='white',
                          font=('Segoe UI', 10, 'bold'),
                          relief=tk.RAISED,
                          bd=2,
                          cursor='hand2',
                          command=lambda idx=i: self.on_desktop_button_click(idx))
            btn.pack(side=tk.LEFT, padx=3)
            self.buttons.append(btn)
        
        # Close button
        self.close_button = tk.Button(main_frame,
                             text='✕',
                             width=2,
                             height=1,
                             bg='#b43434',
                             fg='white',
                             font=('Segoe UI', 10, 'bold'),
                             relief=tk.RAISED,
                             bd=2,
                             cursor='hand2',
                             command=self.on_close_button_click)
        self.close_button.pack(side=tk.LEFT, padx=(5, 0))
    
    def on_desktop_button_click(self, index):
        """
        Handler for desktop button clicks.
        
        Args:
            index (int): Index of the desktop to switch to
        """
        if self.mode == "inQuit":
            self.exit_quit_mode()
        self.switch_desktop(index)
    
    def on_close_button_click(self):
        """Handler for close button clicks. Enters quit mode or exits application."""
        if self.mode == "work":
            self.enter_quit_mode()
        else:  # inQuit mode
            print("Exiting application")
            self.root.quit()
            self.root.destroy()
            import sys
            sys.exit(0)
    
    def enter_quit_mode(self):
        """Enters quit confirmation mode (button turns green, full opacity)."""
        print("Entering quit mode")
        self.mode = "inQuit"
        
        # Remove transparency
        self.saved_alpha = self.root.attributes('-alpha')
        self.root.attributes('-alpha', 1.0)
        
        # Change close button to green question mark
        self.close_button.configure(
            text='?',
            bg='#34b434',  # Green
            fg='white'
        )
    
    def exit_quit_mode(self):
        """Exits quit mode back to work mode."""
        print("Returning to work mode")
        self.mode = "work"
        
        # Restore transparency
        self.root.attributes('-alpha', self.saved_alpha)
        
        # Reset close button to red X
        self.close_button.configure(
            text='✕',
            bg='#b43434',  # Red
            fg='white'
        )
    
    def start_drag(self, event):
        """
        Initiates drag operation. Always updates position reference to avoid jump bugs.
        
        Args:
            event: Tkinter event object containing mouse position
        """
        # Initialize drag tracking - ALWAYS set these values to prevent delta calculation bugs
        self.drag_step_count = 0
        self.x = event.x
        self.y = event.y
        
        # Ignore clicks on buttons (they have their own handlers)
        if event.widget.winfo_class() == 'Button':
            return
        
        # Exit quit mode when dragging window
        if self.mode == "inQuit":
            self.exit_quit_mode()
    
    def on_drag(self, event):
        """
        Handles window dragging. 
        
        Args:
            event: Tkinter event object containing mouse position
        """
        self.drag_step_count += 1
        
        # Calculate movement delta
        deltax = event.x - self.x
        deltay = event.y - self.y
        
        print(f"Dragging: delta=({deltax}, {deltay}), step={self.drag_step_count}")
        
        # Move window
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def end_drag(self, event):
        """
        Saves position after dragging (only in work mode and if actually dragged).
        
        Args:
            event: Tkinter event object
        """
        if self.mode == "work" and hasattr(self, 'drag_step_count') and self.drag_step_count > 1:
            self.save_config()
    
    def switch_desktop(self, index):
        """
        Switches to specified desktop by simulating Win+Ctrl+Arrow key combinations.
        
        Args:
            index (int): Target desktop index (0-based)
        """
        try:
            # Calculate how many steps we need to move
            steps = index - self.current_desktop
            
            if steps == 0:
                return  # Already on the correct desktop
            
            # Windows keyboard combination: Win + Ctrl + Arrow
            VK_LWIN = 0x5B
            VK_CONTROL = 0x11
            VK_LEFT = 0x25
            VK_RIGHT = 0x27
            
            # Determine direction
            arrow_key = VK_RIGHT if steps > 0 else VK_LEFT
            steps = abs(steps)
            
            # Execute the steps
            for _ in range(steps):
                # Press keys
                ctypes.windll.user32.keybd_event(VK_LWIN, 0, 0, 0)
                time.sleep(0.02)
                ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
                time.sleep(0.02)
                ctypes.windll.user32.keybd_event(arrow_key, 0, 0, 0)
                time.sleep(0.02)
                
                # Release keys
                ctypes.windll.user32.keybd_event(arrow_key, 0, 2, 0)
                time.sleep(0.02)
                ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
                time.sleep(0.02)
                ctypes.windll.user32.keybd_event(VK_LWIN, 0, 2, 0)
                
                # Brief pause between steps
                time.sleep(0.1)
            
            # Update desktop index
            self.current_desktop = index
            
            # Update button display immediately
            self.update_current_desktop()
            
        except Exception as e:
            print(f"Error switching desktop: {e}")
    
    def update_current_desktop(self):
        """Updates the visual indication of the currently active desktop."""
        # Get current desktop index from Registry
        detected_desktop = self.get_current_desktop_index()
        
        # If desktop changed, update display
        if detected_desktop != self.current_desktop:
            print(f"Desktop change detected: {self.current_desktop} -> {detected_desktop}")
            self.current_desktop = detected_desktop
        
        # Update all buttons
        for i, btn in enumerate(self.buttons):
            if i == self.current_desktop:
                btn.configure(bg='#0078d7', relief=tk.SUNKEN)
            else:
                btn.configure(bg='#3c3c3c', relief=tk.RAISED)
    
    def auto_update(self):
        """Automatically updates display and checks for desktop count changes."""
        self.update_current_desktop()
        
        # Check every 500ms if number of desktops changed
        new_count = self.get_desktop_count()
        if new_count != self.last_desktop_count:
            print(f"Desktop count changed: {self.last_desktop_count} -> {new_count}")
            self.last_desktop_count = new_count
            self.desktop_count = new_count
            # Recreate UI with new button count
            self.recreate_ui()
        
        self.root.after(500, self.auto_update)  # Update every 500ms for quick response
    
    def recreate_ui(self):
        """Recreates the UI when the number of desktops changes."""
        # Delete all widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Clear button list
        self.buttons = []
        
        # Adjust window width
        width = 20 + (self.desktop_count * 43) + 20  # 43px per desktop button + 20px for close button
        height = 50
        x = self.root.winfo_x()  # Keep current position
        y = self.root.winfo_y()
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Recreate UI
        self.create_ui()
    
    def run(self):
        """Starts the Tkinter main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = VirtualDesktopOverlay()
    app.run()