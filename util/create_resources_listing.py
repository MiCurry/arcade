"""
Quick Index Generator

Generate quick API indexes in Restructured Text Format for Sphinx documentation.
"""

import re
import os
import shutil
from pathlib import Path


def process_resource_directory(out, my_path: Path):

    for cur_node in my_path.iterdir():

        r1 = cur_node.relative_to('.')
        r3 = 'resources/' + str(r1)[20:].replace('\\', '/')
        # print(r3)
        if cur_node.is_dir():

            if str(cur_node).endswith("__"):
                continue

            has_files = False
            for check_node in cur_node.iterdir():
                if check_node.is_file():
                    has_files = True
                    break

            try:
                os.makedirs(f"build/html/{r3}")
            except FileExistsError:
                pass

            # out.write(f"\n{cur_node.name}\n")
            # out.write("-" * len(cur_node.name) + "\n\n")
            process_resource_directory.cell_count = 0

            if has_files:
                out.write(f"\n\n:resources:{r3[10:]}/\n")
                out.write("-" * (len(r3) + 2) + "\n\n")

                out.write(".. raw:: html\n\n")
                out.write("    <table class='resource-table'><tr>\n")
                process_resource_files(out, cur_node)
                out.write("    </tr></table>\n")

            process_resource_directory(out, cur_node)


def process_resource_files(out, my_path: Path):


    for cur_node in my_path.iterdir():
        r1 = cur_node.relative_to('.')
        r3 = 'resources/' + str(r1)[20:].replace('\\', '/')
        # print(r3)
        if not cur_node.is_dir():
            r2 = ":resources:" + str(r1)[20:].replace('\\', '/')
            if process_resource_directory.cell_count % 3 == 0:
                out.write(f"    </tr>\n")
                out.write(f"    <tr>\n")
            if r2.endswith(".png") or r2.endswith(".jpg") or r2.endswith(".gif") or r2.endswith(".svg"):
                out.write(f"    <td>")
                out.write(f"<a href='{r3}'><img alt='{r2}' title='{r2}' src='{r3}'></a><br />")
                out.write(f"{cur_node.name}")
                process_resource_directory.cell_count += 1
                out.write("</td>\n")
            elif r2.endswith(".wav"):
                out.write(f"    <td>")
                out.write(f"<audio controls><source src='{r3}' type='audio/x-wav'></audio><br />")
                out.write(f"{cur_node.name}")
                process_resource_directory.cell_count += 1
                out.write("</td>\n")
            elif r2.endswith(".mp3"):
                out.write(f"    <td>")
                out.write(f"<audio controls><source src='{r3}' type='audio/mpeg'></audio><br />")
                out.write(f"{cur_node.name}")
                process_resource_directory.cell_count += 1
                out.write("</td>\n")
            elif r2.endswith(".ogg"):
                out.write(f"    <td>")
                out.write(f"<audio controls><source src='{r3}' type='audio/ogg'></audio><br />")
                out.write(f"{cur_node.name}")
                process_resource_directory.cell_count += 1
                out.write("</td>\n")
            elif r2.endswith(".url") or r2.endswith(".txt"):
                pass
            else:
                out.write(f"    <td>")
                out.write(f"{cur_node.name}")
                process_resource_directory.cell_count += 1
                out.write("</td>\n")
            # out.write(f"<br />{r2}</td>")
            src = r1
            dst = f"build\\html\\{r3}"
            shutil.copyfile(src, dst)


process_resource_directory.cell_count = 0

def resources():
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)
    try:
        os.makedirs("build/html/resources")
    except FileExistsError:
        pass

    out = open("../doc/resources.rst", "w")

    out.write(".. _resources:\n")
    out.write("\n")
    out.write("Resources\n")
    out.write("=========\n")
    out.write("\n")
    out.write("Resource files are images and sounds built into Arcade that "
              "can be used to quickly build and test simple code without having "
              "to worry about copying files into the project.\n\n")
    out.write("Any file loaded that starts with ``:resources:`` will attempt "
              "to load that file from the library resources instead of the "
              "project directory.\n\n")
    out.write("Many of the resources come from `Kenney.nl <https://kenney.nl/>`_ ")
    out.write("and are licensed under CC0 (Creative Commons Zero). Be sure to ")
    out.write("check out his web page for a much wider selection of assets.")

    out.write("\n")
    process_resource_directory(out, Path('../arcade/resources/'))
    print("Done creating resources.rst")


def main():
    resources()


if __name__ == '__main__':
    main()