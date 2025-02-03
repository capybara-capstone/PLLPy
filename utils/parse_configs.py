import argparse
import json
import logging
import numpy as np
from components.settings import Settings

def check_arg(key: str, dict: dict, req: bool = False):
    if not key in dict:
        if req == True:
            raise Exception("f{key} not defined in {dict}!")
        else:
            return None

    return dict[key]


def parse_ref_clock(settings: Settings, logger: logging, ref_clock: dict):
    fo = check_arg("fo", ref_clock)
    k_vco = check_arg("k_vco", ref_clock)
    if fo:
        settings.clk["fo"] = fo
    if k_vco:
        settings.clk["k_vco"] = k_vco
    logger.info(f"Setting ref_clock settings...\n\t\tfrq:\t{fo}\n\t\tk_vco:\t{k_vco}")

def parse_PFD_loop_filter(settings: Settings, logger: logging, pfd_loop_filter: dict):
    # Reading PFD Loop Filter configurations
    capacitors = check_arg("capacitors", pfd_loop_filter)
    resistors = check_arg("resistors", pfd_loop_filter)
    gains = check_arg("gains", pfd_loop_filter)
    if capacitors:
        settings.pfd["capacitors"] = capacitors
    if resistors:
        settings.pfd["resistors"] = resistors
    if gains:
        settings.pfd["gains"] = gains
    logger.info(f"Setting PFD Loop Filter settings...\n\t\tcapacitors:\t{capacitors}\n\t\tresistors:\t{resistors}\n\t\tgains:\t{gains}")

def parse_VCO(settings: Settings, logger: logging, VCO: dict):
    # Reading VCO configurations
    k_vco = check_arg("k_vco", VCO)
    fo = check_arg("fo", VCO)
    if k_vco:
        settings.vco["k_vco"] = k_vco
    if fo:
        settings.vco["fo"] = fo
    logger.info(f"Setting VCO settings...\n\t\tk_vco:\t{k_vco}\n\t\tfo:\t{fo}")

def parse_divider(settings: Settings, logger: logging, divider: dict):
    # Reading Divider configurations
    divided_value = check_arg("divided_value", divider)
    if divided_value:
        settings.divider['n'] = divided_value
        logger.info(f"Setting Divider settings...\n\t\tdivided_value:\t{divided_value}")


#TODO: decide if we want to put multiple configs in one file, or if each file = one config
# The latter is more appealing for usability's sake... tests shouldn't be a problem, since ideally 
# we're automating all of them

#def parse_args(pll_vco: VCOObject, pll_divider: DividerObject, pll_lpd: LPDObject, PFD_object: PFDObject):
def parse_args(settings: Settings, config_file: str = None):
    logger = logging.getLogger(__name__)
    logger.info('STARTing config settings...')

    if config_file == None:
        logger.info('No configuration file provided, using default values.\nENDing config settings...')
        return
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Default configuration file should be a file called "config.json" in the dir you're calling from
    logger.info(f"Running configuration found in {config_file}.")

    all_args = argparse.Namespace()
    with open(config_file, 'rt') as f:    
        all_args.__dict__.update(json.load(f))

    args = vars(parser.parse_args(namespace=all_args))

    # Re: the TODO: assumes one config per file, this dbg msg is only really helpful if you have multiple configs per file ig /shrug:
    config_name = list(args.keys())[0]
    logger.info(f"Reading configuration named {config_name}.")

    # Mandatory global variables (?)
    VDD = check_arg("VDD", args[config_name])
    VSS = check_arg("VSS", args[config_name])
    time_step = check_arg("time_step", args[config_name])
    stop_time = check_arg("stop_time", args[config_name])
    settings.vdd = VDD
    settings.vss = VSS
    settings.time_step = time_step
    settings.sim_time = stop_time
    logger.info(f"Setting global settings...\n\t\tVDD:\t{VDD}\n\t\tVSS:\t{VSS}\n\t\ttime_step:\t{time_step}\n\t\tstop_time:\t{stop_time}")


    ref_clock = check_arg("ref_clock", args[config_name])
    if (ref_clock):
        parse_ref_clock(settings, logger, ref_clock)

    VCO = check_arg("VCO", args[config_name])
    if (VCO):
        parse_VCO(settings, logger, VCO)

    pfd_loop_filter = check_arg("pfd_loop_filter", args[config_name])
    if (pfd_loop_filter):        
        parse_PFD_loop_filter(settings, logger, pfd_loop_filter) 
    
    divider = check_arg("divider", args[config_name])
    if (divider):
        parse_divider(settings, logger, divider)