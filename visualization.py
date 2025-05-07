import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import logging

logger = logging.getLogger(__name__)

def plot_trajectory(time, states, inputs, reference=None, error=None, save_path=None):
    # Create figure
    fig = plt.figure(figsize=(15, 10))
    
    # Plot position
    ax1 = fig.add_subplot(3, 3, 1)
    ax1.plot(time, states[:, 0], 'b-', label='x')
    ax1.plot(time, states[:, 1], 'g-', label='y')
    ax1.plot(time, states[:, 2], 'r-', label='z')
    if reference is not None:
        ax1.plot(time, reference[:, 0], 'b--', alpha=0.5)
        ax1.plot(time, reference[:, 1], 'g--', alpha=0.5)
        ax1.plot(time, reference[:, 2], 'r--', alpha=0.5)
    ax1.set_title('Position')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Position (m)')
    ax1.legend()
    ax1.grid(True)
    
    # Plot linear velocity
    ax2 = fig.add_subplot(3, 3, 2)
    ax2.plot(time, states[:, 3], 'b-', label='u')
    ax2.plot(time, states[:, 4], 'g-', label='v')
    ax2.plot(time, states[:, 5], 'r-', label='w')
    ax2.set_title('Linear Velocity')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.legend()
    ax2.grid(True)
    
    # Plot orientation
    ax3 = fig.add_subplot(3, 3, 3)
    ax3.plot(time, np.rad2deg(states[:, 6]), 'b-', label='φ (roll)')
    ax3.plot(time, np.rad2deg(states[:, 7]), 'g-', label='θ (pitch)')
    ax3.plot(time, np.rad2deg(states[:, 8]), 'r-', label='ψ (yaw)')
    if reference is not None:
        ax3.plot(time, np.rad2deg(reference[:, 6]), 'b--', alpha=0.5)
        ax3.plot(time, np.rad2deg(reference[:, 7]), 'g--', alpha=0.5)
        ax3.plot(time, np.rad2deg(reference[:, 8]), 'r--', alpha=0.5)
    ax3.set_title('Orientation')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Angle (deg)')
    ax3.legend()
    ax3.grid(True)
    
    # Plot angular velocity
    ax4 = fig.add_subplot(3, 3, 4)
    ax4.plot(time, np.rad2deg(states[:, 9]), 'b-', label='p')
    ax4.plot(time, np.rad2deg(states[:, 10]), 'g-', label='q')
    ax4.plot(time, np.rad2deg(states[:, 11]), 'r-', label='r')
    ax4.set_title('Angular Velocity')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Angular Velocity (deg/s)')
    ax4.legend()
    ax4.grid(True)
    
    # Plot control inputs
    ax5 = fig.add_subplot(3, 3, 5)
    ax5.plot(time, inputs[:, 0], 'b-', label='Thrust')
    ax5.set_title('Thrust')
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('Force (N)')
    ax5.legend()
    ax5.grid(True)
    
    ax6 = fig.add_subplot(3, 3, 6)
    ax6.plot(time, inputs[:, 1], 'b-', label='τx')
    ax6.plot(time, inputs[:, 2], 'g-', label='τy')
    ax6.plot(time, inputs[:, 3], 'r-', label='τz')
    ax6.set_title('Moments')
    ax6.set_xlabel('Time (s)')
    ax6.set_ylabel('Moment (N·m)')
    ax6.legend()
    ax6.grid(True)
    
    # Plot 3D trajectory
    ax7 = fig.add_subplot(3, 3, 7, projection='3d')
    ax7.plot(states[:, 0], states[:, 1], states[:, 2], 'b-')
    ax7.set_title('3D Trajectory')
    ax7.set_xlabel('X (m)')
    ax7.set_ylabel('Y (m)')
    ax7.set_zlabel('Z (m)')
    ax7.grid(True)
    
    # Plot error if provided
    if error is not None:
        ax8 = fig.add_subplot(3, 3, 8)
        ax8.plot(time, error[:, 0], 'b-', label='x error')
        ax8.plot(time, error[:, 1], 'g-', label='y error')
        ax8.plot(time, error[:, 2], 'r-', label='z error')
        ax8.set_title('Position Error')
        ax8.set_xlabel('Time (s)')
        ax8.set_ylabel('Error (m)')
        ax8.legend()
        ax8.grid(True)
        
        ax9 = fig.add_subplot(3, 3, 9)
        ax9.plot(time, np.rad2deg(error[:, 6]), 'b-', label='φ error')
        ax9.plot(time, np.rad2deg(error[:, 7]), 'g-', label='θ error')
        ax9.plot(time, np.rad2deg(error[:, 8]), 'r-', label='ψ error')
        ax9.set_title('Orientation Error')
        ax9.set_xlabel('Time (s)')
        ax9.set_ylabel('Error (deg)')
        ax9.legend()
        ax9.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        logger.info(f"Plot saved to {save_path}")
    
    return fig

def create_animation(time, states):
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Drone visualization properties
    body_size = 0.3
    arm_length = 0.4
    
    # Initialize drone representation
    body = ax.plot([], [], [], 'bo', markersize=10)[0]
    arms = [ax.plot([], [], [], 'r-', linewidth=2)[0] for _ in range(4)]
    trail = ax.plot([], [], [], 'b-', alpha=0.3)[0]
    
    # Set axis limits
    min_x, max_x = np.min(states[:, 0]) - 1, np.max(states[:, 0]) + 1
    min_y, max_y = np.min(states[:, 1]) - 1, np.max(states[:, 1]) + 1
    min_z, max_z = np.min(states[:, 2]) - 1, np.max(states[:, 2]) + 1
    
    ax.set_xlim([min_x, max_x])
    ax.set_ylim([min_y, max_y])
    ax.set_zlim([min_z, max_z])
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Drone Trajectory')
    
    # Animation update function
    def update(i):
        i = min(i, len(time) - 1)  # Ensure i doesn't exceed array length
        
        # Current state
        x, y, z = states[i, 0:3]
        phi, theta, psi = states[i, 6:9]
        
        # Rotation matrix from body to inertial frame
        c_phi, s_phi = np.cos(phi), np.sin(phi)
        c_theta, s_theta = np.cos(theta), np.sin(theta)
        c_psi, s_psi = np.cos(psi), np.sin(psi)
        
        R = np.array([
            [c_theta * c_psi, c_theta * s_psi, -s_theta],
            [s_phi * s_theta * c_psi - c_phi * s_psi, s_phi * s_theta * s_psi + c_phi * c_psi, s_phi * c_theta],
            [c_phi * s_theta * c_psi + s_phi * s_psi, c_phi * s_theta * s_psi - s_phi * c_psi, c_phi * c_theta]
        ])
        
        # Drone arms in body frame
        arm_vectors_body = np.array([
            [arm_length, 0, 0],
            [0, arm_length, 0],
            [-arm_length, 0, 0],
            [0, -arm_length, 0]
        ])
        
        # Transform arms to inertial frame
        arm_vectors_inertial = np.array([R @ arm for arm in arm_vectors_body])
        
        # Update drone visualization
        body.set_data([x], [y])
        body.set_3d_properties([z])
        
        for j, arm in enumerate(arms):
            arm_end = [x, y, z] + arm_vectors_inertial[j]
            arm.set_data([x, arm_end[0]], [y, arm_end[1]])
            arm.set_3d_properties([z, arm_end[2]])
        
        # Update trail
        trail.set_data(states[:i+1, 0], states[:i+1, 1])
        trail.set_3d_properties(states[:i+1, 2])
        
        return [body] + arms + [trail]
    
    # Create animation
    anim = animation.FuncAnimation(
        fig, update, frames=len(time),
        interval=int(1000 * (time[1] - time[0])),
        blit=True
    )
    
    return anim, fig
