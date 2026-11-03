import pandas as pd

ventas = pd.read_csv("Data/raw/ventas.csv")
clientes = pd.read_csv("Data/raw/cliente.csv")

print("=== VENTAS ===")
print(ventas.shape)
ventas.info()
print(ventas.describe())

print("\n=== CLIENTES ===")
print(clientes.shape)
clientes.info()
print(clientes.describe())