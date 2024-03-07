# This file is used to generate the radar charts of the solvent


"""
======================================
Radar chart (aka spider or star chart)
======================================

This example creates a radar chart, also known as a spider or star chart [1]_.

Although this example allows a frame of either 'circle' or 'polygon', polygon
frames don't have proper gridlines (the lines are circles instead of polygons).
It's possible to get a polygon grid by setting GRIDLINE_INTERPOLATION_STEPS in
matplotlib.axis to the desired number of vertices, but the orientation of the
polygon is not aligned with the radial axes.

.. [1] http://en.wikipedia.org/wiki/Radar_chart
"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

# change font globally
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 13


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels,
                                fontsize=8, fontweight='bold')

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def example_data(combined_data):
    # num_solvent = a.shape[0]
    data = [
        ["$n^{2}$", "$B$", "$\epsilon$"],

        ('Sample 11-20', combined_data[10:20]),
        ('Sample 21-30', combined_data[20:30]),
         ('Sample 31-40', combined_data[30:40]),
          ('Sample 41-50', combined_data[40:50]),
    ]


    return data


def obtain_data(data, title, iii):
    # num_solvent = a.shape[0]
    data = [
        ["$n^{2}$", "$B$", "$\epsilon$"],
        (title, data[iii:iii+10]),
    ]
    return data



def generate_colors(num_colors):
    import colorsys
    colors = []
    for i in range(num_colors):
        hue = i / num_colors
        saturation = 0.8
        value = 0.8
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        color_hex = "#{:02X}{:02X}{:02X}".format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        colors.append(color_hex)
    return colors

def distict_colors():
    distinct_colors = [
        "#e60049", "#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]
    return distinct_colors

def data_preprocess():
    import pandas as pd
    solvent_file = 'Solvent_properties_generated.xlsx'
    combined_all_sheet = 'row_data_normalized_2'
    top10_sheet = 'top10_normalized_2'

    xls = pd.ExcelFile(solvent_file)

    # Initialize lists to store data from each sheet
    combined_data = []
    top10_data = []

    # Read data from the first sheet
    sheet1_df = pd.read_excel(xls, sheet_name=combined_all_sheet, header=0, index_col=0)
    for index, row in sheet1_df.iterrows():
        combined_data.append(row.tolist())

    # Read data from the second sheet
    sheet2_df = pd.read_excel(xls, sheet_name=top10_sheet, header=0, index_col=0)
    for index, row in sheet2_df.iterrows():
        top10_data.append(row.tolist())

    return combined_data, top10_data

def plot_10(data_to_plot, data_label, sample_label,file_name,iii):
    fig, ax = plt.subplots(figsize=(6, 4.5),
                             subplot_kw=dict(projection='radar'))

    # Plot the four cases from the example data on separate axes
    for (title, case_data_initial)  in data_to_plot:
        ax.set_ylim(0, 1)
        for d, color in zip(case_data_initial, colors):
            iii +=1
            d = np.array(d).squeeze()
            ax.plot(theta, d, color=color, label = f"{sample_label} {iii}")
            # ax.plot(theta,d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(data_label)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles,labels, ncol =5, loc='lower left',
                       labelspacing=0.1, fontsize=9,frameon=False)



    if file_name == 'radarChart_initialSample':
        note_text = "Normalized $\epsilon$ of S-5: 1.99, S-7: 7.83"
        fig.text(0.81, 0.18, note_text, fontsize = 9,horizontalalignment='right', verticalalignment='bottom',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    if file_name == 'radarChart_top10Sample':
        note_text = "Normalized $\epsilon$ of R-1: 7.83, R-4: 1.99"
        fig.text(0.81, 0.18, note_text, fontsize = 9,horizontalalignment='right', verticalalignment='bottom',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    # plt.show()
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8], size=11)
    plt.tight_layout()
    plt.savefig(f'{file_name}.png', dpi=400,bbox_inches='tight', pad_inches=0.03)
    plt.savefig(f'{file_name}.pdf', dpi=400, bbox_inches='tight', pad_inches=0.03)
    plt.show()


if __name__ == '__main__':

    combined_data, top10_data = data_preprocess()
    # N = a.shape[0]
    N = 3
    theta = radar_factory(N, frame='polygon')

    data = example_data(combined_data)
    initialSample = obtain_data(combined_data, 'Initial samples', 0)
    first10AS = obtain_data(combined_data, 'First 10 active learning samples', 10)
    last10AS = obtain_data(combined_data, 'Last 10 active learning samples', 40)
    top10Sample = obtain_data(top10_data, 'Top 10 ranked samples', 0)

    spoke_labels = data.pop(0)
    spoke_labels_initial =  initialSample.pop(0)
    spoke_labels_first10AS = first10AS.pop(0)
    spoke_labels_last10AS = last10AS.pop(0)
    spoke_labels_top10 = top10Sample.pop(0)

    fig, axes = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,
                             subplot_kw=dict(projection='radar'))
    colors = distict_colors()

    # Plot the four cases from the example data on separate axes

    for ax, (title, case_data)  in zip(axes.flat, data):
        iii = 0
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
        ax.set_ylim(0, 1)
        ax.set_title(title, weight='bold', size='medium', position=(0, 1),
                             horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            d = np.array(d).squeeze()
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(spoke_labels)

    from matplotlib.colorbar import ColorbarBase
    from matplotlib.colors import ListedColormap

    custom_cmap = ListedColormap(colors)
    cax = fig.add_axes([0.1, 0.05, 0.8, 0.02])
    ticks = np.linspace(0, 1, 10)  # 10 evenly spaced ticks from 0 to 1
    tick_labels = np.arange(1, 11)  # Tick labels from 1 to 10
    color_bar = ColorbarBase(cax, cmap=custom_cmap, ticks=ticks, orientation='horizontal')
    color_bar.set_ticklabels(tick_labels)

    # plt.show()
    plt.savefig('radarChart_activeSample.png', dpi=400,bbox_inches='tight', pad_inches=0.03)
    plt.savefig('radarChart_activeSample.pdf', dpi=400, bbox_inches='tight', pad_inches=0.03)
    plt.show()

    plot_10(initialSample, spoke_labels_initial, 'S-','radarChart_initialSample', 0)
    plot_10(first10AS,spoke_labels_first10AS,'S-','radarChart_first10AS',10)
    plot_10(last10AS, spoke_labels_last10AS, 'S-','radarChart_last10AS', 40)
    plot_10(top10Sample, spoke_labels_top10, 'R-','radarChart_top10Sample', 0)




#############################################################################
#
# ------------
#
# References
# """"""""""
#
# The use of the following functions, methods, classes and modules is shown
# in this example:

import matplotlib

matplotlib.path
matplotlib.path.Path
matplotlib.spines
matplotlib.spines.Spine
matplotlib.projections
matplotlib.projections.polar
matplotlib.projections.polar.PolarAxes
matplotlib.projections.register_projection
