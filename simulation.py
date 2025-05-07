import numpy as np
from scipy.integrate import solve_ivp
import logging
from drone_model import nonlinear_dynamics
from lqr_controller import lqr_control

logger = logging.getLogger(__name__)

def run_simulation(A, B, K, initial_state, simulation_time, dt, reference_state=None):
    # Default reference is zero (hover)
    if reference_state is None:
        reference_state = np.zeros_like(initial_state)
    
    # Time vector
    time = np.arange(0, simulation_time, dt)
    num_steps = len(time)
    
    # Initialize arrays for storing results
    states = np.zeros((num_steps, len(initial_state)))
    inputs = np.zeros((num_steps, 4))  # [T, tau_x, tau_y, tau_z]
    reference = np.zeros((num_steps, len(initial_state)))
    error = np.zeros((num_steps, len(initial_state)))
    
    # Set initial state
    states[0] = initial_state
    
    # Parameters for nonlinear simulation
    params = {
        'Ixx': 0.0231,
        'Iyy': 0.0281,
        'Izz': 0.0356,
        'mass': 1.1,
        'g': 9.81
    }
    
    # Equilibrium hover thrust
    hover_thrust = params['mass'] * params['g']
    
    # Simulation loop
    for i in range(num_steps - 1):
        # Current state and time
        t = time[i]
        state = states[i]
        
        # Update reference if needed (e.g., for tracking a trajectory)
        reference[i] = reference_state
        
        # Compute control input using LQR
        lqr_input = lqr_control(state, reference[i], K)
        
        # Add hover thrust to the Z force (first input)
        u = np.copy(lqr_input)
        u[0] += hover_thrust
        
        # Ensure physical limits (simple saturation)
        u[0] = max(0, u[0])  # Thrust can't be negative
        
        # Store control input
        inputs[i] = u
        
        # Compute error
        error[i] = state - reference[i]
        
        # Integrate dynamics over one time step using linear model
        # state_next = state + dt * (A @ state + B @ u)
        
        # For more accurate simulation, use nonlinear dynamics
        sol = solve_ivp(
            lambda t, x: nonlinear_dynamics(t, x, u, params),
            [t, t + dt],
            state,
            method='RK45',
            t_eval=[t + dt]
        )
        
        if sol.success:
            states[i + 1] = sol.y[:, 0]
        else:
            logger.warning(f"Integration failed at time {t}")
            # Fall back to linear approximation
            states[i + 1] = state + dt * (A @ state + B @ u)
    
    # Compute control input for the last time step
    reference[-1] = reference_state
    lqr_input = lqr_control(states[-1], reference[-1], K)
    u = np.copy(lqr_input)
    u[0] += hover_thrust
    u[0] = max(0, u[0])
    inputs[-1] = u
    error[-1] = states[-1] - reference[-1]
    
    # Compile results
    result = {
        'time': time,
        'states': states,
        'inputs': inputs,
        'reference': reference,
        'error': error
    }
    
    return result

def simulate_with_disturbance(A, B, K, initial_state, simulation_time, dt, 
                            disturbance_time, disturbance_force):
    # Time vector
    time = np.arange(0, simulation_time, dt)
    num_steps = len(time)
    
    # Initialize arrays
    states = np.zeros((num_steps, len(initial_state)))
    inputs = np.zeros((num_steps, 4))
    reference = np.zeros((num_steps, len(initial_state)))
    error = np.zeros((num_steps, len(initial_state)))
    
    # Set initial state
    states[0] = initial_state
    
    # Parameters for nonlinear simulation
    params = {
        'Ixx': 0.0221,
        'Iyy': 0.0221,
        'Izz': 0.0366,
        'mass': 1.0,
        'g': 9.81
    }
    
    # Equilibrium hover thrust
    hover_thrust = params['mass'] * params['g']
    
    # Disturbance index
    dist_idx = int(disturbance_time / dt)
    
    # Simulation loop
    for i in range(num_steps - 1):
        # Current state and time
        t = time[i]
        state = states[i]
        
        # Update reference (zero for hover)
        reference[i] = np.zeros_like(state)
        
        # Compute control input
        lqr_input = lqr_control(state, reference[i], K)
        u = np.copy(lqr_input)
        u[0] += hover_thrust
        
        # Apply disturbance if at the right time
        if i == dist_idx:
            u += disturbance_force
            logger.info(f"Applying disturbance at t = {t}")
        
        # Store control input
        inputs[i] = u
        
        # Compute error
        error[i] = state - reference[i]
        
        # Integrate dynamics
        sol = solve_ivp(
            lambda t, x: nonlinear_dynamics(t, x, u, params),
            [t, t + dt],
            state,
            method='RK45',
            t_eval=[t + dt]
        )
        
        if sol.success:
            states[i + 1] = sol.y[:, 0]
        else:
            logger.warning(f"Integration failed at time {t}")
            states[i + 1] = state + dt * (A @ state + B @ u)
    
    # Compute values for the last time step
    reference[-1] = np.zeros_like(states[-1])
    lqr_input = lqr_control(states[-1], reference[-1], K)
    u = np.copy(lqr_input)
    u[0] += hover_thrust
    inputs[-1] = u
    error[-1] = states[-1] - reference[-1]
    
    # Compile results
    result = {
        'time': time,
        'states': states,
        'inputs': inputs,
        'reference': reference,
        'error': error
    }
    
    return result
