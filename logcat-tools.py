import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from datetime import datetime
import zipfile
import os

class AdbLogcatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logcat Tools 0.2")

        self.check_dependencies()

        self.logcat_button = tk.Button(root, text="Start Logcat", command=self.start_logcat)
        self.logcat_button.grid(row=0, column=0, padx=10, pady=5, sticky="nw")

        self.logcat_with_grep_button = tk.Button(root, text="Start Logcat with Grep", command=self.start_logcat_with_grep)
        self.logcat_with_grep_button.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

        self.grep_entry = tk.Entry(root, width=30)
        self.grep_entry.grid(row=2, column=0, padx=10, pady=5, sticky="nw")

        self.set_logcat_size_button = tk.Button(root, text="Set Logcat Size", command=self.set_logcat_size)
        self.set_logcat_size_button.grid(row=3, column=0, padx=10, pady=5, sticky="nw")

        self.reboot_button = tk.Button(root, text="Reboot", command=self.reboot_device)
        self.reboot_button.grid(row=4, column=0, padx=10, pady=5, sticky="nw")

        self.clear_logcat_button = tk.Button(root, text="Clear Logcat", command=self.clear_logcat)
        self.clear_logcat_button.grid(row=5, column=0, padx=10, pady=5, sticky="nw")

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_logging)
        self.stop_button.grid(row=6, column=0, padx=10, pady=5, sticky="nw")

        self.stop_and_save_button = tk.Button(root, text="Stop and Save Logs", command=self.stop_and_save_logs)
        self.stop_and_save_button.grid(row=7, column=0, padx=10, pady=5, sticky="nw")

        self.change_theme_button = tk.Button(root, text="Change Theme", command=self.change_theme)
        self.change_theme_button.grid(row=8, column=0, padx=10, pady=5, sticky="nw")

        self.firmware_tools_button = tk.Button(root, text="Firmware Tools", command=self.run_firmware_tools)
        self.firmware_tools_button.grid(row=9, column=0, padx=10, pady=5, sticky="nw")

        self.close_button = tk.Button(root, text="Close", command=self.close_app)
        self.close_button.grid(row=10, column=0, padx=10, pady=5, sticky="nw")

        self.log_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, bg="black", fg="white", insertbackground="white")
        self.log_display.grid(row=0, column=1, rowspan=11, padx=10, pady=10, sticky="nsew")

        self.log_process = None
        self.grep_param = ""
        self.is_logging = False
        self.update_interval = 500  # milliseconds
        self.log_thread = None

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def check_dependencies(self):
        required_dependencies = ["pip", "adb"]

        for dependency in required_dependencies:
            try:
                subprocess.run([dependency, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                self.install_dependency(dependency)

    def install_dependency(self, package):
        if messagebox.askyesno("Dependency Missing", f"{package} is not installed. Do you want to install it?"):
            try:
                subprocess.run(["python", "-m", "ensurepip", "--default-pip"], check=True)
                subprocess.run(["python", "-m", "pip", "install", "--upgrade", package], check=True)
                messagebox.showinfo("Installation Complete", f"{package} has been installed or upgraded.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Installation Error", f"Failed to install {package}. Please install it manually.")

    def start_logcat(self):
        command = "adb logcat"
        self.start_log_process(command)

    def start_logcat_with_grep(self):
        grep_command = self.grep_entry.get()
        if not grep_command:
            messagebox.showwarning("Warning", "Please enter a grep command.")
            return
        self.grep_param = grep_command
        command = f'adb shell "logcat | grep {grep_command}"'
        self.start_log_process(command)

    def reboot_device(self):
        subprocess.run(["adb", "reboot"])
        messagebox.showinfo("Reboot", "Device is rebooting.")

    def clear_logcat(self):
        subprocess.run(["adb", "logcat", "-c"])
        self.log_display.delete(1.0, tk.END)
        messagebox.showinfo("Clear Logcat", "Logcat has been cleared.")

    def change_theme(self):
        current_bg = self.log_display.cget("bg")
        new_bg = "white" if current_bg == "black" else "black"
        current_fg = self.log_display.cget("fg")
        new_fg = "black" if current_fg == "white" else "white"
        current_insert_bg = self.log_display.cget("insertbackground")
        new_insert_bg = "black" if current_insert_bg == "white" else "white"

        self.log_display.configure(bg=new_bg, fg=new_fg, insertbackground=new_insert_bg)

    def run_firmware_tools(self):
        try:
            subprocess.run(["python", "updatemcu.py"], check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to run Firmware Tools. Make sure 'updatemcu.py' is in the same directory.")

    def start_log_process(self, command):
        self.log_display.delete(1.0, tk.END)
        self.is_logging = True
        self.log_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            text=True, bufsize=1, universal_newlines=True)
        self.log_thread = threading.Thread(target=self.read_logcat_output)
        self.log_thread.start()

    def read_logcat_output(self):
        while self.log_process.poll() is None and self.is_logging:
            try:
                line = self.log_process.stdout.readline()
                if line:
                    self.log_display.insert(tk.END, line)
                    self.log_display.see(tk.END)
            except Exception as e:
                print(f"Error reading logcat output: {e}")

        self.is_logging = False
        self.log_process.terminate()

    def stop_and_save_logs(self):
        self.is_logging = False
        if self.log_process:
            self.log_process.terminate()

        current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
        if self.grep_param:
            log_file_name = f"logcat_{self.grep_param}_{current_datetime}.log"
        else:
            log_file_name = f"logcat_{current_datetime}.log"

        with open(log_file_name, "w") as log_file:
            log_file.write(self.log_display.get(1.0, tk.END))

        # Compress the log file using zip with maximum compression
        compressed_log_file_name = f"{log_file_name}.zip"
        with zipfile.ZipFile(compressed_log_file_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
            zip_file.write(log_file_name, arcname=os.path.basename(log_file_name))

        # Delete the uncompressed log file
        os.remove(log_file_name)

        # Show the full path in the messagebox
        full_path = os.path.abspath(compressed_log_file_name)
        messagebox.showinfo("Logs Saved", f"Logs saved and compressed to:\n{full_path}")

        # Clear grep_param after saving logs
        self.grep_param = ""

    def stop_logging(self):
        self.is_logging = False
        if self.log_process:
            self.log_process.terminate()

    def set_logcat_size(self):
        size_mb = simpledialog.askinteger("Set Logcat Size", "Enter logcat size in MB:")
        if size_mb is not None:
            subprocess.run(['adb', 'logcat', '-G', f'{size_mb}MB'])
            messagebox.showinfo("Set Logcat Size", f"Logcat size set to {size_mb}MB.")

    def close_app(self):
        self.is_logging = False
        if self.log_process:
            self.log_process.terminate()
        if self.log_thread and self.log_thread.is_alive():
            self.log_thread.join()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdbLogcatApp(root)
    app.check_dependencies()  # Call check_dependencies on app startup
    root.mainloop()
