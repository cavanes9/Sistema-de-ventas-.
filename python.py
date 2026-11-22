def mostrar_catalogo(catalogo):
    """Muestra el código, nombre, precio y existencia de cada videojuego."""
    print("\nCATALOGO GAMEZONE")
    for numero, producto in enumerate(catalogo, start=1):
        print(f"\n{numero}. {producto['nombre']}")
        print(f"   Codigo: {producto['codigo']}")
        print(f"   Precio: ${producto['precio']:.2f}")
        print(f"   Existencia: {producto['existencia']} unidad(es)")


def buscar_producto(catalogo, codigo):
    """Busca un producto por código y devuelve el diccionario o None."""
    codigo_buscado = codigo.strip().upper()
    for producto in catalogo:
        if producto["codigo"] == codigo_buscado:
            return producto
    return None


def hay_existencia(existencia, cantidad):
    """Indica si la cantidad es positiva y está disponible."""
    return cantidad > 0 and cantidad <= existencia


def calcular_importe(precio, cantidad):
    """Calcula el importe de una línea de compra, redondeado a centavos."""
    return round(precio * cantidad, 2)


def calcular_total(subtotal, descuento=0.0, impuesto=0.16):
    """Aplica el descuento indicado y luego el impuesto; devuelve el total."""
    subtotal_con_descuento = subtotal * (1 - descuento)
    return round(subtotal_con_descuento * (1 + impuesto), 2)


def actualizar_existencia(existencia, cantidad):
    """Devuelve las unidades que quedan después de una venta válida."""
    return existencia - cantidad


def mostrar_resumen(carrito, catalogo):
    """Imprime las líneas del carrito y desglosa subtotal, descuento e impuesto."""
    print("\nRESUMEN DE COMPRA")
    print("-" * 76)
    subtotal = 0.0
    for codigo, detalle in carrito.items():
        importe = calcular_importe(detalle["precio"], detalle["cantidad"])
        subtotal += importe
        print(
            f"{detalle['nombre']} ({codigo}) | "
            f"{detalle['cantidad']} unidad(es) | ${importe:.2f}"
        )

    subtotal = round(subtotal, 2)
    tasa_descuento = 0.10 if subtotal >= 1000 else 0.0
    descuento_aplicado = round(subtotal * tasa_descuento, 2)
    base_gravable = round(subtotal - descuento_aplicado, 2)
    impuesto = round(base_gravable * 0.16, 2)
    total = calcular_total(subtotal, descuento=tasa_descuento, impuesto=0.16)

    print("-" * 76)
    print(f"Subtotal:  ${subtotal:.2f}")
    print(f"Descuento: -${descuento_aplicado:.2f}")
    print(f"Impuesto:   ${impuesto:.2f}")
    print(f"TOTAL:      ${total:.2f}")
    print("\nINVENTARIO RESTANTE")
    for producto in catalogo:
        print(f"{producto['codigo']} - {producto['nombre']}: {producto['existencia']}")


def main():
    """Controla el catálogo, las ventas y el cierre de la compra."""
    catalogo = [
        {
            "codigo": "G101",
            "nombre": "Nebula Drift",
            "precio": 579.00,
            "existencia": 6,
        },
        {
            "codigo": "G102",
            "nombre": "Pixel Farm",
            "precio": 389.00,
            "existencia": 9,
        },
        {
            "codigo": "G103",
            "nombre": "Dragon's Crownfall",
            "precio": 1_349.00,
            "existencia": 4,
        },
        {
            "codigo": "G104",
            "nombre": "Turbo Kart Legends",
            "precio": 829.00,
            "existencia": 5,
        },
        {
            "codigo": "G105",
            "nombre": "Moonlight Keeper",
            "precio": 279.00,
            "existencia": 12,
        },
    ]
    carrito = {}

    print("Bienvenido(a) a la tienda GAMEZONE.")
    mostrar_catalogo(catalogo)

    while True:
        codigo = input("\nEscribe el codigo del videojuego (o SALIR): ").strip()
        if codigo.upper() == "SALIR":
            break

        producto = buscar_producto(catalogo, codigo)
        if producto is None:
            print("Codigo incorrecto. Intenta nuevamente.")
            continue

        try:
            cantidad = int(input("¿Cuántas unidades deseas?: "))
        except ValueError:
            print("Cantidad no valida. Escribe un numero entero.")
            continue

        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            continue
        if not hay_existencia(producto["existencia"], cantidad):
            print(f"Existencia insuficiente. Hay {producto['existencia']} unidad(es).")
            continue

        importe = calcular_importe(producto["precio"], cantidad)
        producto["existencia"] = actualizar_existencia(
            producto["existencia"], cantidad
        )

        # Si el producto ya estaba en el carrito, se acumula en la misma línea.
        if producto["codigo"] in carrito:
            carrito[producto["codigo"]]["cantidad"] += cantidad
        else:
            carrito[producto["codigo"]] = {
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "cantidad": cantidad,
            }
        print(
            f"Agregado: {cantidad} x {producto['nombre']} "
            f"= ${importe:.2f}. Existencia restante: {producto['existencia']}."
        )

    if carrito:
        mostrar_resumen(carrito, catalogo)
    else:
        print("\nNo se agregaron productos. No hay compra que cobrar.")

    print("\nGracias por comprar en GAMEZONE.")


if __name__ == "__main__":
    main()