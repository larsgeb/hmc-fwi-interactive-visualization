import math
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pandas as pd

# Data location relative to execution location (modify if needed)
folder = "data"
rawSamples = np.load(folder + "/Chain A - thinned 0.5.npy")
sources = np.loadtxt(folder + "/setup/sources.txt")
receivers = np.loadtxt(folder + "/setup/receivers.txt")
if sources.shape == (2,):
    sources = np.expand_dims(sources, axis=0)
if receivers.shape == (2,):
    receivers = np.expand_dims(receivers, axis=0)

# Plotting parameters
plt.rcParams["font.weight"] = "medium"
plt.rcParams["font.size"] = 16


def drawGrid(xstart, xend, zstart, zend, xint=10.0, zint=10.0):
    # Method to draw a regular grid in the current axis.
    for i in np.arange(xstart, xend + 1, xint):
        plt.plot([i, i], [zstart, zend], color="black", alpha=0.1)
    for j in np.arange(zstart, zend + 1, zint):
        plt.plot([xstart, xend], [j, j], color="black", alpha=0.1)


def plotInModel(
    field,
    vmin,
    vmax,
    plotTitle=None,
    colorBarTitle=None,
    cmap=plt.get_cmap("seismic"),
    imAxis=None,  # defaults to matplotlib.pyplot.gca()
    plotAcqGeom=True,
    plotGrid=True,
):
    # Method to plot a 2D field in the acquisition geometry
    if imAxis is None:
        imAxis = plt.gca()
    im = imAxis.imshow(
        field,
        extent=(25 * dx, 75 * dx, 25 * dx, 75 * dx),
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
    )
    imAxis.set_xlim([0, 100 * dx])
    imAxis.set_ylim([0, 100 * dx])
    imAxis.set_xlabel("x [m]")
    imAxis.set_ylabel("z [m]")
    if plotGrid:
        drawGrid(
            25 * dx,
            75 * dx,
            25 * dx,
            75 * dx,
            int(50 / nx) * dx,
            int(50 / ny) * dx,
        )
        imAxis.plot(
            [25 * dx, 25 * dx, 75 * dx, 75 * dx, 25 * dx],
            [25 * dx, 75 * dx, 75 * dx, 25 * dx, 25 * dx],
            color="black",
            alpha=0.75,
        )
    if plotAcqGeom:
        imAxis.scatter(
            sources[:, 0] * dx, sources[:, 1] * dx, marker="x", color="red"
        )
        imAxis.scatter(
            receivers[:, 0] * dx,
            receivers[:, 1] * dx,
            marker="v",
            color="green",
        )
    imAxis.set_title(plotTitle)
    imAxis.invert_yaxis()
    divider = make_axes_locatable(imAxis)
    colorBarAxis = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=colorBarAxis)
    colorBarAxis.set_ylabel(colorBarTitle)
    return imAxis, colorBarAxis, im


def onclick(event):
    # Callback method for correlation fields
    if event.inaxes == ax1:
        axis = 1
    elif event.inaxes == ax2:
        axis = 2
    elif event.inaxes == ax3:
        axis = 3
    else:
        return None

    if (
        event.xdata < 25 * dx
        or event.xdata > 75 * dx
        or event.ydata < 25 * dx
        or event.ydata > 75 * dx
    ):
        return None

    ix = int(np.floor((event.xdata / dx - 25) / 10))
    iz = int(4 - np.floor((event.ydata / dx - 25) / 10))

    icor = ix + iz * 5 + (axis - 1) * 25

    correlations = correlation_matrix[icor, :]

    de_cor = np.zeros((nx, ny))
    vp_cor = np.zeros((nx, ny))
    vs_cor = np.zeros((nx, ny))

    for i in range(0, nx):
        for j in range(0, ny):
            de_cor[i, j] = correlations[i + j * nx]
            vp_cor[i, j] = correlations[i + j * nx + ncells]
            vs_cor[i, j] = correlations[i + j * nx + ncells * 2]

    de_cor = np.transpose(de_cor)
    vp_cor = np.transpose(vp_cor)
    vs_cor = np.transpose(vs_cor)

    global im1, im2, im3
    global highlighted_parameter
    im1.remove()
    im2.remove()
    im3.remove()
    highlighted_parameter.pop(0).remove()
    del highlighted_parameter
    im1 = ax1.imshow(
        de_cor,
        extent=(25 * dx, 75 * dx, 25 * dx, 75 * dx),
        cmap=blue_orange_custom,
        vmin=-0.6,
        vmax=0.6,
    )
    im2 = ax2.imshow(
        vp_cor,
        extent=(25 * dx, 75 * dx, 25 * dx, 75 * dx),
        cmap=blue_orange_custom,
        vmin=-0.6,
        vmax=0.6,
    )
    im3 = ax3.imshow(
        vs_cor,
        extent=(25 * dx, 75 * dx, 25 * dx, 75 * dx),
        cmap=blue_orange_custom,
        vmin=-0.6,
        vmax=0.6,
    )
    highlighted_parameter = drawBoxParameter(icor)
    fig = plt.gcf()
    fig.canvas.draw()
    fig.canvas.flush_events()


def drawBoxParameter(par):
    # Method to draw a white box around a single parameter
    global highlighted_parameter
    if "highlight" in globals():
        highlighted_parameter.pop(0).remove()
        del highlighted_parameter
    axis = math.floor(par / 25)
    if axis == 0:
        axis = ax1
    elif axis == 1:
        axis = ax2
    else:
        axis = ax3
    block = par % 25

    ix = block % 5
    iz = math.floor(block / 5)

    x_arr = (np.array([0, 10, 10, 0, 0]) + ix * 10 + 25) * dx
    z_arr = (np.array([0, 0, 10, 10, 0]) - iz * 10 + 65) * dx

    return axis.plot(x_arr, z_arr, c="white")


# Numerical grid spacing
dx = 1.249

# Inversion grid sizes (assuming it's square)
nx = int(((rawSamples.shape[1] - 1) / 3) ** 0.5)
ny = nx
ncells = nx * ny

# Parse the data
parsed_data = {}
for i in range(0, ncells):
    parsed_data["de_" + str(i).zfill(2)] = rawSamples[::, i]
for i in range(0, ncells):
    parsed_data["vp_" + str(i).zfill(2)] = rawSamples[::, i + ncells]
for i in range(0, ncells):
    parsed_data["vs_" + str(i).zfill(2)] = rawSamples[::, i + ncells * 2]

# Compute statistics
parsed_data = pd.DataFrame(data=parsed_data)  # cast to pandas dataframe
covariance_matrix = parsed_data.cov().values  # compute covariance from samples
# Compute standard deviations
inverse_std_matrix = np.diag(1.0 / (np.diag(covariance_matrix) ** 0.5))
# Compute correlation matrix
correlation_matrix = (
    inverse_std_matrix @ covariance_matrix @ inverse_std_matrix
)

# Initial extracted correlation
correlations = correlation_matrix[15, :]

# Extract the maximum correlation (except r=1)
temporary_matrix = np.copy(correlation_matrix)
temporary_matrix[temporary_matrix >= 0.9] = 0
maximum_non_1_correlation = np.max(np.abs(temporary_matrix))

# Construct correlation fields
de_cor = np.zeros((nx, ny))
vp_cor = np.zeros((nx, ny))
vs_cor = np.zeros((nx, ny))
for i in range(0, nx):
    for j in range(0, ny):
        de_cor[i, j] = correlations[i + j * nx]
        vp_cor[i, j] = correlations[i + j * nx + ncells]
        vs_cor[i, j] = correlations[i + j * nx + ncells * 2]
de_cor = np.transpose(de_cor)
vp_cor = np.transpose(vp_cor)
vs_cor = np.transpose(vs_cor)

# Create figure and axes
figure = plt.figure(figsize=(18, 6))
colour_list = [(0.1, 0.6, 1.0), (0.05, 0.05, 0.05), (0.8, 0.5, 0.1)]
blue_orange_custom = LinearSegmentedColormap.from_list(
    "BlueOrangeCustom", colour_list
)
ax1 = plt.subplot(1, 3, 1)
ax2 = plt.subplot(1, 3, 2)
ax3 = plt.subplot(1, 3, 3)

# Make the subplots fit snugly
plt.subplots_adjust(
    left=0.125, right=0.9, bottom=0.1, top=0.9, wspace=0.6, hspace=0.2
)

# Create images
_, _, im1 = plotInModel(
    de_cor,
    -maximum_non_1_correlation,
    maximum_non_1_correlation,
    "density",
    "correlation coefficient",
    blue_orange_custom,
    imAxis=ax1,
)
_, _, im2 = plotInModel(
    vp_cor,
    -maximum_non_1_correlation,
    maximum_non_1_correlation,
    "Target 1 - chain A\n\nvp",
    "correlation coefficient",
    blue_orange_custom,
    imAxis=ax2,
)
_, _, im3 = plotInModel(
    vs_cor,
    -maximum_non_1_correlation,
    maximum_non_1_correlation,
    "vs",
    "correlation coefficient",
    blue_orange_custom,
    imAxis=ax3,
)

# Highlight the currently selected parameter
highlighted_parameter = drawBoxParameter(15)

# Create callback for click
callback_click = plt.gcf().canvas.mpl_connect("button_press_event", onclick)

# Show the plot
plt.tight_layout()
plt.show()
