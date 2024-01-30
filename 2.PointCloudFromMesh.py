"""
Create point cloud from exsisting mesh.
"""

import open3d as o3d

# download bunny mesh from open3d
#try:
#    mesh = o3d.io.read_triangle_mesh("data/bunny.ply")
#except:
bunny = o3d.data.BunnyMesh()
mesh = o3d.io.read_triangle_mesh(bunny.path)

# visualize
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])

# sample n points from the point cloud
pcd = mesh.sample_points_uniformly(number_of_points=5000)
o3d.visualization.draw_geometries([pcd])

# save point cloud into a ply file
o3d.io.write_point_cloud("output/bunny_pcd.ply", pcd)