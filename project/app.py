from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import datetime
import os

app = Flask(__name__)

PRO_DIR = 'project'
CACHE_DIR = os.path.join('static','cache')
PRO_CACHE_DIR = os.path.join(PRO_DIR,'static','cache')
os.makedirs(CACHE_DIR, exist_ok=True)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CODE_DIR = os.path.join(PRO_DIR,'code')

latest_pdf_path = None  # 用于缓存最近一次生成的PDF文件路径

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_code_files', methods=['GET'])
def list_code_files():
    # print(CODE_DIR)
    files = [f for f in os.listdir(CODE_DIR) if f.endswith('.py')]
    return jsonify(files)

@app.route('/get_code/<filename>', methods=['GET'])
def get_code(filename):
    # print(filename)
    filename=filename.replace('@', '\\')
    file_path = os.path.join(CODE_DIR, filename)
    # print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        return jsonify({'status': 'success', 'code': code})
    else:
        return jsonify({'status': 'error', 'code': ''}), 404

@app.route('/plot', methods=['POST'])
def plot():
    global latest_pdf_path  # 使用全局变量保存PDF路径
    data = request.json['data']
    code = request.json['code']

    df = pd.DataFrame(data).dropna(how='all').dropna(axis=1, how='all')

    local_env = {'data': df, 'pd': pd, 'plt': plt}
    plt.figure(figsize=(8, 6))
    try:
        exec(code, {}, local_env)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        img_filename = f'plot_{timestamp}.png'
        pdf_filename = f'plot_{timestamp}.pdf'

        img_path = os.path.join(CACHE_DIR, img_filename)
        latest_pdf_path = os.path.join(CACHE_DIR, pdf_filename)  # 保存最新路径

        plt.savefig(os.path.join(PRO_DIR, img_path), format='png')
        plt.savefig(os.path.join(PRO_DIR, latest_pdf_path), format='pdf')

        plt.close()

        return jsonify({
            'status': 'success',
            'image_url': os.path.join('static','cache',img_filename)
        })

    except Exception as e:
        plt.close()
        return jsonify({'status':'error', 'error':str(e)})

@app.route('/download_latest_pdf', methods=['GET'])
def download_latest_pdf():
    user_filename = request.args.get('user_filename', 'plot_result.pdf')
    if not user_filename.lower().endswith('.pdf'):
        user_filename += '.pdf'

    global latest_pdf_path
    pro_latest_pdf_path=os.path.join(PRO_DIR, latest_pdf_path)
    # print("尝试下载文件路径：", latest_pdf_path)
    # print("文件是否存在？", os.path.exists(pro_latest_pdf_path))
    if latest_pdf_path and os.path.exists(pro_latest_pdf_path):
        return send_file(latest_pdf_path, as_attachment=True, download_name=user_filename)
    else:
        return "No file generated yet.", 404

@app.route('/code_tree', methods=['GET'])
def code_tree():
    def walk_dir(path):
        entries = []
        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            # print(full_path)
            if os.path.isdir(full_path):
                entries.append({
                    'type': 'folder',
                    'name': item,
                    'children': walk_dir(full_path)
                })
            elif item.endswith('.py'):
                entries.append({
                    'type': 'file',
                    'name': item,
                    'path': os.path.relpath(full_path, CODE_DIR).replace('\\', '@')
                })
        # print(entries)
        return entries

    tree = walk_dir(CODE_DIR)
    return jsonify(tree)

if __name__ == '__main__':
    app.run(debug=True)
