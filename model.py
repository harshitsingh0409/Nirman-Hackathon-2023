import geopandas as gpd
import vtk
import shapely
import pyvista as pv
import numpy as np
from vtk.util import numpy_support as VN


def getHeightMap(gdf):
    # Define the elevation field
    elevation_field = "HEIGHT"

    # Extract the polygon geometries from the GeoDataFrame
    polygons = [vtk.vtkPolygon() for i in range(len(gdf))]
    points = vtk.vtkPoints()

    for i, row in gdf.iterrows():
        geometry = row.geometry
        if isinstance(geometry, shapely.geometry.Polygon):
            boundary = geometry.exterior
            coords = list(boundary.coords)
        elif isinstance(geometry, shapely.geometry.MultiPolygon):
            coords = []
            for polygon in geometry.geoms:
                coords += list(polygon.boundary.coords)
        else:
            raise ValueError("Unsupported geometry type: {}".format(geometry.geom_type))

        polygon = polygons[i]
        polygon.GetPointIds().SetNumberOfIds(len(coords))
        for j, coord in enumerate(coords):
            id = points.InsertNextPoint(coord[0], coord[1], row[elevation_field]+10)
            polygon.GetPointIds().SetId(j, id)

    # Create a PolyData object and add the polygons and points
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    cellarray = vtk.vtkCellArray()
    for polygon in polygons:
        cellarray.InsertNextCell(polygon)

    polydata.SetPolys(cellarray)

    # Convert the VTK PolyData object to a PyVista dataset
    heightDataset = pv.wrap(polydata)
    
    
    return heightDataset

def getBaseMap(gdf):
    # Define the elevation field
    elevation_field = "Z"
    gdf[elevation_field] = 0.0

    # Extract the polygon geometries from the GeoDataFrame
    polygons = [vtk.vtkPolygon() for i in range(len(gdf))]
    points = vtk.vtkPoints()

    for i, row in gdf.iterrows():
        geometry = row.geometry
        if isinstance(geometry, shapely.geometry.Polygon):
            boundary = geometry.exterior
            coords = list(boundary.coords)
        elif isinstance(geometry, shapely.geometry.MultiPolygon):
            coords = []
            for polygon in geometry.geoms:
                coords += list(polygon.boundary.coords)
        else:
            raise ValueError("Unsupported geometry type: {}".format(geometry.geom_type))

        polygon = polygons[i]
        polygon.GetPointIds().SetNumberOfIds(len(coords))
        for j, coord in enumerate(coords):
            id = points.InsertNextPoint(coord[0], coord[1], 0.0)
            polygon.GetPointIds().SetId(j, id)

    # Create a PolyData object and add the polygons and points
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    cellarray = vtk.vtkCellArray()
    for polygon in polygons:
        cellarray.InsertNextCell(polygon)

    polydata.SetPolys(cellarray)

    # Convert the VTK PolyData object to a PyVista dataset
    baseDataset = pv.wrap(polydata)
    return baseDataset

def compileModel(shapdedata):
    
    gdf = gpd.read_file(shapdedata)
    
    heightData = getHeightMap(gdf)
    baseData = getBaseMap(gdf)

    #plane = pv.Plane(center=mesh.center, direction=[0, 0, 1])

    p = pv.Plotter()

    p.add_mesh(heightData, cmap="coolwarm", show_scalar_bar=True, color ="black")
    p.add_mesh(baseData, cmap="coolwarm", show_scalar_bar=True, color="white")
    
    model = heightData.extrude_trim((0, 0, -50.0), baseData)
    
    #x_dim, y_dim, z_dim = baseData.dimensions


    return model

def render3d(modelfile):
    
    # 1. declare meshfile
    mesh = modelfile

    # 2. Create the PyVista plot
    plot = pv.Plotter()
    
            
    # Add the red mesh to the plot
    mesh_color = "#9db9eb"  
    plot.add_mesh(mesh, color=mesh_color)
    
    plot.add_camera_orientation_widget()
    plot.add_floor(color="#343942")
    #plot.add_box_widget()
    plot.add_background_image("static\images\skybackground.jpg")
            
    # Render the plot
    plot.show()
    
    return plot.screenshot()

 
def render2d(modelfile):
    
    # renders a 2d image for the website homepage
    
    # Read the STL file
    mesh = modelfile

    # Create the PyVista plot
    plot = pv.Plotter()
    plot.add_mesh(mesh)
    
    # Set camera position and focal point to achieve a top-down view
    center = mesh.center
    z_bounds = mesh.bounds[4:6]
    plot.camera_position = (0, 0, z_bounds[1]+(2*z_bounds[1]-z_bounds[0]))
    plot.camera_focal_point = (0, 0, center[2])
    plot.viewup=[0,0,0]


    # Fix camera position
    plot.camera_fixed = True
    
    plot.add_floor(color="#343942")

    # Disable user interactions with the plot
    plot.enable_parallel_projection()
    plot.disable_eye_dome_lighting()
    plot.disable_anti_aliasing()
    plot.disable_depth_peeling()
    plot.disable_shadows()
    
    #plot = pv.Plotter(off_screen=True)
    #plot.show(screenshot='static\images\map2d.png')
    plot.show()

    # Take a screenshot of the plot
    return  plot.screenshot()