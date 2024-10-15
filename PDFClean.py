import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

# Función para seleccionar el archivo PDF
def select_pdf():
    pdf_path = filedialog.askopenfilename(title="Selecciona un archivo PDF", filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        pdf_name = os.path.basename(pdf_path)  # Mostrar solo el nombre del archivo
        pdf_label.config(text=pdf_name)
        pdf_label.path = pdf_path  # Guardar la ruta completa en una variable
        return pdf_path
    else:
        return None

# Función para eliminar páginas del PDF
def remove_pages():
    pdf_path = getattr(pdf_label, 'path', None)
    if not pdf_path:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo PDF.")
        return

    try:
        pages_to_remove = list(map(int, pages_entry.get().split(',')))  # Convertir a lista de enteros
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        # Agregar las páginas que no estén en la lista de eliminadas
        for page_num in range(len(reader.pages)):
            if page_num + 1 not in pages_to_remove:  # +1 porque las páginas empiezan en 1
                writer.add_page(reader.pages[page_num])

        # Sobrescribir el archivo PDF original
        with open(pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)
        
        messagebox.showinfo("Éxito", f"Las páginas seleccionadas han sido eliminadas del archivo {os.path.basename(pdf_path)}.")

    except ValueError:
        messagebox.showerror("Error", "Formato incorrecto de páginas. Usa números separados por comas.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("PDFClean - Eliminar páginas")

# Configurar tamaño y diseño de la ventana
root.geometry("400x280")  # Tamaño ajustado para que todo el texto entre
root.resizable(False, False)  # Desactivar redimensionamiento

# Colores para el tema oscuro
bg_color = "#2e2e2e"  # Fondo oscuro
fg_color = "#ffffff"  # Texto blanco
button_color = "#2e8b57"  # Verde claro para el botón

# Aplicar color de fondo a la ventana principal
root.config(bg=bg_color)

# Encabezado
header = tk.Label(root, text="PDFClean", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color)
header.pack(pady=10)

# Etiqueta para mostrar el archivo PDF seleccionado
pdf_label = tk.Label(root, text="Ningún archivo seleccionado", font=("Arial", 12), bg=bg_color, fg=fg_color)
pdf_label.pack(pady=10)

# Botón para seleccionar el archivo PDF
select_button = tk.Button(root, text="Seleccionar PDF", command=select_pdf, font=("Arial", 12), width=20, bg="#444444", fg=fg_color, relief="flat")
select_button.pack(pady=5)

# Entrada para las páginas a eliminar
pages_label = tk.Label(root, text="Páginas a eliminar (separadas por comas):", font=("Arial", 12), bg=bg_color, fg=fg_color)
pages_label.pack(pady=5)
pages_entry = tk.Entry(root, font=("Arial", 12), justify='center', bg="#555555", fg=fg_color, insertbackground=fg_color)
pages_entry.pack(pady=5)

# Botón para ejecutar la eliminación de páginas
remove_button = tk.Button(root, text="Eliminar páginas", command=remove_pages, font=("Arial", 12), width=20, height=2, bg=button_color, fg=fg_color, relief="flat")
remove_button.pack(pady=20)

# Ejecutar la interfaz gráfica
root.mainloop()
