from PIL import Image
import matplotlib.pyplot as plt


img = Image.open('/Users/mac/Desktop/MoS2_IV.png')
plt.imshow(img)
plt.show()

'''
def set_up_iv(self):
    '''
创建储存
I - V
曲线坐标的表格
:return: None
'''
cnn = self.conn.cursor()
f = open(self.cif_dir, 'r')
content = f.read()
r_formula = re.findall('data_(.*?)\n', content)[0]
r_tbl_name = r_formula + "_IV"
tbl_name = "'" + r_tbl_name + "'"
cnn.execute('''
CREATE
TABLE % s
(seq INTEGER PRIMARY KEY   autoincrement,
V                 REAL  NOT NULL,
I                 REAL  NOT NULL)
''' % tbl_name)
    self.conn.commit()

def insert_into_iv(self, coordinate):
    '''
以元组的形式向
iv
表格中插入坐标
:param
coordinate: iv图像某点的坐标（x, y）
:return: None
'''
cnn = self.conn.cursor()
x = coordinate[0]
y = coordinate[1]
f = open(self.cif_dir, 'r')
content = f.read()
r_formula = re.findall('data_(.*?)\n', content)[0]
r_tbl_name = r_formula + "_IV"
tbl_name = "'" + r_tbl_name + "'"
cnn.execute("INSERT INTO {0} VALUES (NULL, {1}, {2})".format(tbl_name, x, y))
self.conn.commit()

def show_iv(self, formula):
'''
显示IV图像
:return: None
'''
cnn = self.conn.cursor()
r_formula = formula
formula = "'" + r_formula + "'"
cnn.execute("SELECT * FROM {}".format('MoS2_IV'))   #
iv_points = []
x_lst = []
y_lst = []
for coordinate in cnn.fetchall():
    iv_points.append(tuple([coordinate[1], coordinate[2]]))
for p in iv_points:
    x_lst.append(p[0])
    y_lst.append(p[1])
x_array = np.array(x_lst)
y_array = np.array(y_lst)
x_new = np.linspace(x_array.min(), x_array.max(), 300)
y_smooth = spline(x_array, y_array, x_new)
plt.xlabel("V")
plt.ylabel("I")
plt.plot(x_new, y_smooth)
plt.show()
'''




# coding=utf-8
import re
import sqlite3
import os


def set_up_db(dir):                 # dir: 数据库的路径 -- /Users/mac/Desktop/crystal.db
    '''
    用于建立 数据库 和 储存物理性质的表格 。
    :param dir: 函数所建立数据库的路径
    :return: None
    '''
    conn = sqlite3.connect(dir)
    cn = conn.cursor()
    cn.execute('''CREATE TABLE test 
                      (ID       INT PRIMARY KEY    NOT NULL,
                       Formula             TEXT    NOT NULL,
                       "a(Å)"              REAL    NOT NULL,
                       "b(Å)"              REAL    NOT NULL,
                       "c(Å)"              REAL    NOT NULL,
                       α                   REAL    NOT NULL,
                       β                   REAL    NOT NULL,
                       γ                   REAL    NOT NULL,
                       Volume              REAL    NOT NULL,
                       Device                      TEXT,
                       Hetero_junction             TEXT,
                       Optimal_Match               TEXT,
                       Layer                       TEXT,
                       "Binding_energy(eV)"        REAL,
                       "Schottky_barrier(eV)"      REAL,
                       Image_dir                   TEXT)''')
    conn.commit()
    conn.close()


def insert_into_db(cif_dir, db_dir, i):   # 录入数据库材料的cif文件路径， 自己建立的材料ID
    '''
    由于把 本地某个cif文件 的 物理性质 储存进相应的表格。
    :param cif_dir: cif文件所在路径
    :param db_dir: 数据库的路径
    :param i: 材料ID(默认从一递增，也可以自己输入)
    :return: None
    '''
    f = open(cif_dir, 'r')     # dir = '/Users/mac/Desktop/1.cif'
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

    conn = sqlite3.connect(db_dir)
    cn = conn.cursor()
    cn.execute("INSERT INTO test (ID, Formula, 'a(Å)', 'b(Å)', 'c(Å)', α, β, γ, Volume) VALUES (%d, %s, %g, %g, %g, %g, %g, %g, %g)" % (i, formula, a, b, c, angle_alpha, angle_beta, angle_gamma, volume))
    conn.commit()
    conn.close()
    f.close()


# def select_element(formula):


def get_paths(dir):        # 包含多个cif文件的目录的路径
    '''

    :param dir: cif文件所在文件夹的路径
    :return: 文件夹内所有cif文件组成的列表
    '''
    r_paths = os.listdir(dir)
    paths = [dir + '/' + x for x in r_paths if x != '.DS_Store']   # '/Users/mac/Desktop/ground'
    print(paths)
    return paths


if __name__ == "__main__":
    db_dir = '/Users/mac/Desktop/crystal.db'
    set_up_db(db_dir)
    paths = get_paths('/Users/mac/Desktop/ground')
    i = 1
    while paths:
        dir = paths.pop(0)
        insert_into_db(dir, db_dir, i)
        i += 1
        print(i)



$$$$$$$$$$$$
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
                               'a(Å)'              REAL    NOT NULL,
                               'b(Å)'              REAL    NOT NULL,
                               'c(Å)'              REAL    NOT NULL,
                               α                   REAL    NOT NULL,
                               β                   REAL    NOT NULL,
                               γ                   REAL    NOT NULL,
                               Volume              REAL    NOT NULL,
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

    def set_up_properties(self, content):
        '''
        建立储存某种材料所有组合器件的物理性质的表(名字：Formula_Device)
        :param db_dir: 数据路径
        :param content: 材料的化学式
        :return: None
        '''
        cnn = self.conn.cursor()
        if content.isdigit():
            cnn.execute("SELECT Formula FROM test WHERE ID={}".format(int(content)))
            content = cnn.fetchone()[0]
        tbl_name = content + "_Device"
        cnn.execute('''CREATE TABLE {0}(
                       Splice_ID                INTEGER, 
                       Splice                      TEXT,  
                       Device                      TEXT,
                       Hetero_junction             TEXT,
                       Optimal_Match               TEXT,
                       Layer                       TEXT,
                       "Binding_energy(eV)"        REAL,
                       "Schottky_barrier(eV)"      REAL,
                       Image_dir                   TEXT)'''.format(tbl_name))
        self.conn.commit()
        self.conn.close()

    def insert_into_properties(self, content, splice_content):
        cnn = self.conn.cursor()
        if content.isdigit():
            cnn.execute("SELECT Formula FROM test WHERE ID={}".format(int(content)))
            r_formula = cnn.fetchone()[0]
            ID = content
        else:
            cnn.execute("SELECT Formula FROM test WHERE Formula={}".format(content))
            ID = cnn.fetchone()[0]
            r_formula = content
        if splice_content.isdigit():
            cnn.execute("SELECT Formula FROM test WHERE ID={}".format(int(splice_content)))
            r_splice_formula = cnn.fetchone()[0]
            splice_ID = splice_content
        else:
            cnn.execute("SELECT Formula FROM test WHERE Formula={}".format(splice_content))
            splice_ID = cnn.fetchone()[0]
            r_splice_formula = splice_content
        tbl_name = r_formula + "_Device"
        print(tbl_name)
        formula = "'" + r_formula + "'"
        splice_formula = "'" + r_splice_formula + "'"
        cnn.execute('''INSERT INTO %s (ID, Formula, Splice_ID, Splice) 
                       VALUES (%d, %s, %d, %s)''' % (tbl_name, int(ID), formula, int(splice_ID), splice_formula))


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
    # object.set_up_properties("AgSe")
    object.insert_into_properties("1", "3")

    # object.set_up_db()
    # object.insert_into_db(10)
    # object.set_up_sites()
    object.close_db()

    print(object.path)



