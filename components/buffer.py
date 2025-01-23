"""Buffer Class"""
import simpy
from bokeh.plotting import figure
from bokeh.models import CustomJSTickFormatter


class Buffer():
    """Models buffer"""

    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.buffer = simpy.Store(env)
        self.monitor = []

    def put(self, value):
        """Adds to buffer and monitor

        :param value: Value to add to the buffer.
        :type value: int|str
        """
        self.buffer.put(value)
        self.monitor.append((self.env.now, value))
        # print(f"@ {self.env.now}| {value} ADDED to {self.name}")

    def get_buffer_waves(self):
        """Plots the buffers over time"""
        unit_time_formatter = CustomJSTickFormatter(code="""
        const thresholds = [1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1, 60];
        const units = ["fs", "ps", "ns", "µs", "ms", "s", "min"];
        let scaled_value = tick;
        let unit = "s";

        for (let i = 0; i < thresholds.length; i++) {
            if (Math.abs(tick) < thresholds[i]) {
                scaled_value = tick / (thresholds[i - 1] || 1);
                unit = units[i - 1];
                if (unit == null){
                    unit = ""
                }
                break;
            }
        }

        return `${scaled_value.toFixed(2)} ${unit}`;
        """)

        buffer = figure(
            title=f"{self.name} Buffer",
            x_axis_label="Time",
            x_axis_type="datetime",
            y_axis_label="Voltage (V)")
        x, y = zip(*self.monitor)
        buffer.line(x, y)
        buffer.xaxis.formatter = unit_time_formatter
        return buffer
