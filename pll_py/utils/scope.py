"""Scope Class for Plotting Data.

The `Scope` class is used to manage and display different types of plots. It supports both local 
matplotlib-based plots and interactive web-based plots using Bokeh. The class allows adding data 
and plotting it either locally on a static plot or interactively on the web. Plots can be organized 
into a grid layout and saved to a file.

Attributes:
    web_figures (list): List to store Bokeh figure objects for web-based plotting.
    local_figures (list): List to store data for local matplotlib plotting.
    grid_columns (int): The number of columns for organizing web-based plots in a grid.
    sizing_mode (str): The sizing mode for Bokeh plots (e.g., 'scale_both').
"""

from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import gridplot
import matplotlib.pyplot as plt

# pylint: disable=C0301


class Scope:
    """
    Initializes a Scope object. Optionally accepts initial data to generate plots on creation.

    The `Scope` class handles the addition of signals and their plotting in either a local or web-based
    interface. It allows for plotting data arrays and organizing the plots in grids for web-based interfaces.
    The plots can be saved as image files or HTML files.

    :param grid_columns: The number of columns for arranging web-based plots in a grid. Default is 1.
    :param fit: Determines the sizing mode for Bokeh plots (e.g., 'scale_both'). Default is 'scale_both'.
    """

    def __init__(self, grid_columns: int = 1, fit: str = 'scale_both'):
        """
        Initialize the Scope object.

        :param grid_columns: The number of columns for organizing web-based plots in a grid.
                              Default is 1 column.
        :param fit: The sizing mode for web-based Bokeh plots (e.g., 'scale_both'). Default is 'scale_both'.
        """
        self.web_figures = []
        self.local_figures = []
        self.grid_columns = grid_columns
        self.sizing_mode = fit

    def add_signal(self, x_arr: list[float], y_arr: list[float], name: str, x_label: str = "X", y_label: str = "Y", plot_type: str = 'local'):
        """
        Adds a new signal to the scope for plotting.

        This method allows adding a signal with x and y arrays and a name. The plot type can be 
        either 'local' (matplotlib) or 'web' (Bokeh), where 'web' plots are interactive and 
        rendered in a grid layout.

        :param x_arr: List of x-values for the signal.
        :param y_arr: List of y-values for the signal.
        :param name: The name of the signal for labeling the plot.
        :param x_label: The label for the x-axis. Default is "X".
        :param y_label: The label for the y-axis. Default is "Y".
        :param plot_type: The type of plot ('local' for matplotlib, 'web' for Bokeh). Default is 'local'.
        """
        if plot_type == 'local':
            self.local_figures.append({
                'x': x_arr,
                'y': y_arr,
                'name': name,
                'x_label': x_label,
                'y_label': y_label
            })
        elif plot_type == 'web':
            p = figure(title=name, x_axis_label=x_label, y_axis_label=y_label,
                       width=800, height=200, sizing_mode=self.sizing_mode, output_backend="webgl")
            p.step(x_arr, y_arr,
                   line_width=2,
                   mode='center')
            self.web_figures.append(p)

    def show(self, plot_type: str = 'local', save_path: str = None):
        """
        Displays the plots in a vertical grid layout.

        This method displays all the added plots. If the `plot_type` is 'local', the plots will
        be shown using matplotlib in a static layout. If the `plot_type` is 'web', the plots will 
        be shown using Bokeh in an interactive web layout. Optionally, the plots can be saved 
        to a file (e.g., as an image for local plots or an HTML file for web plots).

        :param plot_type: The type of plot to display. 'local' for matplotlib or 'web' for Bokeh. Default is 'local'.
        :param save_path: The path where the plot should be saved. If None, the plot is not saved. Default is None.
        """
        if plot_type == 'local':
            fig = plt.figure(figsize=(10, 2 * len(self.local_figures)))

            for i, signal in enumerate(self.local_figures):
                ax = fig.add_subplot(len(self.local_figures), 1, i + 1)
                ax.plot(signal['x'], signal['y'], label=signal['name'])
                ax.set_xlabel(signal['x_label'])
                ax.set_ylabel(signal['y_label'])
                ax.set_title(signal['name'], loc='left')
                ax.grid(True, linestyle='--', alpha=0.7)

            plt.tight_layout()
            if save_path is not None:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.show()
            fig = None

        elif plot_type == 'web':
            layout = gridplot([self.web_figures[i:i + self.grid_columns]
                               for i in range(0, len(self.web_figures), self.grid_columns)],
                              sizing_mode=self.sizing_mode)

            if save_path is not None:
                output_file(filename=save_path)
                save(layout)

            show(layout)
