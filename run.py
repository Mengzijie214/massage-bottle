# 启动文件

from app import  create_app

app = create_app()

# 开发模式
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# 生产模式
# waitress-serve --call 'app:create_app'