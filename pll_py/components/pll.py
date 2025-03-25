"""PLL Class

This module defines a Phase-Locked Loop (PLL) simulation class, which models
the components of a PLL system including the Voltage-Controlled Oscillator (VCO),
Phase Detector (LPD), Loop Filter (LF), Divider, and the PLL scope.

Modules involved in the simulation include:
- `Vco`: Voltage-controlled oscillator.
- `Lpd`: Phase detector.
- `LoopFilter`: Filters the error signal.
- `Divider`: Divider for clock signal.

The simulation can be visualized locally or using web-based plots.
"""

from collections import deque
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import gridplot
from .lpd import Lpd
from .vco import Vco
from .lf import LoopFilter
from .divider import Divider
from ..utils.scope import Scope
from ..utils.logger import setup_log, save_io
from ..utils.formatter import get_time_format, get_volts_format

# pylint: disable=W0212

scope = Scope()


class Pll:
    """A class to simulate and monitor a Phase-Locked Loop (PLL) system.

    This class simulates a PLL system including the VCO, Phase Detector, 
    Loop Filter, Divider, and other components. The simulation can be 
    visualized using matplotlib or Bokeh for real-time analysis.

    Attributes:
        settings (object): Settings for the simulation such as time step and sample count.
        components (dict): Dictionary containing the components of the PLL system.
        scope (Scope): Instance of the Scope class for monitoring the PLL's behavior.
        output (deque): Holds the output of the VCO for visualization.
        time_array (ndarray): Time array used for plotting simulation results.
    """

    def __init__(self, settings, scope_fit='stretch_width'):
        """Initializes the PLL simulation with given settings.

        :param settings: Configuration settings for the PLL simulation.
        :param scope_fit: Determines the fitting behavior for the Scope.
        """
        self.settings = settings
        self.components = {'clk': None,
                           'lpd': None,
                           'lf': None, 'vco': None,
                           'div': None}
        self.scope = Scope(fit=scope_fit)
        self.output = deque([], maxlen=settings.sample_count)
        self.time_array = self.settings.time_array
        self.id = settings.pll['id']
        self.log = None
        self.io_file = None

    def update_logger(self):
        """Updates logger"""
        self.settings.pll['id'] += 1
        self.id = self.settings.pll['id']
        self.log, self.io_file = setup_log(
            name=str(__name__).replace('.', '_'), id=self.id, settings=self.settings)

    def start_cdr(self, data):
        """Starts clock and data recovery mode for PLL"""
        self.update_logger()
        progress_bar = tqdm(total=self.settings.sample_count,
                            desc='Recovering CLK',
                            position=0)
        clk = Vco(settings=self.settings, clk=True)
        lpd = Lpd(settings=self.settings)
        lf = LoopFilter(settings=self.settings)
        vco = Vco(settings=self.settings)
        div = Divider(settings=self.settings)

        self.components = {'clk': clk, 'lpd': lpd,
                           'lf': lf, 'vco': vco, 'div': div}

        lf_out = 0
        div_out = 0
        for sample in data:
            lpd_out_a, lpd_out_b = lpd._process_and_monitor(sample, div_out)
            lf_out = lf._process(lpd_out_a, lpd_out_b)
            vco_out = vco._process_and_monitor(lf_out)
            div_out = div._process_and_monitor(vco_out)

            self.output.append(vco_out)
            progress_bar.update(1)

        self.time_array = np.arange(
            0, self.settings.time_step*len(self.output), self.settings.time_step)
        print('Recovered Clock')

        save_io(io_arrays=[np.arange(0, self.settings.time_step*len(self.output),
                                     self.settings.time_step),
                           data,
                           div.io['output'],
                           lpd.io['output_a'],
                           lpd.io['output_b'],
                           lf.io['output'],
                           vco.io['output']],
                headers=['Time', 'Data', 'Divider Output', 'LPD Output A',
                         'LPD Output B', 'Loop Filter Output', 'VCO Output'],
                io_file=self.io_file)

    def start_and_monitor(self):
        """Starts the PLL simulation and monitors the progress.

        This method runs the PLL simulation while tracking the progress using 
        a progress bar. It updates the components and stores the VCO output 
        for visualization.

        The following components are involved:
        - Voltage-controlled Oscillator (VCO)
        - Phase Detector (LPD)
        - Loop Filter (LF)
        - Divider

        **Example:**

        .. code-block:: python

            pll = Pll(settings)
            pll.start_and_monitor()

        :raises ValueError: If the simulation does not complete successfully.
        """
        self.update_logger()
        progress_bar = tqdm(total=self.settings.sample_count,
                            desc='LOCKING PLL',
                            position=0)
        clk = Vco(settings=self.settings, clk=True)
        lpd = Lpd(settings=self.settings)
        lf = LoopFilter(settings=self.settings)
        vco = Vco(settings=self.settings)
        div = Divider(settings=self.settings)

        self.components = {'clk': clk, 'lpd': lpd,
                           'lf': lf, 'vco': vco, 'div': div}

        lf_out = 0
        div_out = 0
        for _ in range(self.settings.sample_count):
            clk_out = clk._process_and_monitor(1)
            lpd_out_a, lpd_out_b = lpd._process_and_monitor(clk_out, div_out)
            lf_out = lf._process(lpd_out_a, lpd_out_b)
            vco_out = vco._process_and_monitor(lf_out)
            div_out = div._process_and_monitor(vco_out)

            self.output.append(vco_out)
            progress_bar.update(1)

        save_io(io_arrays=[np.arange(0, self.settings.time_step*len(self.output),
                                     self.settings.time_step),
                           clk.io['output'],
                           div.io['output'],
                           lpd.io['output_a'],
                           lpd.io['output_b'],
                           lf.io['output'],
                           vco.io['output']],
                headers=['Time', 'CLK Output', 'Divider Output', 'LPD Output A',
                         'LPD Output B', 'Loop Filter Output', 'VCO Output'],
                io_file=self.io_file)

    def start(self):
        """Starts the PLL simulation without progress monitoring.

        This method runs the PLL simulation and stores the VCO output for
        visualization, without displaying the progress bar.

        **Example:**

        .. code-block:: python

            pll = Pll(settings)
            pll.start()

        :raises ValueError: If the simulation does not complete successfully.
        """
        self.update_logger()
        clk = Vco(settings=self.settings, clk=True)
        lpd = Lpd(settings=self.settings)
        lf = LoopFilter(settings=self.settings)
        vco = Vco(settings=self.settings)
        div = Divider(settings=self.settings)

        self.components = {'clk': clk, 'lpd': lpd,
                           'lf': lf, 'vco': vco, 'div': div}

        lf_out = 0
        div_out = 0
        for _ in range(self.settings.sample_count):
            clk_out = clk._process(1)
            lpd_out_a, lpd_out_b = lpd._process(clk_out, div_out)
            lf_out = lf._process(lpd_out_a, lpd_out_b)
            vco_out = vco._process(lf_out)
            div_out = div._process(vco_out)

            self.output.append(vco_out)

        print('PLL Locked')

    def show(self, plot_type=None, sim_type='PLL', input=None):
        """Generates and displays plots of the simulation outputs.

        This method generates plots for the various components of the PLL system
        (CLK, Divider, LPD outputs, Loop Filter, and VCO). The plots can be generated
        either locally using `matplotlib` or via a web-based interface using `Bokeh`.

        :param plot_type: The type of plot to generate. Options are:
            - 'local': Uses matplotlib for local plotting.
            - 'web': Uses Bokeh for web-based visualization.

        **Example:**

        .. code-block:: python

            pll = Pll(settings)
            pll.show(plot_type='local')  # For local plotting.
            pll.show(plot_type='web')  # For web-based plotting.

        :raises ValueError: If an invalid plot_type is provided.
        """
        self.time_array = self.settings.time_array
        if input is None:
            input = []

        if plot_type is None:
            plot_type = self.settings.global_plot_mode

        if plot_type == 'local':
            fig, axes = plt.subplots(6, 1, figsize=(6, 10))
            if (sim_type == 'PLL'):
                axes[0].plot(self.time_array,
                             self.components['clk'].io['output'], color='b')
                axes[0].set_title('CLK Output', loc='left')
            else:
                axes[0].plot(self.time_array,
                             input, color='b')
                axes[0].set_title('Data Input', loc='left')
            axes[0].grid(True)
            axes[1].plot(self.time_array, self.components['div'].io['output'],
                         color='r')
            axes[1].set_title(
                f'Divider Output- {self.settings.divider}', loc='left')
            axes[1].grid(True)
            axes[2].plot(self.time_array,
                         self.components['lpd'].io['output_a'], color='g')
            axes[2].set_title('LPD Output A', loc='left')
            axes[2].grid(True)

            axes[3].plot(self.time_array,
                         self.components['lpd'].io['output_b'], color='m')
            axes[3].set_title('LPD Output B', loc='left')
            axes[3].grid(True)

            axes[4].plot(self.time_array,
                         self.components['lf'].io['output'], color='c')
            axes[4].set_title(
                f'Loop Filter Output - {self.settings.lf}', loc='left')
            axes[4].grid(True)

            axes[5].plot(self.time_array,
                         self.components['vco'].io['output'], color='c')
            axes[5].set_title(f'VCO Output - {self.settings.vco}', loc='left')
            axes[5].grid(True)
            plt.tight_layout()
            plt.savefig(self.io_file[:-3]+"png", dpi=300, bbox_inches='tight')
            plt.show()

        elif plot_type == 'web':
            if (sim_type == 'PLL'):
                input_f = figure(title='CLK Output', x_axis_label='Seconds', y_axis_label='Volts',
                                 width=800, height=200, sizing_mode='scale_both')

                input_f.step(self.time_array, [*self.components['clk'].io['output']],
                             line_width=2,
                             mode='center')

                input_f.xaxis.formatter = get_time_format()
                input_f.yaxis.formatter = get_volts_format()
            else:
                input_f = figure(title='Data Input', x_axis_label='Seconds', y_axis_label='Volts',
                                 width=800, height=200, sizing_mode='scale_both')

                input_f.step(self.time_array, input,
                             line_width=2,
                             mode='center')

            div_f = figure(title='Divider Output', x_axis_label='Seconds', y_axis_label='Volts',
                           width=800, height=200, sizing_mode='scale_both')

            div_f.step(self.time_array, [*self.components['div'].io['output']],
                       line_width=2,
                       mode='center')

            div_f.xaxis.formatter = get_time_format()
            div_f.yaxis.formatter = get_volts_format()

            lpd_a_f = figure(title='LPD Output A', x_axis_label='Seconds', y_axis_label='Volts',
                             width=800, height=200, sizing_mode='scale_both')

            lpd_a_f.step(self.time_array, [*self.components['lpd'].io['output_a']],
                         line_width=2,
                         mode='center')
            lpd_a_f.xaxis.formatter = get_time_format()
            lpd_a_f.yaxis.formatter = get_volts_format()

            lpd_b_f = figure(title='LPD Output B', x_axis_label='Seconds', y_axis_label='Volts',
                             width=800, height=200, sizing_mode='scale_both')

            lpd_b_f.step(self.time_array, [*self.components['lpd'].io['output_b']],
                         line_width=2,
                         mode='center')
            lpd_b_f.xaxis.formatter = get_time_format()
            lpd_b_f.yaxis.formatter = get_volts_format()

            lf_f = figure(title='Loop Filter Output', x_axis_label='Seconds', y_axis_label='Volts',
                          width=800, height=200, sizing_mode='scale_both')

            lf_f.line(self.time_array, [*self.components['lf'].io['output']],
                      line_width=2)
            lf_f.xaxis.formatter = get_time_format()
            lf_f.yaxis.formatter = get_volts_format()

            vco_f = figure(title='VCO Output', x_axis_label='Seconds', y_axis_label='Volts',
                           width=800, height=200, sizing_mode='scale_both')

            vco_f.step(self.time_array, [*self.components['vco'].io['output']],
                       line_width=2,
                       mode='center')
            vco_f.xaxis.formatter = get_time_format()
            vco_f.yaxis.formatter = get_volts_format()
            layout = gridplot([[input_f],
                               [div_f],
                               [lpd_a_f],
                               [lpd_b_f],
                               [lf_f],
                               [vco_f]], sizing_mode='scale_both')

            output_file(filename=self.io_file[:-3]+"html")
            save(layout)
            show(layout)
