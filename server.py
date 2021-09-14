from flask import Flask
from flask import render_template
from flask import jsonify
import utils
from jieba.analyse import  extract_tags
import string
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route("/time")
def get_time():
    return utils.get_time()

@app.route('/tem')
def hello_world3():
    return render_template("index.html")

#html 中定义了ajax用户提交数据，并跳转到某个页面（/time），
# 之后server跳转过去调用该页面返回数据（time），用户还可以调用（time）来改变html的内容
@app.route('/ajax', methods=["get", "post"])
def hello_world4():
    return '10000'
@app.route("/c1", methods=["get", "post"])
def get_c1_data():
    data = utils.get_c1_data()
    c1_data = {"confirm": int(str(data[0])), "suspect": int(str(data[1])), "heal": int(str(data[2])), "dead": int(str(data[3]))}
    return jsonify(c1_data)
@app.route("/c2", methods=["get", "post"])
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        # print(tup)
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})

@app.route("/l1")
def get_l1_data():
    data = utils.get_l1_data()
    day,confirm,suspect,heal,dead = [],[],[],[],[]
    for a,b,c,d,e in data[7:]:
        day.append(a.strftime("%m-%d")) #a是datatime类型
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day":day,"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})

@app.route("/l2")
def get_l2_data():
    data = utils.get_l2_data()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))  # a是datatime类型
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})
@app.route("/r1")
def get_r1_data():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k,v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


@app.route("/r2")
def get_r2_data():
    data = utils.get_r2_data() #格式 (('民警抗疫一线奋战16天牺牲1037364',), ('四川再派两批医疗队1537382',)
    d = []
    jj=1
    hot_val=100000
    for i in data:
        k = i[0].rstrip(string.digits)  # 移除热搜数字
        # v = i[0][len(k):]  # 获取热搜数字
        v=hot_val//jj
        jj+=1
        ks = extract_tags(k)  # 使用jieba 提取关键字
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})
if __name__ == '__main__':
    app.run()