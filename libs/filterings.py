

class FilteringManager:



    def filter_acceleration(self, x_axis_acceleration, x_samples_counter):
        if x_axis_acceleration[x_samples_counter] <= 6:  # threshold
            x_axis_acceleration[x_samples_counter] = 0
        elif x_axis_acceleration[x_samples_counter]-x_axis_acceleration[x_samples_counter-1] <= 5:
            x_axis_acceleration[x_samples_counter] = x_axis_acceleration[x_samples_counter]
        if x_axis_acceleration[x_samples_counter] > 127:  # sign in order to direction
            x_axis_acceleration[x_samples_counter] = (255 - x_axis_acceleration[x_samples_counter] + 1) * -1

    def filter_aceleration_pro(self,aceleration,bool):
        if bool == True:
            for i in range (len(aceleration)-1):
                if aceleration[i]<=4:
                    aceleration[i]=0
                elif aceleration[i]-aceleration[i-1]<=5:
                    aceleration[i]=aceleration[i]
                if aceleration[i]>127:
                    aceleration[i]=(255-aceleration[i]+1)*-1
        else:
            for i in range (len(aceleration)):
                if aceleration[i]<=4:
                    aceleration[i]=0
                elif aceleration[i]-aceleration[i-1]<=5:
                    aceleration[i]=aceleration[i]
                if aceleration[i]>127:
                    aceleration[i]=(255-aceleration[i]+1)*-1



