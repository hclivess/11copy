import customtkinter as ctk
import json
import os
import shutil
from pathlib import Path
from tkinter import filedialog, messagebox


class BackupApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("11copy")
        self.geometry("700x500")

        # Set the theme
        ctk.set_appearance_mode("system")  # Use system theme
        ctk.set_default_color_theme("blue")  # Default color theme

        # Load or create config
        self.config_file = "config.json"
        self.config = self.load_config()

        self.create_gui()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"source_dir": "", "target_dir": ""}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_gui(self):
        # Create main frame with consistent padding
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header
        header = ctk.CTkLabel(
            self.main_frame,
            text="11copy",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(pady=10)

        # Source Directory Frame
        source_frame = ctk.CTkFrame(self.main_frame)
        source_frame.pack(fill="x", padx=10, pady=5)

        source_label = ctk.CTkLabel(
            source_frame,
            text="Source Directory:",
            font=ctk.CTkFont(size=14)
        )
        source_label.pack(anchor="w", pady=5, padx=5)

        self.source_var = ctk.StringVar(value=self.config["source_dir"])
        self.source_entry = ctk.CTkEntry(
            source_frame,
            textvariable=self.source_var,
            width=480,
            height=32
        )
        self.source_entry.pack(side="left", padx=5)

        source_btn = ctk.CTkButton(
            source_frame,
            text="Browse",
            width=100,
            height=32,
            command=self.select_source
        )
        source_btn.pack(side="left", padx=5)

        # Target Directory Frame
        target_frame = ctk.CTkFrame(self.main_frame)
        target_frame.pack(fill="x", padx=10, pady=5)

        target_label = ctk.CTkLabel(
            target_frame,
            text="Target Directory:",
            font=ctk.CTkFont(size=14)
        )
        target_label.pack(anchor="w", pady=5, padx=5)

        self.target_var = ctk.StringVar(value=self.config["target_dir"])
        self.target_entry = ctk.CTkEntry(
            target_frame,
            textvariable=self.target_var,
            width=480,
            height=32
        )
        self.target_entry.pack(side="left", padx=5)

        target_btn = ctk.CTkButton(
            target_frame,
            text="Browse",
            width=100,
            height=32,
            command=self.select_target
        )
        target_btn.pack(side="left", padx=5)

        # Progress bar
        progress_frame = ctk.CTkFrame(self.main_frame)
        progress_frame.pack(fill="x", padx=10, pady=5)

        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        self.progress_bar.set(0)

        # Status
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            progress_frame,
            textvariable=self.status_var,
            wraplength=700
        )
        self.status_label.pack(pady=10)

        # Backup Button
        backup_btn = ctk.CTkButton(
            self.main_frame,
            text="Start Backup",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=200,
            height=50,
            command=self.start_backup
        )
        backup_btn.pack(pady=20)

        # Theme switcher
        theme_frame = ctk.CTkFrame(self.main_frame)
        theme_frame.pack(fill="x", padx=20, pady=(20, 0))

        theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        theme_switch.pack(side="right")

        # Bind entry changes
        self.source_var.trace_add("write", self.on_source_change)
        self.target_var.trace_add("write", self.on_target_change)

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def on_source_change(self, *args):
        self.config["source_dir"] = self.source_var.get()
        self.save_config()

    def on_target_change(self, *args):
        self.config["target_dir"] = self.target_var.get()
        self.save_config()

    def select_source(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_var.set(directory)
            self.config["source_dir"] = directory
            self.save_config()

    def select_target(self):
        directory = filedialog.askdirectory()
        if directory:
            self.target_var.set(directory)
            self.config["target_dir"] = directory
            self.save_config()

    def start_backup(self):
        source_dir = self.source_var.get()
        target_dir = self.target_var.get()

        if not source_dir or not target_dir:
            messagebox.showerror("Error", "Please select both source and target directories")
            return

        if not os.path.exists(source_dir):
            messagebox.showerror("Error", "Source directory does not exist")
            return

        # Prevent backup into source directory with proper path comparison
        source_path = os.path.abspath(source_dir)
        target_path = os.path.abspath(target_dir)

        # Compare normalized paths
        if os.path.commonpath([source_path]) == os.path.commonpath([source_path, target_path]):
            messagebox.showerror("Error", "Target directory cannot be inside source directory")
            return

        try:
            self.perform_backup(source_dir, target_dir)
            messagebox.showinfo("Success", "Backup completed successfully!")
            self.status_var.set("Backup completed successfully!")
            self.progress_bar.set(1)
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")

    def perform_backup(self, source_dir, target_dir):
        self.status_var.set("Analyzing files...")
        self.progress_bar.set(0)
        self.update()

        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        # First scan to determine which files need copying
        files_to_copy = []
        for root, dirs, files in os.walk(source_dir):
            rel_path = os.path.relpath(root, source_dir)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, rel_path, file)

                # Skip files with path too long
                if len(dst_file) >= 260:
                    continue

                # Check if file needs to be updated
                needs_copy = False
                if not os.path.exists(dst_file):
                    needs_copy = True
                else:
                    src_mtime = os.path.getmtime(src_file)
                    dst_mtime = os.path.getmtime(dst_file)
                    if src_mtime > dst_mtime:
                        needs_copy = True

                if needs_copy:
                    files_to_copy.append((src_file, dst_file, rel_path))

        total_files = len(files_to_copy)
        copied_files = 0

        if total_files == 0:
            self.status_var.set("No files need updating")
            self.progress_bar.set(1)
            return

        # Perform the actual backup
        for src_file, dst_file, rel_path in files_to_copy:
            try:
                # Ensure target subdirectory exists
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)

                # Copy file with metadata
                shutil.copy2(src_file, dst_file)
                copied_files += 1

            except Exception as e:
                self.status_var.set(f"Error copying {os.path.basename(src_file)}: {str(e)}")
                continue

            self.status_var.set(f"Copying files... ({copied_files}/{total_files})")
            self.progress_bar.set(copied_files / total_files)
            self.update()


def main():
    app = BackupApp()
    app.mainloop()


if __name__ == "__main__":
    main()