import customtkinter as ctk
from api_handler import fetch_sura_list, fetch_ayah

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class QuranMemorizationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Quran Memorization App")
        self.geometry("800x600")

        self.sura_list = fetch_sura_list()
        self.selected_sura = None
        self.current_ayah = 0

        self.sura_frame = ctk.CTkFrame(self)
        self.sura_frame.pack(side="left", fill="both", expand=True)

        sura_names = [f"{sura['englishName']} ({sura['name']})" for sura in self.sura_list]
        self.sura_combobox = ctk.CTkOptionMenu(self.sura_frame, values=sura_names, command=self.open_sura_window)
        self.sura_combobox.pack(pady=20, padx=20)

        self.sura_window = None
        self.ayah_label = None
        self.prev_button = None
        self.next_button = None

    def open_sura_window(self, selected_item):
        try:
            arabic_name = selected_item.rsplit(" (", 1)[1][:-1]
            self.selected_sura = next((sura for sura in self.sura_list if sura['name'] == arabic_name), None)
            if not self.selected_sura:
                print("Sura not found")
                return

            if self.sura_window is None or not self.sura_window.winfo_exists():
                self.sura_window = ctk.CTkToplevel(self)
                self.sura_window.title(f"Sura {self.selected_sura['englishName']} ({self.selected_sura['name']})")
                self.sura_window.geometry("600x400")
                self.sura_window.lift()
                self.sura_window.focus()
                self.sura_window.attributes('-topmost', 1)
                self.sura_window.after(100, lambda: self.sura_window.attributes('-topmost', 0))

                # Main frame to hold ayah frame and navigation frame
                self.main_frame = ctk.CTkFrame(self.sura_window)
                self.main_frame.pack(fill="both", expand=True)

                # Ayah frame with scrolling
                self.ayah_frame = ctk.CTkScrollableFrame(self.main_frame, height=300)  # Set a fixed height
                self.ayah_frame.pack(fill="both", expand=True, pady=10, padx=10)

                self.ayah_label = ctk.CTkLabel(self.ayah_frame, text="", wraplength=550, font=("Arial", 30))
                self.ayah_label.pack(pady=10, padx=10)

                # Navigation frame at the bottom
                self.navigation_frame = ctk.CTkFrame(self.main_frame)
                self.navigation_frame.pack(side="bottom", fill="x", pady=10)

                self.prev_button = ctk.CTkButton(self.navigation_frame, text="Previous Ayah", command=self.show_prev_ayah, state="disabled")
                self.prev_button.pack(side="left", padx=10, pady=10)

                self.next_button = ctk.CTkButton(self.navigation_frame, text="Next Ayah", command=self.show_next_ayah)
                self.next_button.pack(side="right", padx=10, pady=10)
            else:
                self.sura_window.title(f"Sura {self.selected_sura['englishName']} ({self.selected_sura['name']})")
                self.current_ayah = 0
                self.show_next_ayah()
        except Exception as e:
            print("Error in open_sura_window:", e)

    def show_next_ayah(self):
        self.current_ayah += 1
        ayah_text = fetch_ayah(self.selected_sura['number'], self.current_ayah)
        if ayah_text:
            current_text = self.ayah_label.cget("text")
            if current_text:
                new_text = f"{current_text}\n\n{ayah_text}"
            else:
                new_text = ayah_text
            self.ayah_label.configure(text=new_text)
            self.prev_button.configure(state="normal")
            if self.current_ayah >= self.selected_sura['numberOfAyahs']:
                self.next_button.configure(state="disabled")
        else:
            self.current_ayah -= 1  # Reset to previous ayah

    def show_prev_ayah(self):
        if self.current_ayah > 1:
            self.current_ayah -= 1
            current_text = self.ayah_label.cget("text")
            if current_text:
                # Split the text into individual ayahs
                ayahs = current_text.split("\n\n")
                # Remove the last ayah (current ayah)
                ayahs.pop()
                # Join the remaining ayahs back into a single string
                new_text = "\n\n".join(ayahs)
                self.ayah_label.configure(text=new_text)
                self.next_button.configure(state="normal")
            if self.current_ayah == 1:
                self.prev_button.configure(state="disabled")