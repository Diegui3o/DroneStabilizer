import numpy as np
import logging

logger = logging.getLogger(__name__)

def rotation_matrix(phi, theta, psi):
    # Pre-compute trigonometric functions
    c_phi, s_phi = np.cos(phi), np.sin(phi)
    c_theta, s_theta = np.cos(theta), np.sin(theta)
    c_psi, s_psi = np.cos(psi), np.sin(psi)
    
    # Compute rotation matrix
    R = np.array([
        [c_theta * c_psi, c_theta * s_psi, -s_theta],
        [s_phi * s_theta * c_psi - c_phi * s_psi, s_phi * s_theta * s_psi + c_phi * c_psi, s_phi * c_theta],
        [c_phi * s_theta * c_psi + s_phi * s_psi, c_phi * s_theta * s_psi - s_phi * c_psi, c_phi * c_theta]
    ])
    
    return R

def euler_from_quaternion(quaternion):
    w, x, y, z = quaternion
    
    # Roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)
    
    # Pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if np.abs(sinp) >= 1:
        pitch = np.copysign(np.pi / 2, sinp)  # Use 90 degrees if out of range
    else:
        pitch = np.arcsin(sinp)
    
    # Yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)
    
    return np.array([roll, pitch, yaw])

def quaternion_from_euler(roll, pitch, yaw):
    # Pre-compute values
    cr, sr = np.cos(roll * 0.5), np.sin(roll * 0.5)
    cp, sp = np.cos(pitch * 0.5), np.sin(pitch * 0.5)
    cy, sy = np.cos(yaw * 0.5), np.sin(yaw * 0.5)
    
    # Compute quaternion
    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    
    return np.array([w, x, y, z])

def compute_performance_metrics(result):
    # Extract data
    time = result['time']
    states = result['states']
    error = result['error']
    inputs = result['inputs']
    
    # Compute metrics
    
    # Settling time (time to reach within 2% of final value)
    position_error_norm = np.linalg.norm(error[:, 0:3], axis=1)
    threshold = 0.02 * np.max(position_error_norm)
    settling_indices = np.where(position_error_norm < threshold)[0]
    
    if len(settling_indices) > 0:
        settling_time = time[settling_indices[0]]
    else:
        settling_time = float('inf')
    
    # Maximum position error
    max_position_error = np.max(position_error_norm)
    
    # Root mean square error
    rmse_position = np.sqrt(np.mean(position_error_norm**2))
    
    # Integral of absolute error
    iae_position = np.trapz(position_error_norm, time)
    
    # Maximum control effort
    max_control_effort = np.max(np.linalg.norm(inputs, axis=1))
    
    # Total control energy
    control_energy = np.trapz(np.sum(inputs**2, axis=1), time)
    
    # Angular error metrics
    orientation_error_norm = np.linalg.norm(error[:, 6:9], axis=1)
    rmse_orientation = np.sqrt(np.mean(orientation_error_norm**2))
    max_orientation_error = np.max(orientation_error_norm)
    
    # Compile metrics
    metrics = {
        'settling_time': settling_time,
        'max_position_error': max_position_error,
        'rmse_position': rmse_position,
        'iae_position': iae_position,
        'max_control_effort': max_control_effort,
        'control_energy': control_energy,
        'rmse_orientation': rmse_orientation,
        'max_orientation_error': max_orientation_error
    }
    
    return metrics
