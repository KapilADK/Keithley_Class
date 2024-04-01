import pyvisa as visa
import time

class Keithley_260X():
    
    opc_calls_per_second = 10 # frequency to check the completion status of a operation
    
    def __init__(self, GPIB, slot = None):
        """
        Initialize a Keithley 260X SMU. 
        
        Parameters
        ----------
        GPIB : int
            identifier assigned to the SMU connected to a GPIB network
        slot : int
            channel to set or get voltage
            
        Return
        -----
        None
        
        """
        self.GPIB = GPIB
        self.instrument = self.establish_connection()
        
        print("Connection established..........")
        print("")
        print(f"The identification of the SMU is {self.identify()}")
        
        if slot is None:
            raise ValueError(f"Specify a slot for {self.__class__.__name__}: (1 for slot 'a', 2 for slot 'b') ")
        elif slot == 1:
            self.slot = "a"
        elif slot == 2:
            self.slot = "b"
        else:
            raise ValueError(f"Invalid slot '{slot}'. Valid slots are 1 or 2.")
        
        
    def establish_connection(self):
        """
        Establish connection between the PC and the SMU .
        """
        self.rm = visa.ResourceManager() # get a list of connected devices
        return self.rm.open_resource(f"GPIB::{self.GPIB}::INSTR")

    
    def identify(self):
        """
        Get the identification string of the SMU
        
        Return
        ------
        str
        """
        return self.instrument.query('*IDN?').strip()
    
    def is_busy(self):
        """
        Checks if there are any pending operations
        """
        status = int(self.instrument.query("*OPC?"))
        if status == 0:
            return True
        else:
            return False
    
    def enable_sources(self, opc = True):
        """
        Enable the outputs

        Returns
        -------
        None.
        """
        self.instrument.write(f"smu{self.slot}.source.output = smu{self.slot}.OUTPUT_ON")
        if opc:
            while self.is_busy():
                time.sleep(1/ self.opc_calls_per_second)
        
    def disable_sources(self, opc = True):
        """
        Disable the outputs

        Returns
        -------
        None.
        """
        self.instrument.write(f"smu{self.slot}.source.output = smu{self.slot}.OUTPUT_OFF")
        if opc:
            while self.is_busy():
                time.sleep(1/ self.opc_calls_per_second)
                
    def set_voltage(self, voltage_V, opc = True):
        """
        Sets a specified voltage to a specified slot. Don't forget to enable the sources before specifying a voltage.

        Parameters
        ----------
        voltage_V : float

        Returns
        -------
        None.
        """
            
        self.instrument.write(f"smu{self.slot}.source.func = smu{self.slot}.OUTPUT_DCVOLTS")
        if opc:
            while self.is_busy():
                time.sleep(1/self.opc_calls_per_second) 
        self.instrument.write(f"smu{self.slot}.source.levelv = {voltage_V}")
        if opc:
            while self.is_busy():
                time.sleep(1/self.opc_calls_per_second) 
    
    def get_voltage(self):
        """
        Read voltage from a given slot.

        Parameters
        ----------
        None
        
        Returns
        -------
        voltage : float
        """
        voltage = float(self.instrument.query(f"smu{self.slot}.measure.v"))
        return voltage
    
  
        
        