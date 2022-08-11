# Detect-Distance-D435i

The purpose of this application is to calculate a desired distance between certain objects in a given image. 
User must have D435i camera connected via USB and the RealSense SDK installed to run the program. Currently displaying incorrect distance, final calibration must be done. This work has been done by Maryum Fatima during the SU22 CCI internship. 

Options include saving the camera recording as a bag file or using an image as a .png file to compute distance.

Need to enable hole-filling to not display '0.0 meters' using rs2.spatial_filter()
