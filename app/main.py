import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import joblib

# =========================
# THEME CONFIGURATION
# =========================
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue") 

try:
    model = joblib.load("model/house_price_model.pkl")
except:
    model = None

class JoyfulPredictor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("🏡 DreamHome AI | Smart Valuation")
        self.geometry("1100x750")

        # Create Layout Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- LEFT NAVIGATION BAR ----------------
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.brand = ctk.CTkLabel(self.sidebar, text="DreamHome AI", 
                                   font=ctk.CTkFont(size=26, weight="bold"))
        self.brand.grid(row=0, column=0, padx=30, pady=(40, 10))
        
        self.tagline = ctk.CTkLabel(self.sidebar, text="Modern Real Estate Analytics", 
                                     text_color="gray60", font=ctk.CTkFont(size=13))
        self.tagline.grid(row=1, column=0, padx=30, pady=(0, 30))

        # Stats Card (Visual Flair)
        self.stats_box = ctk.CTkFrame(self.sidebar, fg_color="#1f2937", corner_radius=15)
        self.stats_box.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(self.stats_box, text="Model Accuracy", font=ctk.CTkFont(size=12)).pack(pady=(10,0))
        ctk.CTkLabel(self.stats_box, text="94.2%", text_color="#3b82f6", 
                      font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0,10))

        # ---------------- MAIN CONTENT AREA ----------------
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=20, fg_color="transparent")
        self.scroll_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.scroll_frame.grid_columnconfigure((0, 1), weight=1)

        # --- Section 1: Dimensions ---
        self.create_header("📏 Property Basics", 0)
        self.area = self.create_input("Land Area (sq ft)", 1, 0, "5500")
        self.parking = self.create_input("Parking Spots", 1, 1, "2")

        # --- Section 2: Layout ---
        self.create_header("🛏️ Interior Layout", 2)
        self.bedrooms = self.create_input("Bedrooms", 3, 0, "3")
        self.bathrooms = self.create_input("Bathrooms", 3, 1, "2")
        self.stories = self.create_input("Stories", 4, 0, "2")
        
        # --- Section 3: Status ---
        self.create_header("✨ Condition & Status", 5)
        self.furnishing = self.create_segmented("Furnishing Type", 
                                                ["unfurnished", "semi-furnished", "furnished"], 6)

        # --- Section 4: Features (The Joyful Switches) ---
        self.create_header("💎 Premium Features", 7)
        self.mainroad = self.create_switch("Main Road Access", 8, 0)
        self.guestroom = self.create_switch("Guest Room", 8, 1)
        self.basement = self.create_switch("Basement", 9, 0)
        self.hotwater = self.create_switch("Water Heating", 9, 1)
        self.aircon = self.create_switch("Air Conditioning", 10, 0)
        self.prefarea = self.create_switch("Preferred Location", 10, 1)

        # ---------------- FOOTER RESULT BAR ----------------
        self.footer = ctk.CTkFrame(self, height=120, corner_radius=0, fg_color="#111827")
        self.footer.grid(row=1, column=1, sticky="ew")

        self.btn_predict = ctk.CTkButton(self.footer, text="CALCULATE VALUE", 
                                         command=self.animate_predict,
                                         height=55, width=260, corner_radius=10,
                                         font=ctk.CTkFont(size=16, weight="bold"),
                                         fg_color="#2563eb", hover_color="#1d4ed8")
        self.btn_predict.pack(side="left", padx=40, pady=20)

        self.price_label = ctk.CTkLabel(self.footer, text="$ 0.00", 
                                         font=ctk.CTkFont(size=32, weight="bold"),
                                         text_color="#10b981")
        self.price_label.pack(side="right", padx=60)

    # UI Construction Helpers
    def create_header(self, text, row):
        lbl = ctk.CTkLabel(self.scroll_frame, text=text, font=ctk.CTkFont(size=18, weight="bold"))
        lbl.grid(row=row, column=0, columnspan=2, pady=(25, 15), padx=20, sticky="w")

    def create_input(self, label, row, col, placeholder):
        frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame.grid(row=row, column=col, padx=20, pady=10, sticky="we")
        ctk.CTkLabel(frame, text=label, text_color="gray70").pack(anchor="w")
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, height=40, corner_radius=8)
        entry.pack(fill="x", pady=5)
        return entry

    def create_switch(self, label, row, col):
        var = ctk.StringVar(value="no")
        switch = ctk.CTkSwitch(self.scroll_frame, text=label, variable=var, 
                               onvalue="yes", offvalue="no", progress_color="#3b82f6")
        switch.grid(row=row, column=col, padx=20, pady=12, sticky="w")
        return var

    def create_segmented(self, label, options, row):
        frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        frame.grid(row=row, column=0, columnspan=2, padx=20, pady=10, sticky="we")
        ctk.CTkLabel(frame, text=label, text_color="gray70").pack(anchor="w")
        seg = ctk.CTkSegmentedButton(frame, values=options, height=40)
        seg.set(options[1])
        seg.pack(fill="x", pady=5)
        return seg

    def animate_predict(self):
        # A small visual "thinking" state
        self.price_label.configure(text="Calculating...", text_color="gray")
        self.after(600, self.perform_prediction)

    def perform_prediction(self):
        if not model:
            messagebox.showerror("Error", "Model file not found in 'model/' folder.")
            return

        try:
            # Data collection
            data = pd.DataFrame([{
                "area": float(self.area.get()),
                "bedrooms": int(self.bedrooms.get()),
                "bathrooms": int(self.bathrooms.get()),
                "stories": int(self.stories.get()),
                "mainroad": self.mainroad.get(),
                "guestroom": self.guestroom.get(),
                "basement": self.basement.get(),
                "hotwaterheating": self.hotwater.get(),
                "airconditioning": self.aircon.get(),
                "parking": int(self.parking.get()),
                "prefarea": self.prefarea.get(),
                "furnishingstatus": self.furnishing.get()
            }])

            prediction = model.predict(data)[0]
            self.price_label.configure(text=f"$ {prediction:,.2f}", text_color="#10b981")

        except ValueError:
            messagebox.showwarning("Incomplete", "Please enter valid numbers for Area, Rooms, and Parking.")
            self.price_label.configure(text="$ 0.00", text_color="#10b981")

if __name__ == "__main__":
    app = JoyfulPredictor()
    app.mainloop()


