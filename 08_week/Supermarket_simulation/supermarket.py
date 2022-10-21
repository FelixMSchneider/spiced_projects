import numpy as np
import pandas as pd
import pylab as plt


from customer import Customer

class SuperMarket:
    def __init__(self,pm):
        self.start_hour=8
        self.stop_hour=22
        self.year=2020
        self.month=1
        self.day=1
        self.current_time=pd.Timestamp(self.year,self.month,self.day,self.start_hour,0,0)
        self.pm=pm
        #self.nocust=poisson(1.0, 1)
        
    def number_of_customers(self):
        from numpy.random import poisson
        self.newcust_per_min=poisson(1.0, 1)[0] # [0] to get frist element of the array
    
    def run_day_simulator(self):
        cust_cnt=0
        self.cust_dict={}
        while self.current_time < pd.Timestamp(self.year,self.month,self.day,self.stop_hour,0,0):
            self.number_of_customers()
            print(self.current_time)
            for _ in range(self.newcust_per_min):
                cust_cnt+=1
                cust = Customer(self.current_time, cust_cnt+10000, self.pm)
                cust.do_shopping()
                custkey="cust_"+str(cust.cust_id)
                self.cust_dict[custkey]={}
                self.cust_dict[custkey]["track"]=cust.track
                self.cust_dict[custkey]["times"]=cust.timings
            self.current_time=self.current_time + pd.Timedelta("60s")
  
if __name__ == "__main__":

    import pylab as plt

    pm=pd.read_csv("propability_matrix.csv")     
    pm.set_index("location",inplace=True)

    SM=SuperMarket(pm)

    SM.run_day_simulator()
    print(SM.cust_dict)

    import pickle
    pickle.dump(SM.cust_dict, open("custor_dict.pickle", "wb"))
 
