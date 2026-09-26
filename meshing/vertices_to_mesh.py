import math
import itertools
import numpy

type Point = tuple[float, float]
type Size = tuple[float, float]
type Edge = tuple[Point, Point]
type Face = tuple[Edge, ...]


class VoxelLookup:
    def __init__(self, vertices: list[Point]):
        self._voxel_dimensions: Size = tuple(
            VoxelLookup._gen_voxel_dimensions(vertices)
        )
        self._voxels = VoxelLookup._get_voxels(vertices, self._voxel_dimensions)

    @staticmethod
    def _get_voxels(vertices: set[Point], voxel_dimensions: Size):
        voxels: dict[tuple[int, ...], set[Point]] = {}
        for vertex in vertices:
            voxels.setdefault(
                tuple(VoxelLookup._gen_voxel_indices(vertex, voxel_dimensions)), set()
            ).add(vertex)
        return voxels

    @staticmethod
    def _gen_voxel_dimensions(vertices: set[Point]):
        divisions = VoxelLookup._get_divisions(vertices)
        coords_per_dimension: dict[int, list[float]] = dict()
        for vertex in vertices:
            for ix, coord in enumerate(vertex):
                coords_per_dimension.setdefault(ix, []).append(coord)
        for ix, coords in coords_per_dimension.items():
            minimum = min(coords)
            maximum = max(coords)
            yield (maximum - minimum) / divisions

    @staticmethod
    def _get_divisions(vertices):
        return max(1.0, len(vertices) ** 0.5)

    @staticmethod
    def _gen_voxel_indices(point: Point, voxel_dimensions: Size):
        for location, voxel_dimension in zip(point, voxel_dimensions):
            yield int(location / voxel_dimension) if voxel_dimension > 0 else 0

    @property
    def voxel_dimension(self, ix: int):
        return self._voxel_dimensions[ix]

    @property
    def vertices(self):
        for vertices in self._voxels.values():
            for vertex in vertices:
                yield vertex

    def _get_voxel_index(self, point):
        return tuple(VoxelLookup._gen_voxel_indices(point, self._voxel_dimensions))

    def get_voxel(self, root: Point, delta_voxel_index: tuple[int, int] = (0, 0)):
        return self._voxels[
            tuple(
                root_i + delta_i
                for root_i, delta_i in zip(
                    self._get_voxel_index(root), delta_voxel_index
                )
            )
        ]


def alternating_form(vectors: tuple[tuple[float, ...], ...]):
    def _permutation_sign(perm):
        return (-1) ** sum(
            perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm))
        )

    vectors = numpy.array(vectors)
    return sum(
        _permutation_sign(perm)
        * numpy.prod(vectors[numpy.arange(vectors.shape[0]), perm])
        for perm in itertools.permutations(range(vectors.shape[1]), vectors.shape[0])
    )


class Mesh:
    def __init__(self, vertices: list[Point]):
        self.edges: set[Edge] = set()
        self.faces: set[Face] = set()
        self.vertex_voxels = VoxelLookup(vertices)

    def gen_neighbours(self, point: Point):
        for delta in self._gen_deltas(
            [int(i) for i in self.vertex_voxels.voxel_dimension]
        ):
            yield from self.vertex_voxels.get_voxel(point, delta)

    def _gen_deltas(self, dimensions: tuple[int, ...]):
        ranges = [range(-dimension, dimension + 1) for dimension in dimensions]
        return sorted(
            itertools.product(*ranges),
            key=lambda delta: math.dist((0,) * len(delta), delta),
        )

    @staticmethod
    def _get_face_area(face: Face):
        return 0.5 * numpy.linalg.norm(
            sum(
                alternating_form((edge, face[(ix + 1) % len(face)]))
                for ix, edge in enumerate(face)
            )
        )

    @staticmethod
    def _get_face_perimeter(face: Face):
        return sum(
            math.dist(edge, face[(ix + 1) % len(face)]) for ix, edge in enumerate(face)
        )

    def has_high_face_quality(self, face: Face):
        area = self._get_face_area(face)
        perimeter = self._get_face_perimeter(face)
        isoperimetric_ratio = 4 * math.pi * area / (perimeter * perimeter)
        return isoperimetric_ratio >= 0.2

    def gen_faces_from_point(self, point: Point):
        for edge in self.gen_edges_from_point(point):
            if (face := self.get_face_from_edge(edge)) is not None:
                self.faces.add(face)
            else:
                self.edges.remove(edge)

    def get_face_from_edge(self, edge1: Edge):
        face = None
        for edge1point in edge1:
            for edge2 in self.gen_edges_from_point(edge1point):
                for common_point in self.gen_common_points(edge1, edge2):
                    assert edge1point == common_point
                    for edge3 in self.gen_completing_edges([edge1, edge2]):
                        face = (edge1, edge2, edge3)
                        if self.has_high_face_quality(face):
                            return face
                        else:
                            self.edges.remove(edge3)
                            face = None
                if face is None:
                    self.edges.remove(edge2)

    def gen_edges_from_point(self, point: Point):
        for neighbour in self.gen_neighbours(point):
            for edge in self.gen_edges_from_points(point, neighbour):
                yield edge

    def gen_completing_edges(self, edges: list[Edge]):
        points = set()
        joined_points = set()
        for edge1 in edges:
            for point in edge1:
                points.add(point)
            for edge2 in edges:
                joined_points |= set(self.gen_common_points(edge1, edge2))
        lonely_points = sorted(points - joined_points)
        assert len(lonely_points) == 2
        point1, point2 = lonely_points
        for edge in self.gen_edges_from_points(point1, point2):
            yield edge

    def gen_common_points(self, edge1: Edge, edge2: Edge):
        for point in edge1:
            if point in edge2:
                yield point

    def gen_edges_from_points(self, point: Point, neighbour: Point):
        edge = (point, neighbour)
        if not edge in self.edges:
            self.edges.add(edge)
            yield edge
        edge = edge[::-1]
        if not edge in self.edges:
            self.edges.add(edge)
            yield edge
