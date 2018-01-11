import tav250

tav=tav250.TAV250()



powerMeasures=tav.GetPowerMeasures()
currents=tav.GetCurrentMeasures()
voltages=tav.GetVoltageMeasures()
temps=tav.GetTempMeasures()
alarms=tav.GetAlarmsDict()
status=tav.GetStatus()

measures_str='tav_pwr_meas FwdPwr={0[0]},RefPwr={0[1]},InPwr={0[2]},\
PA1_current={1[0]},PADRV_current={1[4]},PA1_voltage={2[0]},\
PADRV_voltage={2[4]}'.format(powerMeasures,currents,voltages)
temps_str='tav_temp temp={0[0]:2}'.format(temps)
alarms_str='tav_alarms rf_temp={rf_temp},psu1={psu1},\
ref_pwr={ref_pwr},psu2={psu2},gain_l_drift={gain_l_drift},ovr_drv={ovr_drv}'.format(**alarms)
status_str='tav_status on_air={on_air},remote={remote}'.format(**status)
print(measures_str)
print(temps_str)
print(alarms_str)
print(status_str)
