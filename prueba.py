import customtkinter as ctk
from tkinter import Listbox, messagebox
import pdfkit  

class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("800x600")
        self.ingredients = {}  

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

        # Crear y ubicar la lista de ingredientes, ahora más grande
        self.ingredient_listbox = Listbox(self.tab_ingredientes, selectmode="single", height=20, width=50)
        self.ingredient_listbox.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

        # Asegurar que la lista ocupe más espacio en la columna
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
        self.ingredient_listbox.insert("end", f"{name} - {quantity}")
        self.ingredient_name_entry.delete(0, "end")
        self.ingredient_qty_entry.delete(0, "end")

    def delete_ingredient(self):
        selected = self.ingredient_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un ingrediente para eliminar.")
            return

        ingredient = self.ingredient_listbox.get(selected)
        name = ingredient.split(" - ")[0]
        del self.ingredients[name]
        self.ingredient_listbox.delete(selected)

    def generate_menu(self):
        if not self.ingredients:
            messagebox.showerror("Error", "No hay ingredientes para generar el menú.")
            return

        menu_content = "<h1>Menú del Restaurante</h1><ul>"
        for name, quantity in self.ingredients.items():
            menu_content += f"<li>{name} - {quantity}</li>"
        menu_content += "</ul>"

        pdfkit.from_string(menu_content, 'menu.pdf')
        messagebox.showinfo("Generar Menú", "Menú generado correctamente como menu.pdf.")

    def create_orders_tab(self):
        ctk.CTkLabel(self.tab_pedidos, text="Gestión de Pedidos").pack(pady=10)

        self.order_name_entry = ctk.CTkEntry(self.tab_pedidos, placeholder_text="Nombre del Pedido")
        self.order_name_entry.pack(pady=10)

        self.order_qty_entry = ctk.CTkEntry(self.tab_pedidos, placeholder_text="Cantidad")
        self.order_qty_entry.pack(pady=10)

        self.add_order_btn = ctk.CTkButton(self.tab_pedidos, text="Agregar Pedido", command=self.add_order)
        self.add_order_btn.pack(pady=10)

        self.order_listbox = Listbox(self.tab_pedidos, selectmode="single")
        self.order_listbox.pack(expand=1, fill="both", pady=10)

    def add_order(self):
        name = self.order_name_entry.get()
        quantity = self.order_qty_entry.get()

        if not name or not quantity:
            messagebox.showerror("Error", "Debe ingresar el nombre y la cantidad del pedido.")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        self.order_listbox.insert("end", f"{name} - {quantity}")
        self.order_name_entry.delete(0, "end")
        self.order_qty_entry.delete(0, "end")

# Inicializar la aplicación
if __name__ == "__main__":
    app = RestauranteApp()
    app.mainloop()


