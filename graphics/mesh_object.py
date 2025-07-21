import trimesh

class MeshObject:
    def __init__(self, filename):
        self.mesh = trimesh.load(filename, force='mesh')
        self.vertices = self.mesh.vertices
        self.faces = self.mesh.faces

    def draw(self):
        from OpenGL.GL import glBegin, glEnd, glVertex3f, glNormal3f, GL_TRIANGLES
        import numpy as np
        
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            # Calculate face normal for better lighting
            v0, v1, v2 = [self.vertices[face[i]] for i in range(3)]
            
            # Calculate normal using cross product
            edge1 = np.array(v1) - np.array(v0)
            edge2 = np.array(v2) - np.array(v0)
            normal = np.cross(edge1, edge2)
            normal = normal / (np.linalg.norm(normal) + 1e-8)  # Normalize
            
            # Set normal for this face
            glNormal3f(normal[0], normal[1], normal[2])
            
            # Draw vertices
            for idx in face:
                v = self.vertices[idx]
                glVertex3f(v[0], v[1], v[2])
        glEnd()

    def create_copy_with_new_vertices(self, new_vertices):
        copy = MeshObject.__new__(MeshObject)
        copy.vertices = new_vertices
        copy.faces = self.faces
        return copy
