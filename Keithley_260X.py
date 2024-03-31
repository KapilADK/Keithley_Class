import pyvisa as visa


class Keithley_260X():
    def __init__(self, GPIB):
        """
        Initialize a Keithley 260X SMU. 
        
        Parameters
        ----------
        
        GPIB = address of the connected SMU
        """
        self.GPIB = GPIB
        self.instrument = self.establish_connection()
        
    def establish_connection(self):
        """
        Establish connection between the PC and the SMU .
        """
        self.rm = visa.ResourceManager() # get a list of connected devices
        return self.rm.open_resource(f'GPIB::{self.GPIB}::INSTR')

    
    def identify(self):
        """
        Get the identification string of the SMU
        """
        return self.instrument.query('*IDN?').strip()
    
    def set_voltage(self, slot, voltage):
        """
        Sets a specified voltage to a specified slot

        Parameters
        ----------
        slot : integer
        voltage : float

        Returns
        -------
        None.

        """
        self.instrument.write('SOUR{}:VOLT {}'.format(slot, voltage))
    
    def get_voltage(self, slot):
        """
        Read voltage from a given slot.

        Parameters
        ----------
        slot : integer

        Returns
        -------
        voltage : float

        """
        return float(self.instrument.query('SOUR{}:VOLT?'.format(slot)))
    
    def enable_sources(self):
        """
        Enable the outputs

        Returns
        -------
        None.

        """
        self.instrument.write('OUTP ON')
        
    def disable_sources(self):
        """
        Disable the outputs

        Returns
        -------
        None.

        """
        self.instrument.write('OUTP OFF')

        
        
        