import pymysql

# file_path = "exam.csv"
# table_name = 'update_time_table'

file_path = "export.csv"
table_name = "TBexport"
try:
    con = pymysql.connect(user="root",
                          passwd="root",
                          db="test",
                          host="47.95.20x.xxx",
                          local_infile=1)
    con.set_charset('utf8')
    cur = con.cursor()
    cur.execute("set names utf8")
    cur.execute("SET character_set_connection=utf8;")

    with open(file_path, 'r', encoding='utf8') as f:
        reader = f.readline()
        print(reader)
        devide = reader.split(',')  # 做成列表
        devide[-1] = devide[-1].rstrip('\n')  # 去除最后的换行符
        print(devide)

    column = ''
    for dd in devide:
        #如果标题过长，只能存成text格式
        if dd == "标题":
            column = column + dd + ' TEXT,'
        else:
            column = column + dd + ' varchar(255),'

    col = column.rstrip(',')  # 去除最后一个多余的，
    # print(column[:-1])

    create_table_sql = 'create table if not exists {} ({}) DEFAULT CHARSET=utf8'.format(table_name, col)
    print(create_table_sql)
    data = 'LOAD DATA LOCAL INFILE \'' + file_path + '\'REPLACE INTO TABLE ' + table_name + ' CHARACTER SET UTF8 FIELDS TERMINATED BY \',\' ENCLOSED BY \'\"\' LINES TERMINATED BY \'\n\' IGNORE 1 LINES;'
    cur.execute(create_table_sql)
    cur.execute(data.encode('utf8'))
    print(cur.rowcount)
    con.commit()
except:
    print("发生错误")
    con.rollback()

finally:
    cur.close()
    con.close()
