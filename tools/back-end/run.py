from flask import Flask, request, render_template
#from access_v1 import chatie # 非官方接口
from access import chatie # 官方接口
import json
 
app = Flask(__name__, template_folder='../front-end', static_folder='../front-end')
 
#api接口前缀
apiPrefix = '/api/v1/'
 
##################  Staff接口  ##################
 
@app.route(apiPrefix + 'updateStaff', methods=['POST'])
def updateStaff():
    data = request.get_data(as_text=True)
    #print(data)
    #print(type(data))
    data =json.loads(data)
    data = json.loads(data)
    print("后端传入数据：",data)
    post_data = chatie(data)
    return json.dumps(post_data)
 
if __name__=="__main__":
    app.run(debug=True, port=3000, threaded=True) 
    # processes多进程占用资源多，所有子进程的东西都是各一份；threaded多线程，共享全局变量。
    # threaded默认true 1.1版本以后