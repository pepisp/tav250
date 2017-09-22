import serial
from time import sleep
_ADDRESS=b'31'
_PREFIX=b'TX'+_ADDRESS
_SUFFIX=b'\r\n'




class TAV250(object):
    def __init__(self,device='/dev/ttyUSB0'):
        self.sp=serial.Serial(device,57600,timeout=1)
        self.onAir
 
    def __del__(self):
        self.sp.close()

    def __sendCmd(self,cmd):
        """Function for writing message to Tav device. It returns bare responce payload."""
        cmd=_PREFIX+cmd+_SUFFIX
#        print(cmd)
        self.sp.write(cmd)
        if int(cmd[4:6])>49:	#if write command then there is no response
#            print('Sending write command '+cmd[4:6]+' No response...')
            return '00'
        sleep(2)
#        print("if it was command i'm not supose to be here")
        resp=self.sp.readline()
        return resp[9:-3]
    @property
    def onAir(self):
#        print("i'm getter")
        resp=self.__sendCmd(b'45')
        self.__isOnAir=False
#        print(resp)
        if int(resp,16)&1:
            self.__isOnAir=True
        return self.__isOnAir
    @onAir.setter
    def onAir(self,isOnAir):
#        print("i' in setter")
        for atempt in range(1,5):
            if isOnAir:
#                print("Lets go onAir!!!")
                self.__sendCmd(b'5003')
#                self.__isOnAir=True
            else:
#                print('lets go offline')
                self.__sendCmd(b'5002')
#                self.__isOnAir=False
            sleep(1)
            if self.onAir==isOnAir:
                return True

        return False
	
    def GetPowerMeasures(self):
        """This function returns power mesuremetns related to the RF"""
        powerMeasures=self.__sendCmd(b'40')
        print(powerMeasures)
        FwdPwr=int(powerMeasures[0:4],16)*0.1
        RefPwr=int(powerMeasures[4:8],16)*0.1
        InPwr=int(powerMeasures[8:],16)*0.1
        sleep(0.2)
        return [FwdPwr,FwdPwr,InPwr]

    def GetCurrentMeasures(self):
        """This function returns currents on PA1-4 """
        currMeasures=self.__sendCmd(b'41')
        currents=[]
        for PA in range(0,9,2):
            currents.append(currMeasures[PA:PA+2])
        return currents

    def GetVoltageMeasures(self):
        """This function returns voltages on PA1-4 """
        currMeasures=self.__sendCmd(b'42')
        currents=[]
        for PA in range(0,9,2):
            currents.append(currMeasures[PA:PA+2])
        return currents
    def GetTempMeasures(self):
        temps=self.__sendCmd(b'43')
        print(temps)
        return [int(temps[0:4],16)*0.1,int(temps[4:],16)*0.1]

    def GetAlarms(self):
        """Function returns active alarms
        TODO: Check bit order 
        """
        alarms=self.__sendCmd(b'44')
        return alarms
if __name__=='__main__':
    tav=TAV250()
#    print(tav.GetPowerMeasures())
#    print(tav.GetCurrentMeasures())
#    print(tav.GetVoltageMeasures())
#    print(tav.GetTempMeasures())
#    sleep(0.1)
#    print(tav.GetAlarms())

    tav.onAir=True	    
    sleep(15)
    tav.onAir=False
    print(tav.onAir)	    
