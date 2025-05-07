import os
import logging
from flask import Flask, render_template, jsonify, request
import numpy as np
from simulation import run_simulation
from lqr_controller import design_lqr
from drone_model import linearize_model, get_state_space_matrices

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Default drone parameters
DEFAULT_PARAMS = {
    'Ixx': 0.0221, 
    'Iyy': 0.0221, 
    'Izz': 0.0366,
    'mass': 1.0,
    'g': 9.81,
    'simulation_time': 15,
    'dt': 0.01,
    'initial_state': np.zeros(12),
    'Q': np.diag([10, 10, 10, 1, 1, 1, 10, 10, 10, 1, 1, 1]),
    'R': np.diag([1, 1, 1, 1])
}

@app.route('/')
def index():
    """Render the main simulation page."""
    return render_template('index.html')

@app.route('/run_simulation', methods=['POST'])
def start_simulation():
    """Run the drone simulation with the provided parameters."""
    try:
        # Get parameters from request or use defaults
        data = request.json or {}
        params = DEFAULT_PARAMS.copy()
        
        # Update parameters if provided in request
        for key in params:
            if key in data:
                if key == 'initial_state':
                    params[key] = np.array(data[key])
                else:
                    params[key] = float(data[key]) if key != 'dt' else float(data[key])
        
        # Handle diagonal Q and R matrices if provided
        if 'Q_diag' in data:
            params['Q'] = np.diag(data['Q_diag'])
        if 'R_diag' in data:
            params['R'] = np.diag(data['R_diag'])
        
        # Create state space model
        A, B = get_state_space_matrices(
            params['Ixx'], params['Iyy'], params['Izz'], 
            params['mass'], params['g']
        )
        
        # Design LQR controller
        K = design_lqr(A, B, params['Q'], params['R'])
        
        # Run simulation
        result = run_simulation(
            A, B, K, 
            params['initial_state'], 
            params['simulation_time'], 
            params['dt']
        )
        
        # Format results for JSON response
        formatted_result = {
            'time': result['time'].tolist(),
            'states': result['states'].tolist(),
            'inputs': result['inputs'].tolist(),
            'reference': result['reference'].tolist(),
            'error': result['error'].tolist(),
            'K': K.tolist()
        }
        
        return jsonify({
            'success': True,
            'result': formatted_result
        })
    
    except Exception as e:
        logger.exception("Error in simulation")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
