import numpy as np
from scipy.integrate import solve_ivp
import logging

logger = logging.getLogger(__name__)

def get_state_space_matrices(Ixx, Iyy, Izz, mass, g):

    # Initialize matrices with zeros
    A = np.zeros((12, 12))
    B = np.zeros((12, 4))
    
    # Fill in the A matrix based on the linearized model
    # Position derivatives
    A[0, 3] = 1.0  # dx/dt = u
    A[1, 4] = 1.0  # dy/dt = v
    A[2, 5] = 1.0  # dz/dt = w
    
    # Velocity derivatives
    A[3, 7] = g    # du/dt = g*theta
    A[4, 6] = -g   # dv/dt = -g*phi
    
    # Angular position derivatives
    A[6, 9] = 1.0  # dphi/dt = p
    A[7, 10] = 1.0  # dtheta/dt = q
    A[8, 11] = 1.0  # dpsi/dt = r
    
    # Fill in the B matrix
    B[5, 0] = 1.0 / mass  # dw/dt = T/m
    B[9, 1] = 1.0 / Ixx   # dp/dt = tau_x/Ixx
    B[10, 2] = 1.0 / Iyy  # dq/dt = tau_y/Iyy
    B[11, 3] = 1.0 / Izz  # dr/dt = tau_z/Izz
    
    return A, B

def nonlinear_dynamics(t, state, u, params):
    
    # Extract state variables
    x, y, z, u_vel, v_vel, w_vel, phi, theta, psi, p, q, r = state
    
    # Extract inputs
    T, tau_x, tau_y, tau_z = u
    
    # Extract parameters
    Ixx = params['Ixx']
    Iyy = params['Iyy']
    Izz = params['Izz']
    mass = params['mass']
    g = params['g']
    
    # Trigonometric functions for convenience
    sin_phi = np.sin(phi)
    cos_phi = np.cos(phi)
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    sin_psi = np.sin(psi)
    cos_psi = np.cos(psi)
    
    # Derivatives for position
    dx = u_vel
    dy = v_vel
    dz = w_vel
    
    # Derivatives for linear velocity
    du = r * v_vel - q * w_vel + g * sin_theta
    dv = p * w_vel - r * u_vel - g * cos_theta * sin_phi
    dw = q * u_vel - p * v_vel - g * cos_theta * cos_phi + T / mass
    
    # Derivatives for angles
    dphi = p + q * sin_phi * np.tan(theta) + r * cos_phi * np.tan(theta)
    dtheta = q * cos_phi - r * sin_phi
    dpsi = q * sin_phi / cos_theta + r * cos_phi / cos_theta
    
    # Derivatives for angular rates
    dp = (Iyy - Izz) * q * r / Ixx + tau_x / Ixx
    dq = (Izz - Ixx) * p * r / Iyy + tau_y / Iyy
    dr = (Ixx - Iyy) * p * q / Izz + tau_z / Izz
    
    return np.array([dx, dy, dz, du, dv, dw, dphi, dtheta, dpsi, dp, dq, dr])
