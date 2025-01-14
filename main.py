import trimesh
import math
from pathlib import Path
from point3d import Point3D
from normal import Normal
from face import Face
from tqdm import tqdm
import time
import multiprocessing
import os

light = Point3D(566740.510010, 243461.329987, 206.579996)

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
    # green - visible, dark gray - hidden
    data = [f"{point.x} {point.y} {point.z} {'0 255 0' if point.mesh else '169 169 169'}\n" for point in points]

    with open(filename, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")
        f.write(''.join(data))

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

def select_obj_file(directory):
    """
    Lists .obj files in the specified directory and allows the user to select one.
    Returns the Path to the selected file or None if no valid file is selected.
    """
    data_path = Path(directory)
    if not data_path.is_dir():
        print(f"Error: '{data_path}' is not a valid directory.")
        return None

    # Fetch all .obj files
    obj_files = list(data_path.glob("*.obj"))

    if not obj_files:
        print("No .obj files found in the directory.")
        return None

    print("Found the following .obj files:")
    for idx, file in enumerate(obj_files, start=1):
        print(f"{idx}: {file.name}")

    # User selects a file to process
    try:
        selection = int(input("Enter the number of the file you want to process: ")) - 1
        if 0 <= selection < len(obj_files):
            return obj_files[selection]
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

# def process_start(sorted_faces, points_sorted_by_distance, light):    
#     print("PROCESS STARTED\n")
#     start_time = time.time()
#     for face in tqdm(sorted_faces, desc="Processing Faces"):
#         # Create a Normal object with face vertices
#         current_normal = Normal(face.a, face.b, face.c)
#         current_normal.process(points_sorted_by_distance, light)

#     end_time = time.time()
#     duration = end_time - start_time
#     print(f"\nPROCESS ENDED\nTotal time taken: {duration:.2f} seconds")
#     save_points_viewshed(points_sorted_by_distance, viewshed_filename)

def process_face(face_data):
    """Helper function to process a single face."""
    face, points_sorted_by_distance, light = face_data
    current_normal = Normal(face.a, face.b, face.c)
    current_normal.process(points_sorted_by_distance, light)
    return True  # Return a dummy value for tracking progress

def process_start(sorted_faces, points_sorted_by_distance, light):
    print("PROCESS STARTED\n")
    start_time = time.time()

    # Prepare data for multiprocessing
    face_data = [(face, points_sorted_by_distance, light) for face in sorted_faces]

    # Use multiprocessing to process faces in parallel
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # Use tqdm for progress tracking with imap_unordered
        results = list(tqdm(
            pool.imap_unordered(process_face, face_data),
            desc="Processing Faces",
            total=len(sorted_faces)
        ))

    end_time = time.time()
    duration = end_time - start_time
    print(f"\nVIEWSHED PROCESS ENDED\nTotal time taken: {duration:.2f} seconds")

    save_points_viewshed(points_sorted_by_distance, f"data/viewshed_points_{len(points_sorted_by_distance)}.ply")

def main():
    #todo measure data preparation
    selected_file = select_obj_file("data")
    if not selected_file:
        return

    filename_without_extension = os.path.splitext(os.path.basename(selected_file))[0]

    filename = f"data/sorted_faces_{filename_without_extension}.txt"
    points_filename = f"data/sorted_points_{filename_without_extension}.txt"

    if not Path(filename).exists() or not Path(points_filename).exists():
        start_time = time.time()
        mesh = trimesh.load(selected_file)

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
        # for face in sorted_faces[:5]: 
        #     print(face, euclidean_distance(face.centroid, light))
        end_time = time.time()
        duration = end_time - start_time
        print(f"\nSORTING PROCESS ENDED\nTotal time taken: {duration:.2f} seconds")
        save_faces_to_file(sorted_faces, filename)
        save_points_to_file(points_sorted_by_distance, points_filename)
    else:
        print("file is prepared")
        sorted_faces = faces = read_faces_from_file(filename)
        points_sorted_by_distance = read_points_from_file(points_filename)

    process_start(sorted_faces, points_sorted_by_distance, light)


if __name__ == "__main__":
    main()