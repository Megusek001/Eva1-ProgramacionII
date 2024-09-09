import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from fpdf import FPDF
from tkinter import ttk

class PDf(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Boleta de pedido', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I', 8)
        self.cell(0, 10, f'Pagina{self.page_no()}', 0, 0, 'C')

    def add_table_header(self):
        self.set_font('Arial', 'I', 8)
        self.set_font('Arial', 'B', 12)
        self.cell(80, 10, 'Producto', 1)
        self.cell(30, 10, 'Cantidad', 1, 0, 'C')
        self.cell(40, 10, 'Precio Unitario', 1, 0, 'C')
        self.cell(40, 10, 'Subtotal', 1, 1, 'C')


    def add_product(self, product, quantity, price):
        self.set_font('Arial', '', 12)
        subtotal = quantity * price
        self.cell(80, 10, product, 1)
        self.cell(30, 10, str(quantity), 1, 0, 'C')
        self.cell(40, 10, f'{price:.2f}', 1, 0, 'C')
        self.cell(40, 10, f'{subtotal:.2f}', 1, 1, 'C')
        return subtotal


    def add_total(self, total):
        self.cell(150, 10, 'Total', 1, 0, 'R')
        self.cell(40, 10, f'{total:.2f}', 1, 1, 'C')


class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("600x600")
        self.ingredients = {}
        self.orders = {}

        self.icons = {
            "Hamburguesa": PhotoImage(file="image/hamburguesa.png"),
            "Papas Fritas": PhotoImage(file="image/papas.png"),
            "Pepsi": PhotoImage(file="image/pepsi.png"),
            "Hotdog": PhotoImage(file="image/hotdog.png")
        }

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=1, fill="both")

        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.create_ingredients_tab()

        self.tab_pedidos = self.tabview.add("Pedidos")
        self.create_orders_tab()

    def create_ingredients_tab(self):
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
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un numero positivo.")
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

        self.tabview.set("Pedidos") 
        products_requirements = {
            "Hamburguesa": {"Pan": 1, "Carne": 1},
            "Papas Fritas": {"Papa": 2},
            "Pepsi": {"Pepsi": 1},
            "Hotdog": {"Pan": 1, "Salchicha": 1},
        }

        for product, required_ingredients in products_requirements.items():
            can_add_product = True
            for ingredient, required_qty in required_ingredients.items():
                if self.ingredients.get(ingredient, 0) < required_qty:
                    can_add_product = False
                    break

            if can_add_product:
                # Añadir botón con icono
                frame = ctk.CTkFrame(self.tab_pedidos)
                frame.pack(pady=10, padx=10, fill="x")

                button = ctk.CTkButton(frame, text=product, command=lambda p=product: self.add_order(p, 2.500))
                button.pack(side="left")

                # Añadir icono del producto
                if product in self.icons:
                    icon_label = ctk.CTkLabel(frame, image=self.icons[product])
                    icon_label.pack(side="left", padx=10)


    def create_orders_tab(self):
        ctk.CTkLabel(self.tab_pedidos, text="Gestión de Pedidos").pack(pady=10)

        #########
    def add_order(self, item_name, price):
        ##########

    def delete_order(self):
        ###########




    def generate_receipt(self):
        if not self.orders:
            messagebox.showerror("Error", "No hay pedidos para generar la boleta.")
            return

        pdf = PDf()
        pdf.add_page()
        pdf.add_table_header()
        
        
        total = 0
        for item, details in self.orders.items():
            subtotal = pdf.add_product(item, details["quantity"], details["price"])
            total += subtotal

        pdf.add_total(total)    
        pdf.output("Boleta.pdf")
        messagebox.showinfo("Éxito", "Boleta generada exitosamente.")

if __name__ == "__main__":
    app = RestauranteApp()
    app.mainloop()
