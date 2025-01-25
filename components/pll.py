"""pll class"""
import os
from bokeh.plotting import show, output_file, save
from bokeh.layouts import gridplot
from components.divider import Divider
from components.lpd import Lpd
from components.vco import Vco
from components.pfd import Pfd
from components.settings import Settings

# pylint: disable=W0718


class Pll():
    """PLL main class"""

    def __init__(self, settings: Settings, name="PLL",  auto_setup: bool = True):
        self.settings = settings
        self.env = settings.env
        self.name = name
        self.components_dict = {}
        self.log = None
        if auto_setup:
            self.setup()

    def setup(self):
        """Set up divider"""
        self.log = self.settings.get_logger(self.name)

    def start(self):
        """Start PLL simulation"""
        clk = self.add_components(Vco(self.settings, 'CLK', clk=True))
        lpd = self.add_components(Lpd(self.settings))
        pfd = self.add_components(Pfd(self.settings))
        vco = self.add_components(Vco(self.settings))
        div = self.add_components(Divider(self.settings))

        # Interconnect modules
        lpd.input_a = clk.output

        pfd.input_a = lpd.output_up
        pfd.input_b = lpd.output_down
        pfd.gains = self.settings.pfd["gains"]
        pfd.resistors = self.settings.pfd["resistors"]
        pfd.capacitors = self.settings.pfd["capacitors"]

        vco.input = pfd.output
        vco.k_vco = self.settings.vco["k_vco"]
        vco.fo = self.settings.vco["fo"]

        div.input = vco.output
        div.n = self.settings.divider["n"]

        lpd.input_b = div.output

        self.log.info("Starting simulation")
        self.env.process(clk.start())
        self.env.process(lpd.start())
        self.env.process(pfd.start())
        self.env.process(vco.start())
        self.env.process(div.start())
        self.env.run(until=self.settings.sim_time)
        self.log.info("Simulation Finished")

        sim_path = self.settings.get_running_dir()
        self.show(save_path=sim_path)

    def add_components(self, component):
        """Adds component instance to PLL components dict

        :param components: Components instances to be added
                           Index is the components name.
        :type components: object | list[Object]
        """
        try:
            self.components_dict[component.name] = component
            self.log.info(f'Component {component.name} added to {self.name}')
        except Exception as e:
            self.log.error(
                f'Component {component.name} NOT added to {self.name}')
            self.log.error(f'ERROR: {e}')

        return component

    def show(self, save_path: str = None):
        """Plots the outputs of the PLL"""
        clk = self.components_dict['CLK']
        div = self.components_dict['Divider']
        pfd = self.components_dict['PFD']
        vco = self.components_dict['VCO']

        clk_output = clk.output.get_buffer_waves()
        div_output = div.output.get_buffer_waves()
        pfd_output = pfd.output.get_buffer_waves()
        vco_output = vco.output.get_buffer_waves()

        grid = gridplot([[div_output,
                        pfd_output,
                        vco_output,
                        clk_output]])
        if save_path is not None:
            show(grid)
            output_file(os.path.join(save_path, 'sim_output.html'))
            save(grid)
