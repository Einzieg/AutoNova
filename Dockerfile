# 使用 sickcodes/docker-osx 镜像
FROM sickcodes/docker-osx:latest

# 安装必要的软件包
RUN brew install python3 --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pyinstaller --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pyautogui --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install opencv-python --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pygetwindow --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY . /app
WORKDIR /app

# 打包项目
CMD ["pyinstaller", "main.spec"]
