import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np
from pyquaternion import Quaternion

import serial
import struct
from threading import Thread
from matplotlib.animation import FuncAnimation

data_format_uart = fmt = "%df"%4
def plot_cube_quaternion(q, color):

    v = np.array([[ 1, 0, 0], [ -0.2, -1, -0.5],
                   [ -0.2, 1, -0.5],  [ 0,0,0], [ -0.2, 0, 0.3]]).transpose()

    v_rot = np.zeros((3,5))
    for i in range(5):
         v_rot[:,i] = q.rotate(v[:,i])

    v_rot = v_rot.transpose()
    verts = [ [v_rot[0],v_rot[1],v_rot[3]], [v_rot[0],v_rot[2],v_rot[3]], [v_rot[0],v_rot[3],v_rot[4]]]

    ax.add_collection3d(Poly3DCollection(verts, facecolors= color, linewidths=1, edgecolors='r', alpha=1))
    return


# def receive_quaternion():
#     ''' Receive quaternion from Serial connection '''
#     quat_values = [1, 0, 0, 0]
#     # read 16 bytes (4 floats)
#     quat_bytes = uart_mcu.read(16)
#     if len(quat_bytes) == 16:
#         # Use little-endian format for 4 floats
#         quat_values = list(struct.unpack('<4f', quat_bytes))  # Convert tuple to list
#         quat_values[1] *= -1
#     q = Quaternion(quat_values)
#     return q
def receive_quaternion():
    '''Receive comma-separated quaternion data (as text) from Serial connection'''
    quat_values = [1, 0, 0, 0]
    try:
        line = uart_mcu.readline().decode('utf-8').strip()  # read one line, decode, and strip newline
        if line:
            parts = line.split(',')  # split CSV text
            if len(parts) == 4:
                quat_values = [float(x) for x in parts]  # convert to floats
                # optional coordinate correction (like before)
                # quat_values[1] *= -1
    except Exception as e:
        print(f"Error reading quaternion: {e}")
    q = Quaternion(quat_values)
    return q




def plot_animation(i):
    ''' Animation function callback to plot the cube '''
    global q
    # clearing the figure
    ax.clear()
    ax.set_xlim(-1, 1)
    ax.set_ylim(1, -1)
    ax.set_zlim(-1, 1)
    ax.invert_zaxis()
    ax.invert_yaxis()
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")
    ax.set_zlabel("z label")
    # plot the cube
    plot_cube_quaternion(q, 'cyan')


def receive_data():
    ''' Thread function to receive data from Serial connection indefinitely '''
    global q
    while True:
        q = receive_quaternion()


if __name__ == "__main__":
    # Create figure and 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect("equal")
    # set axis limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    q = Quaternion(axis=[1, 0, 0], angle=np.pi/4)
    # # Create animation callback
    ani = FuncAnimation(fig, plot_animation, frames=100, interval=10, blit=False)
    
    # # uart comport
    uart_mcu = serial.Serial('/dev/ttyACM0', 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    uart_thread = Thread(target=receive_data, daemon=True)
    uart_thread.start()
    
    plt.show()
