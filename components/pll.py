"""pll class"""
from components.divider import Divider
from components.lpd import Lpd
from components.vco import Vco
from components.pfd import Pfd
from components.settings import Settings
from bokeh.plotting import show
from bokeh.layouts import gridplot


class Pll():
    """PLL main class"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.env = settings.env
        self.components_dict = {}

    def start(self):
        """Start PLL simulation"""
        clk = Vco(self.env, 'CLK', clk=True)
        lpd = Lpd(self.env)
        pfd = Pfd(self.env)
        vco = Vco(self.env)
        div = Divider(self.env)

        self.add_components([clk, lpd, pfd, vco, div])

        lpd.input_a = clk.output

        pfd.input_a = lpd.output_up
        pfd.input_b = lpd.output_down

        vco.input = pfd.output
        div.input = vco.output

        lpd.input_b = div.output

        self.env.process(clk.start())
        self.env.process(lpd.start())
        self.env.process(pfd.start())
        self.env.process(vco.start())
        self.env.process(div.start())
        self.env.run(until=self.settings.sim_time)
        self.show()

    def add_components(self, components):
        """Adds component instance to PLL components dict

        :param components: Components instances to be added
                           Index is the components name.
        :type components: object | list[Object]
        """
        for component in components:
            self.components_dict[component.name] = component

    def show(self):
        """Plots the outputs of the PLL"""
        clk = self.components_dict['CLK']
        div = self.components_dict['Divider']
        pfd = self.components_dict['PFD']
        vco = self.components_dict['VCO']

        clk_output = clk.output.get_buffer_waves()
        div_output = div.output.get_buffer_waves()
        pfd_output = pfd.output.get_buffer_waves()
        vco_output = vco.output.get_buffer_waves()

        show(gridplot([[div_output,
                        pfd_output,
                        vco_output,
                        clk_output]]))
