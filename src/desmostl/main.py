import numpy as np
import struct
import click
import pyperclip


def parse_binary_stl(file_path):
    """Parse a binary STL file and return a matrix of X, Y, Z coordinates."""
    with open(file_path, "rb") as file:
        # Skip the 80-byte header
        file.read(80)

        # Read the number of triangles (4 bytes, unsigned int)
        num_triangles = struct.unpack("I", file.read(4))[0]

        vertices = []

        # Each triangle is 50 bytes: 12 bytes for the normal, 3 vertices (3 floats each, 4 bytes each)
        for _ in range(num_triangles):
            # Skip normal vector (3 floats)
            file.read(12)

            # Read the 3 vertices of the triangle (each vertex is 3 floats)
            for _ in range(3):
                x, y, z = struct.unpack("3f", file.read(12))
                vertices.append([x, y, z])

            # Skip the attribute byte count (2 bytes, not needed)
            file.read(2)

    # Convert the list of vertices into a NumPy array (matrix)
    return np.array(vertices)

@click.command()
@click.argument("path")
@click.option("--print",help="Print out matrix",type=bool)
@click.option("--nocopy",help="Don't copy matrix to clipboard",type=bool)
def main(path,print,nocopy):
    # Parse the binary STL file and get the vertices as a matrix
    matrix = parse_binary_stl(path)

    np.set_printoptions(threshold=np.inf)
    if not nocopy:
        pyperclip.copy(matrix)
    if print:
        # Print the matrix of X, Y, Z coordinates
        click.echo("Matrix of X, Y, Z coordinates:")
        click.echo(matrix)


if __name__ == "__main__":
    main()

