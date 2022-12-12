import pqFrame as pq
import pqBodyForecast as bf
import pandas as pd
import numpy as np

class WeeklyForecast:
    
    def __init__(self,lat,long):
        self.lat = lat
        self.long = long
        self.tf = pq.Transformations(self.lat,self.long)
        
        "Define available body set to view"
        self.body_set = ['moon','mercury','venus','mars','jupiter','saturn','uranus','neptune']

        
    def milkyway_this_week(self):
        """ Create milkyway_this_week function
            
            This function gathers uses data for sun altitude, timeframe give (a week),
            cloud coverage, delta time from start time, and body altitude-azimuth-distance 
            to calculate which body is the best one to observe this week.
            The cost function used in this function takes into account body altitude, 
            body distance compared to max and min distance values, and the cloud coverage
            at the location during the timeframe.
        """
        # Create DataFrame of celestial body locations in the backyard frames
        
        sun_altaz = self.tf.sun_for_me()
        timeframe = self.tf.timeframe
        delta_time = self.tf.delta_time
        clouds = self.tf.check_weather()
        
        # Define max and min distances of each body from earth (in AU).
        max_dist = np.array([0.0027,1.485,1.738,2.680,6.465,10.758,21.3,30.122])
        min_dist = np.array([0.0024,0.308,0.267,0.385,3.927,8.025,17.212,29.046])
        
        # Assign columns for dataframe that will be used
        df_best_time = pd.DataFrame(columns=['day','month','year','hour','minute','deltahrs','sunalt','bodyalt','bodyaz','bodydist','clouds','body'])
        
        # Create dictionary that will be used to add data to dataframe.
        for i,body in enumerate(self.body_set):
            
            body_altaz = self.tf.in_my_sky(body)
            per_body = []
            per_body = {'day': timeframe.ymdhms.day,
                        'month': timeframe.ymdhms.month,
                        'year': timeframe.ymdhms.year,
                        'hour': timeframe.ymdhms.hour,
                        'minute': timeframe.ymdhms.minute,
                        'deltahrs' : delta_time,
                        'sunalt': sun_altaz.alt,
                        'bodyalt' :body_altaz.alt,
                        'bodyaz' : body_altaz.az,
                        'bodydist': body_altaz.distance,
                        'clouds': np.repeat(clouds,288),
                        'body': body
                        }
            # Create dataframe.   
            df_body = pd.DataFrame(per_body)
            # Remove data for daytime by masking values where sun is above -18 deg altitude.
            df_body_night = df_body[df_body['sunalt']<-18]

            cost = []
            
            # Generate for loop to run all data in dataframe through cost function
            # and find best time, and best time index within dataframe.
            for idx in df_body_night.index:
                cost_val =  100*(df_body_night.clouds[idx])+10*abs(df_body_night.bodyalt[idx]-40) #+ 100*((max_dist[i]-min_dist[i])/2 - df_body_night.bodydist[idx])        
                cost.append(cost_val)
            
            i_best_time = cost.index(min(cost))
            df_best_time.loc[len(df_best_time.index)] = df_body_night.iloc[i_best_time]
        
        reward = []
    
        # Take into account distance, reward max value from formula for best 
        # Distance for planet during observation timeframe
        for idx in df_best_time.index:
            dist_avg = (max_dist[idx]-min_dist[idx])/2
            
            reward.append(1 - (df_best_time.bodydist[idx]/dist_avg))
        
        i_best_body = reward.index(max(reward))
        
        best_body = df_best_time.iloc[i_best_body].body
        
        return best_body
    
    def get_plot(self):
        """ Create get_plot function
        
            Plot results for the body found to be the best to observe this week.
            This uses the plotting function from BodyForecast.
        """
        best_body = self.milkyway_this_week()
        bf1 = bf.BodyForecast(self.lat,self.long,best_body)
        bf1.run_all()
        self.fig = bf1.fig
        self.figText = bf1.figText