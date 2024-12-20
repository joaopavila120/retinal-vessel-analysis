import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from image_processing import analisar_retina
import matplotlib.pyplot as plt

class RetinaAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Analisador de Retina")
        self.geometry("700x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.image_path = None
        self.image_preview_label = None

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Analisador de Retina", font=("Arial", 20))
        self.label.pack(pady=20)

        self.button_select = ctk.CTkButton(self, text="Selecionar Imagem", command=self.select_image)
        self.button_select.pack(pady=10)

        self.button_process = ctk.CTkButton(self, text="Processar", command=self.process_image)
        self.button_process.pack(pady=10)

        self.image_frame = ctk.CTkFrame(self, width=300, height=300, corner_radius=10)
        self.image_frame.pack(pady=20)

        self.image_label = ctk.CTkLabel(self.image_frame, text="Prévia da Imagem")
        self.image_label.pack(expand=True)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            img = Image.open(self.image_path)
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)

            if self.image_preview_label is not None:
                self.image_preview_label.destroy()

            self.image_preview_label = ctk.CTkLabel(self.image_frame, image=img_tk, text="")
            self.image_preview_label.image = img_tk
            self.image_preview_label.pack()

    def process_image(self):
        if not self.image_path:
            messagebox.showerror("Erro", "Nenhuma imagem foi selecionada!")
            return

        try:
            img_original, img_gray, img_tophat, bordas, status = analisar_retina(self.image_path)
            
            plt.figure(figsize=(12, 8))
            plt.subplot(1, 4, 1), plt.imshow(img_original), plt.title('Original')
            plt.subplot(1, 4, 2), plt.imshow(img_gray, cmap='gray'), plt.title('Cinza')
            plt.subplot(1, 4, 3), plt.imshow(img_tophat, cmap='gray'), plt.title('Vasos Realçados')
            plt.subplot(1, 4, 4), plt.imshow(bordas, cmap='gray'), plt.title(f"Diagnóstico: {status}")
            plt.tight_layout()
            plt.show()

        except ValueError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar a imagem: {str(e)}")

if __name__ == "__main__":
    app = RetinaAnalyzerApp()
    app.mainloop()
