"""
Create point cloud from rgb-d images.
Depth channel the distance from the camera.
"""
import open3d as o3d

# read the color and the depth image:
color_raw = o3d.io.read_image(
"../data/rgb.jpg")
depth_raw = o3d.io.read_image(
"../data/depth.png")


# create an rgbd image object:
rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw,convert_rgb_to_intensity=False)