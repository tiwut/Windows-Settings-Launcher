import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

SETTINGS_COMMANDS = {
    "Device Manager": "devmgmt.msc",
    "Disk Management": "diskmgmt.msc",
    "System Information": "msinfo32",
    "System Configuration (msconfig)": "msconfig",
    "Task Manager": "taskmgr",
    "Computer Management": "compmgmt.msc",
    "Event Viewer": "eventvwr.msc",
    "Services": "services.msc",
    "Resource Monitor": "resmon",
    "Registry Editor": "regedit",
    "Group Policy Editor": "gpedit.msc",
    "System Properties (Classic)": "sysdm.cpl",
    "Date and Time": "timedate.cpl",
    "Power Options": "powercfg.cpl",
    "Regional Settings": "intl.cpl",
    "ODBC Data Sources": "odbcad32.exe",

    "Network Connections": "ncpa.cpl",
    "Windows Defender Firewall": "firewall.cpl",
    "Remote Desktop Connection": "mstsc",
    "Network Status": "ms-settings:network-status",
    "VPN Settings": "ms-settings:network-vpn",
    "Proxy Settings": "ms-settings:network-proxy",
    "Mobile Hotspot": "ms-settings:network-mobilehotspot",
    
    "Windows Security": "ms-settings:windowsdefender",
    "Credential Manager": "credwiz",
    "User Accounts (Netplwiz)": "netplwiz",
    "Local Users and Groups": "lusrmgr.msc",
    "Certificate Manager": "certmgr.msc",
    "Accounts (User Info)": "ms-settings:yourinfo",
    "Sign-in Options": "ms-settings:signinoptions",

    "About Windows/System": "ms-settings:about",
    "Display Settings": "ms-settings:display",
    "Sound Settings": "ms-settings:sound",
    "Notifications & Focus": "ms-settings:notifications",
    "Power & Sleep": "ms-settings:powersleep",
    "Storage Settings": "ms-settings:storagesense",
    "Troubleshoot Settings": "ms-settings:troubleshoot",
    "Update & Security": "ms-settings:windowsupdate",
    "Recovery Options": "ms-settings:recovery",
    "Privacy & Security": "ms-settings:privacy",
    "Personalization": "ms-settings:personalization",
    "Time & Language": "ms-settings:dateandtime",
    "Gaming (Xbox Game Bar)": "ms-settings:gaming-gamebar",
    
    "Apps & Features": "ms-settings:appsfeatures",
    "Default Apps": "ms-settings:defaultapps",
    "Optional Features": "ms-settings:optionalfeatures",
    "Programs and Features (Classic)": "appwiz.cpl",
    "Bluetooth & Devices": "ms-settings:bluetooth",
    "Printers & Scanners": "ms-settings:printers",
    "Mouse & Touchpad": "ms-settings:mousetouchpad",
    "Keyboard Settings": "ms-settings:keyboard",
    "Mouse Properties (main.cpl)": "main.cpl",

    "Magnifier": "magnify",
    "On-Screen Keyboard": "osk",
    "Narrator": "narrator",
    "Accessibility - Mouse": "ms-settings:easeofaccess-mouse",
    "Calculator": "calc",
    "Notepad": "notepad",
    "Administrative Tools Folder": "control admintools", 
    "Indexing Options": "searchindexer.exe",
    "Color Management": "colorcpl",
}

BG_DARK = "#1E1E1E"
FG_LIGHT = "#FFFFFF"
BG_SECONDARY = "#2D2D2D"
ACCENT_BLUE = "#0A84FF"
TEXT_SUBTLE = "#AAAAAA"

class WindowsSettingsApp(tk.Tk):
    """Main application class for the Windows Settings Launcher with Dark Mode."""
    
    def __init__(self):
        super().__init__()
        self.title("Windows Settings Launcher")
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam') 
        
        self.style.configure('TLabel', background=BG_DARK, foreground=FG_LIGHT, font=('Segoe UI', 10))
        self.style.configure('TFrame', background=BG_DARK)
        self.style.configure('Dark.TEntry', fieldbackground=BG_SECONDARY, foreground=FG_LIGHT, borderwidth=1, relief='flat', font=('Segoe UI', 12))
        
        self.style.configure('Accent.TButton', 
                             background=ACCENT_BLUE, 
                             foreground=FG_LIGHT,
                             font=('Segoe UI', 12, 'bold'),
                             borderwidth=0,
                             padding=[10, 8])
        self.style.map('Accent.TButton', 
                       background=[('active', '#59a8ff'), ('!disabled', ACCENT_BLUE)],
                       foreground=[('active', FG_LIGHT), ('!disabled', FG_LIGHT)])
        
        self.geometry("600x650")
        self.configure(bg=BG_DARK) 
        self.settings_list = sorted(list(SETTINGS_COMMANDS.keys()))
        
        self.create_widgets()
        self.filter_list() 

    def create_widgets(self):
        """Creates the UI elements of the application."""
        
        search_frame = ttk.Frame(self, padding="10 10 10 5")
        search_frame.pack(fill='x')
        
        ttk.Label(search_frame, text="Search Settings:", font=('Segoe UI', 11, 'bold')).pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda name, index, mode: self.filter_list())
        
        search_entry = ttk.Entry(search_frame, 
                                 textvariable=self.search_var, 
                                 width=50,
                                 style='Dark.TEntry')
        search_entry.pack(fill='x', expand=True, ipady=4)
        search_entry.focus_set()

        list_frame = ttk.Frame(self, padding="10 5 10 5")
        list_frame.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        
        self.settings_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Segoe UI', 12),
            bd=0,
            highlightthickness=0,
            selectmode=tk.SINGLE,
            bg=BG_SECONDARY,
            fg=FG_LIGHT,
            selectbackground=ACCENT_BLUE,
            selectforeground="white",
            relief=tk.FLAT 
        )
        self.settings_listbox.bind("<Double-Button-1>", self.open_selected_setting)
        self.settings_listbox.bind("<Return>", self.open_selected_setting)
        
        scrollbar.config(command=self.settings_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.settings_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        
        ttk.Label(
            self, 
            text="Double-click or press Enter to launch the setting.\n(This application is designed for and runs only on Windows)", 
            foreground=TEXT_SUBTLE,
            font=('Segoe UI', 9, 'italic')
        ).pack(pady=(5, 10))
        
        open_button = ttk.Button(
            self, 
            text="Launch Setting", 
            command=self.open_selected_setting, 
            style='Accent.TButton'
        )
        open_button.pack(fill='x', padx=10, pady=(0, 10))
        
    def filter_list(self):
        """Filters the Listbox items based on the search input."""
        search_term = self.search_var.get().lower()
        
        self.settings_listbox.delete(0, tk.END)

        for setting in self.settings_list:
            if search_term in setting.lower():
                self.settings_listbox.insert(tk.END, setting)

    def open_selected_setting(self, event=None):
        """Launches the currently selected Windows setting."""
        try:
            selected_indices = self.settings_listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Warning", "Please select a setting from the list first.")
                return
            
            setting_name = self.settings_listbox.get(selected_indices[0])
            command = SETTINGS_COMMANDS.get(setting_name)

            if command:
                print(f"Attempting to execute command: '{command}'")
                
                try:
                    os.startfile(command)
                    return
                except FileNotFoundError:
                    try:
                        subprocess.run(command, shell=True, check=False)
                    except Exception as e:
                        messagebox.showerror("Launch Error", f"The setting could not be launched. (Error: {e})")
                        print(f"Other launch error for '{command}': {e}")
                
            else:
                messagebox.showerror("Error", "Command not found for this setting.")
                
        except Exception as e:
            messagebox.showerror("General Error", f"An unexpected error occurred: {e}")
            print(f"General error: {e}")

if __name__ == "__main__":
    if os.name != 'nt':
        print("WARNING: This script is exclusively designed for Windows operating systems.")
    
    app = WindowsSettingsApp()
    app.mainloop()