import customtkinter as ctk
from tkinter import Listbox, messagebox, PhotoImage
from fpdf import FPDF
from tkinter import ttk

class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("800x600")
        self.ingredients = {}
        self.orders = {}

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=1, fill="both")

        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.create_ingredients_tab()

        self.tab_pedidos = self.tabview.add("Pedidos")
        self.create_orders_tab()

    def create_ingredients_tab(self):
        # Crear y ubicar los campos de entrada y botones
        self.ingredient_name_entry = ctk.CTkEntry(self.tab_ingredientes, placeholder_text="Nombre del Ingrediente")
        self.ingredient_name_entry.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.ingredient_qty_entry = ctk.CTkEntry(self.tab_ingredientes, placeholder_text="Cantidad")
        self.ingredient_qty_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.add_ingredient_btn = ctk.CTkButton(self.tab_ingredientes, text="Agregar Ingrediente", command=self.add_ingredient)
        self.add_ingredient_btn.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.delete_ingredient_btn = ctk.CTkButton(self.tab_ingredientes, text="Eliminar Ingrediente", command=self.delete_ingredient)
        self.delete_ingredient_btn.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.generate_menu_btn = ctk.CTkButton(self.tab_ingredientes, text="Generar Menú", command=self.generate_menu)
        self.generate_menu_btn.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # Crear y ubicar el Treeview para mostrar ingredientes
        self.ingredient_tree = ttk.Treeview(self.tab_ingredientes, columns=("Nombre", "Cantidad"), show="headings")
        self.ingredient_tree.heading("Nombre", text="Nombre")
        self.ingredient_tree.heading("Cantidad", text="Cantidad")
        self.ingredient_tree.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

        # Configurar la distribución del espacio
        self.tab_ingredientes.grid_columnconfigure(1, weight=1)
        self.tab_ingredientes.grid_rowconfigure(0, weight=1)

    def add_ingredient(self):
        name = self.ingredient_name_entry.get()
        quantity = self.ingredient_qty_entry.get()

        if not name or not quantity:
            messagebox.showerror("Error", "Debe ingresar el nombre y la cantidad del ingrediente.")
            return

        try:
            quantity = float(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return

        self.ingredients[name] = quantity
        self.ingredient_tree.insert("", "end", values=(name, quantity))
        self.ingredient_name_entry.delete(0, "end")
        self.ingredient_qty_entry.delete(0, "end")

    def delete_ingredient(self):
        selected_item = self.ingredient_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un ingrediente para eliminar.")
            return

        item = self.ingredient_tree.item(selected_item)
        name = item["values"][0]
        del self.ingredients[name]
        self.ingredient_tree.delete(selected_item)

    def generate_menu(self):
        if not self.ingredients:
            messagebox.showerror("Error", "No hay ingredientes para generar el menú.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Menú del Restaurante", ln=True, align='C')
        pdf.ln(10)

        for name, quantity in self.ingredients.items():
            pdf.cell(200, 10, txt=f"{name} - {quantity}", ln=True)

        pdf.output("menu.pdf")
        messagebox.showinfo("Generar Menú", "Menú generado correctamente como menu.pdf.")

    def create_orders_tab(self):
        ctk.CTkLabel(self.tab_pedidos, text="Gestión de Pedidos").pack(pady=10)

        # Cargar imágenes para los botones
        self.hamburger_icon = PhotoImage(file="image/icono_hamburguesa_negra_64x64.png")  # Ruta a tu imagen
        self.fries_icon = PhotoImage(file="image/icono_papas_fritas_64x64.png")  # Ruta a tu imagen
        self.pepsi_icon = PhotoImage(file="image/icono_cola_64x64.png")  # Ruta a tu imagen
        self.hotdog_icon = PhotoImage(file="image/icono_hotdog_sin_texto_64x64.png")  # Ruta a tu imagen

        # Botones con iconos
        self.add_hamburger_btn = ctk.CTkButton(self.tab_pedidos, image=self.hamburger_icon, text="Hamburguesa", command=lambda: self.add_order("Hamburguesa"))
        self.add_hamburger_btn.pack(pady=10)

        self.add_fries_btn = ctk.CTkButton(self.tab_pedidos, image=self.fries_icon, text="Papas Fritas", command=lambda: self.add_order("Papas Fritas"))
        self.add_fries_btn.pack(pady=10)

        self.add_pepsi_btn = ctk.CTkButton(self.tab_pedidos, image=self.pepsi_icon, text="Pepsi", command=lambda: self.add_order("Pepsi"))
        self.add_pepsi_btn.pack(pady=10)

        self.add_hotdog_btn = ctk.CTkButton(self.tab_pedidos, image=self.hotdog_icon, text="Hotdog", command=lambda: self.add_order("Hotdog"))
        self.add_hotdog_btn.pack(pady=10)

        self.order_listbox = Listbox(self.tab_pedidos, selectmode="single")
        self.order_listbox.pack(expand=1, fill="both", pady=10)

        # Botón para generar boleta
        self.generate_receipt_btn = ctk.CTkButton(self.tab_pedidos, text="Generar Boleta", command=self.generate_receipt)
        self.generate_receipt_btn.pack(pady=10)

    def add_order(self, item_name):
        quantity = 1  # Se puede ajustar según necesidad
        if item_name in self.orders:
            self.orders[item_name] += quantity
        else:
            self.orders[item_name] = quantity

        self.order_listbox.insert("end", f"{item_name} - {quantity}")

    def generate_receipt(self):
        if not self.orders:
            messagebox.showerror("Error", "No hay pedidos para generar la boleta.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Boleta de Pedido", ln=True, align='C')
        pdf.ln(10)

        for name, quantity in self.orders.items():
            pdf.cell(200, 10, txt=f"{name} - {quantity}", ln=True)

        pdf.output("receipt.pdf")
        messagebox.showinfo("Generar Boleta", "Boleta generada correctamente como receipt.pdf.")

# Inicializar la aplicación
if __name__ == "__main__":
    app = RestauranteApp()
    app.mainloop()
