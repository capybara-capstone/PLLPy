"""Format Helper Functions"""
from bokeh.models import CustomJSTickFormatter


def get_time_format():
    """Creates custom scale for web axis"""
    return CustomJSTickFormatter(code="""
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


def get_freq_format():
    """Creates custom scale for web axis"""
    return CustomJSTickFormatter(code="""
        const thresholds = [1e9, 1e6, 1e3, 1];  // GHz, MHz, KHz, Hz
        const units = ["GHz", "MHz", "KHz", "Hz"];
        let scaled_value = tick;
        let unit = "Hz";  // Default unit is Hertz

        // Iterate over the thresholds to scale the value
        for (let i = 0; i < thresholds.length; i++) {
            if (Math.abs(tick) >= thresholds[i]) {
                scaled_value = tick / thresholds[i];
                unit = units[i];
                break;
            }
        }

        // Return formatted frequency with 2 decimal places and unit
        return `${scaled_value.toFixed(2)} ${unit}`;
    """)


def get_volts_format():
    """Creates custom scale for web axis"""
    return CustomJSTickFormatter(code="""
        const thresholds = [1e6, 1e3, 1, 1e-3, 1e-6];  // MV, kV, V, mV, µV
        const units = ["MV", "kV", "V", "mV", "µV"];
        let scaled_value = tick;
        let unit = "V";  // Default unit is Volts

        // Iterate over the thresholds to scale the value
        for (let i = 0; i < thresholds.length; i++) {
            if (Math.abs(tick) >= thresholds[i]) {
                scaled_value = tick / thresholds[i];
                unit = units[i];
                break;
            }
        }

        // Return formatted voltage with 2 decimal places and unit
        return `${scaled_value.toFixed(2)} ${unit}`;
    """)
