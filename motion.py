from __future__ import division
import    io
import    time
import    picamera
import    cv2
import    numpy as np

class MotionDetector( ):
    def __init__(self, camera, resolution=(160, 90), threshold=20, erosion=10, background_delta=0.3): 
        self.camera = camera 
        self.resolution = resolution 
        self.raw_resolution = (
            (resolution[0] + 31) // 32 * 32, 
            (resolution[1] + 15) // 16 * 16, 
            )
        self.raw_bytes = self.raw_resolution[0] * self.raw_resolution[1]
        self.threshold = threshold
        self.erosion = erosion
        self.background_delta = background_delta
        self.background = None

    def _get_erosion(self):
        return (self.erosion_filter.shape[0] - 1) // 2
    def _set_erosion(self, value):
        self.erosion_filter = cv2.getStructuringElement(cv2.M0RPH_RECT, (value * 2 + 1, value * 2 + 1)) 
    erosion = property(_get_erosion, _set_erosion)
    
    def poll(self):
        stream = io.BytesIO() 
        self.camera.capture(stream, format='yuv', resize=self.resolution, use_video_port=True)
        data = stream.getvalue()[:self.raw_bytes]
        image = np.fromstring(data, dtype=np.uint8).reshape((self.raw_resolution[1], self.raw_resolution[0]) )
        cv2.erode(image, self.erosion_filter) 
        image = image.astype(np.float) 
        if self.background is None: 
            self.background = image 
            return False 
        else:
            diff = cv2.absdiff(image, self.background) 
            diff = diff.astype(np.uint8) 
            diff = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)[1] 
            result = diff.any() 
            cv2.accumulateWeighted(image, self.background, self.background_delta) 
            return result
    
with picamera.PiCamera() as cam: 
    cam.resolution = (1280, 720)
    #Kamera vor dem Beginn warm laufen lassen
    time.sleep(2)
    detector = MotionDetector(cam) 
    while True:
        if detector.poll():
            print("I see you!") 
