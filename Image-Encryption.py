import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mbox
from PIL import Image
import cv2
import numpy as np

class SecurePixApp:
    def __init__(self, window):
        self.window = window
        self.window.geometry("900x600")
        self.window.title("SecurePix - Advanced Image Encryption")
        self.window.configure(bg="#111827")
        
        self.setup_variables()
        self.create_ui()
        
    def setup_variables(self):
        self.current_image_path = None
        self.eimg = None
        self.image_encrypted = None
        self.key = None
        
    def create_ui(self):
        brand_frame = tk.Frame(self.window, bg="#1F2937", pady=40)
        brand_frame.pack(fill="x")
        
        brand_name = tk.Label(brand_frame, 
                            text="SecurePix", 
                            font=("Helvetica", 42, "bold"), 
                            fg="#6EE7B7",
                            bg="#1F2937")
        brand_name.pack()
        
        tagline = tk.Label(brand_frame,
                          text="Advanced Image Security System",
                          font=("Helvetica", 16),
                          fg="#9CA3AF",
                          bg="#1F2937")
        tagline.pack(pady=(5, 0))
        
        status_card = tk.Frame(self.window, bg="#374151", pady=20, padx=30)
        status_card.pack(fill="x", padx=40, pady=30)
        
        status_title = tk.Label(status_card,
                              text="OPERATION STATUS",
                              font=("Helvetica", 12, "bold"),
                              fg="#6EE7B7",
                              bg="#374151")
        status_title.pack()
        
        self.status_label = tk.Label(status_card,
                                   text="Ready to process images",
                                   font=("Helvetica", 14),
                                   fg="#E5E7EB",
                                   bg="#374151")
        self.status_label.pack(pady=(10, 0))
        
        actions_frame = tk.Frame(self.window, bg="#111827", pady=20)
        actions_frame.pack(fill="x", padx=40)
        
        file_frame = tk.Frame(actions_frame, bg="#111827")
        file_frame.pack(fill="x", pady=(0, 20))
        
        self.create_button(file_frame, "📁 Select Image", self.open_img, "#3B82F6", 0, 0)
        self.create_button(file_frame, "💾 Save Image", self.save_img, "#3B82F6", 0, 1)
        
        encrypt_frame = tk.Frame(actions_frame, bg="#111827")
        encrypt_frame.pack(fill="x", pady=(0, 20))
        
        self.create_button(encrypt_frame, "🔒 Encrypt", self.en_fun, "#059669", 0, 0)
        self.create_button(encrypt_frame, "🔓 Decrypt", self.de_fun, "#059669", 0, 1)
        
        reset_frame = tk.Frame(actions_frame, bg="#111827")
        reset_frame.pack(fill="x")
        
        self.create_button(reset_frame, "↺ Reset Image", self.reset, "#6366F1", 0, 0, 2)
        
        footer_frame = tk.Frame(self.window, bg="#111827", pady=30)
        footer_frame.pack(side="bottom", fill="x")
        
        exit_btn = tk.Button(footer_frame,
                           text="Exit SecurePix",
                           command=self.exit_win,
                           font=("Helvetica", 12, "bold"),
                           bg="#DC2626",
                           fg="white",
                           padx=25,
                           pady=12,
                           relief="flat",
                           cursor="hand2")
        exit_btn.pack()
        
    def create_button(self, parent, text, command, color, row, col, colspan=1):
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       font=("Helvetica", 13, "bold"),
                       bg=color,
                       fg="white",
                       padx=35,
                       pady=15,
                       relief="flat",
                       cursor="hand2")
        btn.grid(row=row, column=col, columnspan=colspan, padx=10, pady=8, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
    def open_img(self):
        x = filedialog.askopenfilename(title='Select Image')
        if not x:
            return
            
        try:
            self.current_image_path = x
            self.eimg = Image.open(x)
            self.status_label.config(text=f"✅ Image loaded: {x.split('/')[-1]}")
            mbox.showinfo("SecurePix", "Image loaded successfully!")
        except Exception as e:
            mbox.showerror("Error", f"Failed to open image: {str(e)}")
    
    def en_fun(self):
        if not self.current_image_path:
            mbox.showerror("Error", "Please select an image first!")
            return
            
        try:
            image_input = cv2.imread(self.current_image_path, 0)
            (x1, y) = image_input.shape
            image_input = image_input.astype(float) / 255.0
            
            mu, sigma = 0, 0.1
            self.key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
            self.image_encrypted = image_input / self.key
            
            cv2.imwrite('image_encrypted.jpg', self.image_encrypted * 255)
            self.eimg = Image.open('image_encrypted.jpg')
            
            self.status_label.config(text="🔒 Image encrypted successfully")
            mbox.showinfo("SecurePix", "Image encrypted successfully!")
        except Exception as e:
            mbox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def de_fun(self):
        if self.image_encrypted is None or self.key is None:
            mbox.showerror("Error", "No encrypted image to decrypt!")
            return
            
        try:
            image_output = self.image_encrypted * self.key
            image_output *= 255.0
            
            cv2.imwrite('image_output.jpg', image_output)
            self.eimg = Image.open('image_output.jpg')
            
            self.status_label.config(text="🔓 Image decrypted successfully")
            mbox.showinfo("SecurePix", "Image decrypted successfully!")
        except Exception as e:
            mbox.showerror("Error", f"Decryption failed: {str(e)}")
    
    def reset(self):
        if not self.current_image_path:
            mbox.showerror("Error", "No image to reset!")
            return
            
        try:
            image = cv2.imread(self.current_image_path)[:, :, ::-1]
            self.eimg = Image.fromarray(image)
            self.status_label.config(text=f"↺ Image reset to original")
            mbox.showinfo("SecurePix", "Image reset to original format!")
        except Exception as e:
            mbox.showerror("Error", f"Reset failed: {str(e)}")
    
    def save_img(self):
        if self.eimg is None:
            mbox.showerror("Error", "No image to save!")
            return
            
        try:
            filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
            if not filename:
                return
                
            self.eimg.save(filename)
            self.status_label.config(text=f"💾 Image saved successfully")
            mbox.showinfo("SecurePix", "Image saved successfully!")
        except Exception as e:
            mbox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def exit_win(self):
        if mbox.askokcancel("Exit SecurePix", "Do you want to exit SecurePix?"):
            self.window.destroy()

if __name__ == "__main__":
    window = tk.Tk()
    app = SecurePixApp(window)
    window.protocol("WM_DELETE_WINDOW", app.exit_win)
    window.mainloop()
