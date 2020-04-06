# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:40:28 2020
    Basic example script that uses import_systems_link_data to plot data

@author: Peter
"""

from EnergyUse_Class import EnergyUse

# Extract data from csv

Dicts = EnergyUse()
Dicts.import_systems_link_data('MSM subs Jan+Feb20.csv')


print(len(Dicts.data))


#%% Remove data with only zero valued results

Dicts.clean(True, False)

print(len(Dicts.data))

#%% Remove data with any negative valued results

Dicts.clean(False, True)

print(len(Dicts.data))


#%%
#Dicts.plot_all()

Dicts.data[0]['Datetimes']
