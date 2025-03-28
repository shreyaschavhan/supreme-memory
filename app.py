import os
import random
import customtkinter
from PIL import Image
import datetime
from tkinter import messagebox, filedialog

# Card Manager Class
class CardManager:
    """Manages loading of learning cards from a directory."""
    def __init__(self, directory):
        self.directory = directory

    def fetch_cards(self, count=10):
        """Fetches up to `count` random cards from the directory."""
        if not os.path.isdir(self.directory):
            messagebox.showerror("Error", "Folder does not exist. Please select a valid folder.")
            return []

        files = [f for f in os.listdir(self.directory) if f.endswith(".txt")]
        if not files:
            messagebox.showerror("Error", "No text files found in the folder.")
            return []

        if len(files) < count:
            messagebox.showwarning("Warning", f"Only {len(files)} files found. Showing available files.")

        selected_files = random.sample(files, min(count, len(files)))
        cards = []
        for file in selected_files:
            with open(os.path.join(self.directory, file), "r", encoding="utf-8") as f:
                content = f.read().strip()
            title = file.replace(".txt", "")
            cards.append((title, content))
        return cards

# Main App Class
class App(customtkinter.CTk):
    def __init__(self, card_manager):
        super().__init__()
        self.card_manager = card_manager

        # Window Setup
        self.title("Daily Learning Cards")
        self.geometry("720x500")
        self.configure(fg_color="gray10")

        # Load Icons
        self.book_icon = customtkinter.CTkImage(Image.open("book_icon.png"), size=(24, 24))
        self.folder_icon = customtkinter.CTkImage(Image.open("folder_icon.png"), size=(24, 24))

        # Header Frame
        self.header_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x")

        # Title and Subtitle
        self.title_label = customtkinter.CTkLabel(
            self.header_frame, text="📚 Daily Learning Cards", font=("Segoe UI", 24, "bold"), text_color="white"
        )
        self.title_label.pack(side="left", padx=20, pady=10)

        today = datetime.date.today().strftime("%B %d, %Y")
        self.subtitle_label = customtkinter.CTkLabel(
            self.header_frame, text=f"Cards for {today}", font=("Segoe UI", 14), text_color="gray70"
        )
        self.subtitle_label.pack(side="left", padx=20)

        # Folder Button
        self.folder_button = customtkinter.CTkButton(
            self.header_frame, image=self.folder_icon, text="", width=40, height=40,
            fg_color="transparent", hover_color="#9B56DC", command=self.select_folder
        )
        self.folder_button.pack(side="right", padx=20, pady=10)

        # Main Frame
        self.main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable Frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.main_frame, width=680, corner_radius=10, fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Automatically load cards on startup
        self.load_cards()

    def load_cards(self):
        """Loads and displays cards in the scrollable frame."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        cards = self.card_manager.fetch_cards()
        if not cards:
            return

        for title, content in cards:
            self.create_card(title, content)

        customtkinter.CTkLabel(
            self.scrollable_frame, text="End of Cards", font=("Segoe UI", 14, "italic"), text_color="gray50"
        ).pack(pady=10)

    def create_card(self, title, content):
        """Creates a card with dynamic height."""
        card = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color="gray20")
        card.pack(fill="x", padx=5, pady=5)

        header_frame = customtkinter.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 0))

        icon_label = customtkinter.CTkLabel(header_frame, image=self.book_icon, text="")
        icon_label.pack(side="left", padx=(0, 10))

        title_label = customtkinter.CTkLabel(
            header_frame, text=title, font=("Segoe UI", 16, "bold"), text_color="white"
        )
        title_label.pack(side="left")

        body_label = customtkinter.CTkLabel(
            card, text=content, wraplength=640, justify="left", font=("Segoe UI", 14), text_color="white", anchor="w"
        )
        body_label.pack(fill="x", padx=10, pady=(5, 15))

        # Dynamic Height
        char_per_line = 640 // 8
        num_lines = max(1, (len(content) // char_per_line) + 1)
        min_height = num_lines * 20 + 50
        card.configure(height=min_height)

        # Hover Effects
        card.bind("<Enter>", lambda e: card.configure(fg_color="gray30"))
        card.bind("<Leave>", lambda e: card.configure(fg_color="gray20"))

    def select_folder(self):
        """Updates the folder for loading cards and automatically loads them."""
        folder = filedialog.askdirectory()
        if folder:
            self.card_manager.directory = folder
            messagebox.showinfo("Folder Selected", f"New folder: {folder}")
            self.load_cards()  # Automatically load cards from the new folder

# Run the App
if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("dark-blue")
    LEARNING_FOLDER = r"./notes"  
    card_manager = CardManager(LEARNING_FOLDER)
    app = App(card_manager)
    app.mainloop()
