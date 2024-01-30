import numpy as np
from record3d import Record3DStream
import cv2
from threading import Event
import os


class DemoApp:
    def __init__(self):
        self.event = Event()
        self.session = None
        self.DEVICE_TYPE__TRUEDEPTH = 0
        self.DEVICE_TYPE__LIDAR = 1
        self.rgb = None
        self.depth = None
        self.path = os.path.abspath(os.getcwd())

    def on_new_frame(self):
        """
        This method is called from non-main thread, therefore cannot be used for presenting UI.
        """
        self.event.set()  # Notify the main thread to stop waiting and process new frame.

    def normalize_min_max(self, x, min, max):
        diff_max_min = max - min
        result = x
        if diff_max_min != 0:
            result = (x - min) / (max - min)
        return result
    def on_stream_stopped(self):
        print('Stream stopped, saving last images')
        cv2.imwrite(os.path.join(self.path, "rgb.jpg"), self.rgb)
        print(self.depth.shape)

        min = self.depth.min()
        max = self.depth.max()
        output = self.normalize_min_max(self.depth, min, max)
        print(output)
        #output = clipped.astype(np.uint8)
        cv2.imwrite(os.path.join(self.path, "depth.png"), (output))

        print("Done.")
        return
    def connect_to_device(self, dev_idx):
        print('Searching for devices')
        devs = Record3DStream.get_connected_devices()
        print('{} device(s) found'.format(len(devs)))
        for dev in devs:
            print('\tID: {}\n\tUDID: {}\n'.format(dev.product_id, dev.udid))

        if len(devs) <= dev_idx:
            raise RuntimeError('Cannot connect to device #{}, try different index.'
                               .format(dev_idx))

        dev = devs[dev_idx]
        self.session = Record3DStream()
        self.session.on_new_frame = self.on_new_frame
        self.session.on_stream_stopped = self.on_stream_stopped
        self.session.connect(dev)  # Initiate connection and start capturing

    def get_intrinsic_mat_from_coeffs(self, coeffs):
        return np.array([[coeffs.fx,         0, coeffs.tx],
                         [        0, coeffs.fy, coeffs.ty],
                         [        0,         0,         1]])

    def start_processing_stream(self):
        while True:
            self.event.wait()  # Wait for new frame to arrive

            # Copy the newly arrived RGBD frame
            self.depth = self.session.get_depth_frame()
            self.rgb = self.session.get_rgb_frame()
            intrinsic_mat = self.get_intrinsic_mat_from_coeffs(self.session.get_intrinsic_mat())
            camera_pose = self.session.get_camera_pose()  # Quaternion + world position (accessible via camera_pose.[qx|qy|qz|qw|tx|ty|tz])

            print(intrinsic_mat)

            # You can now e.g. create point cloud by projecting the depth map using the intrinsic matrix.

            # Postprocess it
            if self.session.get_device_type() == self.DEVICE_TYPE__TRUEDEPTH:
                self.depth = cv2.flip(self.depth, 1)
                self.rgb = cv2.flip(self.rgb, 1)

            self.rgb = cv2.cvtColor(self.rgb, cv2.COLOR_RGB2BGR)

            # Show the RGBD Stream
            cv2.imshow('RGB', self.rgb)
            cv2.imshow('Depth', self.depth)
            cv2.waitKey(1)

            self.event.clear()


if __name__ == '__main__':
    app = DemoApp()
    app.connect_to_device(dev_idx=0)
    app.start_processing_stream()