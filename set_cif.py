# coding=utf-8
import sqlite3
from ase.io import read
from ase.visualize import view
from ase.build import cut



def set_cif(db_dir, cif_dir):        # db_dir:database.py中创立的数据库的路径，cif_dir：新建立的cif文件的路径
    '''
    用数据库的数据生成cif文件。
    :param db_dir: 数据库的路径
    :param cif_dir: 函数所建立的cif文件的路径 (任选)
    :return: None
    '''
    conn = sqlite3.connect(db_dir)   # dir = "/Users/mac/Desktop/crystal.db"
    cnn = conn.cursor()

    f = open(cif_dir, 'w')           # cif_dir = "/Users/mac/Desktop/foo.cif"
    f.write("# generated using pymatgen\n")

    r_formula = input("你想创建哪种材料的cif文件，请输入它的化学式：")
    formula = "'" + r_formula + "'"
    cnn.execute("SELECT * FROM test WHERE Formula={}".format(formula))
    f.write("data_{}\n".format(formula.strip("'")))
    row = list(cnn.fetchone())
    print(row)

    f.write("_cell_length_a\t{0}\n".format(row[2]))
    f.write("_cell_length_b\t{0}\n".format(row[3]))
    f.write("_cell_length_c\t{0}\n".format(row[4]))

    f.write("_cell_angle_alpha\t{0}\n".format(row[5]))
    f.write("_cell_angle_beta\t{0}\n".format(row[6]))
    f.write("_cell_angle_gamma\t{0}\n".format(row[7]))

    f.write("_symmetry_Int_Tables_number   1\n")

    f.write("_cell_volume\t{0}\n".format(row[8]))

    f.write("loop_\n")
    f.write(" _symmetry_equiv_pos_site_id\n")
    f.write(" _symmetry_equiv_pos_as_xyz\n")
    f.write("  1  'x, y, z'\n")

    f.write("loop_\n")
    f.write(" _atom_site_type_symbol\n")
    f.write(" _atom_site_label\n")
    f.write(" _atom_site_symmetry_multiplicity\n")
    f.write(" _atom_site_fract_x\n")
    f.write(" _atom_site_fract_y\n")
    f.write(" _atom_site_fract_z\n")
    f.write(" _atom_site_occupancy\n")

    cnn.execute("SELECT * FROM {0}".format(formula))
    sites = [list(x) for x in cnn.fetchall()]
    print(sites)
    for site in sites:
        f.write("%s %s %d %g %g %g %g\n" % (site[0], site[1], site[2], site[3], site[4], site[5], site[6]))

    f.write("loop_\n")
    f.write(" _atom_site_moment_label\n")
    f.write(" _atom_site_moment_crystalaxis_x\n")
    f.write(" _atom_site_moment_crystalaxis_y\n")
    f.write(" _atom_site_moment_crystalaxis_z\n")

    f.close()


if __name__ == "__main__":
    set_cif("/Users/mac/Desktop/default.db", "/Users/mac/Desktop/foo.cif")
    slab = read("/Users/mac/Desktop/foo.cif")
    view(slab)