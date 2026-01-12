from AMAT.planet import Planet
from AMAT.vehicle import Vehicle
import numpy as np
import matplotlib.pyplot as plt

# Set up the planet and atmosphere model.
planet=Planet("EARTH")    
planet.loadAtmosphereModel('../atmdata/Earth/earth-gram-avg.dat', 0 , 1 ,2, 3)

# Create a vehicle object flying in the target planet atmosphere.

# Set up the vehicle : 
# vehicle = Vehicle('X', m = 300 kg, beta = 78.0, L/D = 0.35, A = 3.1416, AoA = 0, RN = 1.54, planet)

vehicle = Vehicle('Starship', 120000.0, 190.0, 0.30, 65.0, 80.0, 0.50, planet)

# Set up entry parameters
# h0 = 180 km, LON = 0 deg, LAT = 0 deg
# v0 = 12 km/s, HDG = 0 deg, FPA = 0 deg
# DOWNRANGE0 = 0 deg, HEATLOAD0 = 0.
vehicle.setInitialState(120.0, 0.0, 0.0, 7.5, 0.0, -1.8, 0.0, 0.0)

# Set up solver
vehicle.setSolverParams(1E-6)

# Propogate vehicle entry trajectory
vehicle.propogateEntry (2400.0,0.1,0.0)
# bank angle = 70 deg arbitrary, actual profile will give more realistic results

# import rcParams to set figure font type
from matplotlib import rcParams



# Extract and save variables to plot
t_min_os         = vehicle.t_minc
h_km_os          = vehicle.h_kmc
acc_net_g_os     = vehicle.acc_net_g
q_stag_con_os    = vehicle.q_stag_con
q_stag_rad_os    = vehicle.q_stag_rad


# Extract and save variable to plot
t_min_us         = vehicle.t_minc
h_km_us          = vehicle.h_kmc
acc_net_g_us     = vehicle.acc_net_g
q_stag_con_us    = vehicle.q_stag_con
q_stag_rad_us    = vehicle.q_stag_rad


fig = plt.figure(figsize=(12,8))
plt.rc('font',family='Times New Roman')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

plt.subplot(2, 2, 1)
plt.plot(vehicle.v_kmsc, vehicle.h_kmc, 'k-', linewidth=2.0)
plt.xlabel('Speed, km/s',fontsize=14)
plt.ylabel('Altitude, km', fontsize=14)
ax=plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.tick_params(axis='x',labelsize=14)
ax.tick_params(axis='y',labelsize=14)

plt.subplot(2, 2, 2)
plt.plot(vehicle.acc_net_g, vehicle.h_kmc, 'b-', linewidth=2.0)
plt.xlabel('Deceleration, Earth g',fontsize=14)
plt.ylabel('Altitude, km', fontsize=14)
ax=plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.tick_params(axis='x',labelsize=14)
ax.tick_params(axis='y',labelsize=14)

plt.subplot(2, 2, 3)
plt.plot(vehicle.q_stag_total, vehicle.h_kmc,'r-', linewidth=2.0)
plt.xlabel('Stagnation point heat-rate, '+r'$W/cm^2$',fontsize=14)
plt.ylabel('Altitude, km', fontsize=14)
ax=plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.tick_params(axis='x',labelsize=14)
ax.tick_params(axis='y',labelsize=14)


plt.subplot(2, 2, 4)
plt.plot(vehicle.heatload/1.0E3, vehicle.h_kmc, 'm-', linewidth=2.0)
plt.xlabel('Stagnation point heat-load, '+r'$kJ/cm^2$',fontsize=14)
plt.ylabel('Altitude, km', fontsize=14)
ax=plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.tick_params(axis='x',labelsize=14)
ax.tick_params(axis='y',labelsize=14)

plt.savefig('../plots/paet-earth.png',bbox_inches='tight')
plt.savefig('../plots/paet-earth.pdf', dpi=300,bbox_inches='tight')
plt.savefig('../plots/paet-earth.eps', dpi=300,bbox_inches='tight')


fig = plt.figure()
fig.set_size_inches([5,5])
plt.rc('font',family='Times New Roman')
plt.plot(t_min_os , q_stag_con_os, linestyle='solid' , color='xkcd:blue',linewidth=1.0,  label='Overshoot convective')
#plt.plot(t_min_os , q_stag_rad_os, linestyle='solid' , color='xkcd:red',linewidth=1.0,  label='Overshoot radiative')
plt.plot(t_min_us , q_stag_con_us, linestyle='solid' , color='xkcd:magenta',linewidth=1.0,  label='Undershoot convective')
#plt.plot(t_min_us , q_stag_rad_us, linestyle='solid' , color='xkcd:green',linewidth=1.0,  label='Undershoot radiative')

plt.xlabel('Time, min',fontsize=10)
plt.ylabel("Stagnation-point heat rate, "+r'$W/cm^2$',fontsize=10)

ax = plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
plt.tick_params(direction='in')
plt.tick_params(axis='x',labelsize=10)
plt.tick_params(axis='y',labelsize=10)

plt.legend(loc='upper right', fontsize=8)


plt.savefig('../plots/craig-lyne-heating.png',bbox_inches='tight')
plt.savefig('../plots/craig-lyne-heating.pdf', dpi=300,bbox_inches='tight')
plt.savefig('../plots/craig-lyne-heating.eps', dpi=300,bbox_inches='tight')

plt.show()

data = np.column_stack((q_stag_con_us, t_min_us*60.0))
np.savetxt( r"C:\Users\imull\OneDrive\Bureau\AMAT\AMAT\examples\flux_vs_time.csv", 
           data, delimiter=",", 
           header="flux_W_cm2,time_sec", 
           comments="" )