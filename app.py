from flask import Flask, jsonify, render_template, request
from bson.json_util import dumps
import random
import certifi
app = Flask(__name__)


from pymongo import MongoClient

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.j7axpsz.mongodb.net/cluster0?retryWrites=true&w=majority')
# client = MongoClient('mongodb+srv://test:sparta@cluster0.zi0ui9l.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta


# 오색조 멤버 구성 db 삽입
# arr = [{'name':"김연수", 'color':"검정"},
#        {'name':"정대신", 'color':"파랑"},
#        {'name':"정호준", 'color':"카키"},
#        {'name':"변다슬", 'color':"노랑"},
#        {'name':"오길환", 'color':"주황"}]

# for i in arr:
#     db.ProjectMembers.insert_one(i)
# doc = {
#         'boss' : "어몽어스",
#         'bossHp' : 500,
#         'count' : 0
#     }
# db.boss.insert_one(doc)


@app.route('/')
def home():
    return render_template('index.html')



@app.route("/main/getcomment", methods = ["GET"])
def main_comment():
    main_list = list(db.main.find({}, {'_id': False}))
    return jsonify({'comments': main_list})

@app.route("/main/postcomment", methods=["POST"])
def team_comment():
    name_receive = request.form['teamname_give']
    comment_receive = request.form['tmc_give']
    count = random.uniform(1, 1000)

    doc = {
        'name' : name_receive,
        'comment': comment_receive,
        'num' : count,
        'done' : 0
    }
    db.main.insert_one(doc)
    return jsonify({'msg': '응원 감사합니다'})
# ////////////////////////////kakhi///////////////////////
@app.route('/kakhi')
def kakhi():
   return render_template('kakhi.html')

@app.route("/kakhi_cmt", methods=["POST"])
def web_kakhi_post():
    nick_receive = request.form['nick_give']
    comment_receive = request.form['comment_give']

    kakhi_list = list(db.kakhi_cmt.find({}, {'id': False}))
    count = len(kakhi_list) + 1;

    doc = {
        'num': count,
        'nick': nick_receive,
        'comment': comment_receive,
        'edit': 0
    }
    db.kakhi_cmt.insert_one(doc)

    return jsonify({'msg': '댓글이 달렸어요!'})

@app.route("/kakhi_cmt", methods=["GET"])
def web_kakhi_get():
    nick_list = list(db.kakhi_cmt.find({}, {'_id': False}))
    return jsonify({'nicks': nick_list})

@app.route("/kakhi_cmt/del", methods=["POST"])
def delete_comment():
    num_receive = request.form['num_give']
    db.kakhi_cmt.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})
@app.route("/kakhi_cmt/clear", methods=["POST"])
def edit_clear():
   num_receive = request.form['num_give']
   edit_receive = request.form['edit_give']

   db.kakhi_cmt.update_one({'num': int(num_receive)}, {'$set':{'edit': 1, 'comment': edit_receive}})
   return jsonify({'msg':' 수정 완료!'})

@app.route("/kakhi_cmt/edit", methods=["POST"])
def edit_comment():
   num_receive = request.form['num_give']

   db.kakhi_cmt.update_one({'num': int(num_receive)}, {'$set':{'edit': 2}})
   return jsonify({'msg':' 수정 하시겠습니까?'})

# ////////////////////////////kakhi///////////////////////


@app.route('/orange')
def orange():
    return render_template('orange.html')

@app.route("/orange/save", methods=["POST"])
def comment_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    pw_receive = request.form['pw_give']

    count = random.uniform(1, 1000)

    doc = {
        'name' : name_receive,
        'comment': comment_receive,
        'pw': pw_receive,
        'num' : count,
    }
    db.orange.insert_one(doc)
    return jsonify({'msg': '응원 감사합니다'})

@app.route("/orange/show", methods=["GET"])
def comment_get():
    comment_list = list(db.orange.find({}, {'_id': False , 'pw' : False}))
    return jsonify({'comments': comment_list})

@app.route("/orange/delete", methods=["POST"])
def comment_delete():
    deletepw_receive = request.form['deletepw_give']
    num_receive = request.form['num_give']
    doc = {
        'num': float(num_receive),
        'pw': deletepw_receive
    }

    gang = db.orange.find_one(doc)
    if(gang == None):
        return jsonify({'msg' : '비밀번호가 일치하지 않습니다'})
    else :
        db.orange.delete_one(gang)
        return jsonify({'msg': '삭제완료'})

@app.route("/correction", methods=["POST"])
def correction():
    correction_receive = request.form['correction_give']
    crtp_receive = request.form['crtp_give']
    crtn_receive = request.form['crtn_give']
    doc = {
        'num': float(crtn_receive),
        'pw': crtp_receive,
    }

    crtq = db.orange.find_one(doc)
    if (crtq == None):
        return jsonify({'msg': '비밀번호가 일치하지 않습니다'})
    else:
        db.orange.update_one({'num': float(crtn_receive)},{'$set':{'comment':correction_receive}})
        return jsonify({'msg': '수정 완료'})

# ////////////////////////////yellow///////////////////////
@app.route('/searchMember', methods=["GET"])
def serchMember():
    member_name = request.args.get("name_give")
    membersData = db.ProjectMembers.find_one({'name': member_name},{'_id': False})
    print(membersData)

    if membersData is None:
        return jsonify({'msg': 'undefined'})
    else:
        return jsonify({'members_Data' : membersData})


@app.route('/yellow')
def getYellow():
    return render_template('yellow.html')


@app.route("/yellow/homework/click", methods=["POST"])
def remove_comment():
    num_receive = request.form['num_give']
    db.YellowVbook.update_one({'num': int(num_receive)},{'$set':{'click':1}})

    return jsonify({'msg': '삭제 완료!'})

@app.route("/yellow/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    visitorbook_list = list(db.YellowVbook.find({}, {'id':False}))
    count = len(visitorbook_list) + 1

    doc = {
        'num':count,
        'name':name_receive,
        'comment':comment_receive,
        'click':0
    }
    db.YellowVbook.insert_one(doc)

    return jsonify({'msg':'기록 완료!'})

@app.route("/yellow/homework", methods=["GET"])
def homework_get():
    visitor_list = list(db.YellowVbook.find({}, {'_id': False}))
    return jsonify({'visitorbooks':visitor_list})
# ////////////////////////////yellow///////////////////////

# ////////////////////////////black///////////////////////
@app.route('/black')
def black():
    return render_template('black.html')

@app.route("/color5", methods=["POST"])
def web_color5_post():
    comment_list = list(db.color5.find({}, {'_id': False}))
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    count = len(comment_list) + 1

    doc = {
        'num': count,
        'name': name_receive,
        'comment': comment_receive,
    }
    db.color5.insert_one(doc)

    return jsonify({'msg': '게시글이 등록되었어요'})


@app.route("/color5", methods=["GET"])
def web_color5_get():
    order_list = list(db.color5.find({}, {'_id': False}))

    return jsonify({'orders': order_list})


@app.route("/color5/delete", methods=["POST"])
def web_color5_delete():
    num_receive = request.form['num_give']
    db.color5.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제가 완료되었어요'})


@app.route("/color5/update", methods=["POST"])
def color5_update():
    name_receive = request.form['name_give']
    num_receive = request.form['num_give']
    comment_receive = request.form['comment_give']
    db.color5.update_one({'num': int(num_receive)}, {'$set': {'name': name_receive}})
    db.color5.update_one({'num': int(num_receive)}, {'$set': {'comment': comment_receive}})
    return jsonify({'msg': '수정 완료!'})
# ////////////////////////////black///////////////////////
# /////////////////////////blue/////////////////////
@app.route('/blue')
def blue():
    return render_template('blue.html')

@app.route("/parc/del", methods=["POST"])
def web_parc_del():
    num_receive = request.form["num_give"]
    db.parc.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/parc", methods=["GET"])
def web_parc_get():
    comment_list = list(db.parc.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

@app.route("/parc", methods=["POST"])
def web_parc_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    comment_list = list(db.parc.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'num': count,
        'name': name_receive,
        'comment': comment_receive,
        'edit' : 0
    }
    db.parc.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

# //////////////////////수정하기//////////////////////////////////////////////////////
@app.route('/parc/edit', methods=["POST"])
def web_parc_edit():
    num_receive = request.form['num_give']
    db.parc.update_one({'num': int(num_receive)},{'$set': {'edit': 2}})
    return jsonify({'msg': '수정 하시겠습니까?'})

# ////////////////////////////수정 완료///////////////////////////////////////////////////////
@app.route('/parc/edit_done', methods=["POST"])
def web_parc_edit_done():
    num_receive = request.form['num_give']
    edit_comment_receive = request.form['edit_comment_receive_give']
    db.parc.update_one({'num':int(num_receive)},{'$set': {'edit': 1, 'comment': edit_comment_receive}})
    return jsonify({'msg': '수정 완료!!'})

# /////////////////////////삭제하기//////////////////////////////////////////////////////////
# /////////////////////////blue//////////////////////
@app.route('/boss/dmg', methods=["POST"])
def bossdmg():
    dmg_receive = request.form['dmg_give']
    print(dmg_receive)
    bossdmg = db.boss.find_one({'boss': '어몽어스' }, {'_id': False})
    print(bossdmg)
    result = bossdmg['bossHp'] - float(dmg_receive)
    print(result)
    db.boss.update_one({'boss' : '어몽어스'},{'$set': {'bossHp': result}})
    hp = db.boss.find_one({'boss': '어몽어스' }, {'_id': False})
    status = hp['bossHp']
    print(status)
    if status < 0:
        db.boss.update_one({'boss': '어몽어스'}, {'$set': {'bossHp': 100}})
        bosskillcount = db.boss.find_one({'boss': '어몽어스'}, {'_id': False})
        print(bosskillcount)
        bosskill = bosskillcount['count']
        bosskilllog = bosskillcount['count'] + int(1)
        db.boss.update_one({'boss': '어몽어스'}, {'$set': {'count': bosskilllog}})
        return jsonify({'bosskill' : bosskill})
    else:
        return jsonify({'boss_hp':hp})

@app.route('/boss/kill', methods=["POST"])
def bosskill():
    name_receive = request.form['name_give']
    killnum_receive = request.form['killnum_give']
    killhtml_receive = request.form['killhtml_give']

    doc = {
        'name' : name_receive,
        'killcount' : killnum_receive,
        'killhtml' : killhtml_receive
    }

    db.bossKillLog.insert_one(doc)
    return jsonify({'msg': '명예의 전당 등록 완료!'})

@app.route('/boss/killlog', methods=["GET"])
def bosskilllog():
    kill_list = list(db.bossKillLog.find({},{'_id': False}))
    print(kill_list)
    return jsonify({'kill_list': kill_list})

@app.route('/boss/heal', methods=["POST"])
def bosshp():
    heal_receive = request.args.get['heal_give']
    bossheal = db.boss.find_one({'boss': '어몽어스' }, {'_id': False})
    result = bossheal['bossHp'] + float(heal_receive)
    db.boss.update_one({'boss' : '어몽어스'},{'$set': {'bossHp': result}})
    hp = db.boss.find_one({'boss': '어몽어스' }, {'_id': False})
    return jsonify({'boss_hp':hp})

@app.route('/boss/hp', methods=["GET"])
def bossstatus():

    bossdmg = db.boss.find_one({'boss': '어몽어스' }, {'_id': False})
    result = bossdmg['bossHp']
    return jsonify({'hp':result})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
