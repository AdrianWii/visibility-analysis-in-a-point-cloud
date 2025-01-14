input_file = "data/viewshed_points.txt"
output_file = "data/viewshed_points.ply"

# Read, filter, and process data
points = []
with open(input_file, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 4 and parts[3] == "1":  # Check for flag == 1
            x, y, z = map(float, parts[:3])
            points.append((x, y, z))

# Write the PLY file
with open(output_file, "w") as f:
    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write(f"element vertex {len(points)}\n")
    f.write("property float x\n")
    f.write("property float y\n")
    f.write("property float z\n")
    f.write("end_header\n")
    for x, y, z in points:
        f.write(f"{x} {y} {z}\n")