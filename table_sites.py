# coding=utf-8
import re
import sqlite3
from database import get_paths


def set_up_sites(db_dir, cif_dir):        # cif_dir: 已存在的cif文件的路径, db_dir:database.py中创立数据库的路径
    '''
    建立 储存晶胞各点坐标的列表。
    :param db_dir: 数据库的路径
    :param cif_dir: cif文件的路径
    :return: None
    '''
    f = open(cif_dir, 'r')                # cif_dir = '/Users/mac/Desktop/1.cif'
    content = f.read()
    # print(content)
    r_formula = re.findall('data_(.*?)\n', content)[0]
    print(r_formula)
    formula = "'" + r_formula + "'"
    r_sites = re.findall('_atom_site_occupancy(.*?)loop_', content, re.S)[0]
    sites = r_sites.split('\n')
    sites.remove('')

    conn = sqlite3.connect(db_dir)        # '/Users/mac/Desktop/crystal.db'
    cnn = conn.cursor()
    cnn.execute('''CREATE TABLE %s
                       (Element             TEXT    NOT NULL,
                        Num                 TEXT    NOT NULL,
                        U1                  INT     NOT NULL,
                        X                   REAL    NOT NULL,
                        Y                   REAL    NOT NULL, 
                        Z                   REAL    NOT NULL,
                        U2                  INT     NOT NULL)''' % formula)
    conn.commit()

    for x in sites:
        if x is '':
            sites.remove(x)
    for i in range(0, len(sites)):
        row_lst = sites[i].split()
        print(row_lst)
        element = "'" + row_lst[0] + "'"
        order = row_lst[0] + str(i + 1)
        num = "'" + order + "'"
        cnn.execute("INSERT INTO %s (Element,Num,U1,X,Y,Z,U2) VALUES (%s, %s, 1, %g, %g, %g, 1)" % (formula, element, num, float(row_lst[3]), float(row_lst[4]), float(row_lst[5])))
        conn.commit()
    conn.close()


if __name__ == "__main__":
    paths = get_paths('/Users/mac/Desktop/ground')
    db_dir = '/Users/mac/Desktop/crystal.db'
    for x in paths:
        set_up_sites(db_dir, x)

