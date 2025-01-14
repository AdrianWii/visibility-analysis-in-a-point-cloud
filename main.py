import trimesh
import math
from pathlib import Path
from point3d import Point3D
from normal import Normal
from face import Face
from tqdm import tqdm
import time

filename = "data/sorted_faces.txt"
points_filename = "data/sorted_points.txt"
viewshed_filename = "data/viewshed_points.txt"


def euclidean_distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2 +
        (point1.z - point2.z) ** 2
    )

def save_faces_to_file(sorted_faces, filename):
    data = [f"{face.a.x} {face.a.y} {face.a.z} {face.b.x} {face.b.y} {face.b.z} {face.c.x} {face.c.y} {face.c.z}\n" for face in sorted_faces]
    with open(filename, "w") as file:
        file.write(''.join(data))

def read_faces_from_file(filename):
    faces = []
    
    with open(filename, 'r') as file:
        for line in file:
            # Split the line into 9 numbers (3 points, each with x, y, z)
            coords = list(map(float, line.strip().split()))
            
            # Create Point3D objects for each vertex of the face
            a = Point3D(coords[0], coords[1], coords[2])
            b = Point3D(coords[3], coords[4], coords[5])
            c = Point3D(coords[6], coords[7], coords[8])
            
            face = Face(a, b, c)            
            faces.append(face)
    
    return faces

def save_points_to_file(points, filename):
    data = [f"{point.x} {point.y} {point.z}\n" for point in points]
    with open(filename, "w") as file:
        file.write(''.join(data))

def save_points_viewshed(points, filename):
    data = [f"{point.x} {point.y} {point.z} {point.mesh}\n" for point in points]
    with open(filename, "w") as file:
        file.write(''.join(data))

def read_points_from_file(filename):
    points = []
    
    with open(filename, 'r') as file:
        for line in file:
            coords = list(map(float, line.strip().split()))            
            points.append(Point3D(coords[0], coords[1], coords[2]))
    
    return points

def process_face(face, points, light):
    current_normal = Normal(face.a, face.b, face.c)
    current_normal.process(points, light)

def process_start(sorted_faces, points_sorted_by_distance, light):    
    print("PROCESS STARTED\n")
    start_time = time.time()
    for face in tqdm(sorted_faces, desc="Processing Faces"):
        # Create a Normal object with face vertices
        current_normal = Normal(face.a, face.b, face.c)
        current_normal.process(points_sorted_by_distance, light)

    end_time = time.time()
    duration = end_time - start_time
    print(f"\nPROCESS ENDED\nTotal time taken: {duration:.2f} seconds")
    save_points_viewshed(points_sorted_by_distance, viewshed_filename)


light = Point3D(566740.510010, 243461.329987, 206.579996)

if not Path(filename).exists() or not Path(points_filename).exists():
    mesh = trimesh.load('data/wawel_mesh_large.obj')

    vertices = mesh.vertices  # numpy array of shape (n_vertices, 3)
    faces = mesh.faces        # numpy array of shape (n_faces, 3)

    face_objects = []
    for face_indices in faces:
        a = Point3D(*vertices[face_indices[0]])
        b = Point3D(*vertices[face_indices[1]])
        c = Point3D(*vertices[face_indices[2]])
        face_objects.append(Face(a, b, c))

    sorted_faces = sorted(face_objects, key=lambda face: euclidean_distance(face.centroid, light))
    points = [Point3D(x, y, z) for x, y, z in mesh.vertices]
    points_sorted_by_distance = sorted(points, key=lambda p: euclidean_distance(p, light))

    # Output the list of Face objects
    for face in sorted_faces[:5]: 
        print(face, euclidean_distance(face.centroid, light))

    save_faces_to_file(sorted_faces, filename)
    save_points_to_file(points_sorted_by_distance, points_filename)
else:
    print("file is prepared")
    sorted_faces = faces = read_faces_from_file(filename)
    points_sorted_by_distance = read_points_from_file(points_filename)

process_start(sorted_faces, points_sorted_by_distance, light)
