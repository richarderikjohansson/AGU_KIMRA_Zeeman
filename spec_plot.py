import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# --- functions ---
def read_hdf5(filename):
    """
    Function to read hdf5 files

    Parameters:
    filename (str) : path to the file

    Returns:
    dictionary (dict): A dictionary with the data 
    """

    with h5py.File(filename,"r") as file:

        if "kimra_data" in file.keys():
            dataset = file["kimra_data"]

        else:
            dataset = file

        dictionary = dict()
        for key in dataset.keys(): #pyright:ignore
            try: 
                dictionary[key] = dataset[key][:] #pyright:ignore
            except ValueError:
                dictionary[key] = dataset[key][()] #pyright:ignore 

        return dictionary

def mm_scaler(data):

    """
    A min max scaler function to scale the normalize the measurements so
    their features can be distinguished and compared

    Parameters:
    data (np.array) : The spectra to be normalzed

    Returns:

    (np.array) : The normalized spectra

    """

    minval = min(data)
    maxval = max(data)

    norm_data = (data-minval)/(maxval - minval)
    return norm_data

def get_bound(data,f0):
    """
    Function to get start end end index from frequency where the bandwith is 30 MHz 
    and from a line center

    Parameters:
    data (np.array) : Frequency vector
    f0 (float) : Line center

    Returns:
    s (int) : Start index of slice
    s (int) : End index of slice
    """
    
    f = data - f0
    s = np.where(f > -1.5e7)[0][0]
    e = np.where(f > 1.5e7)[0][0]

    return s,e


# --- driver code ---

f0 = 233.9461e9 # linecenter
s = 4635 # index where frequency is -15 MHz from linecenter
e = 5028 # index where frequency is 15 MHz from linecenter

# list comprehensions to read all data
simulations = [read_hdf5("data/simulation/"+file) for file in sorted(os.listdir("data/simulation"))]
measurements = [read_hdf5("data/measurements/"+file) for file in sorted(os.listdir("data/measurements"))]

# subplots all directions
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2, figsize=(15,9), sharey=True, sharex=True)

# phi = 0
ax1.plot((measurements[0]["f"][s:e]-f0)/1e6, mm_scaler(measurements[0]["y"][s:e]), label="Measurement", color="black")
ax1.plot(simulations[0]["f"], mm_scaler(simulations[0]["I"]+simulations[0]["Q"]), label="Simulation (I+Q)", color="red")
ax1.legend(loc="best", fontsize=12, frameon=True, bbox_to_anchor=(0.97,0.95))
ax1.set_ylabel(r"$T_B$"+" (Normalized)", fontsize=16)
ax1.tick_params(axis="both", labelsize=13)
ax1.minorticks_on()
ax1.grid(which='major', color='black', linestyle='-', linewidth=0.75, alpha=.2)
ax1.grid(which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=.2)
ax1.text(0.10,0.90, r"$(a)$", transform=ax1.transAxes,fontsize=17,color="black", verticalalignment="top")

# phi = 180
ax2.plot((measurements[1]["f"][s:e]-f0)/1e6, mm_scaler(measurements[1]["y"][s:e]), label="Measurement", color="black")
ax2.plot(simulations[1]["f"], mm_scaler(simulations[1]["I"]+simulations[1]["Q"]), label="Simulation (I+Q)", color="red")
ax2.legend(loc="best", fontsize=12, frameon=True, bbox_to_anchor=(0.97,0.95))
ax2.tick_params(axis="both", labelsize=13)
ax2.minorticks_on()
ax2.grid(which='major', color='black', linestyle='-', linewidth=0.75, alpha=.2)
ax2.grid(which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=.2)
ax2.text(0.10,0.90, r"$(b)$", transform=ax2.transAxes,fontsize=17,color="black", verticalalignment="top")

# phi = 90
ax3.plot((measurements[2]["f"][s:e]-f0)/1e6, mm_scaler(measurements[2]["y"][s:e]), label="Measurement", color="black")
ax3.plot(simulations[3]["f"], mm_scaler(simulations[3]["I"]-simulations[3]["Q"]), label="Simulation (I-Q)", color="red")
ax3.legend(loc="best", fontsize=12, frameon=True, bbox_to_anchor=(0.97,0.95))
ax3.set_xlabel(r"$\nu - \nu_0$ [MHz]", fontsize=16)
ax3.set_ylabel(r"$T_B$"+" (Normalized)", fontsize=16)
ax3.tick_params(axis="both", labelsize=13)
ax3.minorticks_on()
ax3.grid(which='major', color='black', linestyle='-', linewidth=0.75, alpha=.2)
ax3.grid(which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=.2)
ax3.text(0.10,0.90, r"$(c)$", transform=ax3.transAxes,fontsize=17,color="black", verticalalignment="top")

# phi = 270
ax4.plot((measurements[3]["f"][s:e]-f0)/1e6, mm_scaler(measurements[3]["y"][s:e]), label="Measurement", color="black")
ax4.plot(simulations[2]["f"], mm_scaler(simulations[2]["I"]-simulations[2]["Q"]), label="Simulation (I-Q)", color="red")
ax4.legend(loc="best", fontsize=12, frameon=True, bbox_to_anchor=(0.97,0.95))
ax4.set_xlabel(r"$\nu - \nu_0$ [MHz]", fontsize=16)
ax4.tick_params(axis="both", labelsize=13)
ax4.minorticks_on()
ax4.grid(which='major', color='black', linestyle='-', linewidth=0.75, alpha=.2)
ax4.grid(which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=.2)
ax4.text(0.10,0.90, r"$(d)$", transform=ax4.transAxes,fontsize=17,color="black", verticalalignment="top")
plt.tight_layout()

fig.savefig("imgs/allsubs.pdf")


# full spectrum plot
freq = measurements[2]["f"][20::]
spec = measurements[2]["y"][20::]
s,e = get_bound(data=freq, f0=f0)

xmin, xmax, ymin, ymax = freq[s]/1e9, freq[e]/1e9, 120, 134
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(freq/1e9,spec, color="black")
ax.tick_params(axis="both", labelsize=13)
ax.set_xlabel(r"$\nu$ [GHz]", fontsize=16)
ax.set_ylabel(f"$T_B$ [K]", fontsize=16)

inset_ax = inset_axes(ax, width="30%", height="50%", loc="center")
inset_ax.plot(freq/1e9, spec, color="black")
inset_ax.set_xlim(xmin, xmax)
inset_ax.set_ylim(ymin, ymax)
inset_ax.set_title(r"Zeeman affected transition of $^{16}O^{18}O$", fontsize=12)
# Mark the zoomed area on the main plot
inset_ax.set_xticks([])
inset_ax.set_yticks([])
inset_ax.tick_params(left=False, bottom=False)  # Hide tick marks
#inset_ax.set_ticks_position('none')  # Remove tick lines

mark_inset(ax, inset_ax, loc1=2, loc2=3, fc="none", ec="0.5")
plt.tight_layout()

fig.savefig("imgs/full_spec.pdf")
