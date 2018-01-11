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

    def __s16(self,value):
        return -(value & 0x8000) | (value & 0x7fff)

    def __sendCmd(self,cmd):
        """Function for writing message to Tav device. It returns bare responce payload."""
        cmd=_PREFIX+cmd+_SUFFIX
#        print(cmd)
        self.sp.write(cmd)
        if int(cmd[4:6])>49:	#if write command then there is no response
#            print('Sending write command '+cmd[4:6]+' No response...')
            return '00'
        sleep(0.5)
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
        FwdPwr=self.__s16(int(powerMeasures[0:4],16))*0.1
        RefPwr=self.__s16(int(powerMeasures[4:8],16))*0.1
        InPwr=self.__s16(int(powerMeasures[8:],16))*0.1
        sleep(0.2)
        return [FwdPwr,RefPwr,InPwr]

    def GetCurrentMeasures(self):
        """This function returns currents on PA1-4 """
        currMeasures=self.__sendCmd(b'41')
        currents=[]
        for PA in range(0,20,4):
            currents.append(int(currMeasures[PA:PA+4],16)*0.1)
        return currents

    def GetVoltageMeasures(self):
        """This function returns voltages on PA1-4 """
        currMeasures=self.__sendCmd(b'42')
        currents=[]
        for PA in range(0,20,4):
            currents.append(int(currMeasures[PA:PA+4],16)*0.1)
        return currents
    def GetTempMeasures(self):
        temps=self.__sendCmd(b'43')
        return [int(temps[0:4],16)*0.1,int(temps[4:],16)*0.1]

    def GetAlarms(self):
        """Function returns active alarms
        TODO: Check bit order
        """
        alarms=self.__sendCmd(b'44')
        return int(alarms,16)

    def GetAlarmsDict(self):
        """Function returns active alarms in form of dicionary
        """
        alarms=self.GetAlarms()
        alarmsDict={'ovr_drv':bool(alarms & 0x0001),'ref_pwr':bool(alarms & 0x0002),\
        'rf_temp':bool(alarms & 0x0004),'gain_l_drift':bool(alarms & 0x0008),\
        'psu1':bool(alarms & 0x0010),'psu2':bool(alarms & 0x0020)}
        return alarmsDict

    def GetStatus(self):
        """
            Function returns dicionary with aplifier status
        """
        status=int(self.__sendCmd(b'45'),16)
        statusDict={'on_air':bool(status & 0x0001),'remote':bool(status & 0x0002)}
        return statusDict

    def GetPowerSettings(self):
        """
            Function gets output power and Mode settings
        """
        response=self.__sendCmd(b'47')
        values=[response[0:2],int(response[2:6],16)*0.1,int(response[6:10],16)*0.1,int(response[10:14],16)*0.1]
        return values
    def SetPowerSettings(self,Value):
        """
            Function sets output power and Mode
            Mode=0x01 ALC Working Mode
        """
        #self.__sendCmd(b'5101023001F403D4')
        self.__sendCmd(b'510101F5023A0502')
        sleep(1)
        status=self.GetPowerSettings()

        return status

if __name__=='__main__':
    tav=TAV250()
    #print(tav.GetPowerMeasures())
    #print(tav.GetCurrentMeasures())
    #print(tav.GetVoltageMeasures())
    #print(tav.GetTempMeasures())
    #sleep(0.1)
    #print(tav.GetAlarms())
    #print(tav.GetAlarmsDict())
    print(tav.GetStatus())
    print(tav.SetPowerSettings(50))
#    tav.onAir=True
#    sleep(15)
#    tav.onAir=False
#    print(tav.onAir)
