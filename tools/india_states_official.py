"""Simplified India state outlines (official Survey of India boundary, J&K incl. PoK, Gilgit-Baltistan, Aksai Chin).

Each feature carries `name` (display) and `key`, the lower-case place label Prism's news geography returns
('delhi', 'uttar pradesh' ...), so a dashboard can join on it directly.

    python3 tools/india_states_official.py INDIA_STATES.geojson OUT.geojson
"""
import json
import sys

from shapely.geometry import Point, mapping, shape

ALIAS = {"NCT of Delhi": ("Delhi", "delhi"), "Arunanchal Pradesh": ("Arunachal Pradesh", "arunachal pradesh"),
         "Andaman & Nicobar Island": ("Andaman and Nicobar Islands", "andaman and nicobar islands"),
         "Dadara & Nagar Havelli": ("Dadra and Nagar Haveli", "dadra and nagar haveli"),
         "Daman & Diu": ("Daman and Diu", "daman and diu"), "Jammu & Kashmir": ("Jammu and Kashmir", "jammu and kashmir")}


def main(src, out):
    feats = []
    jk = None
    for f in json.load(open(src))["features"]:
        n = f["properties"]["ST_NM"]
        name, key = ALIAS.get(n, (n, n.lower()))
        g = shape(f["geometry"]).buffer(0).simplify(0.02, preserve_topology=True)
        if key == "jammu and kashmir":
            jk = g
        feats.append({"type": "Feature", "properties": {"name": name, "key": key}, "geometry": mapping(g)})
    for place, lon, lat in (("Gilgit", 74.31, 35.92), ("Muzaffarabad", 73.47, 34.37), ("Aksai Chin", 79.5, 35.2)):
        assert jk is not None and jk.contains(Point(lon, lat)), f"{place} is outside Jammu and Kashmir"
    json.dump({"type": "FeatureCollection", "features": feats}, open(out, "w"), separators=(",", ":"))
    print(f"{len(feats)} states -> {out}; J&K verified for Gilgit, Muzaffarabad, Aksai Chin")


if __name__ == "__main__":
    main(*sys.argv[1:3])
