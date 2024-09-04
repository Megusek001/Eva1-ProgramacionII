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
        self.ingredient_name_entry = ctk.CTkEntry(self.tab_ingredientes, placeholder_text="Nombre del Ingrediente")
        self.ingredient_name_entry.pack(pady=10)

        self.ingredient_qty_entry = ctk.CTkEntry(self.tab_ingredientes, placeholder_text="Cantidad")
        self.ingredient_qty_entry.pack(pady=10)

        self.add_ingredient_btn = ctk.CTkButton(self.tab_ingredientes, text="Agregar Ingrediente", command=self.add_ingredient)
        self.add_ingredient_btn.pack(pady=10)

        self.delete_ingredient_btn = ctk.CTkButton(self.tab_ingredientes, text="Eliminar Ingrediente", command=self.delete_ingredient)
        self.delete_ingredient_btn.pack(pady=10)

        self.generate_menu_btn = ctk.CTkButton(self.tab_ingredientes, text="Generar Menú", command=self.generate_menu)
        self.generate_menu_btn.pack(pady=10)

        
        self.ingredient_listbox = Listbox(self.tab_ingredientes, selectmode="single")
        self.ingredient_listbox.pack(expand=1, fill="both", pady=10)

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
        
        
        messagebox.showinfo("Generar Menú", "Menú generado correctamente.")

    
    def create_orders_tab(self):
    
        ctk.CTkLabel(self.tab_pedidos, text="Gestión de Pedidos").pack(pady=10)
        # Agregar animaciones y lógica para gestionar los menús y generar boletos.
    

# Inicializar la aplicación
if __name__ == "__main__":
    app = RestauranteApp()
    app.mainloop()
