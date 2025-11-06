# 超高难度五子棋 (Kivy版 - 适配在线打包)

这是一个使用Kivy框架构建的超高难度五子棋游戏，已适配在线APK打包服务。

## 如何在线打包APK

您可以使用支持Kivy项目的在线构建服务（例如，官方的Kivy Build Service或GitHub与Buildozer的集成）来生成APK。以下是通用步骤：

1. **准备项目**:
   - 将本项目的所有文件（`main.py`, `game.py`, `ai.py`, `buildozer.spec`, `requirements.txt`）上传到您的GitHub仓库。

2. **使用在线打包服务**:
   - 访问您选择的在线打包服务网站。
   - 授权服务访问您的GitHub仓库。
   - 选择包含您五子棋项目的仓库。
   - 启动构建过程。

3. **下载APK**:
   - 构建完成后，服务会提供一个下载链接，您可以直接下载APK文件到您的电脑或手机。

## 项目文件说明

- `main.py`: Kivy应用主文件，负责UI和交互。
- `game.py`: 游戏核心逻辑，包括棋盘状态、胜负判断等。
- `ai.py`: 游戏AI，实现了基于Alpha-Beta剪枝的极大极小值算法。
- `buildozer.spec`: Buildozer打包配置文件，已为您预先配置好。
- `requirements.txt`: 项目依赖，在线服务会自动安装这些库。

## 游戏特点

- **超高难度AI**: 挑战强大的AI对手。
- **移动端优化**: 界面已为手机触摸操作优化。
- **跨平台**: 基于Kivy，理论上也可在iOS、Windows、macOS上运行。

## 注意事项

- 确保您的GitHub仓库是公开的，或在线服务有权访问私有仓库。
- `buildozer.spec`中的`source.dir = .`表示源文件在根目录，请确保文件结构正确。
- 在线打包服务可能会有队列，请耐心等待构建完成。
