import customtkinter as ctk
import json
import os
import shutil
from pathlib import Path
import hashlib
from tkinter import filedialog, messagebox
from typing import List, Dict


class FolderPairFrame(ctk.CTkFrame):
    def __init__(self, master, index: int, initial_data: Dict, on_remove=None, on_change=None):
        super().__init__(master)
        self.index = index
        self.on_remove = on_remove
        self.on_change = on_change

        # Create inner frame for better organization
        self.inner_frame = ctk.CTkFrame(self)
        self.inner_frame.pack(fill="x", padx=5, pady=5)

        # Pair header with remove button
        header_frame = ctk.CTkFrame(self.inner_frame)
        header_frame.pack(fill="x", pady=(0, 5))

        pair_label = ctk.CTkLabel(
            header_frame,
            text=f"Folder Pair {index + 1}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        pair_label.pack(side="left", padx=5)

        remove_btn = ctk.CTkButton(
            header_frame,
            text="Remove",
            width=80,
            height=25,
            command=self._on_remove
        )
        remove_btn.pack(side="right", padx=5)

        # Source Directory
        source_frame = ctk.CTkFrame(self.inner_frame)
        source_frame.pack(fill="x", pady=2)

        source_label = ctk.CTkLabel(source_frame, text="Source:", width=60)
        source_label.pack(side="left", padx=5)

        self.source_var = ctk.StringVar(value=initial_data.get("source_dir", ""))
        self.source_entry = ctk.CTkEntry(source_frame, textvariable=self.source_var, width=350)
        self.source_entry.pack(side="left", padx=5)

        source_btn = ctk.CTkButton(
            source_frame,
            text="Browse",
            width=80,
            command=lambda: self._browse_directory("source")
        )
        source_btn.pack(side="left", padx=5)

        # Target Directory
        target_frame = ctk.CTkFrame(self.inner_frame)
        target_frame.pack(fill="x", pady=2)

        target_label = ctk.CTkLabel(target_frame, text="Target:", width=60)
        target_label.pack(side="left", padx=5)

        self.target_var = ctk.StringVar(value=initial_data.get("target_dir", ""))
        self.target_entry = ctk.CTkEntry(target_frame, textvariable=self.target_var, width=350)
        self.target_entry.pack(side="left", padx=5)

        target_btn = ctk.CTkButton(
            target_frame,
            text="Browse",
            width=80,
            command=lambda: self._browse_directory("target")
        )
        target_btn.pack(side="left", padx=5)

        # Bind changes
        self.source_var.trace_add("write", self._on_change)
        self.target_var.trace_add("write", self._on_change)

    def _browse_directory(self, dir_type: str):
        directory = filedialog.askdirectory()
        if directory:
            if dir_type == "source":
                self.source_var.set(directory)
            else:
                self.target_var.set(directory)

    def _on_remove(self):
        if self.on_remove:
            self.on_remove(self.index)

    def _on_change(self, *args):
        if self.on_change:
            self.on_change(self.index, {
                "source_dir": self.source_var.get(),
                "target_dir": self.target_var.get()
            })

    def get_data(self) -> Dict:
        return {
            "source_dir": self.source_var.get(),
            "target_dir": self.target_var.get()
        }


class BackupApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("11copy")
        self.geometry("800x600")

        # Set the theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Load or create config
        self.config_file = "config.json"
        self.config = self.load_config()

        # Initialize folder pairs list
        self.folder_pairs: List[FolderPairFrame] = []

        self.create_gui()

        # Load saved folder pairs
        for pair_data in self.config.get("folder_pairs", []):
            self.add_folder_pair(pair_data)

    def load_config(self) -> Dict:
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"folder_pairs": []}

    def save_config(self):
        self.config["folder_pairs"] = [pair.get_data() for pair in self.folder_pairs]
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def create_gui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header
        header = ctk.CTkLabel(
            self.main_frame,
            text="11copy",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(pady=10)

        # Scrollable frame for folder pairs
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Add Folder Pair button
        add_btn = ctk.CTkButton(
            self.main_frame,
            text="Add Folder Pair",
            command=lambda: self.add_folder_pair()
        )
        add_btn.pack(pady=10)

        # Progress frame
        progress_frame = ctk.CTkFrame(self.main_frame)
        progress_frame.pack(fill="x", padx=10, pady=5)

        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        self.progress_bar.set(0)

        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            progress_frame,
            textvariable=self.status_var,
            wraplength=700
        )
        self.status_label.pack(pady=5)

        # Options Frame
        options_frame = ctk.CTkFrame(self.main_frame)
        options_frame.pack(fill="x", padx=10, pady=5)

        # Checkboxes
        checks_frame = ctk.CTkFrame(options_frame)
        checks_frame.pack(side="left", fill="x", padx=5)

        self.two_way_var = ctk.BooleanVar(value=False)
        two_way_check = ctk.CTkCheckBox(
            checks_frame,
            text="Two-way sync",
            variable=self.two_way_var
        )
        two_way_check.pack(side="left", padx=5)

        self.validate_var = ctk.BooleanVar(value=False)
        validate_check = ctk.CTkCheckBox(
            checks_frame,
            text="Validate copies",
            variable=self.validate_var
        )
        validate_check.pack(side="left", padx=5)

        # Start button
        backup_btn = ctk.CTkButton(
            options_frame,
            text="Start Backup",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=200,
            height=40,
            command=self.start_backup
        )
        backup_btn.pack(side="right", padx=5)

        # Theme switcher
        theme_frame = ctk.CTkFrame(self.main_frame)
        theme_frame.pack(fill="x", padx=10, pady=5)

        theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        theme_switch.pack(side="right")

    def add_folder_pair(self, initial_data: Dict = None):
        if initial_data is None:
            initial_data = {"source_dir": "", "target_dir": ""}

        pair_frame = FolderPairFrame(
            self.scroll_frame,
            len(self.folder_pairs),
            initial_data,
            on_remove=self.remove_folder_pair,
            on_change=self.on_pair_change
        )
        pair_frame.pack(fill="x", pady=5)
        self.folder_pairs.append(pair_frame)
        self.save_config()

    def remove_folder_pair(self, index: int):
        if 0 <= index < len(self.folder_pairs):
            self.folder_pairs[index].destroy()
            self.folder_pairs.pop(index)

            # Update indices of remaining pairs
            for i, pair in enumerate(self.folder_pairs):
                pair.index = i

            self.save_config()

    def on_pair_change(self, index: int, data: Dict):
        self.save_config()

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def _calculate_md5(self, filepath: str) -> str:
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def start_backup(self):
        if not self.folder_pairs:
            messagebox.showerror("Error", "Please add at least one folder pair")
            return

        total_files = 0
        copied_files = 0

        try:
            # Process each folder pair
            for pair in self.folder_pairs:
                data = pair.get_data()
                source_dir = data["source_dir"]
                target_dir = data["target_dir"]

                if not source_dir or not target_dir:
                    continue

                if not os.path.exists(source_dir):
                    self.status_var.set(f"Source directory does not exist: {source_dir}")
                    continue

                # Prevent backup into source directory
                source_path = os.path.abspath(source_dir)
                target_path = os.path.abspath(target_dir)

                if os.path.abspath(target_path).startswith(os.path.abspath(source_path)):
                    self.status_var.set(f"Target cannot be inside source: {target_dir}")
                    continue

                # Perform backup for this pair
                files = self.perform_backup(source_dir, target_dir)
                total_files += files[0]
                copied_files += files[1]

            if total_files > 0:
                messagebox.showinfo("Success", f"Backup completed! Processed {copied_files} of {total_files} files.")
            else:
                messagebox.showinfo("Complete", "No files needed updating")

            self.status_var.set("Backup completed successfully!")
            self.progress_bar.set(1)

        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")

    def perform_backup(self, source_dir: str, target_dir: str) -> tuple[int, int]:
        self.status_var.set(f"Analyzing files in {source_dir}...")
        self.progress_bar.set(0)
        self.update()

        # Create directories if they don't exist
        os.makedirs(target_dir, exist_ok=True)

        # First scan to determine which files need copying
        files_to_copy = []

        # Source to target scan
        for root, dirs, files in os.walk(source_dir):
            rel_path = os.path.relpath(root, source_dir)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, rel_path, file)

                if len(dst_file) >= 260:  # Skip files with path too long
                    continue

                needs_copy = False
                needs_validation = self.validate_var.get()

                if os.path.exists(dst_file):
                    src_mtime = os.path.getmtime(src_file)
                    dst_mtime = os.path.getmtime(dst_file)
                    if src_mtime > dst_mtime:
                        needs_copy = True
                else:
                    needs_copy = True

                if needs_copy or needs_validation:
                    files_to_copy.append((src_file, dst_file, rel_path, "source", needs_copy))

        # Target to source scan (if two-way sync is enabled)
        if self.two_way_var.get():
            for root, dirs, files in os.walk(target_dir):
                rel_path = os.path.relpath(root, target_dir)
                for file in files:
                    dst_file = os.path.join(root, file)
                    src_file = os.path.join(source_dir, rel_path, file)

                    if len(src_file) >= 260:  # Skip files with path too long
                        continue

                    needs_copy = False
                    needs_validation = self.validate_var.get()

                    if os.path.exists(src_file):
                        dst_mtime = os.path.getmtime(dst_file)
                        src_mtime = os.path.getmtime(src_file)
                        if dst_mtime > src_mtime:
                            needs_copy = True
                    else:
                        needs_copy = True

                    if needs_copy or needs_validation:
                        files_to_copy.append((dst_file, src_file, rel_path, "target", needs_copy))

        total_files = len(files_to_copy)
        copied_files = 0

        if total_files == 0:
            self.status_var.set("No files need updating")
            self.progress_bar.set(1)
            return (0, 0)

        # Perform the actual backup
        for src_file, dst_file, rel_path, direction, needs_copy in files_to_copy:
            try:
                if needs_copy:
                    # Ensure target subdirectory exists
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)

                    # Copy file with metadata
                    shutil.copy2(src_file, dst_file)

                # Validate if enabled (both for copied and existing files)
                if self.validate_var.get():
                    action = "Validating" if not needs_copy else "Copying"
                    self.status_var.set(f"{action} {os.path.basename(src_file)}...")
                    self.update()

                    src_md5 = self._calculate_md5(src_file)
                    dst_md5 = self._calculate_md5(dst_file)
                    if src_md5 != dst_md5:
                        raise Exception(
                            f"File validation failed for {os.path.basename(src_file)} - checksums don't match")

                copied_files += 1

            except Exception as e:
                self.status_var.set(f"Error processing {os.path.basename(src_file)}: {str(e)}")
                continue

            direction_text = "→" if direction == "source" else "←"
            action_text = "Validating" if not needs_copy else "Copying"
            self.status_var.set(f"{action_text} files... ({copied_files}/{total_files}) {direction_text}")
            self.progress_bar.set(copied_files / total_files)
            self.update()

        return (total_files, copied_files)


def main():
    app = BackupApp()
    app.mainloop()


if __name__ == "__main__":
    main()
