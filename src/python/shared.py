

def calcular_error(a: tuple, b: tuple, grid_x, grid_y, instance):
    # Inicializa el error acumulado a 0.
    error = 0

    # Extrae las coordenadas x e y para el punto a y b usando los índices de a en las grillas grid_x y grid_y.
    ax, ay = grid_x[a[0]], grid_y[a[1]]
    bx, by = grid_x[b[0]], grid_y[b[1]]

    # Itera sobre cada punto x en el conjunto de datos.
    for i, x in enumerate(instance["x"]):
        # Si el punto actual x está entre ax y bx...
        if ax <= x <= bx:
            # Calculamos el valor de y predicho por la recta que pasa por a y b.
            predicted_y = ((by - ay) / (bx - ax)) * (x - ax) + ay
            # Acumulamos el error absoluto entre el y predicho y el y real para este punto.
            error += abs(instance["y"][i] - predicted_y)

    # Devuelve el error total acumulado para todos los puntos en el rango de interés.
    return error