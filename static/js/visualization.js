// Chart objects
let positionChart = null;
let orientationChart = null;
let controlChart = null;
let errorChart = null;
let trajectory3DChart = null;

// Simulation data
let simulationData = null;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Set up form submission
    const form = document.getElementById('simulationForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        runSimulation();
    });
    
    // Initialize empty charts
    initializeCharts();
});

// Function to initialize empty charts
function initializeCharts() {
    // Position chart
    const positionCtx = document.getElementById('positionChart').getContext('2d');
    positionChart = new Chart(positionCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'X Position (m)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Y Position (m)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Z Position (m)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Drone Position'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time (s)'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Position (m)'
                    }
                }
            }
        }
    });
    
    // Orientation chart
    const orientationCtx = document.getElementById('orientationChart').getContext('2d');
    orientationChart = new Chart(orientationCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Roll φ (deg)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Pitch θ (deg)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Yaw ψ (deg)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Drone Orientation'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time (s)'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Angle (deg)'
                    }
                }
            }
        }
    });
    
    // Control chart
    const controlCtx = document.getElementById('controlChart').getContext('2d');
    controlChart = new Chart(controlCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Thrust (N)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'τx (N·m)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'τy (N·m)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'τz (N·m)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Control Inputs'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time (s)'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Control Input'
                    }
                }
            }
        }
    });
    
    // Error chart
    const errorCtx = document.getElementById('errorChart').getContext('2d');
    errorChart = new Chart(errorCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Position Error (m)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Orientation Error (deg)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    data: [],
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Error Metrics'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time (s)'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Error'
                    }
                }
            }
        }
    });
    
    // 3D Trajectory (just a placeholder, we'll use a scatter chart to represent it)
    const trajectory3DCtx = document.getElementById('trajectory3D').getContext('2d');
    trajectory3DChart = new Chart(trajectory3DCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Drone Trajectory',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.5)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Drone Trajectory (X-Y Projection)'
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'X Position (m)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Y Position (m)'
                    }
                }
            }
        }
    });
}

// Function to run the simulation
function runSimulation() {
    // Show loading indicator
    document.getElementById('simulationInfo').innerText = 'Running simulation...';
    
    // Collect parameters from the form
    const params = {
        Ixx: parseFloat(document.getElementById('Ixx').value),
        Iyy: parseFloat(document.getElementById('Iyy').value),
        Izz: parseFloat(document.getElementById('Izz').value),
        mass: parseFloat(document.getElementById('mass').value),
        g: 9.81,
        simulation_time: parseFloat(document.getElementById('simulationTime').value),
        dt: parseFloat(document.getElementById('dt').value),
        initial_state: [
            parseFloat(document.getElementById('initial_x').value),
            parseFloat(document.getElementById('initial_y').value),
            parseFloat(document.getElementById('initial_z').value),
            0, 0, 0, // Initial velocities
            deg2rad(parseFloat(document.getElementById('initial_phi').value)),
            deg2rad(parseFloat(document.getElementById('initial_theta').value)),
            deg2rad(parseFloat(document.getElementById('initial_psi').value)),
            0, 0, 0  // Initial angular rates
        ],
        // Get Q matrix values from the form or use defaults
        Q_diag: [
            parseFloat(document.getElementById('q_x').value || 10),
            parseFloat(document.getElementById('q_y').value || 10),
            parseFloat(document.getElementById('q_z').value || 10),
            parseFloat(document.getElementById('q_u').value || 1),
            parseFloat(document.getElementById('q_v').value || 1),
            parseFloat(document.getElementById('q_w').value || 1),
            parseFloat(document.getElementById('q_phi').value || 10),
            parseFloat(document.getElementById('q_theta').value || 10),
            parseFloat(document.getElementById('q_psi').value || 10),
            parseFloat(document.getElementById('q_p').value || 1),
            parseFloat(document.getElementById('q_q').value || 1),
            parseFloat(document.getElementById('q_r').value || 1)
        ],
        // Get R matrix values from the form or use defaults
        R_diag: [
            parseFloat(document.getElementById('r_thrust').value || 1),
            parseFloat(document.getElementById('r_taux').value || 1),
            parseFloat(document.getElementById('r_tauy').value || 1),
            parseFloat(document.getElementById('r_tauz').value || 1)
        ]
    };
    
    // Send request to the server
    fetch('/run_simulation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Save simulation data
            simulationData = data.result;
            
            // Update charts
            updateCharts(simulationData);
            
            // Display performance metrics
            displayMetrics(simulationData);
            
            // Update info
            document.getElementById('simulationInfo').innerText = 'Simulation completed successfully';
        } else {
            document.getElementById('simulationInfo').innerText = 'Error: ' + data.error;
            console.error('Simulation error:', data.error);
        }
    })
    .catch(error => {
        document.getElementById('simulationInfo').innerText = 'Error: ' + error;
        console.error('Fetch error:', error);
    });
}

// Function to update all charts with simulation data
function updateCharts(data) {
    // Extract data
    const time = data.time;
    const states = data.states;
    const inputs = data.inputs;
    const error = data.error;
    
    // Calculate position error norm and orientation error norm
    const positionErrorNorm = [];
    const orientationErrorNorm = [];
    
    for (let i = 0; i < error.length; i++) {
        // Position error (x, y, z)
        const posErr = Math.sqrt(
            error[i][0]**2 + 
            error[i][1]**2 + 
            error[i][2]**2
        );
        
        // Orientation error (phi, theta, psi)
        const oriErr = Math.sqrt(
            error[i][6]**2 + 
            error[i][7]**2 + 
            error[i][8]**2
        ) * (180 / Math.PI); // Convert to degrees
        
        positionErrorNorm.push(posErr);
        orientationErrorNorm.push(oriErr);
    }
    
    // Update position chart
    positionChart.data.labels = time;
    positionChart.data.datasets[0].data = states.map(state => state[0]);
    positionChart.data.datasets[1].data = states.map(state => state[1]);
    positionChart.data.datasets[2].data = states.map(state => state[2]);
    positionChart.update();
    
    // Update orientation chart (convert radians to degrees)
    orientationChart.data.labels = time;
    orientationChart.data.datasets[0].data = states.map(state => state[6] * (180 / Math.PI));
    orientationChart.data.datasets[1].data = states.map(state => state[7] * (180 / Math.PI));
    orientationChart.data.datasets[2].data = states.map(state => state[8] * (180 / Math.PI));
    orientationChart.update();
    
    // Update control chart
    controlChart.data.labels = time;
    controlChart.data.datasets[0].data = inputs.map(input => input[0]);
    controlChart.data.datasets[1].data = inputs.map(input => input[1]);
    controlChart.data.datasets[2].data = inputs.map(input => input[2]);
    controlChart.data.datasets[3].data = inputs.map(input => input[3]);
    controlChart.update();
    
    // Update error chart
    errorChart.data.labels = time;
    errorChart.data.datasets[0].data = positionErrorNorm;
    errorChart.data.datasets[1].data = orientationErrorNorm;
    errorChart.update();
    
    // Update 3D trajectory (as X-Y projection for simplicity)
    const trajectoryData = [];
    for (let i = 0; i < states.length; i++) {
        trajectoryData.push({
            x: states[i][0],
            y: states[i][1]
        });
    }
    
    trajectory3DChart.data.datasets[0].data = trajectoryData;
    trajectory3DChart.update();
}

// Function to display performance metrics
function displayMetrics(data) {
    // Extract data
    const time = data.time;
    const states = data.states;
    const error = data.error;
    const K = data.K;
    
    // Calculate position error norm
    const positionErrorNorm = [];
    for (let i = 0; i < error.length; i++) {
        const posErr = Math.sqrt(
            error[i][0]**2 + 
            error[i][1]**2 + 
            error[i][2]**2
        );
        positionErrorNorm.push(posErr);
    }
    
    // Settling time (time to reach within 2% of final value)
    const maxError = Math.max(...positionErrorNorm);
    const threshold = 0.02 * maxError;
    let settlingTime = "N/A";
    
    for (let i = 0; i < positionErrorNorm.length; i++) {
        if (positionErrorNorm[i] <= threshold) {
            settlingTime = time[i].toFixed(2);
            break;
        }
    }
    
    // Maximum position error
    const maxPositionError = maxError.toFixed(4);
    
    // RMS error
    const rmsePosition = Math.sqrt(
        positionErrorNorm.reduce((sum, error) => sum + error * error, 0) / positionErrorNorm.length
    ).toFixed(4);
    
    // Create metrics HTML
    const metricsHTML = `
        <table class="table table-sm">
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Settling Time</td>
                <td>${settlingTime} s</td>
            </tr>
            <tr>
                <td>Max Position Error</td>
                <td>${maxPositionError} m</td>
            </tr>
            <tr>
                <td>RMSE Position</td>
                <td>${rmsePosition} m</td>
            </tr>
            <tr>
                <td>LQR Controller K</td>
                <td><button class="btn btn-sm btn-outline-info" onclick="showKMatrix()">View Matrix</button></td>
            </tr>
        </table>
    `;
    
    document.getElementById('metrics-container').innerHTML = metricsHTML;
}

// Function to show the K matrix
function showKMatrix() {
    if (!simulationData || !simulationData.K) {
        alert("No K matrix data available");
        return;
    }
    
    const K = simulationData.K;
    let matrixHTML = '<div class="table-responsive"><table class="table table-sm table-bordered">';
    
    // Add header
    matrixHTML += '<thead><tr><th></th>';
    for (let i = 0; i < K[0].length; i++) {
        matrixHTML += `<th>x${i+1}</th>`;
    }
    matrixHTML += '</tr></thead><tbody>';
    
    // Add rows
    for (let i = 0; i < K.length; i++) {
        matrixHTML += `<tr><th>u${i+1}</th>`;
        for (let j = 0; j < K[i].length; j++) {
            matrixHTML += `<td>${K[i][j].toFixed(4)}</td>`;
        }
        matrixHTML += '</tr>';
    }
    
    matrixHTML += '</tbody></table></div>';
    
    // Create modal to display the matrix
    const modalHTML = `
        <div class="modal fade" id="kMatrixModal" tabindex="-1" aria-labelledby="kMatrixModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="kMatrixModalLabel">LQR Gain Matrix (K)</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        ${matrixHTML}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to the page
    const modalContainer = document.createElement('div');
    modalContainer.innerHTML = modalHTML;
    document.body.appendChild(modalContainer);
    
    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('kMatrixModal'));
    modal.show();
    
    // Remove the modal from the DOM when hidden
    document.getElementById('kMatrixModal').addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modalContainer);
    });
}

// Helper function to convert degrees to radians
function deg2rad(degrees) {
    return degrees * (Math.PI / 180);
}

// Function to load preset configurations for Q and R matrices
function loadPreset(preset) {
    // Default preset (balanced)
    let qValues = {
        x: 10, y: 10, z: 10,
        u: 1, v: 1, w: 1,
        phi: 10, theta: 10, psi: 10,
        p: 1, q: 1, r: 1
    };
    
    let rValues = {
        thrust: 1,
        taux: 1,
        tauy: 1,
        tauz: 1
    };
    
    // Configure values based on preset
    switch(preset) {
        case 'aggressive':
            // Higher position and orientation weights, lower control costs
            qValues = {
                x: 20, y: 20, z: 20,
                u: 2, v: 2, w: 2,
                phi: 20, theta: 20, psi: 20,
                p: 2, q: 2, r: 2
            };
            rValues = {
                thrust: 0.5,
                taux: 0.5,
                tauy: 0.5,
                tauz: 0.5
            };
            break;
            
        case 'smooth':
            // Lower position and orientation weights, higher control costs
            qValues = {
                x: 5, y: 5, z: 5,
                u: 0.5, v: 0.5, w: 0.5,
                phi: 5, theta: 5, psi: 5,
                p: 0.5, q: 0.5, r: 0.5
            };
            rValues = {
                thrust: 2,
                taux: 2,
                tauy: 2,
                tauz: 2
            };
            break;
            
        case 'position':
            // Higher position weights than orientation
            qValues = {
                x: 20, y: 20, z: 20,
                u: 2, v: 2, w: 2,
                phi: 5, theta: 5, psi: 5,
                p: 0.5, q: 0.5, r: 0.5
            };
            rValues = {
                thrust: 1,
                taux: 1,
                tauy: 1,
                tauz: 1
            };
            break;
            
        case 'orientation':
            // Higher orientation weights than position
            qValues = {
                x: 5, y: 5, z: 5,
                u: 0.5, v: 0.5, w: 0.5,
                phi: 20, theta: 20, psi: 20,
                p: 2, q: 2, r: 2
            };
            rValues = {
                thrust: 1,
                taux: 1,
                tauy: 1,
                tauz: 1
            };
            break;
            
        case 'default':
        default:
            // Use the default values defined above
            break;
    }
    
    // Update form inputs with the selected values
    document.getElementById('q_x').value = qValues.x;
    document.getElementById('q_y').value = qValues.y;
    document.getElementById('q_z').value = qValues.z;
    document.getElementById('q_u').value = qValues.u;
    document.getElementById('q_v').value = qValues.v;
    document.getElementById('q_w').value = qValues.w;
    document.getElementById('q_phi').value = qValues.phi;
    document.getElementById('q_theta').value = qValues.theta;
    document.getElementById('q_psi').value = qValues.psi;
    document.getElementById('q_p').value = qValues.p;
    document.getElementById('q_q').value = qValues.q;
    document.getElementById('q_r').value = qValues.r;
    
    document.getElementById('r_thrust').value = rValues.thrust;
    document.getElementById('r_taux').value = rValues.taux;
    document.getElementById('r_tauy').value = rValues.tauy;
    document.getElementById('r_tauz').value = rValues.tauz;
}
