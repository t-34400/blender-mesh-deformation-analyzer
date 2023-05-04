import bpy
from mathutils import Vector

from typing import List, Tuple


ZERO_DIVISION_THRESHOLD = 0.00001


def get_strains_of_mesh(original_vertices: List[Vector], target_vertices: List[Vector], faces: List[List[int]]) -> List[float]:
    vertex_count = len(original_vertices)
    angle_list = [0] * vertex_count
    strain_list = [0] * vertex_count
    
    for face in faces:
        # triangulate
        last_vertex_index_in_face = len(face) - 1
        triangle_faces_vertex_indices_in_face = [[triangle_index, triangle_index + 1, last_vertex_index_in_face] for triangle_index in range(0, last_vertex_index_in_face - 1)]
        triangle_faces = [[face[vertex_index_in_face] for vertex_index_in_face in triangle_face_vertex_indices_in_face] for triangle_face_vertex_indices_in_face in triangle_faces_vertex_indices_in_face]
        for triangle_face in triangle_faces:
            original_triangle = [original_vertices[vertex_indices] for vertex_indices in triangle_face]
            target_triangle = [target_vertices[vertex_indices] for vertex_indices in triangle_face]
            strain = get_strain_of_triangle_mesh(original_triangle, target_triangle)
            angles = get_angles(original_triangle)
            for i in range(0, 3):                
                vertex_index = triangle_face[i]
                angle = angles[i]
                angle_list[vertex_index] += angle
                strain_list[vertex_index] += strain * angle
                           
    return [safe_divide(strain, angle) for strain, angle in zip(strain_list, angle_list)]


def safe_divide(dividend, divisor):
    if abs(divisor) < ZERO_DIVISION_THRESHOLD:
        return 0
    return dividend / divisor 

            
def get_strain_of_triangle_mesh(original_triangle: List[Vector], target_triangle: List[Vector]) -> float:
    strain_matrix = get_strain_matrix(original_triangle, target_triangle)
    principal_strains = jacobi_step(strain_matrix[0][0], strain_matrix[1][1], strain_matrix[0][1])
    return max(principal_strains)
    
    
def get_strain_matrix(original_triangle: List[Vector], target_triangle: List[Vector]) -> List[List[float]]:
    vec_a = original_triangle[1] - original_triangle[0]
    vec_b = original_triangle[2] - original_triangle[0]
    abs_vec_a, vec_b_parallel, vec_b_perp = get_components_of_vectors(vec_a, vec_b)
    
    vec_ap = target_triangle[1] - target_triangle[0]
    vec_bp = target_triangle[2] - target_triangle[0]
    abs_vec_ap, vec_bp_parallel, vec_bp_perp = get_components_of_vectors(vec_ap, vec_bp)
    
    if vec_b_perp < ZERO_DIVISION_THRESHOLD:
        return [[(abs_vec_ap - abs_vec_a) / abs_vec_a, 0], [0, 0]]
    else:
        diag_0 = (abs_vec_ap - abs_vec_a) / abs_vec_a
        non_diag = 0.5 * (vec_bp_parallel - (1 + diag_0) * vec_b_parallel) / vec_b_perp
        diag_1 = (vec_bp_perp - vec_b_perp) / vec_b_perp
        return [
            [diag_0, non_diag],
            [non_diag, diag_1],
        ]
    
    
def get_components_of_vectors(vec_a: Vector, vec_b: Vector) -> Tuple[float, float, float]:
    abs_vec_a = vec_a.length
    unit_vec_a = vec_a.normalized()
    vec_b_parallel = vec_b.dot(unit_vec_a)
    vec_b_perp = (vec_b - vec_b_parallel * unit_vec_a).length
    return (abs_vec_a, abs(vec_b_parallel), vec_b_perp)


def jacobi_step(diag_0: float, diag_1: float, non_diag: float) -> List[float]:
    cos2theta = 0
    sin2theta = 1
    if abs(diag_1 - diag_0) > ZERO_DIVISION_THRESHOLD:
        tan2theta = 2 * non_diag / (diag_1 - diag_0)
        cos2theta = 1 / (tan2theta**2 + 1) ** 0.5
        sin2theta = cos2theta * tan2theta
    rotated_diag_0 = 0.5 * diag_0 * (1 + cos2theta) - non_diag * sin2theta + 0.5 * diag_1 * (1 - cos2theta)
    rotated_diag_1 = 0.5 * diag_0 * (1 - cos2theta) + non_diag * sin2theta + 0.5 * diag_1 * (1 + cos2theta)
    return [rotated_diag_0, rotated_diag_1]


def get_angles(triangle: List[Vector]) -> List[float]:
    angles = []
    for i in range(0, 3):
        vec_a = triangle[(i+1) % 3] - triangle[i]
        vec_b = triangle[(i+2) % 3] - triangle[i]
        angles.append(vec_a.angle(vec_b))
    return angles
