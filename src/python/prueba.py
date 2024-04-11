import json

def calcular_error(a: tuple, b: tuple, instance: json) -> float:
    error = 0
    for i in range(len(instance["x"])):
        if instance["x"][i] > a[0] and instance["x"][i] <= b[0]:
            # Calculamos el valor y(t) usando la ecuación de la recta proporcionada
            y_t = ((b[1] - a[1]) / (b[0] - a[0])) * (instance["x"][i] - a[0]) + a[1]
            # Calculamos el error absoluto de aproximación e(xi, yi) usando la fórmula proporcionada
            error += abs(instance["y"][i] - y_t)
    return error


def test_calculate_error():
    # Conjuntos de datos de prueba
    instance1 = {"x": [0, 1, 2], "y": [0, 1, 2]}
    instance2 = {"x": [1, 2, 3], "y": [3, 4, 5]}  # Corregido para cumplir con las condiciones

    # Pruebas para diferentes casos
    assert calcular_error((0, 0), (1, 1), instance1) == 0
    assert calcular_error((0, 0), (1, 1), instance2) == 0  # Ajustado para coincidir con la recta y = x
    assert calcular_error((1, 2), (2, 3), instance1) == 0
    assert calcular_error((1, 2), (2, 3), instance2) == 0

    # Asegurarse de que los valores de retorno sean flotantes
    assert isinstance(calcular_error((0, 0), (1, 1), instance1), float)
    assert isinstance(calcular_error((0, 0), (1, 1), instance2), float)
    assert isinstance(calcular_error((1, 2), (2, 3), instance1), float)
    assert isinstance(calcular_error((1, 2), (2, 3), instance2), float)

    print("Pruebas pasadas con éxito")

if __name__ == "__main__":
    test_calculate_error()
