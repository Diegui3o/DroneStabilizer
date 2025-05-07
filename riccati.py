import numpy as np
from scipy.linalg import solve_continuous_are, eigvals

# === 1. Parámetros físicos ===
print("\n=== 1. Parámetros físicos ===")
m = 1.1
W = 0.63
L = 0.63
H = 0.1

Ix = m * ((W**2 + H**2) / 12)
Iy = m * ((L**2 + H**2) / 12)
Iz = m * ((L**2 + W**2) / 12)

print(f"Momentos de inercia:")
print(f"Ix = {Ix:.4f} kg·m²")
print(f"Iy = {Iy:.4f} kg·m²")
print(f"Iz = {Iz:.4f} kg·m²")

# === 2. Matriz A ===
print("\n=== 2. Matriz A (9x9) ===")
A = np.array([
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0]
])
print("Matriz A (dinámica del sistema):")
print(np.round(A, 4))

# === 3. Matriz B ===
print("\n=== 3. Matriz B (9x3) ===")
B = np.array([
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [1/Ix, 0, 0],
    [0, 1/Iy, 0],
    [0, 0, 1/Iz],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
])
print("Matriz B (entradas de control):")
print(np.round(B, 4))

# === 4. Matrices de peso Q y R ===
print("\n=== 4. Matrices de peso Q y R ===")
Q = np.diag([0.02, 0.01, 0.1, 0.12, 0.05, 0.1, 10, 10, 10])
R = np.diag([1, 1, 0.1])

print("Matriz Q (9x9):")
print(np.round(Q, 4))
print("\nMatriz R (3x3):")
print(np.round(R, 4))

# === 5. Solución de la ecuación algebraica de Riccati ===
print("\n=== 5. Solución de la ecuación de Riccati ===")
P = solve_continuous_are(A, B, Q, R)
print("Matriz P (9x9) solución de Riccati:")
print(np.round(P, 4))

# === 6. Cálculo de la matriz de ganancia K ===
print("\n=== 6. Cálculo de la matriz de ganancia K ===")
K_total = np.linalg.inv(R) @ B.T @ P
print("Matriz de ganancia total K_total (3x9):")
print(np.round(K_total, 4))

# === 7. Separación en K_c y K_i ===
print("\n=== 7. Separación en K_c y K_i ===")
K_c = K_total[:, :6]  # Primeras 6 columnas
K_i = K_total[:, 6:]  # Últimas 3 columnas

print("\nMatriz K_c (3x6) - ganancias para estados principales:")
print(np.round(K_c, 4))
print("\nMatriz K_i (3x3) - ganancias para estados integrales:")
print(np.round(K_i, 4))

# === 8. Verificación de estabilidad ===
print("\n=== 8. Verificación de estabilidad ===")
A_cl = A - B @ K_total
eigs = eigvals(A_cl)
print("Autovalores del sistema en lazo cerrado:")
print(np.round(eigs, 4))
print("\nPartes reales de los autovalores:")
print(np.round(np.real(eigs), 4))

if np.all(np.real(eigs) < 0):
    print("\n✅ Sistema cerrado ESTABLE (todas las partes reales son negativas)")
else:
    print("\n❌ Sistema cerrado INESTABLE (hay partes reales positivas)")

# === 9. Descomposición adicional para entender K ===
print("\n=== 9. Descomposición adicional de K ===")
print("\nComponente R⁻¹Bᵀ:")
R_inv_BT = np.linalg.inv(R) @ B.T
print(np.round(R_inv_BT, 4))

print("\nComponente BᵀP:")
BT_P = B.T @ P
print(np.round(BT_P, 4))

print("\nVerificación: K_total = R⁻¹ @ (Bᵀ @ P)")
verification = np.linalg.inv(R) @ (B.T @ P)
print("¿Son iguales K_total y la verificación?", np.allclose(K_total, verification))