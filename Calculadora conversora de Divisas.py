import tkinter as tk
from tkinter import messagebox
import yfinance as yf

def obtener_tasa_divisa(origen, destino):
    #Obtiene la tasa de cambio entre dos monedas usando yfinance.
    simbolo = f"{origen}{destino}=X"  # Formato para Yahoo Finance
    divisa = yf.Ticker(simbolo)
    
    try:
        # Obtener el último precio de la divisa (la tasa de cambio)
        data = divisa.history(period="1d")
        
        # Verificar si los datos están vacíos
        if data.empty:
            raise ValueError(f"No se encontró información para el par de divisas {simbolo}.")
        
        tasa = data['Close'].iloc[0]
        return tasa
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la tasa de cambio: {e}")
        return None

def calcular_conversion():
    #Realiza la conversión de divisas cuando el usuario presiona el botón.
    try:
        moneda_origen = moneda_origen_var.get()
        moneda_destino = moneda_destino_var.get()
        cantidad = float(cantidad_entry.get())
        
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return
        
        # Obtener la tasa de cambio
        tasa = obtener_tasa_divisa(moneda_origen, moneda_destino)
        
        if tasa is None:
            return
        
        # Realizar la conversión
        cantidad_convertida = cantidad * tasa
        resultado_label.config(text=f"{cantidad} {moneda_origen} = {cantidad_convertida:.2f} {moneda_destino}")
    
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora de Conversión de Divisas")

# Crear las variables para las opciones seleccionadas
moneda_origen_var = tk.StringVar()
moneda_destino_var = tk.StringVar()

# Crear los elementos de la interfaz
tk.Label(root, text="Cantidad a convertir:").grid(row=0, column=0, padx=10, pady=10)

cantidad_entry = tk.Entry(root)
cantidad_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Moneda de origen:").grid(row=1, column=0, padx=10, pady=10)

moneda_origen_menu = tk.OptionMenu(root, moneda_origen_var, 'USD', 'EUR', 'COP', 'ARS', 'GBP', 'VES')
moneda_origen_menu.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Moneda de destino:").grid(row=2, column=0, padx=10, pady=10)

moneda_destino_menu = tk.OptionMenu(root, moneda_destino_var, 'USD', 'EUR', 'COP', 'ARS', 'GBP', 'VES')
moneda_destino_menu.grid(row=2, column=1, padx=10, pady=10)

# Botón para calcular la conversión
calcular_button = tk.Button(root, text="Convertir", command=calcular_conversion)
calcular_button.grid(row=3, column=0, columnspan=2, pady=10)

# Label para mostrar el resultado
resultado_label = tk.Label(root, text="", font=('Helvetica', 14))
resultado_label.grid(row=4, column=0, columnspan=2, pady=10)

# Configurar la moneda por defecto
moneda_origen_var.set("USD")
moneda_destino_var.set("EUR")

# Iniciar la aplicación
root.mainloop()

