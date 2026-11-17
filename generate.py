#!/usr/bin/env python3
"""Build the Kodi repository index (zips/addons.xml + .md5) and collect the
add-on zips into zips/<id>/<id>-<version>.zip. Run from the repo root."""
import hashlib
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
ZIPS = os.path.join(ROOT, "zips")

# (addon source dir, prebuilt zip path or None to zip the folder itself)
SOURCES = [
    ("/home/claude/nlziet-kodi-addon", "plugin.video.nlziet"),
    ("/home/claude/videoland-kodi-addon", "plugin.video.videoland.nl"),
    (os.path.join(ROOT, "repository.djdirty"), "repository.djdirty"),
]


def addon_meta(addon_xml):
    root = ET.parse(addon_xml).getroot()
    return root.get("id"), root.get("version"), root


def build_addon_zip(src_dir, addon_id, version):
    """Prefer the add-on's own build-release.py (git-tracked files); otherwise
    zip the folder (for the repository add-on itself)."""
    out_dir = os.path.join(ZIPS, addon_id)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "{}-{}.zip".format(addon_id, version))
    script = os.path.join(src_dir, "scripts", "build-release.py")
    if os.path.exists(script):
        subprocess.run(["python", script], cwd=src_dir, check=True,
                       stdout=subprocess.DEVNULL)
        built = os.path.join(src_dir, "build", "{}-{}.zip".format(addon_id, version))
        shutil.copy2(built, dest)
    else:
        # Zip the folder under a top-level <addon_id>/ path (Kodi requirement).
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
            for base, _dirs, files in os.walk(src_dir):
                for name in files:
                    full = os.path.join(base, name)
                    rel = os.path.relpath(full, src_dir)
                    zf.write(full, os.path.join(addon_id, rel))
    return dest


def main():
    os.makedirs(ZIPS, exist_ok=True)
    addons_root = ET.Element("addons")
    for src_dir, addon_id in SOURCES:
        addon_xml = os.path.join(src_dir, "addon.xml")
        aid, version, node = addon_meta(addon_xml)
        assert aid == addon_id, "{} != {}".format(aid, addon_id)
        build_addon_zip(src_dir, addon_id, version)
        addons_root.append(node)
        print("  {} {}".format(addon_id, version))
    # Write addons.xml
    xml_bytes = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + \
        ET.tostring(addons_root, encoding="utf-8")
    index = os.path.join(ZIPS, "addons.xml")
    with open(index, "wb") as handle:
        handle.write(xml_bytes)
    md5 = hashlib.md5(xml_bytes).hexdigest()
    with open(index + ".md5", "w") as handle:
        handle.write(md5)
    print("addons.xml md5:", md5)


if __name__ == "__main__":
    main()
