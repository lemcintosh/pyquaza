import pqFrame as pq
import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt, dates
from astropy.visualization import astropy_mpl_style

def cost_fx(cloud,alt):
    """ Define Cost function for finding the best time to observe a specified body
    
    Args: Cloud coverage value for given location and altitude value for body
    
    Returns: Calculated cost for each observation time within the given week
    
    """
    # Cost Calculation gives highest cost to cloud coverage because reduced visibility
    # prevents good observation opportunity
    cost = 100*(cloud)+((abs(alt-40)*10))
    return cost

class BodyForecast:
    """ Create class BodyForescast
    
        Attributes: lat (Latitude),
                    long (Longitude),
                    body (Celestial Body of choice)
                    tf (transformation data from pq.Transformations)
                    
        Functions:  body_this_week,
                    set_body_df,
                    set_body_df,
                    cut_daytime,
                    best_time,
                    plot_one_body
                    
        Functions within this class help gather and analyze data to provide
        the user with the best viewing time for a selected body within 
        a week time frame from a given location.
    """
    
    # Use built in Python method to assign latitude, longitude, body,
    # and pq.Transformation values.
    def __init__(self, lat, long, body):
        self.lat = lat
        self.long = long
        self.body = body
        self.tf = pq.Transformations(self.lat, self.long)
        
    def body_this_week(self):
        """ Create body_this_week function
        
            Takes data from pq.Transformations and converts it to the necessary
            data for this module: Body altitude-azimuth, Sun Altitude-Azimuth,
            time frame for observation, and delta time from starting time.
        """
        
        self.body_altaz = self.tf.in_my_sky(self.body)
        self.sun_altaz = self.tf.sun_for_me()
        self.timeframe = self.tf.timeframe
        self.delta_time = self.tf.delta_time
        
        return self.body_altaz, self.sun_altaz, self.timeframe, self.delta_time
    
    
    def set_body_df(self):
        """ Create set_body_df function
            
            Takes data obtained in body_this_week and generates a dataframe
            that can be easily used in future functions.
        """
        
        # Create cloud coverage data set.
        clouds = self.tf.check_weather()
        
        # Generate dictionary with all data needed for future analysis.
        data = {'day': self.timeframe.ymdhms.day,
                'month': self.timeframe.ymdhms.month,
                'year': self.timeframe.ymdhms.year,
                'hour': self.timeframe.ymdhms.hour,
                'minute': self.timeframe.ymdhms.minute,
                'deltahrs' : self.delta_time,
                'sunalt': self.sun_altaz.alt,
                'bodyalt' :self.body_altaz.alt,
                'bodyaz' : self.body_altaz.az,
                'clouds': np.repeat(clouds,288)}
        
        # Convert dictionary into data frame.
        self.dataframe = pd.DataFrame(data)
        
        return self.dataframe
    
    def cut_daytime(self):
        """ Create cut_daytime function
            
            Removes all daytime data from dataframe generated in set_body_df
            by removing all values where the sun altitude is above -18 degrees
            of the observers horizon. 
            This helps reduce the data points used in analysis and thus makes
            the program run faster.
        """
        
        # Use mask to remove daytime data
        self.df_night = self.dataframe[self.dataframe['sunalt']<-18]
        
        return self.df_night
    
    
    def best_time(self):
        """ Create best_time function
        
            Calculates cost value for all data points in dataframe that remains
            after cut_daytime function is performed.
            This function will calculate the minimal cost value and return
            the best time and best date for observing the desired body.
        """
        
        cost = []
        
        # Generate for loop to run all data points through cost function and
        # add values to cost list.
        for i in self.df_night.index:
            cost.append(cost_fx(self.df_night.clouds[i],self.df_night.bodyalt[i]))
        
        # Find min cost and obtain values using the index.
        self.i_best = cost.index(min(cost))
        self.best_time_val = self.df_night.iloc[self.i_best]
        best_day = self.best_time_val.day
        self.best_night = self.df_night[self.df_night['day']==best_day]
        
        return self.best_time_val, self.best_night, self.i_best
    
    
    def plot_onebody(self):
        """ Create plot_onebody function
        
            Takes data obtained in best_time and set_body_df to create plot 
            for desired body best observation time and also plot the data
            for the night when the body can be best observed. 
            If values for observations are below horizon (altitude > 0), then
            body cannot be observed from user's location and message will
            appear instead of plot.
        """
        # Get best time values using index obrained in best_time function.
        df_best_time = self.df_night.iloc[self.i_best]
        # Remove values where body would be below horizon
        cut_negative = self.best_night[self.best_night['bodyalt']>0]
        
        # Open subplot.
        fig, ax = plt.subplots();
        
        # Generate variables so that it is easier to write in plot functions.
        day = int(self.best_time_val.day)
        month = int(self.best_time_val.month)
        year = int(self.best_time_val.year)
        hour = int(self.best_time_val.hour)
        minute = int(self.best_time_val.minute)
        cloud = int(self.best_time_val.clouds)
        az = self.best_time_val.bodyaz
        
        # Create if statement. If dataframe is empty after removing values where
        # body is below horizon, then give message that body is not visible at the time.
        if cut_negative.empty:
            fig = plt.figure(figsize = (12,8))
            plt.grid(False)
            plt.annotate('Body cannot be seen this week.',(0.5,0.5),ha='center',va='center',fontsize=24)
            plt.savefig('body.png')
            figText = ""
            plt.close()
        
        # Otherwise, plot best time to observe and body location throughout the
        # night when it is best to observe it.
        else:
            besttime = self.dataframe.loc[self.dataframe['deltahrs'] == df_best_time.deltahrs]
            besttimei = besttime.index
            besttime_dt = datetime(int(besttime.year), int(besttime.month), int(besttime.day), int(besttime.hour), int(besttime.minute))
            besttime_alt = besttime.bodyalt

            index = np.arange(besttimei[0]-10,besttimei[0]+11,1)
            dts = []
            alts = []
            azs = []
            
            # Create data sets with date, body altitude, and body azimuth to plot using for loop.
            for i in index:
                bfdf = self.dataframe.iloc[[i]]
                dts.append(datetime(int(bfdf.year), int(bfdf.month), int(bfdf.day), int(bfdf.hour), int(bfdf.minute)))
                alts.append(bfdf.bodyalt)
                azs.append(bfdf.bodyaz)
            
            # Plot datasets obtained. Azimuth will be plotted as a color gradient,
            # The overall plot will have a star for denoting the best time for observation
            # and the body's altitude throught the same night plotted.
            plt.style.use(astropy_mpl_style);            
            ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d %H:%M'));
            for label in ax.get_xticklabels(which='major'):
                label.set(rotation=30, horizontalalignment='right');
            plt.plot(besttime_dt, besttime_alt, 'r*', markersize = 10, label = 'Best Time to Observe');
            plt.scatter(dts, alts, c=azs, label= f'{self.body.capitalize()}', lw=0, s=15, cmap='viridis');
            plt.colorbar().set_label('Azimuth [deg]');
            plt.legend(loc = 'upper right');
            plt.ylim(0, 90);
            plt.xlabel('Viewing Date & Time');
            plt.ylabel('Altitude [deg]');
            plt.tight_layout()
            plt.savefig('body.png', dpi=800)
            plt.close()
            figText = f"Best View Date: \n{month}/{day}/{year} \n\nBest View Time: \n{hour} HR {minute} min \n\nCloud Coverage: \n{cloud}% \n\nAzimuth Position: \n{az:.2f}°"
            
        self.fig = fig
        self.figText = figText
        
        return 
    
    def run_all(self):
        
        self.body_this_week()
        self.set_body_df()
        self.cut_daytime()
        self.best_time()
        self.plot_onebody()
        return