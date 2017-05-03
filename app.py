# -*- coding:utf8 -*-

import os
import os.path
import json
import leveldb
import userdb
#import publisher

from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    session,
    Response,
    )
from datetime import datetime
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
from werkzeug.utils import secure_filename


session_opts = {
    #'session.type': 'ext:memcached',
    'session.type': 'memory',
    #'session.url': '127.0.0.1:8000',
    #'session.data_dir': './cache',
}

class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        session.save()

app = Flask(__name__)

app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
app.session_interface = BeakerSessionInterface()

USER_FOLDER = './static/userdirs'

#helper functions
def create_userdir(usrfldr):
    if not os.path.exists(usrfldr):
        os.mkdir(usrfldr)
    subfolders = ['advds', 'adimgs', 'info', 'commpics', 'commgov', 'commsqr', 'commuseum']
    for f in subfolders:
        subf = os.path.join(usrfldr, f)
        if not os.path.exists(subf):
            os.mkdir(subf)

def set_ad_video_in_session():
    op = userdb.DbOperation()
    user = op.get(session['user'])
    folder = os.path.join(USER_FOLDER, session['user'], 'advds')
    #print folder
    allvideo = os.listdir(folder)
    videoinfo = []
    for v in allvideo:
        name, ext = os.path.splitext(v)
        size = os.path.getsize(os.path.join(folder, v)) / 1024
        videoinfo.append((name, size, ext, user.area))
    videoinfo = enumerate(videoinfo)
    session['advideo'] = videoinfo

@app.route("/oldindex")
def oi():
    return render_template('/index_orig.html')

@app.route("/")
def index():
    return redirect('/ad')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usr = request.form['regular']
        pas = request.form['pass']
        if 'checkbox1' in request.form:
            pass
            #print request.form['checkbox1']
        else:
            #print 'not checked'
            pass
        op = userdb.DbOperation()
        if op.verify(usr, pas):
            if 'user' not in session:
                session['user'] = usr
            else:
                if session['user'] == usr:
                    pass
                    #print 'stored session: {}'.format(session['user'])
                else:
                    #print 'another user use this session'
                    session['user'] = usr
            upath = os.path.join(USER_FOLDER, usr)
            if not os.path.exists(upath):
                create_userdir(upath)
            return redirect('/ad/video')
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.delete()
    return redirect('/login')

@app.route("/blank")
def blank():
    return render_template('blank.html')

@app.route("/media")
def media():
    return render_template('media.html')

@app.route("/ad")
def ad():
    if 'user' in session:
        set_ad_video_in_session()
        op = userdb.DbOperation()
        user = op.get(session['user'])
        return render_template('ad.html', usersname=user.name)
    return redirect('/login')

@app.route("/face-recognition")
def face_recg():
    if 'user' in session:
        op = userdb.DbOperation()
        user = op.get(session['user'])
        return render_template('face_recg.html', usersname=user.name)
    return redirect('/login')

@app.route("/pav-detect")
def pav_det():
    if 'user' in session:
        op = userdb.DbOperation()
        user = op.get(session['user'])
        return render_template('pav-detect.html', usersname=user.name)
    return redirect('/login')

@app.route("/ad/video", methods=['GET', 'POST'])
def vedio():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    if request.method == 'POST':
        filename = request.form['filename']
        videofile = request.files['file']
        videopath = os.path.join(USER_FOLDER, user.username, 'advds',
                                 videofile.filename)
        if not os.path.isfile(videopath):
            videofile.save(videopath)
            abspath = os.path.abspath(videopath)
            #print abspath
            publisher.publish('advds&&%s'%(abspath), session['user'])
            #print session['user']
            print 'add video', user.username
            op.add_video(filename, videofile.filename, user.username, datetime.now())
            #print filename
    folder = os.path.join(USER_FOLDER, user.username, 'advds')
    #allvideo = os.listdir(folder)
    allvideo = op.get_video_by_user(user.username)
    videoinfo = []
    for v in allvideo:
        name, ext = os.path.splitext(v.videoname)
        size = os.path.getsize(os.path.join(folder, v.videoname)) / 1024
        videoinfo.append((v.cid, name, size, ext, user.area))
    #videoinfo = enumerate(videoinfo)
    session['advideo'] = videoinfo
    return render_template('ad_vedio.html', videoinfo=videoinfo, usersname=user.name)

@app.route("/ad/video/del/<idx>")
def del_video(idx):
    if 'user' not in session:
        return redirect('/login')
    idx = int(idx)
    op = userdb.DbOperation()
    user = op.get(session['user'])
    folder = os.path.join(USER_FOLDER, user.username, 'advds')
    todel = op.get_video_by_rowid(idx)
    fp = os.path.join(folder, todel.videoname)
    if os.path.isfile(fp):
        os.remove(fp)
        op.del_video_by_rowid(idx)
    else:
        pass
        #print fp, 'not existing'
    #allvideo = os.listdir(folder)
    allvideo = op.get_video_by_user(user.username)
    videoinfo = []
    for v in allvideo:
        name, ext = os.path.splitext(v.videoname)
        size = os.path.getsize(os.path.join(folder, v.videoname)) / 1024
        videoinfo.append((v.cid, name, size, ext, user.area))
    session['advideo'] = videoinfo
    return render_template('ad_vedio.html', videoinfo=videoinfo, usersname=user.name)

@app.route("/infosrv/pics")
def infopic():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    infoitems = op.get_info_items_by_user(user.username)
    infofolder = os.path.join(USER_FOLDER, user.username, 'info')
    items = []
    for info in infoitems:
        items.append((info.picname, os.path.join(infofolder, info.picname).strip('.'),
            os.path.join(infofolder, info.qrname).strip('.'), info.cid))
    return render_template('infosrv.html', usersname=user.name, infoitems=items)

@app.route("/infosrv/pics/add", methods=['POST'])
def info_add_pic():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    filename = request.form['picname']
    picfile = request.files['picfile']
    qr = request.files['qrcode']
    infofolder = os.path.join(USER_FOLDER, user.username, 'info')
    if picfile.filename and qr.filename:
        picpath = os.path.join(infofolder, picfile.filename)
        name, ext = os.path.splitext(picfile.filename)
        qrname = '.'.join(['-'.join([name, 'qrind']), 'png'])
        txtfile = '.'.join([name, 'txt'])
        txtpath = os.path.join(infofolder, txtfile)
        qrpath = os.path.join(infofolder, qrname)
        if not os.path.isfile(picpath):
            picfile.save(picpath)
            if not os.path.isfile(qrpath):
                qr.save(qrpath)
            with open(txtpath, 'wb') as txtfd:
                #print filename
                txtfd.write(filename.encode('utf8'))
            op.add_info_item(filename, picfile.filename, qrname, txtfile, user.username, datetime.now())
            abspath = os.path.abspath(picpath)
            publisher.publish('info&&%s'%(abspath), session['user'])
            publisher.publish('info&&%s'%(qrpath), session['user'])
            publisher.publish('info&&%s'%(txtpath), session['user'])
    return redirect("/infosrv/pics")

@app.route("/infosrv/del/<idx>")
def del_info(idx):
    if 'user' not in session:
        return redirect('/login')
    idx = int(idx)
    op = userdb.DbOperation()
    info = op.get_info_item_by_rowid(idx)
    infofolder = os.path.join(USER_FOLDER, info.user, 'info')
    picpath = os.path.join(infofolder, info.picname)
    qrpath = os.path.join(infofolder, info.qrname)
    if os.path.isfile(picpath):
        os.remove(picpath)
        if os.path.isfile(qrpath):
            os.remove(qrpath)
        op.del_info_item_by_rowid(idx)
    else:
        pass
        #print 'deleting info pic not existing.'

    return redirect('/infosrv/pics')

@app.route("/commsrv")
def commsrv():
    return render_template('commsrv.html')

@app.route("/commsrv/mypics")
def pics():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    pics = op.get_comm_pics_by_user(user.username)
    commpicfolder = os.path.join(USER_FOLDER, user.username, 'commpics')
    allpics = []
    for pic in pics:
        allpics.append((pic.picname,
                        os.path.join(commpicfolder, pic.picname).strip('.'),
                        os.path.join(commpicfolder, pic.textname).strip('.'),
                        pic.cid))
    return render_template('commpics.html', usersname=user.name, infoitems=allpics)

@app.route("/commsrv/mypics/add", methods=['POST'])
def add_comm_pic():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    filename = request.form['picname']
    picfile = request.files['picfile']
    txtfile = request.files['desctext']
    if not filename.strip():
        filename = picfile.filename
    if picfile.filename:
        infofolder = os.path.join(USER_FOLDER, user.username, 'commpics')
        picpath = os.path.join(infofolder, picfile.filename)
        txtpath = os.path.join(infofolder, txtfile.filename)
        abspath = os.path.abspath(picpath)
        abstxtp = os.path.abspath(txtpath)
        if not os.path.isfile(picpath):
            picfile.save(picpath)
            txtfile.save(txtpath)
            op.add_comm_pic(filename, picfile.filename, txtfile.filename, user.username, datetime.now())
            publisher.publish('commpics&&%s'%(abspath,), session['user'])
            publisher.publish('commpics&&%s'%(abstxtp,), session['user'])
    return redirect("/commsrv/mypics")

@app.route("/commsrv/mypics/del/<idx>")
def del_commpic(idx):
    if 'user' not in session:
        return redirect('/login')
    idx = int(idx)
    op = userdb.DbOperation()
    pic = op.get_comm_pic_by_rowid(idx)
    commpicfolder = os.path.join(USER_FOLDER, pic.user, 'commpics')
    picpath = os.path.join(commpicfolder, pic.picname)
    if os.path.isfile(picpath):
        os.remove(picpath)
    else:
        pass
        #print 'deleting commpic not existing.'
    op.del_comm_pic_by_rowid(idx)
    return redirect('/commsrv/mypics')

@app.route("/commsrv/museum")
def museum():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    pics = op.get_museum_pics_by_user(user.username)
    folder = os.path.join(USER_FOLDER, user.username, 'commuseum')
    allpics = []
    for pic in pics:
        allpics.append((pic.picname,
                        os.path.join(folder, pic.picname).strip('.'),
                        os.path.join(folder, pic.textname).strip('.'),
                        pic.cid))
    return render_template('commuseum.html', usersname=user.name, infoitems=allpics)

@app.route("/commsrv/museum/add", methods=["POST"])
def muadd():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    filename = request.form['picname']
    picfile = request.files['picfile']
    txtfile = request.files['desctext']
    if not filename.strip():
        filename = picfile.filename
    if picfile.filename:
        folder = os.path.join(USER_FOLDER, user.username, 'commuseum')
        picpath = os.path.join(folder, picfile.filename)
        txtpath = os.path.join(folder, txtfile.filename)
        abspath = os.path.abspath(picpath)
        abstxtp = os.path.abspath(txtpath)
        if not os.path.isfile(picpath):
            picfile.save(picpath)
            txtfile.save(txtpath)
            op.add_museum_pic(filename, picfile.filename, txtfile.filename, user.username, datetime.now())
            publisher.publish('commuseum&&%s'%(abspath,), session['user'])
            publisher.publish('commuseum&&%s'%(abstxtp,), session['user'])
    return redirect("/commsrv/museum")

@app.route("/commsrv/museum/del/<idx>")
def mudel(idx):
    if 'user' not in session:
        return redirect('/login')
    idx = int(idx)
    op = userdb.DbOperation()
    pic = op.get_museum_pic_by_rowid(idx)
    folder = os.path.join(USER_FOLDER, pic.user, 'commuseum')
    picpath = os.path.join(folder, pic.picname)
    if os.path.isfile(picpath):
        os.remove(picpath)
    else:
        pass
        #print 'deleting commpic not existing.'
    op.del_museum_pic_by_rowid(idx)
    return redirect('/commsrv/museum')

@app.route("/commsrv/dancing")
def dancing():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    folder = os.path.join(USER_FOLDER, user.username, 'dance')
    allvideo = op.get_dancing_video_by_user(user.username)
    videoinfo = []
    for v in allvideo:
        name, ext = os.path.splitext(v.videoname)
        size = os.path.getsize(os.path.join(folder, v.videoname)) / 1024
        videoinfo.append((v.cid, name, size, ext, user.area))
    #videoinfo = enumerate(videoinfo)
    session['advideo'] = videoinfo
    return render_template('dancing.html', videoinfo=videoinfo, usersname=user.name)

@app.route("/dancing/video", methods=['POST'])
def dancing_add():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    folder = 'dance' #'commsqr'
    if request.method == 'POST':
        filename = request.form['filename']
        videofile = request.files['file']
        if videofile.filename:
            videopath = os.path.join(USER_FOLDER, user.username, folder, videofile.filename)
            abspath = os.path.abspath(videopath)
            if not os.path.isfile(videopath):
                videofile.save(videopath)
                op.add_dancing_video(filename, videofile.filename, user.username, datetime.now())
                publisher.publish('%s&&%s'%('commsqr', abspath,), session['user'])
                #print filename
    return redirect('/commsrv/dancing')
    '''
    folder = os.path.join(USER_FOLDER, user.username, 'commsqr')
    allvideo = op.get_dancing_video_by_user(user.username)
    videoinfo = []
    for v in allvideo:
        name, ext = os.path.splitext(v.videoname)
        size = os.path.getsize(os.path.join(folder, v.videoname)) / 1024
        videoinfo.append((v.cid, name, size, ext, user.area))
    session['advideo'] = videoinfo
    return render_template('dancing.html', videoinfo=videoinfo, usersname=user.name)
    '''

@app.route("/dancing/video/del/<idx>")
def del_dancing(idx):
    if 'user' not in session:
        return redirect('/login')
    idx = int(idx)
    op = userdb.DbOperation()
    user = op.get(session['user'])
    folder = os.path.join(USER_FOLDER, user.username, 'dance')
    todel = op.get_dancing_video_by_rowid(idx)
    fp = os.path.join(folder, todel.videoname)
    if os.path.isfile(fp):
        os.remove(fp)
        op.del_dancing_video_by_rowid(idx)
    else:
        pass
        #print fp, 'not existing'
    return redirect('/commsrv/dancing')
    '''
    allvideo = op.get_dancing_video_by_user(user.username)
    videoinfo = []
    for v in allvideo:
        name, ext = os.path.splitext(v.videoname)
        size = os.path.getsize(os.path.join(folder, v.videoname)) / 1024
        videoinfo.append((v.cid, name, size, ext, user.area))
    session['advideo'] = videoinfo
    return render_template('dancing.html', videoinfo=videoinfo, usersname=user.name)
    '''

@app.route("/opengov/breaking")
def govern():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    pics = op.get_breaking_pics_by_user(user.username)
    folder = os.path.join(USER_FOLDER, user.username, 'breaking')
    allpics = []
    for pic in pics:
        allpics.append((pic.picname,
                        os.path.join(folder, pic.picname).strip('.'),
                        os.path.join(folder, pic.textname).strip('.'),
                        pic.cid))
    return render_template('breaking.html', usersname=user.name, infoitems=allpics)

@app.route("/opengov/breaking/add", methods=["POST"])
def addgov():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    filename = request.form['picname']
    picfile = request.files['picfile']
    txtfile = request.files['desctext']
    folder = 'breaking'
    if not filename.strip():
        filename = picfile.filename
    if picfile.filename:
        rfolder = os.path.join(USER_FOLDER, user.username, folder)
        picpath = os.path.join(rfolder, picfile.filename)
        txtpath = os.path.join(rfolder, txtfile.filename)
        abspath = os.path.abspath(picpath)
        txtabspath = os.path.abspath(txtpath)
        if not os.path.isfile(picpath):
            picfile.save(picpath)
            txtfile.save(txtpath)
            op.add_breaking_pic(filename, picfile.filename, txtfile.filename, user.username, datetime.now())
            publisher.publish('%s&&%s'%(folder, abspath,), session['user'])
            publisher.publish('%s&&%s'%(folder, txtabspath,), session['user'])
    return redirect("/opengov/breaking")

@app.route("/opengov/breaking/del/<idx>")
def delgov(idx):
    if 'user' not in session:
        return redirect('/login')
    idx = int(idx)
    op = userdb.DbOperation()
    pic = op.get_breaking_pic_by_rowid(idx)
    folder = os.path.join(USER_FOLDER, pic.user, 'breaking')
    picpath = os.path.join(folder, pic.picname)
    rootp, _ = os.path.splitext(picpath)
    txtpath = rootp + '.txt'
    if os.path.isfile(picpath):
        os.remove(picpath)
        if os.path.isfile(txtpath):
            os.remove(txtpath)
    else:
        pass
        #print 'deleting breaking not existing.'
    op.del_breaking_pic_by_rowid(idx)
    return redirect('/opengov/breaking')

@app.route("/opengov/convinient")
def conv():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    pics = op.get_convinient_pics_by_user(user.username)
    folder = os.path.join(USER_FOLDER, user.username, 'convinient')
    allpics = []
    for pic in pics:
        allpics.append((pic.picname,
                        os.path.join(folder, pic.picname).strip('.'),
                        os.path.join(folder, pic.textname).strip('.'),
                        pic.cid))
    return render_template('convinient.html', usersname=user.name, infoitems=allpics)

@app.route("/opengov/convinient/add", methods=["POST"])
def addconv():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    user = op.get(session['user'])
    filename = request.form['picname']
    picfile = request.files['picfile']
    txtfile = request.files['desctext']
    folder = 'convinient'
    if not filename.strip():
        filename = picfile.filename
    if picfile.filename:
        rfolder = os.path.join(USER_FOLDER, user.username, folder)
        picpath = os.path.join(rfolder, picfile.filename)
        txtpath = os.path.join(rfolder, txtfile.filename)
        abspath = os.path.abspath(picpath)
        txtabspath = os.path.abspath(txtpath)
        if not os.path.isfile(picpath):
            picfile.save(picpath)
            txtfile.save(txtpath)
            op.add_convinient_pic(filename, picfile.filename, txtfile.filename, user.username, datetime.now())
            publisher.publish('%s&&%s'%(folder, abspath,), session['user'])
            publisher.publish('%s&&%s'%(folder, txtabspath,), session['user'])
    return redirect("/opengov/convinient")

@app.route("/opengov/convinient/del/<idx>")
def delconv(idx):
    if 'user' not in session:
        return redirect('/login')
    idx = int(idx)
    op = userdb.DbOperation()
    pic = op.get_convinient_pic_by_rowid(idx)
    folder = os.path.join(USER_FOLDER, pic.user, 'convinient')
    picpath = os.path.join(folder, pic.picname)
    rootp, _ = os.path.splitext(picpath)
    txtpath = rootp + '.txt'
    if os.path.isfile(picpath):
        os.remove(picpath)
        if os.path.isfile(txtpath):
            os.remove(txtpath)
    else:
        pass
        #print 'deleting convinient not existing.'
    op.del_convinient_pic_by_rowid(idx)
    return redirect('/opengov/convinient')

@app.route("/usrmng/users")
def users():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    users = op.get_bin_users_by_admin('super')
    return render_template('usermng.html', users=users, towns=op.get_towns())

@app.route("/usrmng/user/add", methods=['POST'])
def adduser():
    if 'user' not in session:
        return redirect('/login')
    name = request.form['name']
    phone = request.form['phone']
    cardno = request.form['cardno']
    town = request.form['townname']
    if town:
        town = town.split(';')[-1].strip() # only store town code
    coun = request.form['countryname']
    if coun:
        coun = coun.split(';')[1].strip() # only store country code
    devno = request.form['devno']
    if devno:
        devno = devno.split(';')[1].strip()
    seqno = int(request.form['seqno'])
    #print town, coun, devno, seqno
    if not town or not coun or not devno:
        return '<h2>必须输入乡镇，行政村和位点信息!</h2>'
    op = userdb.DbOperation()
    if not op.update_bin_user_basic_info(town, coun, devno, seqno, name, phone, cardno):
        #print 'user not found:', name
        op.add_bin_user(cardno, town, coun, devno, seqno,
                        'super', name, phone) # hack with super user
    else:
        print 'user existing: ', name
    return redirect('/usrmng/users')

@app.route("/usrmng/del/<cid>", methods=["GET"])
def del_bin_user(cid):
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    #op.del_bin_user_by_cardno(cardno)
    op.del_bin_user_by_id(cid)
    return redirect('/usrmng/users')

@app.route("/usrmng/edit", methods=["GET"])
def usredit():
    name = request.args.get('name')
    cid = request.args.get('cid')
    phone = request.args.get('phone')
    cardno = request.args.get('cardno')
    #print name, cid, phone, cardno
    op = userdb.DbOperation()
    ret = op.update_bin_user_by_id(cid, name, phone, cardno)
    if ret:
        return 'ok'
    else:
        return 'nok'

@app.route("/bin/use/report/<cardno>")
def bin_report(cardno):
    #print 'use report ', cardno
    op = userdb.DbOperation()
    op.update_bin_user_count(cardno)
    return 'ok'

@app.route("/user-query", methods=["POST"])
def query():
    cardno = request.form['cardno']
    #print cardno
    op = userdb.DbOperation()
    usr = op.get_bin_user_by_cardno(cardno)
    rank = op.get_bin_user_rank(cardno)
    result = {'name': usr.name, 'mobile': usr.phone, 'rank': rank, 'count': usr.count}
    js = json.dumps(result)
    #print js
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5000'
    return resp

@app.route("/user-query/<card>")
def user_query(card):
    #print card
    return {'rank': 1, 'mobile': '88888888888', 'name': 'haitong'}

@app.route("/distribution")
def dist():
    if 'user' not in session:
        return redirect('/login')
    return render_template('distrib.html', terminals=[])

@app.route("/terminals")
def terms():
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    terms = op.get_geoinfo()
    #print terms
    return render_template('terminals.html',
        terminals=terms, usersname=session['user'],
        towns=op.get_towns())

@app.route("/terminals/add", methods=['POST'])
def add_term():
    if 'user' not in session:
        return redirect('/login')
    tn = request.form['townname'].strip()
    tc = request.form['towncode'].strip()
    cn = request.form['countryname'].strip()
    cc = request.form['countrycode'].strip()
    dn = request.form['devname'].strip()
    dc = request.form['devcode'].strip()
    ip = request.form['ipaddr'].strip()
    op = userdb.DbOperation()
    op.add_geoinfo(tn, tc, cn, cc, dn, dc, ip)
    return redirect('/terminals')

@app.route("/terminals/del/<cid>")
def del_term(cid):
    if 'user' not in session:
        return redirect('/login')
    op = userdb.DbOperation()
    op.del_geoinfo(int(cid))
    return redirect('/terminals')

@app.route("/q/countries")
def get_counts():
    townid = int(request.args.get('towninfo').split(';')[0])
    op = userdb.DbOperation()
    couns = op.get_countries_by_townid(townid)
    jscouns = []
    for c in couns:
        jscouns.append({'cn': c.counname, 'cc': c.councode, 'ti': c.townid, 'cid': c.cid})
    jsres = json.dumps({'data': jscouns})
    #print jsres
    resp = Response(jsres, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5000'
    return resp

@app.route("/q/terminals")
def get_terms():
    cid = int(request.args.get('countryinfo').split(';')[-1])
    op = userdb.DbOperation()
    terminals = op.get_terminals_by_country_id(cid)
    jsterms = []
    for t in terminals:
        jsterms.append({'tn': t.termname, 'tc': t.termcode, 'ci': t.counid, 'cid': t.cid, 'ip': t.ipaddr})
    jsres = json.dumps({'data': jsterms})
    #print jsres
    resp = Response(jsres, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5000'
    return resp

@app.route("/q/geotree")
def get_geotree():
    data0 = [{"text": "Asia", "id": "asia"},
      {"text": "Africa", "id": "africa"},
      {"text": "Europe", "id": "euro",
       "children": [ {"text": "France", "id": "fr"},
                     {"text": "Germany", "id": "ger", "children": [
                        {"text": "munich", "id": "mu"},
                        {"text": "bolin", "id": "bo"}
                     ]}]}];
    data = userdb.get_geo_tree()
    jsres = json.dumps({'data': data})
    resp = Response(jsres, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5000'
    return resp

@app.route("/set/selected")
def set_selected():
    if 'user' not in session:
        return redirect('/login')
    hosts = request.args.get('selected')
    hosts = [h for h in hosts.split(';') if '-' not in h]
    hosts = ';'.join(hosts)
    ldb = leveldb.LevelDB('./distsdb')
    ldb.Put(session['user'], hosts)
    return 'ok'

if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=True)
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
