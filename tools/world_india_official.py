"""Build a world country GeoJSON whose India polygon is the official Survey of India outline.

The vega-datasets world-110m topojson draws India without PoK, Gilgit-Baltistan and Aksai Chin. This
replaces India's geometry with the union of the official state outlines and draws India last, so the
claimed territory is shown as India. Each feature carries id (ISO numeric), iso3 and name.

    python3 tools/world_india_official.py WORLD_110M.json INDIA_STATES.geojson OUT.geojson
"""
import json
import sys

import pycountry
from shapely.geometry import Point, mapping, shape
from shapely.ops import unary_union


def decode(topo, obj="countries"):
    sc, tr = topo["transform"]["scale"], topo["transform"]["translate"]
    arcs = []
    for a in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in a:
            x += dx
            y += dy
            pts.append([x * sc[0] + tr[0], y * sc[1] + tr[1]])
        arcs.append(pts)

    def ring(idx):
        out = []
        for i in idx:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(seg if not out else seg[1:])
        return out
    feats = []
    for g in topo["objects"][obj]["geometries"]:
        if g["type"] == "Polygon":
            geom = {"type": "Polygon", "coordinates": [ring(r) for r in g["arcs"]]}
        elif g["type"] == "MultiPolygon":
            geom = {"type": "MultiPolygon", "coordinates": [[ring(r) for r in p] for p in g["arcs"]]}
        else:
            continue
        feats.append({"id": g.get("id"), "geometry": geom})
    return feats


def main(world, states, out):
    feats = decode(json.load(open(world)))
    india = unary_union([shape(f["geometry"]).buffer(0) for f in json.load(open(states))["features"]])
    india = india.simplify(0.03, preserve_topology=True)
    for name, lon, lat in (("Gilgit", 74.31, 35.92), ("Muzaffarabad", 73.47, 34.37), ("Aksai Chin", 79.5, 35.2)):
        assert india.contains(Point(lon, lat)), f"{name} is outside the India outline"
    res = []
    for f in feats:
        try:
            num = int(f["id"])
        except (TypeError, ValueError):
            continue
        c = pycountry.countries.get(numeric=f"{num:03d}")
        if num == 356:
            continue
        res.append({"type": "Feature", "id": num, "properties": {"id": num, "iso3": c.alpha_3 if c else "",
                                                                  "name": c.name if c else ""},
                    "geometry": f["geometry"]})
    res.append({"type": "Feature", "id": 356, "properties": {"id": 356, "iso3": "IND", "name": "India",
                                                             "outline": "Survey of India official outline"},
                "geometry": mapping(india)})
    json.dump({"type": "FeatureCollection", "features": res}, open(out, "w"), separators=(",", ":"))
    print(f"{len(res)} countries -> {out}; India verified for Gilgit, Muzaffarabad, Aksai Chin")


if __name__ == "__main__":
    main(*sys.argv[1:4])
