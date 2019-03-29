# coding=utf-8
import re
import sqlite3


class DatabaseRow:
    def __init__(self, db_dir, *cif_dir):
        '''
        DatabaseRow类：创建并完善 Database 的类方法的集合
        :param db_dir: 数据库的路径
        :param cif_dir: 本地cif文件的路径
        '''
        self.path = db_dir
        self.conn = sqlite3.connect(self.path)
        for x in cif_dir:
            self.cif_dir = x

    def set_up_db(self):
        '''
        创建 test (用于储存材料物理性质的表格)
        :return: None
        '''
        # 先连接
        cn = self.conn.cursor()
        cn.execute('''CREATE TABLE test 
                              (ID       INT PRIMARY KEY    NOT NULL,
                               Formula             TEXT    NOT NULL,
                               'a(Å)'                      REAL,
                               'b(Å)'                      REAL,
                               'c(Å)'                      REAL,
                               α                           REAL,
                               β                           REAL,
                               γ                           REAL,
                               Volume                      REAL,
                               Device                      TEXT,
                               Hetero_junction             TEXT,
                               Optimal_Match               TEXT,
                               Layer                       TEXT,
                               "Binding_energy(eV)"        REAL,
                               "Schottky_barrier(eV)"      REAL,
                               Image_dir                   TEXT)''')
        self.conn.commit()

    def insert_into_db(self, i):
        '''
        将cif_dir处的材料插入test表格
        :param i: 材料的ID
        :return: None
        '''
        f = open(self.cif_dir, 'r')  # dir = '/Users/mac/Desktop/1.cif'
        content = f.read()
        r_formula = re.findall('data_(.*?)\n', content)[0]
        formula = "'" + r_formula + "'"
        symmetry = re.findall('_symmetry_space_group_name_H-M(.*?)\n', content)[0].strip()
        a = float(re.findall('_cell_length_a(.*?)\n', content)[0].strip())
        b = float(re.findall('_cell_length_b(.*?)\n', content)[0].strip())
        c = float(re.findall('_cell_length_c(.*?)\n', content)[0].strip())
        angle_alpha = float(re.findall('_cell_angle_alpha(.*?)\n', content)[0].strip())
        angle_beta = float(re.findall('_cell_angle_beta(.*?)\n', content)[0].strip())
        angle_gamma = float(re.findall('_cell_angle_gamma(.*?)\n', content)[0].strip())
        volume = float(re.findall('_cell_volume(.*?)\n', content)[0].strip())

        # 先连接
        cn = self.conn.cursor()
        cn.execute(
            "INSERT INTO test (ID, Formula, 'a(Å)', 'b(Å)', 'c(Å)', α, β, γ, Volume) VALUES (%d, %s, %g, %g, %g, %g, %g, %g, %g)" % (
            i, formula, a, b, c, angle_alpha, angle_beta, angle_gamma, volume))
        self.conn.commit()

    def set_up_relation(self):
        '''
        创建表格储存所有的堆垛情况(多对多关系)
        :return: None
        '''
        cnn = self.conn.cursor()
        cnn.execute('''CREATE TABLE relation(
                       ID         INT,
                       Formula    TEXT,
                       Splice_ID  INT,
                       Splice     TEXT,
                       Device                      TEXT,
                       Hetero_junction             TEXT,
                       Optimal_Match               TEXT,
                       Layer                       TEXT,
                       "Binding_energy(eV)"        REAL,
                       "Schottky_barrier(eV)"      REAL,
                       Image_dir                   TEXT)''')
        self.conn.commit()

    def set_up_sites(self):
        '''
        创建储存各点坐标的表格
        :return: None
        '''
        f = open(self.cif_dir, 'r')
        content = f.read()
        # print(content)
        r_formula = re.findall('data_(.*?)\n', content)[0]
        print(r_formula)
        formula = "'" + r_formula + "'"
        r_sites = re.findall('_atom_site_occupancy(.*?)loop_', content, re.S)[0]
        sites = r_sites.split('\n')
        sites.remove('')

        cnn = self.conn.cursor()
        cnn.execute('''CREATE TABLE %s
                               (Element             TEXT    NOT NULL,
                                Num                 TEXT    NOT NULL,
                                U1                  INT     NOT NULL,
                                X                   REAL    NOT NULL,
                                Y                   REAL    NOT NULL, 
                                Z                   REAL    NOT NULL,
                                U2                  INT     NOT NULL)''' % formula)
        self.conn.commit()

        for x in sites:
            if x is '':
                sites.remove(x)
        for i in range(0, len(sites)):
            row_lst = sites[i].split()
            print(row_lst)
            element = "'" + row_lst[0] + "'"
            order = row_lst[0] + str(i + 1)
            num = "'" + order + "'"
            cnn.execute("INSERT INTO %s (Element,Num,U1,X,Y,Z,U2) VALUES (%s, %s, 1, %g, %g, %g, 1)" % (
            formula, element, num, float(row_lst[3]), float(row_lst[4]), float(row_lst[5])))
            self.conn.commit()

    def set_cif(self, new_cif_db):
        '''
        根据数据库中信息创建cif文件
        :param new_cif_db: 新创建cif文件的路径
        :return: None
        '''
        cnn = self.conn.cursor()

        f = open(new_cif_db, 'a')  # cif_dir = "/Users/mac/Desktop/foo.cif"
        f.write("# generated using pymatgen\n")

        cnn.execute("SELECT * FROM test WHERE Formula={}".format(self.formula))
        f.write("data_{}\n".format(self.formula.strip("'")))
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

        cnn.execute("SELECT * FROM {0}".format(self.formula))
        sites = [list(x) for x in cnn.fetchall()]
        print(sites)
        for site in sites:
            f.write("%s %s %d %g %g %g %g\n" % (site[0], site[1], site[2], site[3], site[4], site[5], site[6]))

        f.write("loop_\n")
        f.write(" _atom_site_moment_label\n")
        f.write(" _atom_site_moment_crystalaxis_x\n")
        f.write(" _atom_site_moment_crystalaxis_y\n")
        f.write(" _atom_site_moment_crystalaxis_z\n")

    def close_db(self):
        '''
        断开数据库连接
        '''
        self.conn.close()


if __name__ == "__main__":
    object = DatabaseRow('/Users/mac/Desktop/crystal.db', '/Users/mac/Desktop/2.cif')
    # object.set_up_relation()
    # content = input("输入材料的ID或化学式：")
    # splice = input("输入用于堆垛的材料的化学式或ID")
    # object.set_up_properties(content)
    # object.insert_into_properties(content, splice)
    # object.set_up_db()
    # object.insert_into_db(10)
    # object.set_up_sites()
    print(object.path)
    object.close_db()
