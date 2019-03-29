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
                       "a(Å)"              REAL,
                       "b(Å)"              REAL,
                       "c(Å)"              REAL,
                       α                   REAL,
                       β                   REAL,
                       γ                   REAL,
                       Volume              REAL,
                       Device                      TEXT,
                       Hetero_junction             TEXT,
                       Optimal_Match               TEXT,
                       Layer                       TEXT,
                       "Binding_energy(eV)"        REAL,
                       "Schottky_barrier(eV)"      REAL,
                       Image_dir           TEXT)''')
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


def set_up_properties(db_dir, content):
    '''
    建立储存某种材料所有组合器件的物理性质
    :param db_dir: 数据路径
    :param content: 材料的化学式
    :return:
    '''
    conn = sqlite3.connect(db_dir)
    cnn = conn.cursor()
    if content.isdigit():
        cnn.execute("SELECT Formula FROM test WHERE ID={}".format(int(content)))
        content = cnn.fetchone()[0]
    tbl_name = content + "_Device"
    cnn.execute('''CREATE TABLE {0}(
                   ID           INTEGER PRIMARY KEY,
                   Formula           TEXT  NOT NULL,
                   Splice                      TEXT,  
                   Device                      TEXT,
                   Hetero_junction             TEXT,
                   Optimal_Match               TEXT,
                   Layer                       TEXT,
                   "Binding_energy(eV)"        REAL,
                   "Schottky_barrier(eV)"      REAL,
                   Image_dir                   TEXT)'''.format(tbl_name))
    conn.commit()
    conn.close()



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
    paths = get_paths('/Users/mac/Desktop/crys')
    i = 1
    while paths:
        dir = paths.pop(0)
        insert_into_db(dir, db_dir, i)
        # set_up_properties(db_dir, str(i))
        i += 1
        print(i)

