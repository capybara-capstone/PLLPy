"""Parameter Sweeper Class"""

from .logger import setup_log
# pylint: disable=W1203 disable=W0622


class Sweeper():
    """
    A class to sweep through different parameter values for a PLL component
    and log the results.

    Attributes:
        pll: An instance of the PLL system.
        log: Logger instance for recording events.
        io_file: Log file name for storing results.
        results: A list to store the sweep results.
    """

    def __init__(self, pll, id: int):
        """
        Initializes the Sweeper instance.

        Args:
            pll: The phase-locked loop (PLL) system instance.
            id (int): Identifier for the logging instance.
        """
        self.pll = pll
        self.log, self.io_file = setup_log(name=str(__name__).replace(
            '.', '_'), id=id, settings=self.pll.settings, csv=False)
        self.results = []

    def start(self, block: str, parameter: str, values: list):
        """
        Starts sweeping a given parameter over a range of values for a specified PLL block.

        Args:
            block (str): The PLL block to modify ('vco', 'lf', 'clk', or 'div').
            parameter (str): The name of the parameter to sweep.
            values (list): A list of values to set for the parameter.

        Returns:
            None
        """
        if block not in self.pll.components.keys():
            self.log.info(
                'Block not found in PLL components. Check block name.')
            self.log.info(
                f'Available components are {self.pll.components.keys()}')
            print('Block not found in PLL components. Check block name.')
            print(f'Available components are {self.pll.components.keys()}')
            return None

        match block:
            case 'vco':
                self.log.info('Starting Sweeper for VCO')
                for value in values:
                    self.log.info(self.pll.settings.set_vco_parameter(
                        parameter=parameter, value=value))
                    self.pll.start_and_monitor()
                    self.pll.show(plot_type=self.pll.settings.global_plot_mode)
                    self.log.info(f'Results at {self.pll.io_file[:-4]}')
            case 'lf':
                self.log.info('Starting Sweeper for Loop Filter')
                for value in values:
                    self.log.info(self.pll.settings.set_lf_parameter(
                        parameter=parameter, value=value))
                    self.pll.start_and_monitor()
                    self.pll.show(plot_type=self.pll.settings.global_plot_mode)
                    self.log.info(f'Results at {self.pll.io_file[:-4]}')
            case 'clk':
                self.log.info('Starting Sweeper for Clock')
                for value in values:
                    self.log.info(self.pll.settings.set_clk_parameter(
                        parameter=parameter, value=value))
                    self.pll.start_and_monitor()
                    self.pll.show(plot_type=self.pll.settings.global_plot_mode)
                    self.log.info(f'Results at {self.pll.io_file[:-4]}')
            case 'div':
                self.log.info('Starting Sweeper for Divider')
                for value in values:
                    self.log.info(self.pll.settings.set_divider_parameter(
                        parameter=parameter, value=value))
                    self.pll.start_and_monitor()
                    self.pll.show(plot_type=self.pll.settings.global_plot_mode)
                    self.log.info(f'Results at {self.pll.io_file[:-4]}')
