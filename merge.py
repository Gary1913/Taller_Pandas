from pathlib import Path

PROCESSED = Path(__file__).parent / "Data" / "processed"


def validar_premerge(clientes, ventas):
    """Revisa que el merge se pueda hacer. Devuelve True si todo está bien, False si no.

    Revisar:
    - Que exista la columna "id_cliente" en los dos dataframes.
    - Que "id_cliente" no esté repetido en clientes.
    - Que "id_cliente" tenga el mismo tipo en los dos dataframes.
    - Cuántas ventas no tienen cliente asociado (esto solo se informa, no falla).
    """
    # TODO 6: escribir las validaciones y devolver True o False.
    print("\n[validación] Revisando las tablas antes del merge...")

    if "id_cliente" not in clientes.columns or "id_cliente" not in ventas.columns:
        print("[validación] ERROR: falta la columna id_cliente en alguna tabla.")
        return False
    print("[validación] La columna id_cliente existe en ambas tablas.")

    repetidos = clientes["id_cliente"].duplicated().sum()
    if repetidos > 0:
        print(f"[validación] ERROR: hay {repetidos} id_cliente repetidos en clientes.")
        return False
    print("[validación] No hay id_cliente repetidos en clientes.")

    tipo_clientes = clientes["id_cliente"].dtype
    tipo_ventas = ventas["id_cliente"].dtype
    if tipo_clientes != tipo_ventas:
        print(f"[validación] ERROR: tipos distintos ({tipo_clientes} vs {tipo_ventas}).")
        return False
    print(f"[validación] El tipo de id_cliente coincide: {tipo_clientes}.")

    sin_cliente = (~ventas["id_cliente"].isin(clientes["id_cliente"])).sum()
    print(f"[validación] Ventas sin cliente asociado: {sin_cliente}")

    return True


def unir(clientes, ventas):
    """Une ventas con clientes usando "id_cliente" y guarda el resultado en Data/processed/merge.csv.

    Pistas:
    - Usar pd.merge(...) o ventas.merge(...).
    - Usar how="left" para no perder ventas.
    - Usar validate="m:1" para confirmar que cada venta tiene un solo cliente.
    - Guardar con df.to_csv(...) en PROCESSED / "merge.csv".
    """
    # TODO 7: validar con validar_premerge(), hacer el merge, guardar el CSV y devolver el dataframe.
    if not validar_premerge(clientes, ventas):
        print("[merge] No se hizo el merge porque la validación falló.")
        return None

    df = ventas.merge(clientes, on="id_cliente", how="left", validate="m:1")

    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "merge.csv", index=False)

    print(f"\n[merge] Ventas: {ventas.shape} | Clientes: {clientes.shape}")
    print(f"[merge] Resultado del merge: {df.shape}")
    print(f"[merge] Guardado en: {PROCESSED / 'merge.csv'}")
    return df