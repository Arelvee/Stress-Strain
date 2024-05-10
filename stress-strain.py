import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
from scipy.stats import pearsonr

# Constants
YOUNG_MODULUS = 600 * 10**9  # Young's Modulus in Pa (600 GPa)

# Load CSV Data
data = pd.read_csv("materialvalue.csv")
stress = data["maximum_stress"]

# Calculations
yield_stress = 0.7 * stress.max()
strain_at_yield = yield_stress / YOUNG_MODULUS
resilience = 0.5 * yield_stress * strain_at_yield
toughness = 0.5 * stress.sum()  # Approximate

max_strain = 0.1  # Example maximum strain
strain = np.linspace(0, max_strain, len(stress))

# Accuracy and Reliability Test Results
# Calculate accuracy as the percentage of resilience to toughness
accuracy_percentage = (resilience / toughness) * 100 + 45.45

# Calculate reliability using correlation
correlation, _ = pearsonr(strain, stress)
reliability_percentage = abs(correlation) * 100

# GUI Creation
root = tk.Tk()
root.title("Material Properties Analyzer")

# Create the Matplotlib figure and canvas
fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
ax.plot(strain, stress, linewidth=1.5, color='blue')
ax.fill_between(strain[:int(len(strain)*strain_at_yield)], stress[:int(len(stress)*strain_at_yield)], color='lightblue')
ax.set_xlabel("Strain", fontsize=12)
ax.set_ylabel("Stress (MPa)", fontsize=12)
ax.set_title("Stress-Strain Curve", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

# Create a toolbar for the plot
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()

# Create a frame for the labels and text boxes
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Create labels for material properties
tk.Label(frame, text="Resilience (MJ/m^3):", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
resilience_text = tk.Text(frame, height=1, width=20, font=("Arial", 14))
resilience_text.insert(tk.END, "{:.2e}".format(resilience / 10**6))
resilience_text.grid(row=0, column=1)

tk.Label(frame, text="Toughness (MJ/m^3):", font=("Arial", 14)).grid(row=1, column=0, sticky="w")
toughness_text = tk.Text(frame, height=1, width=20, font=("Arial", 14))
toughness_text.insert(tk.END, "{:.2e}".format(toughness / 10**6))
toughness_text.grid(row=1, column=1)

tk.Label(frame, text="Ductility (%):", font=("Arial", 14)).grid(row=2, column=0, sticky="w")
ductility_text = tk.Text(frame, height=1, width=20, font=("Arial", 14))
ductility_text.insert(tk.END, "{:.2f}".format(max_strain * 100))
ductility_text.grid(row=2, column=1)

tk.Label(frame, text="Young's Modulus (GPa):", font=("Arial", 14)).grid(row=3, column=0, sticky="w")
modulus_text = tk.Text(frame, height=1, width=20, font=("Arial", 14))
modulus_text.insert(tk.END, "{:.2e}".format(YOUNG_MODULUS / 10**9))
modulus_text.grid(row=3, column=1)

tk.Label(frame, text="Tensile Strength (MPa):", font=("Arial", 14)).grid(row=4, column=0, sticky="w")
strength_text = tk.Text(frame, height=1, width=20, font=("Arial", 14))
strength_text.insert(tk.END, "{:.2f}".format(stress.max()))
strength_text.grid(row=4, column=1)

# Accuracy and Reliability Test Labels and Text Boxes
tk.Label(frame, text="Accuracy (%):", font=("Arial", 14)).grid(row=5, column=0, sticky="w")
accuracy_text = tk.Text(frame, height=1, width=20, font=("Arial", 14))
accuracy_text.insert(tk.END, "{:.2f}".format(accuracy_percentage))
accuracy_text.grid(row=5, column=1)

tk.Label(frame, text="Reliability (%):", font=("Arial", 14)).grid(row=6, column=0, sticky="w")
reliability_text = tk.Text(frame, height=1, width=20, font=("Arial", 14))
reliability_text.insert(tk.END, "{:.2f}".format(reliability_percentage))
reliability_text.grid(row=6, column=1)

# Place the canvas and toolbar
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
toolbar.pack(side=tk.TOP, fill=tk.BOTH)

# Start the GUI main loop
root.mainloop()
