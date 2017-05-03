#!/usr/bin/python
# -*- coding: utf-8 -*-

""" User Database
"""

import copy
import sqlalchemy
import leveldb

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Integer,
    ForeignKey,
    func,
    create_engine,
    desc
    )
from sqlalchemy.orm import (
    relationship,
    backref,
    sessionmaker
    )
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = None
engine = None
session = None

def sql_init():
    global Base
    global engine
    global session
    Base = declarative_base()
    engine = create_engine('sqlite:///employee.sqlite', encoding='utf-8')
    session = sessionmaker()
    session.configure(bind=engine)

sql_init()


class Employee(Base):
    __tablename__ = 'lfemployee'
    #id = Column(Integer, primary_key=True)
    username = Column(String, primary_key=True)
    password = Column(String)
    name = Column(String)
    mobile = Column(String)
    area = Column(String)
    areacode = Column(String)
    role = Column(String) # root or areamng
    desc = Column(String) # discription about this guy

    def __repr__(self):
        return 'name: {}; username: {}'.format(self.name, self.username)

class Advideo(Base):
    __tablename__ = 'advideo'
    #__table_args__ = {'sqlite_autoincrement': True}
    cid = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    videoname = Column(String)
    user = Column(String)
    time = Column(DateTime)


class InfoItem(Base):
    __tablename__ = 'infoservice'
    __table_args__ = {'sqlite_autoincrement': True}
    cid = Column(Integer, primary_key=True)
    filename = Column(String)
    picname = Column(String)
    qrname = Column(String)
    textname = Column(String)
    user = Column(String)
    time = Column(DateTime)

class DancingVideo(Base):
    __tablename__ = 'dancing'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    videoname = Column(String)
    user = Column(String)
    time = Column(DateTime)

class CommPic(Base):
    __tablename__ = 'commpic'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    picname = Column(String)
    textname = Column(String)
    user = Column(String)
    time = Column(DateTime)

class Museum(Base):
    __tablename__ = 'museum'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    picname = Column(String)
    textname = Column(String)
    user = Column(String)
    time = Column(DateTime)

class GovernInfo(Base):
    __tablename__ = 'governinfo'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    picname = Column(String)
    textname = Column(String)
    user = Column(String)
    time = Column(DateTime)

class Breaking(Base):
    __tablename__ = 'breaking'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    picname = Column(String)
    textname = Column(String)
    user = Column(String)
    time = Column(DateTime)

class Convinient(Base):
    __tablename__ = 'convinient'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    picname = Column(String)
    textname = Column(String)
    user = Column(String)
    time = Column(DateTime)

class User(Base):
    __tablename__ = 'userinfo'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(String)
    cardno = Column(String)
    town = Column(String)
    country = Column(String)
    devno = Column(String)
    seqno = Column(Integer)
    admin = Column(String)
    count = Column(Integer)

class GeoInfo(Base):
    __tablename__ = 'geoinfo'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    townname = Column(String)
    towncode = Column(String)
    counname = Column(String)
    councode = Column(String)
    devname  = Column(String)
    devcode  = Column(String)
    ipaddr   = Column(String)

class Town(Base):
    __tablename__ = 'towninfo'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    townname = Column(String)
    towncode = Column(String)

class Country(Base):
    __tablename__ = 'countryinfo'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    counname = Column(String)
    councode = Column(String)
    townid = Column(Integer)

class Terminal(Base):
    __tablename__ = 'terminfo'
    cid = Column(Integer, primary_key=True, autoincrement=True)
    termname = Column(String)
    termcode = Column(String)
    counid = Column(Integer)
    ipaddr = Column(String)


class DbOperation():
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = session()

    def add(self, username, password, name, mobile, area, areacode, role, desc=''):
        emp = Employee(
            username=username,
            password=password,
            name=name,
            mobile=mobile,
            area=area,
            areacode=areacode,
            role=role,
            desc=desc)
        #s = session()
        try:
            self.session.add(emp)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            print 'record already existing, username: {}'.format(username)

    # Adv video functions
    def add_video(self, filename, videoname, user, time):
        video = Advideo(filename=filename, videoname=videoname, user=user, time=datetime.now())
        try:
            self.session.add(video)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            print 'record already existing, filename: {}'.format(filename)

    def get_video_by_user(self, user):
        return self.session.query(Advideo).filter(Advideo.user==user).all()

    def get_video_by_rowid(self, rid):
        return self.session.query(Advideo).filter(Advideo.cid==rid).first()

    def del_video_by_rowid(self, rid):
        try:
            self.session.delete(self.get_video_by_rowid(rid))
            self.session.commit()
        except:
            print 'No del needed {}'.format(rid)

    #info item functions
    def add_info_item(self, fn, pn, qr, txt, user, t):
        info = InfoItem(filename=fn, picname=pn, qrname=qr, textname=txt, user=user, time=t)
        try:
            self.session.add(info)
            self.session.commit()
        except:
            self.session.rollback()
            print 'add info item failed {}'.format(filename)

    def get_info_items_by_user(self, user):
        return self.session.query(InfoItem).filter(InfoItem.user==user).all()

    def get_info_item_by_rowid(self, rid):
        return self.session.query(InfoItem).filter(InfoItem.cid==rid).first()

    def del_info_item_by_rowid(self, rid):
        try:
            self.session.delete(self.get_info_item_by_rowid(rid))
            self.session.commit()
        except:
            print 'No infoitem del needed {}'.format(rid)

    #dancing video functions
    def add_dancing_video(self, filename, videoname, user, time):
        video = DancingVideo(filename=filename, videoname=videoname, user=user, time=datetime.now())
        try:
            self.session.add(video)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            print 'dancing video already existing, filename: {}'.format(filename)

    def get_dancing_video_by_user(self, user):
        return self.session.query(DancingVideo).filter(DancingVideo.user==user).all()

    def get_dancing_video_by_rowid(self, rid):
        return self.session.query(DancingVideo).filter(DancingVideo.cid==rid).first()

    def del_dancing_video_by_rowid(self, rid):
        try:
            self.session.delete(self.get_dancing_video_by_rowid(rid))
            self.session.commit()
        except:
            print 'No del dancing needed {}'.format(rid)

    #commpics function
    def add_comm_pic(self, fn, pn, tn, user, t):
        info = CommPic(filename=fn, picname=pn, textname=tn, user=user, time=t)
        try:
            self.session.add(info)
            self.session.commit()
        except:
            self.session.rollback()
            print 'add CommPic failed {}'.format(filename)

    def get_comm_pics_by_user(self, user):
        return self.session.query(CommPic).filter(CommPic.user==user).all()

    def get_comm_pic_by_rowid(self, rid):
        return self.session.query(CommPic).filter(CommPic.cid==rid).first()

    def del_comm_pic_by_rowid(self, rid):
        try:
            self.session.delete(self.get_comm_pic_by_rowid(rid))
            self.session.commit()
        except:
            print 'No CommPic del needed {}'.format(rid)

    #museum functions
    def add_museum_pic(self, fn, pn, tn, user, t):
        mupic = Museum(filename=fn, picname=pn, textname=tn, user=user, time=t)
        try:
            self.session.add(mupic)
            self.session.commit()
        except:
            self.session.rollback()
            print 'add Museum pic failed {}'.format(filename)

    def get_museum_pics_by_user(self, user):
        return self.session.query(Museum).filter(Museum.user==user).all()

    def get_museum_pic_by_rowid(self, rid):
        return self.session.query(Museum).filter(Museum.cid==rid).first()

    def del_museum_pic_by_rowid(self, rid):
        try:
            self.session.delete(self.get_museum_pic_by_rowid(rid))
            self.session.commit()
        except:
            print 'No Museum del needed {}'.format(rid)

    #governinfo functions
    def add_govern_pic(self, fn, pn, tn, user, t):
        govpic = GovernInfo(filename=fn, picname=pn, textname=tn, user=user, time=t)
        try:
            self.session.add(govpic)
            self.session.commit()
        except:
            self.session.rollback()
            print 'add Govern Info pic failed {}'.format(filename)

    def get_govern_pics_by_user(self, user):
        return self.session.query(GovernInfo).filter(GovernInfo.user==user).all()

    def get_govern_pic_by_rowid(self, rid):
        return self.session.query(GovernInfo).filter(GovernInfo.cid==rid).first()

    def del_govern_pic_by_rowid(self, rid):
        try:
            self.session.delete(self.get_govern_pic_by_rowid(rid))
            self.session.commit()
        except:
            print 'No goverinfo del needed {}'.format(rid)

    def add_breaking_pic(self, fn, pn, tn, user, t):
        brkpic = Breaking(filename=fn, picname=pn, textname=tn, user=user, time=t)
        try:
            self.session.add(brkpic)
            self.session.commit()
        except:
            self.session.rollback()
            print 'add Breaking Info pic failed {}'.format(filename)

    def get_breaking_pics_by_user(self, user):
        return self.session.query(Breaking).filter(Breaking.user==user).all()

    def get_breaking_pic_by_rowid(self, rid):
        return self.session.query(Breaking).filter(Breaking.cid==rid).first()

    def del_breaking_pic_by_rowid(self, rid):
        try:
            self.session.delete(self.get_breaking_pic_by_rowid(rid))
            self.session.commit()
        except:
            print 'No goverinfo del needed {}'.format(rid)

    def add_convinient_pic(self, fn, pn, tn, user, t):
        convpic = Convinient(filename=fn, picname=pn, textname=tn, user=user, time=t)
        try:
            self.session.add(convpic)
            self.session.commit()
        except:
            self.session.rollback()
            print 'add Convinient Info pic failed {}'.format(filename)

    def get_convinient_pics_by_user(self, user):
        return self.session.query(Convinient).filter(Convinient.user==user).all()

    def get_convinient_pic_by_rowid(self, rid):
        return self.session.query(Convinient).filter(Convinient.cid==rid).first()

    def del_convinient_pic_by_rowid(self, rid):
        try:
            self.session.delete(self.get_convinient_pic_by_rowid(rid))
            self.session.commit()
        except:
            print 'No goverinfo del needed {}'.format(rid)

    def add_bin_user(self, cardno, town, country, devno, seqno, admin, name='', phone='', count=0):
        u = User(name=name, phone=phone, cardno=cardno, town=town,
                 country=country, devno=devno, admin=admin, seqno=seqno, count=count)
        try:
            self.session.add(u)
            self.session.commit()
        except:
            self.session.rollback()
            print 'add bin user failed {}'.format(cardno)

    def get_bin_users_by_admin(self, admin):
        return self.session.query(User).filter(User.admin==admin).all()

    def get_bin_user_by_id(self, rid):
        return self.session.query(User).filter(User.cid==rid).first()

    def get_bin_user_by_cardno(self, cardno):
        return self.session.query(User).filter(User.cardno==cardno).first()

    def get_bin_user_by_geoinfo(self, town, country, dev, seq):
        return self.session.query(User).filter(User.town==town
            , User.country==country
            , User.devno==dev
            , User.seqno==seq).first()

    def get_bin_user_rank(self, cardno):
        users = self.session.query(User).order_by(desc(User.count))
        for i, u in enumerate(users):
            if u.cardno == cardno:
                return i+1
        return 'unknown'

    def del_bin_user_by_cardno(self, cardno):
        try:
            self.session.delete(self.get_bin_user_by_cardno(cardno))
            self.session.commit()
        except:
            print 'No bin user deleted {}'.format(cardno)

    def del_bin_user_by_id(self, rid):
        try:
            self.session.delete(self.get_bin_user_by_id(rid))
            self.session.commit()
        except:
            print 'No bin user deleted {}'.format(rid)

    def update_bin_user_count(self, cardno):
        u = self.get_bin_user_by_cardno(cardno)
        u.count += 1
        try:
            self.session.commit()
        except:
            print 'update user bin use failed, cardno: {}'.format(cardno)

    def update_bin_user_basic_info(self, town, country, devno, seqno,
                                name='', phone='', cardno='88888888'):
        u = self.get_bin_user_by_geoinfo(town, country, devno, seqno)
        if u:
            u.name = name
            u.phone = phone
            u.cardno = cardno
            self.session.commit()
            return True
        else:
            return False

    def update_bin_user_by_id(self, cid, name='', phone='', cardno='88888888'):
        u = self.get_bin_user_by_id(cid)
        if u:
            u.name = name
            u.phone = phone
            u.cardno = cardno
            self.session.commit()
            return True
        else:
            return False

    def get(self, username):
        return self.session.query(Employee).filter(Employee.username==username).first()

    def verify(self, u, p):
        user = self.session.query(Employee).filter(Employee.username==u).first()
        if user.password == p:
            return True
        else:
            return False

    def update(self, username):
        emp = self.get(username)
        #some thing to update
        try:
            self.session.add(emp)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            print 'record update failed, User: {}'.format(username)

    def add_geoinfo(self, tn, tc, cn, cc, dn, dc, ip):
        g = GeoInfo(townname=tn, towncode=tc, counname=cn, councode=cc,
            devname=dn, devcode=dc, ipaddr=ip)
        try:
            self.session.add(g)
            self.session.commit()
        except:
            self.session.rollback()
            print 'add geoinfo failed, {}'.format(tn)

    def get_geoinfo(self):
        return self.session.query(GeoInfo).all()

    def get_geoinfo_by_id(self, id):
        return self.session.query(GeoInfo).filter(GeoInfo.cid==id).first()

    def del_geoinfo(self, id):
        try:
            self.session.delete(self.get_geoinfo_by_id(id))
            self.session.commit()
        except:
            print 'No geoinfo deleted {}'.format(id)

    def add_town(self, townname, towncode):
        t = Town(townname=townname, towncode=towncode)
        try:
            self.session.add(t)
            self.session.commit()
        except Exception as e:
            print 'add towninfo failed, {}'.format(e)

    def get_towns(self):
        return self.session.query(Town).all()

    def add_country(self, counname, councode, townid):
        t = Country(counname=counname, councode=councode, townid=townid)
        try:
            self.session.add(t)
            self.session.commit()
        except Exception as e:
            print 'add country failed, {}'.format(e)

    def get_countries_by_townid(self, townid):
        return self.session.query(Country).filter(Country.townid==townid).all()

    def add_terminal(self, tn, tc, ci, ip):
        tmn = Terminal(termname=tn, termcode=tc, counid=ci, ipaddr=ip)
        try:
            self.session.add(tmn)
            self.session.commit()
        except Exception as e:
            print 'add terminal failed. {}'.format(e)

    def get_terminals_by_country_id(self, counid):
        return self.session.query(Terminal).filter(Terminal.counid==counid).all()

def create_all_users():
    users = [
        {'username': 'dipuadmin', 'password': 'dipuadmin', 'name': '递铺街道管理员'.decode('utf8'), 'mobile': '00000000000',
         'area': '递铺街道'.decode('utf8'), 'areacode': 10, 'role': 'areamng'},
        {'username': 'lingfengadmin', 'password': 'lingfengadmin', 'name': '灵峰街道管理员'.decode('utf8'), 'mobile': '00000000000',
         'area': '灵峰街道'.decode('utf8'), 'areacode': 11, 'role': 'areamng'},
        {'username': 'shangshuadmin', 'password': 'shangshuadmin', 'name': '上墅乡管理员'.decode('utf8'), 'mobile': '00000000000',
         'area': '上墅乡'.decode('utf8'), 'areacode': 12, 'role': 'areamng'},
        {'username': 'zhangwuadmin', 'password': 'zhangwuadmin', 'name': '鄣吴镇管理员'.decode('utf8'), 'mobile': '00000000000',
         'area': '鄣吴镇'.decode('utf8'), 'areacode': 13, 'role': 'areamng'},
        {'username': 'tianhuangpingadmin', 'password': 'tianhuangpingadmin', 'name': '天荒坪管理员'.decode('utf8'), 'mobile': '00000000000',
         'area': '天荒坪'.decode('utf8'), 'areacode': 14, 'role': 'areamng'},

        {'username': 'admin', 'password': 'admin2016', 'name': '总管理员'.decode('utf8'), 'mobile': '00000000000',
         'area': '安吉'.decode('utf8'), 'areacode': 00, 'role': 'root'}
    ]
    op = DbOperation()
    for u in users:
        op.add(u['username'], u['password'], u['name'], u['mobile'], u['area'], u['areacode'], u['role'])

def add_towns():
    towns = [
        (u'灵峰街道', 'LF'),
        (u'上墅乡', 'SS'),
        (u'递铺街道', 'DP'),
        (u'天荒坪镇', 'THP'),
        (u'鄣吴镇', 'ZW'),
    ]
    op = DbOperation()
    for t in towns:
        n, c = t
        op.add_town(n, c)
    print 'towns added'

def add_countries():
    countries = [
        (u'灵峰村', 'LF', 1),
        (u'剑山村', 'JS', 1),
        (u'大竹园村', 'DZY', 1),
        (u'城南村', 'CN', 1),
        (u'碧门村', 'BM', 1),
        (u'霞泉村', 'XQ', 1),
        (u'刘家塘村', 'LJT', 2),
        (u'田垓村', 'TG', 2),
        (u'上墅村', 'SS', 2),
        (u'罗村', 'LC', 2),
        (u'施阮村', 'SL', 2),
        (u'龙王村', 'LW', 2),
        (u'董岭村', 'DL', 2),
        (u'鲁家村', 'LJ', 3),
        (u'古城村', 'GC', 3),
        (u'白水湾村', 'BSW', 4),
        (u'井村', 'JC', 4),
        (u'山河村', 'SH', 4),
        (u'横路村', 'HL', 4),
        (u'余村', 'YC', 4),
        (u'银坑村', 'YK', 4),
        (u'马吉村', 'MJ', 4),
        (u'西鹤村', 'XH', 4),
        (u'五鹤村', 'WH', 4),
        (u'港口村', 'GK', 4),
        (u'鄣吴村', 'ZW', 5),
        (u'玉华村', 'YH', 5),
        (u'景坞村', 'JW', 5),
        (u'民乐村', 'ML', 5),
        (u'上吴村', 'SW', 5),
        (u'上堡村', 'SBC', 5),
    ]
    op = DbOperation()
    for c in countries:
        name, code, id = c
        op.add_country(counname=name, councode=code, townid=id)
    print 'countries added'

def add_terminals():
    terminals = [
        (u'下扇社区', 'A', 1, u'172.18.1.27'),
        (u'水口社区', 'B', 1, u'172.18.1.9'),
        (u'河边', 'A', 2, u'172.18.1.5'),
        (u'河边社区', 'B', 2, u'172.18.1.6'),
        (u'村委社区', 'C', 2, u'172.18.1.7'),
        (u'中管', 'A', 3, u'172.18.1.28'),
        (u'村委', 'B', 3, u'172.18.1.42'),
        (u'城南村', 'A', 4, u'172.18.1.8'),
        (u'碧门村', 'A', 5, u'172.18.1.4'),
        (u'霞泉村', 'A', 6, u'172.18.1.29'),
        (u'村委', 'A', 7, u'172.18.1.39'),
        (u'狮子石', 'B', 7, u'172.18.1.40'),
        (u'村委', 'A', 8, u'172.18.1.17'),
        (u'主路边', 'B', 8, u'172.18.1.33'),
        (u'松果', 'A', 9, u'172.18.1.34'),
        (u'三岔路口', 'B', 9, u'172.18.1.43'),
        (u'桥边', 'A', 10, u'172.18.1.35'),
        (u'车站', 'B', 10, u'172.18.1.36'),
        (u'施善村', 'A', 11, u'172.18.1.18'),
        (u'村委', 'B', 11, u'172.18.1.19'),
        (u'阮村', 'A', 12, u'172.18.1.2'),
        (u'龙王村', 'B', 12, u'172.18.1.3'),
        (u'村委', 'A', 13, u'172.18.1.37'),
        (u'农家乐', 'B', 13, u'172.18.1.38'),
        (u'村委', 'A', 14, u'172.18.1.13'),
        (u'大路桥', 'B', 14, u'172.18.1.14'),
        (u'夏家上', 'C', 14, u'172.18.1.12'),
        (u'六安桥', 'D', 14, u'172.18.1.41'),
        (u'村委', 'A', 15, u'172.18.1.60'),
        (u'河边', 'B', 15, u'172.18.1.61'),
        (u'菜场', 'A', 16, u'172.18.1.32'),
        (u'河边', 'B', 16, u'172.18.1.57'),
        (u'墩上', 'A', 17, u'172.18.1.45'),
        (u'姚家大院', 'B', 17, u'172.18.1.46'),
        (u'石门村', 'A', 18, u'172.18.1.47'),
        (u'沿街商铺', 'B', 18, u'172.18.1.48'),
        (u'村委门口', 'A', 19, u'172.18.1.20'),
        (u'潘村', 'B', 19, u'172.18.1.21'),
        (u'路边电线', 'A', 20, u'172.18.1.58'),
        (u'山边上', 'B', 20, u'172.18.1.59'),
        (u'银坑景区', 'A', 21, u'172.18.1.30'),
        (u'路边', 'B', 21, u'172.18.1.31'),
        (u'卫生院', 'A', 22, u'172.18.1.51'),
        (u'杨家塘村', 'B', 22, u'172.18.1.52'),
        (u'村委', 'A', 23, u'172.18.1.53'),
        (u'西吉坞', 'B', 23, u'172.18.1.54'),
        (u'村委', 'A', 24, u'172.18.1.55'),
        (u'大竹海', 'B', 24, u'172.18.1.56'),
        (u'桐坞里', 'A', 25, u'172.18.1.15'),
        (u'东坞里', 'B', 25, u'172.18.1.16'),
        (u'车站', 'A', 26, u'172.18.1.62'),
        (u'昌硕小学', 'B', 26, u'172.18.1.63'),
        (u'玉华1', 'A', 27, u'172.18.1.64'),
        (u'玉华2', 'B', 27, u'172.18.1.65'),
        (u'村委', 'A', 28, u'172.18.1.66'),
        (u'无蚊村', 'B', 28, u'172.18.1.67'),
        (u'村委', 'A', 29, u'172.18.1.22'),
        (u'水库边上', 'B', 29, u'172.18.1.68'),
        (u'低处', 'A', 30, u'172.18.1.69'),
        (u'高处', 'B', 30, u'172.18.1.23'),
        (u'污水站', 'A', 31, u'172.18.1.24'),
        (u'路边', 'B', 31, u'172.18.1.25'),
    ]
    op = DbOperation()
    for t in terminals:
        n, c, ci, ip = t
        op.add_terminal(n, c, ci, ip)
    print 'add terminals done'

def get_geo_tree(user='dipuadmin'):
    tree = []
    op = DbOperation()
    ldb = leveldb.LevelDB('./distsdb')
    checked = ldb.Get(user)
    print checked
    towns = op.get_towns()
    for town in towns:
        twnode = {"text": town.townname, "id": 'twn-'+town.towncode,
            "icon": "fa fa-street-view fa-large"}
        ch_couns = op.get_countries_by_townid(town.cid)
        town_children = []
        for coun in ch_couns:
            cnnode = {"text": coun.counname, "id": 'cn-'+coun.councode,
                "icon": "fa fa-home fa-large"}
            ch_terms = op.get_terminals_by_country_id(coun.cid)
            coun_children = []
            for term in ch_terms:
                tmnode = {"text": term.termname+term.termcode, "id": term.ipaddr,
                    "icon": "fa fa-tree fa-large", "state": {}}
                if term.ipaddr in checked.split(';'):
                    tmnode['state']['checked'] = True
                coun_children.append(tmnode)
            cnnode['children'] = coun_children
            town_children.append(cnnode)
        twnode['children'] = town_children
        tree.append(twnode)
    return tree

import unittest
class TestEmployee(unittest.TestCase):

    def test_verify(self):
        emop = DbOperation()
        self.assertTrue(emop.verify('dipuadmin', 'dipuadmin'))
        self.assertTrue(emop.verify('admin', 'admin2016'))

    def test_add_video(self):
        op = DbOperation()
        op.add_video('', 'mov_ddd0.mp4', 'dipuadmin', datetime.now())
        video = op.get_video_by_user('dipuadmin')
        for f in video:
            print f.cid, f.filename
        s = session()
        #print s.query(Advideo).first().time
        print s.query(Advideo).count()
        self.assertTrue(s.query(Advideo).count()!=0)

    def test_update_user_count(self):
        op = DbOperation()
        #op.add_bin_user('michelle', '15555555555', '11111111', 'dipuadmin')
        #op.update_bin_user_count('11111111')
        u = op.get_bin_user_by_cardno('11111111')
        if u:
            print u.count
            self.assertTrue(u.count == 2)

    def test_get_bin_user_rank(self):
        op = DbOperation()
        op.add_bin_user('michelle', '15555555555', '22222222', 'binjiang', 'puyan', 'dongguan', 'dipuadmin')
        for i in range(5):
            op.update_bin_user_count('22222222')
        rank = op.get_bin_user_rank('22222222')
        self.assertTrue(rank == 1)

    def test_get_geo_tree(self):
        print get_geo_tree()


if __name__ == '__main__':
    #create_all_users()
    #add_towns()
    #add_countries()
    #add_terminals()
    #s = session()
    #print s.query(Employee).count()
    #for u in s.query(Employee):
    #    print u.username, u.name
    unittest.main()
