"""Copyright 2008 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.5'
__date__ = 'October 23 2008'

from threading import *
from ctypes import *
from Phidgets.Phidget import *
from Phidgets.PhidgetException import *
import sys

class InterfaceKit(Phidget):
    """This class represents a Phidget Interface Kit. All methods to read and write data to and from an Interface Kit are implemented in this class.
    
    There are many types of Interface Kits, but each is simply a collection of 0 or more digital inputs, digital outpus and analog sensors.
    Inputs can be read and outputs can be set, and event handlers can be set for each of these.
    
    See your hardware documentation for more information on the I/O specific to your Phidget.
    
    Extends:
        Phidget
    """
    def __init__(self):
        """The Constructor Method for the InterfaceKit Class
        """
        Phidget.__init__(self)
        
        self.__inputChange = None
        self.__outputChange = None
        self.__sensorChange = None
        
        self.__onInputChange = None
        self.__onSensorChange = None
        self.__onOutputChange = None
        
        self.dll.CPhidgetInterfaceKit_create(byref(self.handle))
        
        if sys.platform == 'win32':
            self.__INPUTCHANGEHANDLER = WINFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_int)
            self.__OUTPUTCHANGEHANDLER = WINFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_int)
            self.__SENSORCHANGEHANDLER = WINFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_int)
        elif sys.platform == 'darwin' or sys.platform == 'linux2':
            self.__INPUTCHANGEHANDLER = CFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_int)
            self.__OUTPUTCHANGEHANDLER = CFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_int)
            self.__SENSORCHANGEHANDLER = CFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_int)

    def getInputCount(self):
        """Returns the number of ditigal inputs on this Interface Kit.
        
        Not all interface kits have the same number of digital inputs, and some don't have any digital inputs at all.
        
        Returns:
            The Number of analog inputs <int>.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached.
        """
        inputCount = c_int()
        result = self.dll.CPhidgetInterfaceKit_getInputCount(self.handle, byref(inputCount))
        if result > 0:
            raise PhidgetException(result)
        else:
            return inputCount.value

    def getInputState(self, index):
        """Returns the state of a digital input.
        
        Digital inputs read True where they are activated and False when they are in their default state.
        Be sure to check getInputCount first if you are unsure as to the number of inputs, so as not to set an Index that is out of range.
        
        Parameters:
            index<int>: Index of the input.
        
        Returns:
            State of the input <boolean>.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        inputState = c_int()
        result = self.dll.CPhidgetInterfaceKit_getInputState(self.handle, c_int(index), byref(inputState))
        if result > 0:
            raise PhidgetException(result)
        else:
            if inputState.value == 1:
                return True
            else:
                return False

    def __nativeInputChangeEvent(self, handle, usrptr, index, value):
        if self.__inputChange != None:
            if value == 1:
                state = True
            else:
                state = False
            device = self.getSerialNum()                                        ## Ruth: added the device arg
            self.__inputChange(InputChangeEventArgs(index, state, device))      ## Ruth: added the device arg
        return 0

    def setOnInputChangeHandler(self, inputChangeHandler):
        """Set the InputChange Event Handler.
        
        The input change handler is a method that will be called when an input on this Interface Kit has changed.
        
        Parameters:
            inputChangeHandler: hook to the inputChangeHandler callback function.
        
        Exceptions:
            PhidgetException
        """
        self.__inputChange = inputChangeHandler
        self.__onInputChange = self.__INPUTCHANGEHANDLER(self.__nativeInputChangeEvent)
        result = self.dll.CPhidgetInterfaceKit_set_OnInputChange_Handler(self.handle, self.__onInputChange, None)
        if result > 0:
            raise PhidgetException(result)

    def getSensorCount(self):
        """Returns the number of analog inputs on the Interface Kit.
        
        Not all interface kits have the same number of analog inputs, and some don't have any analog inputs at all.
        
        Returns:
            Number of analog inputs <int>.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached.
        """
        sensorCount = c_int()
        result = self.dll.CPhidgetInterfaceKit_getSensorCount(self.handle, byref(sensorCount))
        if result > 0:
            raise PhidgetException(result)
        else:
            return sensorCount.value

    def getSensorValue(self, index):
        """Returns the value of a analog input.
        
        The analog inputs are where analog sensors are attached on the InterfaceKit 8/8/8.
        On the Linear and Circular touch sensor Phidgets, analog input 0 represents position on the slider.
        
        The valid range is 0-1000. In the case of a sensor, this value can be converted to an actual sensor
        value using the formulas provided here: http://www.phidgets.com/documentation/Sensors.pdf
        
        Parameters:
            index<int>: Index of the sensor.
        
        Returns:
            The Sensor value <int>
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        sensorValue = c_int()
        result = self.dll.CPhidgetInterfaceKit_getSensorValue(self.handle, c_int(index), byref(sensorValue))
        if result > 0:
            raise PhidgetException(result)
        else:
            return sensorValue.value

    def getSensorRawValue(self, index):
        """Returns the raw value of a analog input.
        
        This is a more accurate version of getSensorValue. The valid range is 0-4095.
        Note however that the analog outputs on the Interface Kit 8/8/8 are only 10-bit values and this value represents an oversampling to 12-bit.
        
        Parameters:
            index<int>: Index of the sensor.
        
        Returns:
            The Raw Sensor value <int>
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        sensorValue = c_int()
        result = self.dll.CPhidgetInterfaceKit_getSensorRawValue(self.handle, c_int(index), byref(sensorValue))
        if result > 0:
            raise PhidgetException(result)
        else:
            return sensorValue.value

    def getSensorChangeTrigger(self, index):
        """Returns the change trigger for an analog input.
        
        This is the amount that an inputs must change between successive SensorChangeEvents.
        This is based on the 0-1000 range provided by getSensorValue. This value is by default set to 10 for most Interface Kits with analog inputs.
        
        Parameters:
            index<int>: Index of the sensor.
        
        Returns:
            The Trigger value <int>
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        sensitivity = c_int()
        result = self.dll.CPhidgetInterfaceKit_getSensorChangeTrigger(self.handle, c_int(index), byref(sensitivity))
        if result > 0:
            raise PhidgetException(result)
        else:
            return sensitivity.value

    def setSensorChangeTrigger(self, index, value):
        """Sets the change trigger for an analog input.
        
        This is the amount that an inputs must change between successive SensorChangeEvents.
        This is based on the 0-1000 range provided by getSensorValue. This value is by default set to 10 for most Interface Kits with analog inputs.
        
        Parameters:
            index<int>: Index of the sensor.
            value<int>: The Trigger Value.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        result = self.dll.CPhidgetInterfaceKit_setSensorChangeTrigger(self.handle, c_int(index), c_int(value))
        if result > 0:
            raise PhidgetException(result)

    def __nativeSensorChangeEvent(self, handle, usrptr, index, value):
        if self.__sensorChange != None:
            device = self.getSerialNum()                                        ## Ruth: added the device arg
            self.__sensorChange(SensorChangeEventArgs(index, value, device))    ## Ruth: added the device arg
        return 0

    def setOnSensorChangeHandler(self, sensorChangeHandler):
        """Set the SensorChange Event Handler.
        
        The sensor change handler is a method that will be called when a sensor on
        this Interface Kit has changed by at least the Trigger that has been set for this sensor.
        
        Parameters:
            sensorChangeHandler: hook to the sensorChangeHandler callback function.
        
        Exceptions:
            PhidgetException
        """
        self.__sensorChange = sensorChangeHandler
        self.__onSensorChange = self.__SENSORCHANGEHANDLER(self.__nativeSensorChangeEvent)
        result = self.dll.CPhidgetInterfaceKit_set_OnSensorChange_Handler(self.handle, self.__onSensorChange, None)
        if result > 0:
            raise PhidgetException(result)

    def getOutputCount(self):
        """Returns the number of digital outputs on this Interface Kit.
        
        Not all interface kits have the same number of digital outputs, and some don't have any digital outputs at all.
        
        Returns:
            The Number of digital outputs <int>.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached.
        """
        outputCount = c_int()
        result = self.dll.CPhidgetInterfaceKit_getOutputCount(self.handle, byref(outputCount))
        if result > 0:
            raise PhidgetException(result)
        else:
            return outputCount.value

    def getOutputState(self, index):
        """Returns the state of a digital output.
        
        Depending on the Phidget, this value may be either the value that you last wrote out to the Phidget, or the value that the Phidget last returned.
        This is because some Phidgets return their output state and others do not.
        This means that with some devices, reading the output state of a pin directly after setting it, may not return the value that you just set.
        
        Be sure to check getOutputCount first if you are unsure as to the number of outputs, so as not to attempt to get an Index that is out of range.
        
        Parameters:
            index<int>: Index of the output.
        
        Returns:
            State of the output <boolean>.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        outputState = c_int()
        result = self.dll.CPhidgetInterfaceKit_getOutputState(self.handle, c_int(index), byref(outputState))
        if result > 0:
            raise PhidgetException(result)
        else:
            if outputState.value == 1:
                return True
            else:
                return False

    def setOutputState (self, index, state):
        """Sets the state of a digital output.
        
        Setting this to True will activate the output, False is the default state.
        
        Parameters:
            index<int>: Index of the output.
            state<boolean>: State to set the output to.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if the index is out of range.
        """
        if state == True:
            value = 1
        else:
            value = 0
        result = self.dll.CPhidgetInterfaceKit_setOutputState(self.handle, c_int(index), c_int(value))
        if result > 0:
            raise PhidgetException(result)

    def __nativeOutputChangeEvent(self, handle, usrptr, index, value):
        if self.__outputChange != None:
            if value == 1:
                state = True
            else:
                state = False
            self.__outputChange(OutputChangeEventArgs(index, state))
        return 0

    def setOnOutputChangeHandler(self, outputChangeHandler):
        """Sets the OutputChange Event Handler.
        
        The output change handler is a method that will be called when an output on this Interface Kit has changed.
        
        Parameters:
            outputChangeHandler: hook to the outputChangeHandler callback function.
        
        Exceptions:
            PhidgetException
        """
        self.__outputChange = outputChangeHandler
        self.__onOutputChange = self.__OUTPUTCHANGEHANDLER(self.__nativeOutputChangeEvent)
        result = self.dll.CPhidgetInterfaceKit_set_OnOutputChange_Handler(self.handle, self.__onOutputChange, None)
        if result > 0:
            raise PhidgetException(result)

    def getRatiometric(self):
        """Gets the ratiometric state for the analog sensors
        
        Returns:
            State of the Ratiometric setting.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if this phidget does not support ratiometric.
        """
        ratiometricState = c_int()
        result = self.dll.CPhidgetInterfaceKit_getRatiometric(self.handle, byref(ratiometricState))
        if result > 0:
            raise PhidgetException(result)
        else:
            if ratiometricState.value == 1:
                return True
            else:
                return False

    def setRatiometric(self, state):
        """Sets the ratiometric state for the analog inputs.
        
        The default is for ratiometric to be set on and this is appropriate for most sensors.
        
        False - off
        True - on
        
        Parameters:
            state<boolean>: State of the ratiometric setting.
        
        Exceptions:
            PhidgetException: If this Phidget is not opened and attached, or if this Phidget does not support ratiometric.
        """
        if state == True:
            value = 1
        else:
            value = 0
        result = self.dll.CPhidgetInterfaceKit_setRatiometric(self.handle, c_int(value))
        if result > 0:
            raise PhidgetException(result)
