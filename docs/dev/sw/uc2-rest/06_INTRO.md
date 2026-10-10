# UC2-REST

:::warning Outdated
Current documentation: [uc2rest reference](../interface/reference/python-uc2rest.md).
:::

This explains the basic functionality of the UC2-REST Python interface in conjunction with the UC2-ESP32 mainboard. This was mostly designed to interface with ImSwitch.

The main repositories:
- https://github.com/openUC2/UC2-REST/
- https://github.com/youseetoo/uc2-esp32
- https://github.com/openUC2/imswitch


Available modules:

```py
    def __init__(self, host=None, port=31950, serialport=None, identity="UC2_Feather", baudrate=BAUDRATE, NLeds=64, SerialManager=None, DEBUG=False, logger=None):
        '''
        This client connects to the UC2-REST microcontroller that can be found here
        https://github.com/openUC2/UC2-REST

        generally speaking you send/receive JSON documents that will cause an:
        1. action => "/XXX_act"
        2. getting => "/XXX_get"

        you can send commands through wifi/http or usb/serial
        '''
        if logger is None:
            self.logger = Logger()
        else:
            self.logger = logger

        # perhaps we are in the browser?
        self.isPyScript = False

        # initialize communication channel (# connect to wifi or usb)
        if serialport is not None:
            # use USB connection
            self.serial = Serial(serialport, baudrate, parent=self, identity=identity, DEBUG=DEBUG)
            self.is_serial = True
            self.is_connected = self.serial.is_connected
            self.serial.DEBUG = DEBUG
        elif host is not None:
            # use client in wireless mode
            self.is_wifi = True
            self.host = host
            self.port = port

            # check if host is up
            self.logger.debug(f"Connecting to microscope {self.host}:{self.port}")
            #self.is_connected = self.isConnected()
        elif SerialManager is not None:
            # we are trying to access the controller from .a web browser
            self.serial = SerialManagerWrapper(SerialManager, parent=self)
            self.isPyScript = True
        else:
            self.logger.error("No ESP32 device is connected - check IP or Serial port!")


        if not self.isPyScript: from .updater import updater

        # import libraries depending on API version
        self.logger.debug("Using API version 2")        

        #FIXME
        #self.set_state(debug=False)

        # initialize state
        self.state = State(self)
        if not self.isPyScript:
            state = self.state.get_state()

        # initialize config
        if not self.isPyScript:
            self.config = config(self)

        # initialize cmdRecorder
        self.cmdRecorder = cmdRecorder(self)

        # initialize LED matrix
        self.led = LedMatrix(self, NLeds=NLeds)

        # initilize motor
        self.motor = Motor(self)

        # initialize rotator
        self.rotator = Rotator(self)

        # initiliaze homing
        self.home = Home(self)

        # initialize temperature
        self.temperature = Temperature(self)

        # initialize laser
        self.state = State(self)

        # initialize galvo
        self.galvo = Galvo(self)

        # initialize laser
        self.laser = Laser(self)

        # initialize wifi
        self.wifi = Wifi(self)

        # initialize camera
        self.camera = Camera(self)

        # initialize analog
        self.analog = Analog(self)

        # initialize digital out
        self.digitalout = DigitalOut(self)

        # initialize messaging
        self.message = Message(self)

        # initialize config
        if False: # not self.isPyScript:
            self.config = config(self)
            try: self.pinConfig = self.config.loadConfigDevice()
            except: self.pinConfig = None

        # initialize updater
        if not self.isPyScript:
            try: self.updater = updater(parent=self)
            except: self.updater = None

        # initialize module controller
        self.modules = Modules(parent=self)
```
