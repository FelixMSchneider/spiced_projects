'''
Customer Class
'''
import random
import pandas as pd


class Customer:
    '''
    Customer Class
    '''
    def __init__(self, entry_time,custid,probability_matrix):
        '''
        Initialization of Customer
        '''
        self.location = "entry"
        self.probability_matrix = probability_matrix
        assert type(entry_time) == pd._libs.tslibs.timestamps.Timestamp , "entry time has to be pandas.Timestamp"
        self.current_time = entry_time
        self.cust_id=custid

    def do_next_move(self):
        '''
        Moves Custumer 1 step forward in time and update the self.location based on the propabilities given in probability_matrix
        '''
        pm=self.probability_matrix
        locations=list(pm.columns)
        probabilities=pm.loc[self.location]
        if self.location != "entry":
            self.current_time = self.current_time + pd.Timedelta("60s")
        self.location=random.choices(locations,weights=list(probabilities))[0]

    def do_shopping(self):
        '''
        Let a custumer (initiaized at entry) do the random walk through the supermarket until it reaches the checkout.
        At 22 o clock checkout is forced
        '''
        self.track=[self.location,]
        self.timings=[self.current_time,]
        while self.location !="checkout":
            self.do_next_move()
            if self.current_time.hour >= 22:
                self.track.append("checkout")
                self.timings.append(self.current_time)
                break
            self.track.append(self.location)
            self.timings.append(self.current_time)
        self.get_times()

    def get_times(self):
        '''
        convert Timestamp to Hour:Minutes string
        '''
        hours   = [t.hour   for t in self.timings]
        minutes = [t.minute for t in self.timings]
        self.times=[str(h).zfill(2) + ":"+ str(minutes[i]).zfill(2) for i,h in enumerate(hours)]

    def plot(self):
        '''
        plot the random walk of the customer
        '''
        import pylab as plt
        plt.plot(self.times, self.track, "o")
        plt.plot(self.times, self.track, "--")
        plt.show()

if __name__ == "__main__":

    pm=pd.read_csv("propability_matrix.csv")
    pm.set_index("location",inplace=True)

    cust=Customer(pd.Timestamp(2020,1,1,12,59,0),1,pm)
    cust.do_shopping()
    cust.plot()
