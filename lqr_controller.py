import numpy as np
import scipy.linalg as la
import logging

logger = logging.getLogger(__name__)

def design_lqr(A, B, Q, R):
    # Check if the system is controllable
    if not is_controllable(A, B):
        logger.warning("System is not controllable!")
    
    # Solve the Riccati equation
    try:
        P = la.solve_continuous_are(A, B, Q, R)
        
        # Calculate the LQR gain matrix
        K = np.linalg.inv(R) @ B.T @ P
        
        logger.info(f"LQR design successful. K shape: {K.shape}")
        return K
    
    except Exception as e:
        logger.error(f"Error in LQR design: {e}")
        raise

def is_controllable(A, B):
    n = A.shape[0]  # System order
    
    # Build the controllability matrix
    C = B.copy()
    A_power = np.eye(n)
    
    for i in range(1, n):
        A_power = A_power @ A
        C = np.hstack((C, A_power @ B))
    
    # Check the rank of the controllability matrix
    rank = np.linalg.matrix_rank(C)
    
    return rank == n

def lqr_control(state, reference, K):
    # Compute the error between current state and reference
    error = state - reference
    
    # Compute the control input
    u = -K @ error
    
    return u
