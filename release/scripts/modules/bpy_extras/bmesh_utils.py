# SPDX-License-Identifier: GPL-2.0-or-later

__all__ = (
    "bmesh_linked_uv_islands",
)

import bmesh


def match_uv(face, vert, uv, uv_layer):
    for loop in face.loops:
        if loop.vert == vert:
            return uv == loop[uv_layer].uv
    return False


def bmesh_linked_uv_islands(bm, uv_layer):
    """
    Returns lists of face indices connected by UV islands.

    For meshes use :class:`bpy.types.Mesh.mesh_linked_uv_islands` instead.

    :arg bm: the bmesh used to group with.
    :type bmesh: :class:`BMesh`
    :arg uv_layer: the UV layer to source UVs from.
    :type bmesh: :class:`BMLayerItem`
    :return: list of lists containing polygon indices
    :rtype: list
    """

    result = []
    bm.faces.ensure_lookup_table()

    used = set()
    for seed_face in bm.faces:
        seed_index = seed_face.index
        if seed_index in used:
            continue  # Face has already been processed.
        used.add(seed_index)
        island = [seed_index]
        stack = [seed_face]  # Faces still to consider on this island.
        while stack:
            current_face = stack.pop()
            for loop in current_face.loops:
                v = loop.vert
                uv = loop[uv_layer].uv
                for f in v.link_faces:
                    if f.index in used:
                        continue
                    if not match_uv(f, v, uv, uv_layer):
                        continue

                    # `f` is part of island, add to island and stack
                    used.add(f.index)
                    island.append(f.index)
                    stack.append(f)
        result.append(island)

    return result