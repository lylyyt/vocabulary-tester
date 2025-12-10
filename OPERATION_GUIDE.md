# 英语词汇测试系统 - 操作说明

本指南将帮助您在下载文件后通过终端命令打开英语词汇测试系统。

## 前提条件

在开始之前，请确保您的计算机已安装以下软件：

- **Python 3.7 或更高版本**
  - 您可以从 [Python官方网站](https://www.python.org/downloads/) 下载并安装
  - 安装时请勾选 "Add Python to PATH" 选项

## 步骤 1.5：安装依赖（可选但推荐）

项目可能依赖一些Python库，您可以通过以下命令安装：

```bash
# 进入项目目录后执行
pip install -r requirements.txt
```

如果您的系统同时安装了 Python 2 和 Python 3，请尝试：

```bash
pip3 install -r requirements.txt
```

## 步骤 1：下载项目文件

### 方式一：使用 Git 克隆（推荐）

在终端中执行以下命令克隆项目：

```bash
git clone https://github.com/your-username/english-vocabulary-tester.git
```

### 方式二：直接下载 ZIP 文件

1. 访问项目的 GitHub 页面
2. 点击绿色的 "Code" 按钮
3. 选择 "Download ZIP"
4. 将下载的 ZIP 文件解压到您选择的目录

## 步骤 2：打开终端

根据您的操作系统，打开相应的终端：

- **Windows**：
  - 按下 `Win + R` 键
  - 输入 `cmd` 或 `powershell` 并按下回车

- **macOS**：
  - 打开 "Launchpad" -> "其他" -> "终端"

- **Linux**：
  - 使用快捷键 `Ctrl + Alt + T` 打开终端

## 步骤 3：导航到项目目录

### Windows 系统

如果您的项目文件在 D 盘（或其他非系统盘），请按照以下步骤操作：

1. **切换到 D 盘**：
   ```bash
   D:
   ```

2. **进入项目目录**（请根据您的实际路径调整）：
   ```bash
   cd "d:\2025 Python\python class work\lecture work\english-vocabulary-tester"
   ```

### macOS / Linux 系统

```bash
cd /path/to/english-vocabulary-tester
```

**注意**：请将 `/path/to/` 替换为您实际的项目路径。

## 步骤 4：运行程序

### 方式一：直接运行（简单）

在项目目录中执行以下命令启动英语词汇测试系统：

```bash
python gui.py
```

如果您的系统同时安装了 Python 2 和 Python 3，请尝试：

```bash
python3 gui.py
```

### 方式二：使用虚拟环境（推荐）

项目包含一个虚拟环境目录 `.venv`，您可以使用它来避免依赖冲突：

#### Windows 系统

```bash
# 激活虚拟环境
.venv\Scripts\activate.bat

# 运行程序
python gui.py

# 退出虚拟环境（完成后）
deactivate
```

在 PowerShell 中：

```powershell
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 运行程序
python gui.py

# 退出虚拟环境（完成后）
deactivate
```

#### macOS / Linux 系统

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行程序
python gui.py

# 退出虚拟环境（完成后）
deactivate
```

## 常见问题及解决方案

### 问题 1：找不到文件或路径错误

**错误信息**：
```
python: can't open file 'gui.py': [Errno 2] No such file or directory
```

**解决方案**：
- 请确保您已正确导航到项目目录
- 检查 `gui.py` 文件是否存在于当前目录中
- 使用 `dir`（Windows）或 `ls`（macOS/Linux）命令查看当前目录下的文件

### 问题 2：Python 不是内部或外部命令

**错误信息**：
```
'python' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

**解决方案**：
- 重新安装 Python，并确保勾选了 "Add Python to PATH" 选项
- 或手动将 Python 安装路径添加到系统环境变量

### 问题 3：在 Windows PowerShell 中使用 && 分隔符报错

**错误信息**：
```
标记 "&&" 不是此版本中的有效语句分隔符。
```

**解决方案**：
- 使用分号 `;` 代替 `&&`：
  ```powershell
  D:; cd "d:\path\to\project"; python gui.py
  ```
- 或在命令提示符（cmd）中使用 `&&`

## 使用提示

1. 程序启动后，系统会自动加载初中词汇数据
2. 您可以在界面上选择不同的词汇模块和测试模式
3. 测试完成后，系统会生成统计报告和错题本

## 联系方式

如果您在使用过程中遇到其他问题，请在 GitHub 项目页面提交 Issues 或联系项目维护者。

---

希望本指南能帮助您顺利使用英语词汇测试系统！