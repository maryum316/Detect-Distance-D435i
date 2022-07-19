import pyrealsense2 as rs
import numpy as np
import cv2
import math 
import matplotlib.pyplot as plt
 
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
 
# Get camera device and enable stream
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
 
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
 
# Start streaming
profile = pipeline.start(config)
 
align_to = rs.stream.depth
align = rs.align(align_to)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
 
 
try:
   while True:
 
       # Wait for a coherent pair of frames: depth and color
       frames = pipeline.wait_for_frames()
       depth_frame = frames.get_depth_frame()
       color_frame = frames.get_color_frame()
       if not depth_frame or not color_frame:
           continue
 
       # Convert images to numpy arrays
       depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
       depth_image = np.asanyarray(depth_frame.get_data())
       color_image = np.asanyarray(color_frame.get_data())
 
       # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
       depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.10), cv2.COLORMAP_JET)
 
       depth_colormap_dim = depth_colormap.shape
       color_colormap_dim = color_image.shape
 
       # If depth and color resolutions are different, resize color image to match depth image for display
       if depth_colormap_dim != color_colormap_dim:
           resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
           images = np.hstack((resized_color_image, depth_colormap))
       else:
           images = np.hstack((color_image, depth_colormap))
 
        # Show images
       cv2.namedWindow('Camera View', cv2.WINDOW_AUTOSIZE)
       cv2.imshow('Camera View', images)
       key = cv2.waitKey(1)
       if key & 0xFF == ord('q') or key == 27:
           cv2.destroyAllWindows()
 
 
 
       if key==115: # Press 's' to save
           img = cv2.waitKey(0)
           print('picture was taken')
          
 
       if key==114: # Press 'r' for distance between two points
           xOne = input("Enter the first x-coordinate: ")
           yOne = input("Enter the first y-coordinate: ")
           zOne = 0
 
           xTwo = input("Enter the second x-coordinate: ")
           yTwo = input("Enter the second y-coordinate: ")
           zTwo = 0
 
           distTwoPoints = round(math.sqrt(((int(xTwo) - int(xOne)) ** 2) + ((int(yTwo) - int(yOne)) ** 2) + ((int(zTwo) - int(zOne)) ** 2)))
           # Converts from pixels to meters
           distTwoPoints = distTwoPoints * 0.0002645833       
           print("The distance between the two coordinates is: ", distTwoPoints)
 
 
       if key==111: # Press 'o' for distance from middle pixel
           x, y = 320, 240  # this had to be half of the resolution 640x480, this takes the distance from the center of the window
 
           depth = round(depth_frame.get_distance(x, y), 3)
           color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
           dx ,dy, dz = rs.rs2_deproject_pixel_to_point(color_intrin, [x,y], depth)
           distance = round(math.sqrt(((dx)**2) + ((dy)**2) + ((dz)**2)), 3)
 
           print("Distance from camera to pixel (meters):", distance)
           print("Z-depth from camera surface to pixel surface (meters):", depth)
 
       if key==109: # Press 'm' for meshgrid
           x = np.linspace(0, 639, 640)
           y = np.linspace(0, 479, 480)
           xx, yy = np.meshgrid(x, y)
           zz = np.sqrt(xx**2 + yy**2) # use distance formula?
           xs, ys = np.meshgrid(x, y)
           zs = np.sqrt(xs**2 + ys**2)
           xs.shape, ys.shape, zs.shape
           np.array_equal(zz, zs)
 
           h = plt.contourf(x, y, zs)
           plt.axis('scaled')
           plt.title("Distance Values")
           plt.xlabel("640")
           plt.ylabel("480")
           plt.colorbar()
           plt.show()
 
 
       if key==108: # Press 'l' for clicking points in image window
          
           def click_event(event, x11, y11, flags, param):
               if event == cv2.EVENT_LBUTTONDOWN:
                   point1 = (x11,y11)
                   print(point1)
          
                   if event == cv2.EVENT_LBUTTONDOWN:
                           x12, y12 = event.x12, event.y12
                           point2 = (x12,y12)
                           print(point2)
               
                           font = cv2.FONT_HERSHEY_SIMPLEX
                           #distance = round(math.sqrt((str(x2) - str(x)) ** 2) + ((str(y2) - str(y)) ** 2))
                           #distance *= 0.0002645833 # used to convert to meters

                           cv2.putText(img, str(x11) + ',' + str(y11), (x11,y11), font, 1, (255, 0, 0), 2)
                           cv2.putText(img, str(x12) + ',' + str(y12), (x12,y12), font, 1, (255, 0, 0), 2)
                           cv2.line(img, point1, point2, (0,255,0), thickness=3, lineType=4)

                           #cv2.putText(img + 'Distance is ' + str(distance), font, 1, (255, 0, 0), 2)
                           cv2.imshow('window', img)
 
 
           if __name__ == "__main__":
               img = cv2.imread('imageTwo.png', 1)
               cv2.imshow('window', img)
               cv2.setMouseCallback('window', click_event)
               cv2.waitKey(0)
               cv2.destroyAllWindows()
                
finally:
 
   # Stop streaming
   pipeline.stop()
