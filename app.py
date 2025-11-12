import customtkinter as ctk
import tkinter
from tkinter import filedialog, messagebox
import os
import json
import shutil
from datetime import datetime
from PIL import Image
import fnmatch

# --- App Setup ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class FileWranglerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FileWrangler")
        self.geometry("1100x800")
        self.minsize(1000, 750)

        self.folder_path = ctk.StringVar()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, RenamerPage, OrganizerPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit FileWrangler?"):
            self.destroy()

# --- Page 1: The Revamped Home Page ---
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.canvas = tkinter.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.draw_gradient()
        self.bind("<Configure>", self.draw_gradient)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        logo_font = ctk.CTkFont(family="Arial", size=48, weight="bold")
        ctk.CTkLabel(self, text="FileWrangler", font=logo_font, text_color="#FFFFFF").grid(row=0, column=0, pady=(60, 10))
        ctk.CTkLabel(self, text="The easy way to rename and organize your files.", font=ctk.CTkFont(size=16), text_color="#DCE4EE").grid(row=1, column=0, pady=(0, 60))
        
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0)
        
        button_font = ctk.CTkFont(size=18)
        ctk.CTkButton(button_frame, text="Rename Files", font=button_font, command=lambda: controller.show_frame("RenamerPage"), width=250, height=60, border_spacing=10).pack(side="left", padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Organize Folder", font=button_font, command=lambda: controller.show_frame("OrganizerPage"), width=250, height=60, border_spacing=10).pack(side="left", padx=20, pady=20)

        ctk.CTkButton(self, text="Quit", command=self.controller.quit_app, width=120, fg_color="transparent", border_width=2).grid(row=3, column=0, pady=(0, 40))

    def draw_gradient(self, event=None):
        self.canvas.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        (r1,g1,b1) = (46, 52, 64)
        (r2,g2,b2) = (59, 66, 82)
        for i in range(height):
            nr = int(r1 + (r2 - r1) * i / height)
            ng = int(g1 + (g2 - g1) * i / height)
            nb = int(b1 + (b2 - b1) * i / height)
            color = f'#{nr:02x}{ng:02x}{nb:02x}'
            self.canvas.create_line(0, i, width, i, fill=color, tags="gradient")

# --- Page 2: The Renamer Page ---
class RenamerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.original_files, self.preview_files = {}, []
        self.last_rename_log_path = os.path.join(os.path.expanduser("~"), ".filewrangler_undo.json")
        self.replace_from, self.replace_to, self.add_prefix, self.add_suffix = ctk.StringVar(), ctk.StringVar(), ctk.StringVar(), ctk.StringVar()
        self.change_case_option, self.seq_num_start, self.exif_date_format = ctk.StringVar(value="None"), ctk.StringVar(value="1"), ctk.StringVar(value="%Y-%m-%d_%H-%M-%S")
        self.add_seq_num, self.use_exif_date, self.include_subfolders = ctk.BooleanVar(), ctk.BooleanVar(), ctk.BooleanVar()
        self.create_widgets()
        self.update_widget_states()
        for var in [self.replace_from, self.replace_to, self.add_prefix, self.add_suffix, self.change_case_option, self.add_seq_num, self.seq_num_start, self.use_exif_date, self.exif_date_format, self.include_subfolders]:
            var.trace_add("write", self.update_preview)

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        top_frame = ctk.CTkFrame(self); top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew"); top_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(top_frame, text="< Back to Home", command=lambda: self.controller.show_frame("HomePage"), width=120).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(top_frame, textvariable=self.controller.folder_path, state="readonly").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(top_frame, text="Select Folder...", command=self.select_folder).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkCheckBox(top_frame, text="Include Subfolders", variable=self.include_subfolders).grid(row=0, column=3, padx=10, pady=10)
        list_frame = ctk.CTkFrame(self); list_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew"); list_frame.grid_columnconfigure((0, 1), weight=1); list_frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(list_frame, text="Original Filenames", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=(5,0)); ctk.CTkLabel(list_frame, text="Preview of New Filenames", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=(5,0))
        self.original_listbox = tkinter.Listbox(list_frame, borderwidth=0, highlightthickness=0, bg="#2B2B2B", fg="#DCE4EE", selectbackground="#1F6AA5"); self.original_listbox.grid(row=1, column=0, padx=(10,0), pady=10, sticky="nsew")
        self.preview_listbox = tkinter.Listbox(list_frame, borderwidth=0, highlightthickness=0, bg="#2B2B2B", fg="#DCE4EE", selectbackground="#1F6AA5"); self.preview_listbox.grid(row=1, column=1, padx=(10,0), pady=10, sticky="nsew")
        bottom_frame = ctk.CTkFrame(self); bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew"); bottom_frame.grid_columnconfigure(0, weight=1)
        tab_view = ctk.CTkTabview(bottom_frame); tab_view.grid(row=0, column=0, sticky="nsew", padx=(0,10)); tab_view.add("Basic"); tab_view.add("Advanced"); tab_view.add("Photo")
        basic_tab, adv_tab, photo_tab = tab_view.tab("Basic"), tab_view.tab("Advanced"), tab_view.tab("Photo")
        basic_tab.grid_columnconfigure((1, 3), weight=1); adv_tab.grid_columnconfigure(1, weight=1); photo_tab.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(basic_tab, text="Replace:").grid(row=0, column=0, padx=10, pady=10, sticky="w"); ctk.CTkEntry(basic_tab, textvariable=self.replace_from).grid(row=0, column=1, padx=5, pady=10, sticky="ew"); ctk.CTkLabel(basic_tab, text="With:").grid(row=0, column=2, padx=10, pady=10); ctk.CTkEntry(basic_tab, textvariable=self.replace_to).grid(row=0, column=3, padx=5, pady=10, sticky="ew")
        ctk.CTkLabel(basic_tab, text="Add Prefix:").grid(row=1, column=0, padx=10, pady=10, sticky="w"); ctk.CTkEntry(basic_tab, textvariable=self.add_prefix).grid(row=1, column=1, padx=5, pady=10, sticky="ew"); ctk.CTkLabel(basic_tab, text="Add Suffix:").grid(row=1, column=2, padx=10, pady=10); ctk.CTkEntry(basic_tab, textvariable=self.add_suffix).grid(row=1, column=3, padx=5, pady=10, sticky="ew")
        ctk.CTkLabel(adv_tab, text="Change Case:").grid(row=0, column=0, padx=10, pady=10, sticky="w"); ctk.CTkComboBox(adv_tab, variable=self.change_case_option, values=["None", "lowercase", "UPPERCASE", "Title Case"]).grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        ctk.CTkCheckBox(adv_tab, text="Add Sequence No. Start:", variable=self.add_seq_num).grid(row=1, column=0, sticky="w", padx=10, pady=10); ctk.CTkEntry(adv_tab, textvariable=self.seq_num_start, width=50).grid(row=1, column=1, sticky="w", padx=5, pady=10)
        ctk.CTkCheckBox(photo_tab, text="Rename using Photo Date (EXIF)", variable=self.use_exif_date).grid(row=0, column=0, padx=10, pady=10, sticky="w"); ctk.CTkLabel(photo_tab, text="Date Format:").grid(row=1, column=0, sticky="w", padx=10, pady=10); ctk.CTkEntry(photo_tab, textvariable=self.exif_date_format).grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        action_frame = ctk.CTkFrame(bottom_frame); action_frame.grid(row=0, column=1, sticky="ns")
        
        self.apply_button = ctk.CTkButton(action_frame, text="Apply Renaming", command=self.apply_renaming, fg_color="#28a745", hover_color="#218838")
        self.apply_button.pack(fill="x", padx=10, pady=10)
        # --- THE ONLY CHANGE IS HERE ---
        self.undo_button = ctk.CTkButton(action_frame, text="Undo Last Rename", command=self.undo_renaming, fg_color="#546E7A", hover_color="#455A64")
        self.undo_button.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(action_frame, text="Reset Rules", command=self.reset_rules).pack(fill="x", padx=10, pady=(20, 10))

    def on_show(self): self.update_widget_states()
    def update_widget_states(self):
        state = "normal" if self.controller.folder_path.get() else "disabled"
        self.apply_button.configure(state=state)
        self.undo_button.configure(state="normal" if os.path.exists(self.last_rename_log_path) else "disabled")
    def reset_rules(self):
        self.replace_from.set(""), self.replace_to.set(""), self.add_prefix.set(""), self.add_suffix.set(""), self.change_case_option.set("None")
        self.add_seq_num.set(False), self.seq_num_start.set("1"), self.use_exif_date.set(False)
        self.update_preview()
    def select_folder(self):
        path = filedialog.askdirectory(title="Select a Folder")
        if path: self.controller.folder_path.set(path); self.load_files()
    def load_files(self):
        path = self.controller.folder_path.get()
        if not path: return
        self.original_listbox.delete(0, tkinter.END); self.original_files.clear()
        try:
            if self.include_subfolders.get():
                for dirpath, _, filenames in os.walk(path):
                    for filename in filenames: self.original_files[os.path.join(dirpath, filename)] = os.path.relpath(os.path.join(dirpath, filename), path)
            else:
                for filename in os.listdir(path):
                    full_path = os.path.join(path, filename)
                    if os.path.isfile(full_path): self.original_files[full_path] = filename
            for display_name in sorted(self.original_files.values()): self.original_listbox.insert(tkinter.END, display_name)
        except Exception as e: messagebox.showerror("Error", f"Failed to read folder: {e}")
        self.update_preview(); self.update_widget_states()
    def get_exif_date(self, file_path):
        try:
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if exif_data: date_str = exif_data.get(36867); return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S') if date_str else None
        except: return None
    def update_preview(self, *args):
        self.preview_listbox.delete(0, tkinter.END); self.preview_files = []
        try: start_num = int(self.seq_num_start.get())
        except ValueError: start_num = 1
        sorted_paths = sorted(self.original_files.keys(), key=lambda k: self.original_files[k])
        for i, full_path in enumerate(sorted_paths):
            display_name = self.original_files[full_path]; subfolder_path, filename_ext = os.path.dirname(display_name), os.path.basename(display_name)
            filename, extension = os.path.splitext(filename_ext); new_name = filename
            if self.use_exif_date.get():
                date_obj = self.get_exif_date(full_path)
                if date_obj:
                    try: new_name = date_obj.strftime(self.exif_date_format.get())
                    except: new_name = "invalid_date_format"
                else: new_name = "no_exif_date"
            else:
                if self.replace_from.get(): new_name = new_name.replace(self.replace_from.get(), self.replace_to.get())
                new_name = self.add_prefix.get() + new_name + self.add_suffix.get()
                case = self.change_case_option.get()
                if case == "lowercase": new_name = new_name.lower()
                elif case == "UPPERCASE": new_name = new_name.upper()
                elif case == "Title Case": new_name = new_name.title()
            if self.add_seq_num.get(): new_name = f"{new_name}_{start_num + i}"
            final_name_with_path = os.path.join(subfolder_path, new_name + extension) if subfolder_path else new_name + extension
            self.preview_files.append(final_name_with_path); self.preview_listbox.insert(tkinter.END, final_name_with_path)
    def apply_renaming(self):
        base_path = self.controller.folder_path.get()
        if not base_path or not messagebox.askyesno("Confirm Rename", f"Are you sure you want to rename {len(self.original_files)} files?"): return
        rename_log, errors, count = [], [], 0
        sorted_paths = sorted(self.original_files.keys(), key=lambda k: self.original_files[k])
        for old_full_path, new_relative_path in zip(sorted_paths, self.preview_files):
            new_full_path = os.path.join(base_path, new_relative_path)
            try:
                if old_full_path != new_full_path:
                    os.makedirs(os.path.dirname(new_full_path), exist_ok=True); os.rename(old_full_path, new_full_path)
                    rename_log.append({"original": old_full_path, "new": new_full_path}); count+=1
            except Exception as e: errors.append(f"'{os.path.basename(old_full_path)}': {e}")
        if rename_log:
            try:
                with open(self.last_rename_log_path, 'w') as f: json.dump(rename_log, f, indent=4)
            except Exception as e: messagebox.showerror("Error", f"Could not save undo log: {e}")
        if errors: messagebox.showerror("Errors Occurred", "\n".join(errors))
        else: messagebox.showinfo("Success", f"Successfully renamed {count} files.")
        self.load_files()
    def undo_renaming(self):
        if not os.path.exists(self.last_rename_log_path) or not messagebox.askyesno("Confirm Undo", "Undo the last rename operation?"): return
        try:
            with open(self.last_rename_log_path, 'r') as f: rename_log = json.load(f)
        except Exception as e: messagebox.showerror("Error", f"Could not read undo log: {e}"); return
        errors, count = [], 0
        for entry in reversed(rename_log):
            try: os.renames(entry['new'], entry['original']); count+=1
            except Exception as e: errors.append(f"Could not revert '{os.path.basename(entry['new'])}': {e}")
        if errors: messagebox.showerror("Errors Occurred", "\n".join(errors))
        else: messagebox.showinfo("Success", f"Successfully reverted {count} filenames."); os.remove(self.last_rename_log_path)
        self.load_files()

# --- Page 3: The Upgraded Organizer Page ---
class OrganizerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.files_in_folder = []
        self.organize_option = ctk.StringVar(value="extension")
        self.custom_pattern = ctk.StringVar(value="Invoice-*")
        self.custom_folder = ctk.StringVar(value="Invoices")

        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(2, weight=1)
        top_frame = ctk.CTkFrame(self); top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew"); top_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(top_frame, text="< Back to Home", command=lambda: self.controller.show_frame("HomePage"), width=120).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(top_frame, textvariable=self.controller.folder_path, state="readonly").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(top_frame, text="Select Folder...", command=self.select_folder).grid(row=0, column=2, padx=10, pady=10)

        options_frame = ctk.CTkFrame(self); options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(options_frame, text="Organize files into subfolders based on:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        ctk.CTkRadioButton(options_frame, text="File Extension (e.g., 'jpg_files', 'pdf_files')", variable=self.organize_option, value="extension").pack(anchor="w", padx=20, pady=5)
        ctk.CTkRadioButton(options_frame, text="Date Modified (e.g., '2025-10', '2025-11')", variable=self.organize_option, value="date").pack(anchor="w", padx=20, pady=5)
        ctk.CTkRadioButton(options_frame, text="File Category (e.g., 'Images', 'Documents')", variable=self.organize_option, value="category").pack(anchor="w", padx=20, pady=5)
        
        custom_frame = ctk.CTkFrame(options_frame, fg_color="transparent"); custom_frame.pack(fill="x", expand=True)
        ctk.CTkRadioButton(custom_frame, text="Custom Pattern:", variable=self.organize_option, value="custom").grid(row=0, column=0, padx=20, pady=5)
        ctk.CTkEntry(custom_frame, placeholder_text="e.g., Report-*.pdf", textvariable=self.custom_pattern).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(custom_frame, text="move to folder:").grid(row=0, column=2, padx=5)
        ctk.CTkEntry(custom_frame, placeholder_text="e.g., Reports", textvariable=self.custom_folder).grid(row=0, column=3, padx=5)

        self.file_listbox = tkinter.Listbox(self, borderwidth=0, highlightthickness=0, bg="#2B2B2B", fg="#DCE4EE", selectbackground="#1F6AA5")
        self.file_listbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.organize_button = ctk.CTkButton(self, text="Organize Files Now", height=40, command=self.organize_files)
        self.organize_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

    def on_show(self): self.load_files(); self.update_widget_states()
    def update_widget_states(self): self.organize_button.configure(state="normal" if self.controller.folder_path.get() else "disabled")
    def select_folder(self):
        path = filedialog.askdirectory(title="Select a Folder");
        if path: self.controller.folder_path.set(path); self.load_files()
    def load_files(self):
        self.file_listbox.delete(0, tkinter.END); self.files_in_folder.clear()
        path = self.controller.folder_path.get()
        if not path: return
        try:
            self.files_in_folder = sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            for filename in self.files_in_folder: self.file_listbox.insert(tkinter.END, filename)
        except Exception as e: messagebox.showerror("Error", f"Could not read folder: {e}")
        self.update_widget_states()
    def organize_files(self):
        folder = self.controller.folder_path.get()
        if not folder or not messagebox.askyesno("Confirm Organize", f"This will move files into new subfolders. Are you sure?"): return
        
        FILE_CATEGORIES = { 'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'], 'Documents': ['.pdf', '.docx', '.txt', '.pptx', '.xlsx', '.odt'], 'Audio': ['.mp3', '.wav', '.aac'], 'Video': ['.mp4', '.mkv', '.mov', '.avi'], 'Archives': ['.zip', '.rar', '.7z', '.tar.gz'] }
        
        moved_count, errors = 0, []
        files_to_organize = list(self.files_in_folder)
        option = self.organize_option.get()
        for filename in files_to_organize:
            full_path, subfolder_name = os.path.join(folder, filename), "Other_Files"
            if not os.path.exists(full_path): continue
            
            if option == "extension":
                ext = os.path.splitext(filename)[1]
                subfolder_name = "No_Extension" if not ext else ext[1:].lower() + "_Files"
            elif option == "date":
                mtime = os.path.getmtime(full_path)
                subfolder_name = datetime.fromtimestamp(mtime).strftime('%Y-%m')
            elif option == "category":
                ext = os.path.splitext(filename)[1].lower()
                for category, extensions in FILE_CATEGORIES.items():
                    if ext in extensions: subfolder_name = category; break
            elif option == "custom":
                pattern = self.custom_pattern.get(); custom_folder = self.custom_folder.get()
                if custom_folder and fnmatch.fnmatch(filename, pattern): subfolder_name = custom_folder
                else: continue
            try:
                subfolder_path = os.path.join(folder, subfolder_name)
                os.makedirs(subfolder_path, exist_ok=True)
                shutil.move(full_path, os.path.join(subfolder_path, filename)); moved_count += 1
            except Exception as e: errors.append(f"Could not move '{filename}': {e}")
        
        if errors: messagebox.showerror("Errors Occurred", "\n".join(errors))
        else: messagebox.showinfo("Success", f"Successfully organized {moved_count} files.")
        self.load_files()

if __name__ == "__main__":
    app = FileWranglerApp()
    app.mainloop()