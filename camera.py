import cv2
import time
import datetime
import filecmp
import error
import stream_parser


class Camera():

    def __init__(self, url):
        self.id = None
        self.url = url

        self.timeInitialized = time.time()  # Holds the time that the class was initialized
        self.refImage = None                # Holds the string name of the reference image
        self.startImage = None              # Holds the string name of the start image
        self.endImage = None                # Holds the string name of the end image
        self.startTime = 0                  # Holds the unix start time that the start image was captured
        self.endTime = 0                    # Holds the unix start time that the end image was captured
                                            # The frame rate is the difference between these two times. 

        self.parser = None                  # This is the image stream parser object it will always be for static images. 
        self.parser = stream_parser.ImageStreamParser(url)

    def get_ref_image(self):
        # Set the timestamp of the snapshot that will be downloaded.
        frame_timestamp = time.time()
        try:
            # Download the image.
            frame, _ = self.parser.get_frame()
            self.refImage = 'Pictures/ref_{}.png'.format(datetime.datetime.fromtimestamp(frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))

            cv2.imwrite(self.refImage, frame)

        except error.UnreachableCameraError:
            raise error.UnreachableCameraError('get_ref_image_ERROR: Image could not be retrieved for Url: {}'.format(self.url))

        except Exception as e:
            raise e


    def get_start_image(self):
        if self.startTime == 0 and self.refImage != None:
            frame_timestamp = time.time()
            self.startImage = None
            try:
                # Download the image.
                frame, _ = self.parser.get_frame()
                self.startImage = 'Pictures/start.png'
                cv2.imwrite(self.startImage, frame)

                if self.startImage == None or frame_timestamp == None:
                    raise Exception("get_start_image_ERROR: Image could not be retrieved.")

                if filecmp.cmp(self.refImage, self.startImage) == False:
                    self.startTime = frame_timestamp

            except Exception as e:
                raise e


    def get_end_image_and_framerate(self):
        framerate = 0
        if self.startTime != 0:
            frame_timestamp = time.time()
            self.endImage = None
            try:
                # Download the image.
                frame, _ = self.parser.get_frame()
                self.endImage = 'Pictures/end.png'
                cv2.imwrite(self.endImage, frame)

                if self.endImage == None or frame_timestamp == None:
                    raise Exception("EndERROR: Image could not be retrieved.")
                    
                if filecmp.cmp(self.startImage, self.endImage) == False:
                    self.endTime = frame_timestamp
                    framerate = "{:.2f}".format(self.endTime - self.startTime)

            except Exception as e:
                raise e

        return framerate



