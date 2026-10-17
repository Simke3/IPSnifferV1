import os
import platform
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IPSniffer")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Main Container
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title Label
        self.title_label = ttk.Label(
            self.main_frame, 
            text="IPSNIFFER", 
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=10)
        
        # Input Frame
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=10)
        
        self.entry_label = ttk.Label(self.input_frame, text="Enter IP Address:", font=("Arial", 10))
        self.entry_label.pack(side=tk.LEFT, padx=5)
        
        self.ip_entry = ttk.Entry(self.input_frame, font=("Arial", 10), width=20)
        self.ip_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.ip_entry.focus()
        
        # Bind Enter key to the ping function
        self.ip_entry.bind("<Return>", lambda event: self.start_ping_thread())
        
        # Check Button
        self.check_button = ttk.Button(
            self.main_frame, 
            text="Check Status", 
            command=self.start_ping_thread
        )
        self.check_button.pack(pady=10)
        
        # Result Display Label
        self.result_label = tk.Label(
            self.main_frame, 
            text="Status: Idle", 
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#555555",
            relief=tk.GROOVE,
            pady=10
        )
        self.result_label.pack(fill=tk.X, pady=10)

    def start_ping_thread(self):
        """Starts the ping process in a background thread to keep the GUI responsive."""
        target_ip = self.ip_entry.get().strip()
        if not target_ip:
            self.result_label.config(text="Status: Please enter a valid IP!", fg="orange")
            return
            
        self.result_label.config(text="Status: Checking...", fg="blue")
        self.check_button.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.ping_device, args=(target_ip,))
        thread.daemon = True
        thread.start()

    def ping_device(self, ip):
        # Determine the OS specific ping parameters
        is_windows = platform.system().lower() == "windows"
        param = "-n" if is_windows else "-c"
        
        try:
            if is_windows:
            
                result = subprocess.run(
                    ["ping", param, "1", "-w", "1000", ip],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=0x08000000
                )
            else:
                result = subprocess.run(
                    ["ping", param, "1", "-W", "1", ip],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # Update GUI elements safely from the thread
            if result.returncode == 0:
                self.root.after(0, self.update_gui_success, ip)
            else:
                self.root.after(0, self.update_gui_failure, ip)
                
        except Exception as e:
            self.root.after(0, self.update_gui_error, str(e))

    def update_gui_success(self, ip):
        self.result_label.config(text=f"ONLINE: Device {ip} is active!", fg="white", bg="green")
        self.check_button.config(state=tk.NORMAL)

    def update_gui_failure(self, ip):
        self.result_label.config(text=f"OFFLINE: Device {ip} did not respond.", fg="white", bg="red")
        self.check_button.config(state=tk.NORMAL)
        
    def update_gui_error(self, error_msg):
        self.result_label.config(text=f"Error: Unable to execute ping.", fg="black", bg="yellow")
        self.check_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()
