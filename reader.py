import matplotlib.pyplot as plt
import numpy as np

def parser(filename):
    path = "/Users/nachiketbhanushali/Library/CloudStorage/GoogleDrive-nachi2904@gmail.com/My Drive/Summer 2024/VARIA Spectra/" + str(filename)
    with open(path, 'r') as file:
        lines = file.readlines()[1:]
    int_time = int(lines[0][9:-1])  # integration time in ms
    lines = lines[1:]
    parsed_data = lines
    for i in range(len(lines)):
        lines[i] = lines[i].strip().split(',')[0].split()
        parsed_data[i] = [float(s.strip()) for s in lines[i]]
    parsed_data.sort(key=lambda x: x[0])
    return int_time, parsed_data

def plotter(data, filename, scaled = False):
    if not scaled:
        x, y = zip(*data)
        plt.figure()
        plt.plot(x, y, label=filename, color='blue')
        plt.xlim(0, 1130)
        plt.ylim(-500, 65000)
        plt.xlabel(r'$\lambda$ (nm)')
        plt.ylabel('Counts')
        plt.grid(True)
        plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center')
        plt.tight_layout()
        plt.show()
    else:
        x, y = zip(*data)
        y_scaled = np.array(y)/max(y)
        plt.figure()
        plt.plot(x, y_scaled, label=filename, color='blue')
        plt.xlim(0, 1130)
        plt.ylim(-0.1, 1)
        plt.xlabel(r'$\lambda$ (nm)')
        plt.ylabel('Intensity (arb)')
        plt.grid(True)
        plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center')
        plt.tight_layout()
        plt.show()

def two_plotter(data1, data2, filename1, filename2, scaled = False):
    if not scaled:
        x1, y1 = zip(*data1)
        x2, y2 = zip(*data2)
        plt.figure()
        plt.plot(x1, y1, label=filename1, color='blue')
        plt.plot(x2, y2, label=filename2, color='red')
        plt.xlim(0, 1130)
        plt.ylim(-500, 65000)
        plt.xlabel(r'$\lambda$ (nm)')
        plt.ylabel('Counts')
        plt.grid(True)
        plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center')
        plt.tight_layout()
        plt.show()
    else:
        x1, y1 = zip(*data1)
        x2, y2 = zip(*data2)
        y1_scaled = np.array(y1) / max(y1)
        y2_scaled = np.array(y2) / max(y2)
        plt.figure()
        plt.plot(x1, y1_scaled, label=filename1, color='blue')
        plt.plot(x2, y2_scaled, label=filename2, color='red')
        plt.xlim(0, 1130)
        plt.ylim(-0.1, 1)
        plt.xlabel(r'$\lambda$ (nm)')
        plt.ylabel('Intensity (arb)')
        plt.grid(True)
        plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center')
        plt.tight_layout()
        plt.show()

file1 = "20_8_24_VARIA_100P_532_100_NOVA_Spec_OD4_Before_2.SSM"
time1, data1 = parser(file1)

file2 = "20_8_24_VARIA_100P_532_100_NOVA_Spec_OD3_After.SSM"
time2, data2 = parser(file2)

two_plotter(data1, data2, file1, file2, scaled = True)

"""
x1, y1 = zip(*data1)
x2, y2 = zip(*data2)

# Create the plot
plt.figure()

# Plot the data
plt.plot(x1, y1, label='filename1', color='blue')
plt.plot(x2, y2, label='filename2', color='red')

# Set plot range (x and y limits)
plt.xlim(190, 1130)
plt.ylim(-200, 65000)

# Add labels
plt.xlabel(r'$\lambda$ (nm)')
plt.ylabel('Counts')

# Add grid lines
plt.grid(True)

# Add legend
plt.legend()

# Show the plot
plt.show()
"""
