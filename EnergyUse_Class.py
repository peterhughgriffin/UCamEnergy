import numpy as np
import matplotlib.pyplot as plt
import datetime

class EnergyUse:
    """Main Data class"""
    def __init__(self):
        pass

    def import_systems_link_data(self,filename,strip_empty=False):
        """
        Inputs: a path to a .csv file from the systemslink bulk data export
        Outputs: a list of dictionaries, each one corresponding to a different meter.
        """
        self.filename = filename
        
        with open(filename) as infile: 
            # Skip the first 3 lines, seems to just be header info
            for _ in range(3):
                next(infile) 
            
            # Create empty list, append each dictionary
            dicts=[]
            for line in infile:
                # For each line, create a dictionary with all the info
                data = line[:].split(",")
                datetimes=np.empty(48,dtype=object)
                datetime_start=datetime.datetime.strptime(data[6], '%d/%m/%Y')
                for i in range(48):
                    datetimes[i] = datetime_start + datetime.timedelta(minutes=30*i)            
                values=[float(number) for number in data[7:7+48]]
                day_dict = {
                    "Data Set Type":data[0],
                    "Site Name":data[1],
                    "Site Code":data[2],
                    "Reference Number":data[3],
                    "MPAN":data[4],
                    "Meter Serial Number":data[5],
                    "Date":data[6],
                    "Datetimes":datetimes,
                    "Values":values,
                }
                # Append this to the first list of dictionaries
                if strip_empty:
                    if not sum(values)==0:
                        dicts.append(day_dict)
                else:
                    dicts.append(day_dict)
                
            # Sort the dictionaries by reference code, then by date
            sorted_dicts = sorted(dicts, key = lambda x: (x["Reference Number"], x["Datetimes"][0]))
            
            # Merge all datetimes and values for dictionaries with the same reference number
            merged_dicts = []
            temp_dict = sorted_dicts[0]
            for i in range(len(sorted_dicts)-1):
                if sorted_dicts[i]["Reference Number"] == sorted_dicts[i+1]["Reference Number"]:
                    temp_dict["Datetimes"] = np.concatenate((temp_dict["Datetimes"],sorted_dicts[i+1]["Datetimes"]))
                    temp_dict["Values"] = temp_dict["Values"] + sorted_dicts[i+1]["Values"]
                else:
                    merged_dicts.append(temp_dict)
                    temp_dict=sorted_dicts[i+1]
                    
        self.data = merged_dicts
    
    def plot_all(self):
        for n in self.data:
            plt.plot(n["Datetimes"],n["Values"])
            
            
    def clean(self,empty, neg):
        """
        A function to remove invalid data, should be some flexibility about what is removed (see issue #1)
        empty - Binary flag to select if empty data is removed (True) or not (False)
        neg - Binary flag to select if negative data is removed (True) or not (False)
        """
        if empty:
            self.data= [i for i in self.data if not all(v==0 for v in i["Values"])]

        if neg:
            self.data= [i for i in self.data if not any(v <0 for v in i["Values"])]


       
    def filter(self,start_date, end_date):
        # A function to filter data to a given date range (see issue #2)
        pass
        