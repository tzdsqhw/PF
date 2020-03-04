import sqlite3


# 创建连接
def createtable(username):
    con = sqlite3.connect('./shopcar.db')
    # 创建游标对象
    cur = con.cursor()
    tn = username + '_table'
    # 编写创建表的sql语句
    sql = '''create table %s(
          goodsid INTEGER primary key,
          num INTEGER 
      )''' % tn
    try:
        # 执行sql语句
        cur.execute(sql)
        print('创建表成功')
    except Exception as e:
        print(e)
        print('创建表失败')
    finally:
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()


def insertg(username, gid, num,type):
    con = sqlite3.connect('./shopcar.db')
    # 创建游标对象
    cur = con.cursor()
    tn = username + '_table'
    # 编写创建表的sql语句
    sql0='select  count(*) from %s where goodsid = ?' % tn
    sql1 = 'update %s set num=? where goodsid=?'%tn
    sql = 'insert into %s(goodsid,num) values(?,?)' % tn
    sql2='select num from %s where goodsid=?'%tn
    cur.execute(sql0,(gid,))
    # 获取结果集
    flag = cur.fetchall()

    print(flag)
    cur.execute(sql2, (gid,))

    if flag[0][0]==0:
        try:
            cur.execute(sql, (gid, num))
            con.commit()
            print('插入数据成功')
        except Exception as e:
            print(e)
            con.rollback()
            print('插入数据失败')

        finally:
            # 关闭游标连接
            cur.close()
            # 关闭数据库连接
            con.close()
    else:
        if type=="1":
            try:
                cur.execute(sql1, (num, gid))
                # 提交事务
                con.commit()
                print('修改成功')
            except Exception as e:
                print(e)
                print('修改失败')
                con.rollback()
            finally:
                # 关闭游标连接
                cur.close()
                # 关闭数据库连接
                con.close()
        elif type=="2":
            try:
                num=cur.fetchall()
                print(num[0][0]+1)
                cur.execute(sql1, (num[0][0]+1, gid))
                # 提交事务
                con.commit()
                print('修改成功')
            except Exception as e:
                print(e)
                print('修改失败')
                con.rollback()
            finally:
                # 关闭游标连接
                cur.close()
                # 关闭数据库连接
                con.close()
def delet(username,goodsid):
    con = sqlite3.connect('./shopcar.db')
    # 创建游标对象
    cur = con.cursor()
    tn = username + '_table'
    # 编写创建表的sql语句
    sql = 'delete from %s where goodsid=?' % tn
    try:
        cur.execute(sql, (goodsid,))
        # 提交事务
        con.commit()
        print('删除成功')
    except Exception as e:
        print(e)
        print('删除失败')
        con.rollback()
    finally:
        # 关闭连接
        con.close()
def clean(username):
    con = sqlite3.connect('./shopcar.db')
    # 创建游标对象
    cur = con.cursor()
    tn = username + '_table'
    # 编写创建表的sql语句
    sql = 'delete from %s' % tn
    try:
        cur.execute(sql)
        # 提交事务
        con.commit()
        print('删除成功')
    except Exception as e:
        print(e)
        print('删除失败')
        con.rollback()
    finally:
        # 关闭连接
        con.close()
def showall(username):
    con = sqlite3.connect('./shopcar.db')
    # 创建游标对象
    cur = con.cursor()
    tn = username + '_table'
    # 编写创建表的sql语句
    sql = 'select * from %s' % tn
    try:
        cur.execute(sql)
        # 获取结果集
        goods_all = cur.fetchall()
        print(goods_all)
    except Exception as e:
        print(e)
        print('查询所有数据失败')
    finally:
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        return goods_all
