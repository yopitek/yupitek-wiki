---
title：“Hak5 USB Rubber Ducky v2 原厂技术说明书与全功能操作手册”
model：“USB Rubber Ducky v2”
manufacturer：“Hak5”
category：“按键注入攻击工具”
docs_url：“https://docs.hak5.org/usb-rubber-ducky/”
version：“2.0”
locale：“zh-cn”
---

# Hak5 USB Rubber Ducky v2 原厂技术说明书与全功能操作手册

> USB Rubber Ducky v2 是享誉全球的原创击键注入（Keystroke Injection）渗透测试工具。伪装为标准 USB U 盘，具备高达每分钟 1,000 字以上的高速注入能力，搭载强大的 DuckyScript 3.0 编程语言，支持变量、条件分支、循环、函数、动态外发与 Jitter 防御规避。

---

## 目录

- [**1. 产品概述与快速入门指南**](#1-产品概述与快速入门指南)
  - [1.1 USB Rubber Ducky 原厂介绍](#1-1-usb-rubber-ducky-原厂介绍)
  - [1.2 开箱快速上手指南 (Quack-Start Guide)](#1-2-开箱快速上手指南-quack-start-guide)
  - [1.3 DuckyScript™ 语法速查表](#1-3-duckyscript-语法速查表)
- [**2. DuckyScript 基础语法与硬件控制**](#2-duckyscript-基础语法与硬件控制)
  - [2.1 第一支载荷：Hello，World!](#2-1-第一支载荷-hello-world)
  - [2.2 按键注入核心机制 (Keystroke Injection)](#2-2-按键注入核心机制-keystroke-injection)
  - [2.3 代码注释 (REM 指令)](#2-3-代码注释-rem-指令)
  - [2.4 延迟等待控制 (DELAY 指令)](#2-4-延迟等待控制-delay-指令)
  - [2.5 实体按钮交互控制 (The Button)](#2-5-实体按钮交互控制-the-button)
  - [2.6 RGB LED 状态指示灯控制 (The LED)](#2-6-rgb-led-状态指示灯控制-the-led)
- [**3. 逻辑控制、变量、条件判断与函数**](#3-逻辑控制变量条件判断与函数)
  - [3.1 ATTACKMODE 攻击模式配置](#3-1-attackmode-攻击模式配置)
  - [3.2 常量定义 (DEFINE 常量)](#3-2-常量定义-define-常量)
  - [3.3 变量声明与内存操作 (VAR 变量)](#3-3-变量声明与内存操作-var-变量)
  - [3.4 算术与逻辑运算符 (Operators)](#3-4-算术与逻辑运算符-operators)
  - [3.5 条件判断控制结构 (IF / ELSE IF / ELSE)](#3-5-条件判断控制结构-if--else-if--else)
  - [3.6 循环控制结构 (WHILE 循环)](#3-6-循环控制结构-while-循环)
  - [3.7 自定义函数定义与调用 (FUNCTION)](#3-7-自定义函数定义与调用-function)
- [**4. 进阶攻击技术与隐蔽外发**](#4-进阶攻击技术与隐蔽外发)
  - [4.1 随机数生成与防御规避 (Randomization)](#4-1-随机数生成与防御规避-randomization)
  - [4.2 按键长按与组合控制 (HOLD / RELEASE)](#4-2-按键长按与组合控制-hold--release)
  - [4.3 载荷流程控制 (RESTART / STOP)](#4-3-载荷流程控制-restart--stop)
  - [4.4 输入抖动规避分析 (Jitter)](#4-4-输入抖动规避分析-jitter)
  - [4.5 载荷隐蔽与混淆防护 (Payload Hiding)](#4-5-载荷隐蔽与混淆防护-payload-hiding)
  - [4.6 存储活动监控 (Storage Activity)](#4-6-存储活动监控-storage-activity)
  - [4.7 锁定键状态读取 (Caps/Num/Scroll Lock Keys)](#4-7-锁定键状态读取-capsnumscroll-lock-keys)
  - [4.8 带外隐蔽外发技术 (Covert Exfiltration)](#4-8-带外隐蔽外发技术-covert-exfiltration)
  - [4.9 扩展插件系统 (Extensions)](#4-9-扩展插件系统-extensions)
  - [4.10 条件编译机制 (Conditional Compilation)](#4-10-条件编译机制-conditional-compilation)
- [**5. 实战技巧、常见疑难排解与维护指引**](#5-实战技巧常见疑难排解与维护指引)
  - [5.1 常见问题排查 (Common Issues)](#5-1-常见问题排查-common-issues)
  - [5.2 最佳实践与实战技巧 (Tips & Best Practices)](#5-2-最佳实践与实战技巧-tips--best-practices)
  - [5.3 固件更新与出厂恢复指南 (Firmware Updates & Recovery)](#5-3-固件更新与出厂恢复指南-firmware-updates--recovery)

---

## 1. 产品概述与快速入门指南

<!-- section：overview -->
### 1.1 USB Rubber Ducky 原厂介绍

USB Rubber Ducky 是享誉全球的专业按键注入（Keystroke Injection）攻击设备。自 2010 年问世以来，已成为网络安全红队渗透测试员、系统审计人员与白帽黑客必备的标准硬件装备。

外观上，USB Rubber Ducky 伪装成普通的 USB U 盘；然而插入目标计算机时，操作系统会将其识别为标准人机接口设备（Human Interface Device，HID 键盘）。由于现代操作系统对键盘设备具备先天信任，USB Rubber Ducky 能直接绕过传统端点防护软件（EDR、杀毒软件）的软件执行拦截限制，以每分钟超过 1,000 字的超高速自动键入预设的脚本。

在最新世代的 USB Rubber Ducky v2 中，硬件架构迎来了重大革新，换装高速 32-bit ARM Cortex-M4 处理器，并引入全新 DuckyScript 3.0 语言规范，正式从单纯的按键重放器进化为具备完整计算能力的硬件攻击平台。

### 硬件技术规格与原厂校准基准表

| 硬件规格细项 | 原厂官方技术规格说明 |
|---|---|
| **SoC / 微控制器 (MCU)** | 32-bit ARM Cortex-M4 微控制器 |
| **内部存储接口** | MicroSD 存储卡插槽（支持 FAT32 文件系统）|
| **按键注入速率** | 极速按键注入（速率超过每分钟 1,000 字 / >1000 WPM）|
| **实体交互触发器** | 集成式机身微动按钮（支持载荷手动暂停、分段执行）|
| **主机连接接口** | 标准 USB Type-A 公头 |
| **状态诊断指示灯** | 多色可编程 RGB LED 状态指示灯 |
| **机身保护外壳** | Hak5 标准半透明 USB U 盘保护外壳 |
| **脚本语言版本** | DuckyScript 3.0（具备条件判断、变量、循环与函数能力）|

---

### 1.2 开箱快速上手指南 (Quack-Start Guide)

要开始使用 USB Rubber Ducky v2，请按照下列标准流程操作：

1. **取出 MicroSD 存储卡**：使用随附的取卡针轻推 MicroSD 卡槽，取出 MicroSD 卡。
2. **放入载荷文件**：使用读卡器将 MicroSD 卡连接至工作站，在存储卡根目录下创建名为 `payload.dd` 的文本文件。
3. **编写测试脚本**：
   ```duckyscript
   REM 基础测试载荷
   DEFAULT_DELAY 100
   DELAY 2000
   GUI r
   DELAY 500
   STRING notepad.exe
   ENTER
   DELAY 1000
   STRING Hello from USB Rubber Ducky v2!
   ENTER
   ```
4. **装回存储卡并插入目标主机**：将 MicroSD 卡插回 USB Rubber Ducky，随后插入目标计算机的 USB 接口。
5. **观察运行**：设备将自动枚举为 HID 键盘，并在指定的延迟后全自动执行击键指令。

---

<!-- section：features -->
### 1.3 DuckyScript™ 语法速查表

DuckyScript 3.0 为专属击键注入领域的宏语言，其核心保留字包含：

| 指令关键字 | 功能说明 | 实 slide 语法示例 |
|---|---|---|
| `REM` | 代码注释，不被编译器执行 | `REM 这是注释说明` |
| `STRING` | 依序模拟敲击指定的 ASCII 字符串 | `STRING whoami /all` |
| `STRINGLN` | 键入字符串并在末尾自动追加换行（Enter）| `STRINGLN powershell` |
| `DELAY` | 暂停指定毫秒数 | `DELAY 1500` |
| `DEFAULT_DELAY` | 设置所有击键指令之间的默认全局间隔 | `DEFAULT_DELAY 50` |
| `GUI` / `WINDOWS` | 触发 Windows / Super / Command 键 | `GUI r` |
| `ENTER` / `MENU` | 敲击 Enter 换行键或右键菜单快捷键 | `ENTER` |
| `ALT` / `CTRL` / `SHIFT` | 标准修饰按键 | `CTRL ALT DEL` |
| `ATTACKMODE` | 设置 USB 枚举模式（HID、STORAGE 或复合模式）| `ATTACKMODE HID` |
| `BUTTON` | 检测实体按钮按下状态 | `WAIT_FOR_BUTTON_PRESS` |
| `LED` | 调整机身 RGB LED 颜色与闪烁模式 | `LED_R` / `LED_OFF` |

---

## 2. DuckyScript 基础语法与硬件控制

<!-- section：configuration -->
### 2.1 第一支载荷：Hello，World!

在 DuckyScript 中，最简单的演示为唤醒系统对话框并键入文字。

```duckyscript
REM === Hello World 演示载荷 ===
DELAY 3000
GUI r
DELAY 500
STRING notepad.exe
ENTER
DELAY 1000
STRING Hello，World!
ENTER
```

> [!TIP]
> 插入目标计算机后，操作系统枚举驱动程序需要时间，建议在载荷最前端加入 `DELAY 2000` 至 `DELAY 3000`，确保主机完全识别 HID 键盘后再开始发送击键。

---

### 2.2 按键注入核心机制 (Keystroke Injection)

USB Rubber Ducky 支持标准 USB HID 键盘规范中的所有键码：
- **功能按键**：`F1` 至 `F12`
- **方向键与编辑键**：`UP`、`DOWN`、`LEFT`、`RIGHT`、`PAGEUP`、`PAGEDOWN`、`HOME`、`END`、`INSERT`、`DELETE`
- **锁定按键**：`CAPSLOCK`、`NUMLOCK`、`SCROLLLOCK`
- **组合热键**：可单行叠加多个修饰按键，如 `CTRL SHIFT ESC`（打开 Windows 任务管理器）。

---

### 2.3 代码注释 (REM 指令)

`REM`（Remark）用于标注作者、版本信息与作战策略说明，所有 `REM` 开头的内容均不会输出至目标主机。

```duckyscript
REM Author：Yupitek Security Team
REM Description：Windows Credential Harvester
REM Target：Windows 11 Enterprise
```

---

### 2.4 延迟等待控制 (DELAY 指令)

延迟是击键注入攻击能否 100% 成功的关键核心：
- `DELAY n`：精确等待 `n` 毫秒（例如 `DELAY 500` 代表等待 0.5 秒）。
- `DEFAULT_DELAY n` 或 `DEFAULTDELAY n`：在每个命令之间自动插入 `n` 毫秒等待，避免目标系统缓冲区溢出或丢字。

---

### 2.5 实体按钮交互控制 (The Button)

USB Rubber Ducky v2 机身上配备实体按钮，可在 DuckyScript 3.0 中实现灵活的交互流程：
- `WAIT_FOR_BUTTON_PRESS`：载荷运行至此会完全暂停，直到操作员实体按下面板按钮才继续运行。
- `BUTTON_DEF`：定义按钮在运行期间被按下时触发的异步中断处理程序。

```duckyscript
REM 等待操作员手动授权攻击
LED_YELLOW
WAIT_FOR_BUTTON_PRESS
LED_GREEN
STRINGLN authorized_attack_sequence.bat
```

---

### 2.6 RGB LED 状态指示灯控制 (The LED)

机身内置 RGB LED 可提供操作员即时的攻击进度反馈，或在隐蔽行动中完全关闭：
- `LED_OFF`：关闭 LED 指示灯（隐蔽作战模式推荐）。
- `LED_R` / `LED_G` / `LED_B`：分别切换为红、绿、蓝色常亮。
- 支持自定义十六进制颜色与呼吸灯模式。

```duckyscript
LED_OFF
REM 攻击运行中保持全黑
STRINGLN powershell -NoP -NonI -W Hidden -Exec Bypass -File a.ps1
REM 攻击完成亮绿灯 1 秒后熄灭
LED_G
DELAY 1000
LED_OFF
```

---

## 3. 逻辑控制、变量、条件判断与函数

### 3.1 ATTACKMODE 攻击模式配置

`ATTACKMODE` 命令用于控制 USB Rubber Ducky 呈现给操作系统的硬件外观身份：
- `ATTACKMODE HID`：仅作为纯键盘设备（最高隐蔽性）。
- `ATTACKMODE STORAGE`：作为 USB 大容量存储设备（访问 MicroSD 内容）。
- `ATTACKMODE HID STORAGE`：复合模式（同时启用键盘与存储设备）。

支持自定义硬件指纹参数（VID / PID / 序列号 / 制造商），以精确伪装为目标企业核准的合法外设硬件：
```duckyscript
ATTACKMODE HID VID_046 D PID_C31 C MAN_Hak5 PROD_DUCKY SERIAL_1337
```

---

### 3.2 常量定义 (DEFINE 常量)

在 DuckyScript 3.0 中，可使用 `DEFINE` 声明常量，增强脚本可读性与可维护性：
```duckyscript
DEFINE #TARGET_USER admin
DEFINE #SLEEP_TIME 1000

DELAY #SLEEP_TIME
STRING #TARGET_USER
ENTER
```

---

### 3.3 变量声明与内存操作 (VAR 变量)

使用 `VAR` 声明全局或局部变量，并可进行动态计数或状态暂存：
```duckyscript
VAR $FOO = 10
VAR $TRIES = 0

$TRIES = ($TRIES + 1)
```

---

### 3.4 算术与逻辑运算符 (Operators)

支持标准算术运算与布尔逻辑运算：
- 算术：`+`、`-`、`*`、`/`、`%`
- 关系比较：`==`、`!=`、`<`、`>`、`<=`、`>=`
- 逻辑：`&&`、`||`、`!`

---

### 3.5 条件判断控制结构 (IF / ELSE IF / ELSE)

借助条件逻辑，单支载荷可自动判断目标环境或按钮状态，执行不同攻击路径：
```duckyscript
VAR $OS_FOUND = 1

IF ($OS_FOUND == 1) THEN
    STRINGLN echo Windows Detected
ELSE
    STRINGLN echo Alternate OS Detected
END_IF
```

---

### 3.6 循环控制结构 (WHILE 循环)

支持 `WHILE` 条件循环，适合用于重试机制或定时轮询：
```duckyscript
VAR $COUNT = 0
WHILE ($COUNT < 5)
    STRINGLN ping -n 1 127.0.0.1
    DELAY 1000
    $COUNT = ($COUNT + 1)
END_WHILE
```

---

### 3.7 自定义函数定义与调用 (FUNCTION)

使用 `FUNCTION` 封装可重复利用的击键序列：
```duckyscript
FUNCTION RUN_COMMAND(cmd)
    GUI r
    DELAY 400
    STRING cmd
    ENTER
    DELAY 800
END_FUNCTION

RUN_COMMAND(“cmd.exe”)
RUN_COMMAND(“powershell.exe”)
```

---

## 4. 进阶攻击技术与隐蔽外发

### 4.1 随机数生成与防御规避 (Randomization)

DuckyScript 3.0 内置伪随机数生成器（`$_RANDOM_INT`），可动态产生随机延迟或随机文件名，大幅打乱 EDR 行为特征分析：
```duckyscript
VAR $RAND_DELAY = ($_RANDOM_INT % 500)
DELAY $RAND_DELAY
```

---

### 4.2 按键长按与组合控制 (HOLD / RELEASE)

可模拟人类操作中的持续长按动作（例如长按 Shift 触发粘滞键或特定系统热键）：
```duckyscript
HOLD SHIFT
STRING abcdef
RELEASE SHIFT
```

---

### 4.3 载荷流程控制 (RESTART / STOP)

- `STOP_PAYLOAD`：立即终止当前载荷执行并使微控制器进入待机休眠。
- `RESTART_PAYLOAD`：重新由第一行开始重新运行载荷。

---

### 4.4 输入抖动规避分析 (Jitter)

现代化端点检测系统会监控键盘输入速率。一般机器输入每键间隔为固定毫秒，极易被行为启发式防护识别为恶意宏。DuckyScript 3.0 的 Jitter 功能可为每个字符敲击自动注入正负随机微小延迟，精准模拟真人打字特征。

---

### 4.5 载荷隐蔽与混淆防护 (Payload Hiding)

在目标系统中执行时，可搭配进阶技巧隐匿痕迹：
- 利用 `GUI r` 呼叫极简临时进程。
- 清除 Windows 运行历史记录（RunMRU）。
- 在 MicroSD 分区中隐藏载荷二进制文件。

---

### 4.6 存储活动监控 (Storage Activity)

当设置为复合模式（`ATTACKMODE HID STORAGE`）时，Ducky 可即时检测目标操作系统是否正在对 MicroSD 进行读写访问，借此精准判定文件外发何时完成。

---

### 4.7 锁定键状态读取 (Caps/Num/Scroll Lock Keys)

USB 键盘协议中，目标主机每次按下 Caps Lock、Num Lock 或 Scroll Lock 时，主机会主动向键盘发送 1 个字节的 HID Output Report 回传灯号状态。

USB Rubber Ducky v2 可即时读取此状态反馈！这意味着即使目标主机网络断开、USB U 盘读写被完全禁用，目标计算机端仍可通过 PowerShell 快速切换 Caps Lock 状态，以二进制方式将数据回传给 USB Rubber Ducky！

---

### 4.8 带外隐蔽外发技术 (Covert Exfiltration)

结合锁定键状态回传或外挂硬件存储，USB Rubber Ducky 实现了业界首创的无网络、纯键盘接口数据外发（Keystroke Exfiltration）。受测主机在未连接互联网且未插 U 盘的情况下，敏感数据即可由 Ducky 内部内存安全截获。

---

### 4.9 扩展插件系统 (Extensions)

DuckyScript 支持引入社区与原厂提供的扩展功能模块，通过 `EXTENSION` 关键字可扩展特化操作系统语义与自动化脚本。

---

### 4.10 条件编译机制 (Conditional Compilation)

支持依据编译目标架构或环境标志进行条件式编译，使单支源代码文件能够同时适配 Windows、macOS 与 Linux 系统。

---

<!-- section：maintenance -->
## 5. 实战技巧、常见疑难排解与维护指引

### 5.1 常见问题排查 (Common Issues)

| 异常症状 | 潜在成因分析 | 建议排查步骤 |
|---|---|---|
| **插入后完全无击键反应** | 目标主机 USB 枚举速度较慢，或缺少初始延迟 | 在载荷开头加入 `DELAY 3000` |
| **打字出现乱码或按键错位** | 目标主机键盘布局（Layout）非英文美规 (US) | 确认目标操作系统输入法已切换为美式键盘 |
| **指示灯闪烁红灯** | MicroSD 卡接触不良或未找到 `payload.dd` | 重新格式化 MicroSD 为 FAT32 并检查文件名大小写 |
| **部分快捷键无法触发** | UAC 权限限制或系统锁定状态 | 先行评估目标账号权限或调整输入流程 |

---

### 5.2 最佳实践与实战技巧 (Tips & Best Practices)

1. **分段测试**：编写复杂 DuckyScript 时，善用 `WAIT_FOR_BUTTON_PRESS` 与 `LED` 进行单步断点调试。
2. **合理延迟**：重要窗口弹出指令后，务必给予至少 500 至 1,000 毫秒的系统加载缓冲。
3. **外壳保护**：携带时避免金属异物碰触裸露的 MicroSD 金手指接触点。

---

### 5.3 固件更新与出厂恢复指南 (Firmware Updates & Recovery)

若需更新 USB Rubber Ducky v2 内部固件或进行出厂恢复：
1. 长按机身实体按钮不放。
2. 将设备插入计算机 USB 接口，持续按住按钮 3 秒后放开。
3. 设备将枚举为名为 `DUCKY` 的维护 U 盘分区。
4. 将 Hak5 官方下载的最新固件二进制文件复制进该分区。
5. 待 LED 指示灯呈现红绿交替闪烁完成后重新插拔即可。
