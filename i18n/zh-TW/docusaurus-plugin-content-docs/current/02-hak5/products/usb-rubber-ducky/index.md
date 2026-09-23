---
title: "Hak5 USB Rubber Ducky v2 原廠技術說明書與全功能操作手冊"
model: "USB Rubber Ducky v2"
manufacturer: "Hak5"
category: "按鍵注入攻擊工具"
docs_url: "https://docs.hak5.org/usb-rubber-ducky/"
version: "2.0"
locale: "zh-tw"
---

# Hak5 USB Rubber Ducky v2 原廠技術說明書與全功能操作手冊

> USB Rubber Ducky v2 是享譽全球的原創擊鍵注入（Keystroke Injection）滲透測試工具。偽裝為標準 USB 隨身碟，具備高達每分鐘 1,000 字以上的高速注入能力，搭載強大的 DuckyScript 3.0 程式語言，支援變數、條件分支、迴圈、函式、動態外傳與 Jitter 防禦規避。

---

## 目錄

- [**1. 產品概述與快速入門指南**](#1-產品概述與快速入門指南)
  - [1.1 USB Rubber Ducky 原廠介紹](#1-1-usb-rubber-ducky-原廠介紹)
  - [1.2 開箱快速上手指南 (Quack-Start Guide)](#1-2-開箱快速上手指南-quack-start-guide)
  - [1.3 DuckyScript™ 語法速查表](#1-3-duckyscript-語法速查表)
- [**2. DuckyScript 基礎語法與硬體控制**](#2-duckyscript-基礎語法與硬體控制)
  - [2.1 第一支酬載：Hello，World!](#2-1-第一支酬載-hello-world)
  - [2.2 按鍵注入核心機制 (Keystroke Injection)](#2-2-按鍵注入核心機制-keystroke-injection)
  - [2.3 程式碼註解 (REM 指令)](#2-3-程式碼註解-rem-指令)
  - [2.4 延遲等待控制 (DELAY 指令)](#2-4-延遲等待控制-delay-指令)
  - [2.5 實體按鈕互動控制 (The Button)](#2-5-實體按鈕互動控制-the-button)
  - [2.6 RGB LED 狀態指示燈控制 (The LED)](#2-6-rgb-led-狀態指示燈控制-the-led)
- [**3. 邏輯控制、變數、條件判斷與函式**](#3-邏輯控制變數條件判斷與函式)
  - [3.1 ATTACKMODE 攻擊模式設定](#3-1-attackmode-攻擊模式設定)
  - [3.2 常數定義 (DEFINE 常數)](#3-2-常數定義-define-常數)
  - [3.3 變數宣告與記憶體操作 (VAR 變數)](#3-3-變數宣告與記憶體操作-var-變數)
  - [3.4 算術與邏輯運算子 (Operators)](#3-4-算術與邏輯運算子-operators)
  - [3.5 條件判斷控制結構 (IF / ELSE IF / ELSE)](#3-5-條件判斷控制結構-if--else-if--else)
  - [3.6 迴圈控制結構 (WHILE 迴圈)](#3-6-迴圈控制結構-while-迴圈)
  - [3.7 自訂函式定義與呼叫 (FUNCTION)](#3-7-自訂函式定義與呼叫-function)
- [**4. 進階攻擊技術與隱蔽外傳**](#4-進階攻擊技術與隱蔽外傳)
  - [4.1 隨機數生成與防禦規避 (Randomization)](#4-1-隨機數生成與防禦規避-randomization)
  - [4.2 按鍵長按與組合控制 (HOLD / RELEASE)](#4-2-按鍵長按與組合控制-hold--release)
  - [4.3 酬載流程控制 (RESTART / STOP)](#4-3-酬載流程控制-restart--stop)
  - [4.4 輸入抖動規避分析 (Jitter)](#4-4-輸入抖動規避分析-jitter)
  - [4.5 酬載隱蔽與混淆防護 (Payload Hiding)](#4-5-酬載隱蔽與混淆防護-payload-hiding)
  - [4.6 隨身碟儲存活動監控 (Storage Activity)](#4-6-隨身碟儲存活動監控-storage-activity)
  - [4.7 鎖定鍵狀態讀取 (Caps/Num/Scroll Lock Keys)](#4-7-鎖定鍵狀態讀取-capsnumscroll-lock-keys)
  - [4.8 帶外隱蔽外傳技術 (Covert Exfiltration)](#4-8-帶外隱蔽外傳技術-covert-exfiltration)
  - [4.9 擴充套件系統 (Extensions)](#4-9-擴充套件系統-extensions)
  - [4.10 條件編譯機制 (Conditional Compilation)](#4-10-條件編譯機制-conditional-compilation)
- [**5. 實戰技巧、常見疑難排解與維護指引**](#5-實戰技巧常見疑難排解與維護指引)
  - [5.1 常見問題排查 (Common Issues)](#5-1-常見問題排查-common-issues)
  - [5.2 最佳實踐與實戰技巧 (Tips & Best Practices)](#5-2-最佳實踐與實戰技巧-tips--best-practices)
  - [5.3 韌體更新與出廠復原指南 (Firmware Updates & Recovery)](#5-3-韌體更新與出廠復原指南-firmware-updates--recovery)

---

## 1. 產品概述與快速入門指南

<!-- section：overview -->
### 1.1 USB Rubber Ducky 原廠介紹

USB Rubber Ducky 是享譽全球的專業按鍵注入（Keystroke Injection）攻擊裝置。自 2010 年問世以來，已成為資安紅隊滲透測試員、系統稽核人員與道德駭客必備的標準硬體配備。

外觀上，USB Rubber Ducky 偽裝成一般的 USB 隨身碟；然而插入目標電腦時，作業系統會將其識別為標準人機介面裝置（Human Interface Device，HID 鍵盤）。由於現代作業系統對鍵盤裝置具備先天固有信任，USB Rubber Ducky 能直接繞過傳統端點防護軟體（EDR、防毒軟體）的軟體執行封鎖限制，以每分鐘超過 1,000 字的超高速自動鍵入預設的指令碼。

在最新世代的 USB Rubber Ducky v2 中，硬體架構迎來了重大革新，換裝高速 32-bit ARM Cortex-M4 處理器，並導入全新 DuckyScript 3.0 語言規格，正式從單純的按鍵重放器進化為具備完整計算能力的硬體攻擊平台。

### 硬體技術規格與原廠校準基準表

| 硬體規格細項 | 原廠官方技術規格說明 |
|---|---|
| **SoC / 微控制器 (MCU)** | 32-bit ARM Cortex-M4 微控制器 |
| **內部儲存介面** | MicroSD 記憶卡插槽（支援 FAT32 檔案系統）|
| **按鍵注入速率** | 極速按鍵注入（速率超過每分鐘 1,000 字 / >1000 WPM）|
| **實體互動觸發器** | 整合式機身微動按鈕（支援酬載手動暫停、分段執行）|
| **主機連接介面** | 標準 USB Type-A 公頭 |
| **狀態診斷燈號** | 多色可程式化 RGB LED 狀態指示燈 |
| **機身保護外殼** | Hak5 標準半透明 USB 隨身碟保護外殼 |
| **指令碼語言版本** | DuckyScript 3.0（具備條件判斷、變數、迴圈與函式能力）|

---

### 1.2 開箱快速上手指南 (Quack-Start Guide)

要開始使用 USB Rubber Ducky v2，請依照下列標準程序操作：

1. **取出 MicroSD 記憶卡**：使用隨附的退卡工具輕推 MicroSD 卡槽，取出 MicroSD 卡。
2. **放入酬載檔案**：使用讀卡機將 MicroSD 卡連接至工作站，在記憶卡根目錄下建立名為 `payload.dd` 的文字檔案。
3. **編寫測試指令碼**：
   ```duckyscript
   REM 基礎測試酬載
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
4. **裝回記憶卡並插入目標主機**：將 MicroSD 卡插回 USB Rubber Ducky，隨後插入目標電腦的 USB 連接埠。
5. **觀察執行**：裝置將自動列舉為 HID 鍵盤，並於指定的延遲後全自動執行擊鍵指令。

---

<!-- section：features -->
### 1.3 DuckyScript™ 語法速查表

DuckyScript 3.0 為專屬擊鍵注入領域的巨集語言，其核心保留字包含：

| 指令關鍵字 | 功能說明 | 實用語法範例 |
|---|---|---|
| `REM` | 程式碼註解，不被編譯器執行 | `REM 這是註解說明` |
| `STRING` | 依序模擬敲擊指定的 ASCII 字串 | `STRING whoami /all` |
| `STRINGLN` | 鍵入字串並在結尾自動追加換行（Enter）| `STRINGLN powershell` |
| `DELAY` | 暫停指定毫秒數 | `DELAY 1500` |
| `DEFAULT_DELAY` | 設定所有擊鍵指令之間的預設全域間隔 | `DEFAULT_DELAY 50` |
| `GUI` / `WINDOWS` | 觸發 Windows / Super / Command 鍵 | `GUI r` |
| `ENTER` / `MENU` | 敲擊 Enter 換行鍵或右鍵功能表快捷鍵 | `ENTER` |
| `ALT` / `CTRL` / `SHIFT` | 標準修飾按鍵 | `CTRL ALT DEL` |
| `ATTACKMODE` | 設定 USB 列舉模式（HID、STORAGE 或複合模式）| `ATTACKMODE HID` |
| `BUTTON` | 偵測實體按鈕按下狀態 | `WAIT_FOR_BUTTON_PRESS` |
| `LED` | 調整機身 RGB LED 顏色與閃爍模式 | `LED_R` / `LED_OFF` |

---

## 2. DuckyScript 基礎語法與硬體控制

<!-- section：configuration -->
### 2.1 第一支酬載：Hello，World!

在 DuckyScript 中，最簡單的示範為喚醒系統對話框並鍵入文字。

```duckyscript
REM === Hello World 示範酬載 ===
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
> 插入目標電腦後，作業系統列舉驅動程式需要時間，建議於酬載最前端加入 `DELAY 2000` 至 `DELAY 3000`，確保主機完全識別 HID 鍵盤後才開始傳送擊鍵。

---

### 2.2 按鍵注入核心機制 (Keystroke Injection)

USB Rubber Ducky 支援標準 USB HID 鍵盤規格中的所有鍵碼：
- **功能按鍵**：`F1` 至 `F12`
- **方向鍵與編輯鍵**：`UP`、`DOWN`、`LEFT`、`RIGHT`、`PAGEUP`、`PAGEDOWN`、`HOME`、`END`、`INSERT`、`DELETE`
- **鎖定按鍵**：`CAPSLOCK`、`NUMLOCK`、`SCROLLLOCK`
- **組合熱鍵**：可單行堆疊多個修飾按鍵，如 `CTRL SHIFT ESC`（開啟 Windows 工作管理員）。

---

### 2.3 程式碼註解 (REM 指令)

`REM`（Remark）用於標註作者、版本資訊與作戰策略說明，所有 `REM` 開頭之內容皆不會輸出至目標主機。

```duckyscript
REM Author：Yupitek Security Team
REM Description：Windows Credential Harvester
REM Target：Windows 11 Enterprise
```

---

### 2.4 延遲等待控制 (DELAY 指令)

延遲是擊鍵注入攻擊能否 100% 成功的關鍵核心：
- `DELAY n`：精確等待 `n` 毫秒（例如 `DELAY 500` 代表等待 0.5 秒）。
- `DEFAULT_DELAY n` 或 `DEFAULTDELAY n`：在每個命令之間自動插入 `n` 毫秒等待，避免目標系統緩衝區溢位或漏字。

---

### 2.5 實體按鈕互動控制 (The Button)

USB Rubber Ducky v2 機身上配備實體按鈕，可在 DuckyScript 3.0 中實現靈活的互動流程：
- `WAIT_FOR_BUTTON_PRESS`：酬載執行至此會完全暫停，直到操作員實體按下面板按鈕才繼續執行。
- `BUTTON_DEF`：定義按鈕在執行期間被按下時觸發的非同步中斷處理常式。

```duckyscript
REM 等待操作員手動授權攻擊
LED_YELLOW
WAIT_FOR_BUTTON_PRESS
LED_GREEN
STRINGLN authorized_attack_sequence.bat
```

---

### 2.6 RGB LED 狀態指示燈控制 (The LED)

機身內建 RGB LED 可提供操作員即時的攻擊進度回饋，或在隱蔽行動中完全關閉：
- `LED_OFF`：關閉 LED 指示燈（隱蔽作戰模式推薦）。
- `LED_R` / `LED_G` / `LED_B`：分別切換為紅、綠、藍色恆亮。
- 支援自訂十六進位顏色與呼吸燈模式。

```duckyscript
LED_OFF
REM 攻擊執行中保持黑暗
STRINGLN powershell -NoP -NonI -W Hidden -Exec Bypass -File a.ps1
REM 攻擊完成亮綠燈 1 秒後熄滅
LED_G
DELAY 1000
LED_OFF
```

---

## 3. 邏輯控制、變數、條件判斷與函式

### 3.1 ATTACKMODE 攻擊模式設定

`ATTACKMODE` 命令用於控制 USB Rubber Ducky 呈現給作業系統的硬體外觀身分：
- `ATTACKMODE HID`：僅作為純鍵盤裝置（最高隱蔽性）。
- `ATTACKMODE STORAGE`：作為 USB 大容量儲存裝置（存取 MicroSD 內容）。
- `ATTACKMODE HID STORAGE`：複合模式（同時啟用鍵盤與儲存裝置）。

支援自訂硬體指紋參數（VID / PID / 序號 / 製造商），以精確偽裝為目標企業核准之合法周邊硬體：
```duckyscript
ATTACKMODE HID VID_046 D PID_C31 C MAN_Hak5 PROD_DUCKY SERIAL_1337
```

---

### 3.2 常數定義 (DEFINE 常數)

在 DuckyScript 3.0 中，可使用 `DEFINE` 宣告常數，增強指令碼可讀性與維護性：
```duckyscript
DEFINE #TARGET_USER admin
DEFINE #SLEEP_TIME 1000

DELAY #SLEEP_TIME
STRING #TARGET_USER
ENTER
```

---

### 3.3 變數宣告與記憶體操作 (VAR 變數)

使用 `VAR` 宣告全域或區域變數，並可進行動態計數或狀態暫存：
```duckyscript
VAR $FOO = 10
VAR $TRIES = 0

$TRIES = ($TRIES + 1)
```

---

### 3.4 算術與邏輯運算子 (Operators)

支援標準算術運算與布林邏輯運算：
- 算術：`+`、`-`、`*`、`/`、`%`
- 關係比較：`==`、`!=`、`<`、`>`、`<=`、`>=`
- 邏輯：`&&`、`||`、`!`

---

### 3.5 條件判斷控制結構 (IF / ELSE IF / ELSE)

藉由條件邏輯，單一酬載可自動判斷目標環境或按鈕狀態，執行不同攻擊路徑：
```duckyscript
VAR $OS_FOUND = 1

IF ($OS_FOUND == 1) THEN
    STRINGLN echo Windows Detected
ELSE
    STRINGLN echo Alternate OS Detected
END_IF
```

---

### 3.6 迴圈控制結構 (WHILE 迴圈)

支援 `WHILE` 條件迴圈，適合用於重試機制或定時巡檢：
```duckyscript
VAR $COUNT = 0
WHILE ($COUNT < 5)
    STRINGLN ping -n 1 127.0.0.1
    DELAY 1000
    $COUNT = ($COUNT + 1)
END_WHILE
```

---

### 3.7 自訂函式定義與呼叫 (FUNCTION)

使用 `FUNCTION` 封裝可重複利用之擊鍵序列：
```duckyscript
FUNCTION RUN_COMMAND(cmd)
    GUI r
    DELAY 400
    STRING cmd
    ENTER
    DELAY 800
END_FUNCTION

RUN_COMMAND(「cmd.exe」)
RUN_COMMAND(「powershell.exe」)
```

---

## 4. 進階攻擊技術與隱蔽外傳

### 4.1 隨機數生成與防禦規避 (Randomization)

DuckyScript 3.0 內建偽隨機數生成器（`$_RANDOM_INT`），可動態產生隨機延遲或隨機檔名，大幅打亂 EDR 行為特徵分析：
```duckyscript
VAR $RAND_DELAY = ($_RANDOM_INT % 500)
DELAY $RAND_DELAY
```

---

### 4.2 按鍵長按與組合控制 (HOLD / RELEASE)

可模擬人類操作中的持續長按動作（例如長按 Shift 觸發相黏鍵或特定遊戲熱鍵）：
```duckyscript
HOLD SHIFT
STRING abcdef
RELEASE SHIFT
```

---

### 4.3 酬載流程控制 (RESTART / STOP)

- `STOP_PAYLOAD`：立即終止當前酬載執行並使微控制器進入待機休眠。
- `RESTART_PAYLOAD`：重新由第一行開始重新執行酬載。

---

### 4.4 輸入抖動規避分析 (Jitter)

現代化端點偵測系統會監控鍵盤輸入速率。一般機器輸入每鍵間隔為固定毫秒，極易被行為啟發式防護辨識為惡意巨集。DuckyScript 3.0 的 Jitter 功能可為每個字元敲擊自動注入正負隨機微小延遲，精準模擬真人打字特徵。

---

### 4.5 酬載隱蔽與混淆防護 (Payload Hiding)

在目標系統中執行時，可搭配進階技巧隱匿痕跡：
- 利用 `GUI r` 呼叫極簡暫存行程。
- 清除 Windows 執行歷程記錄（RunMRU）。
- 在 MicroSD 磁區中隱藏酬載二進位檔。

---

### 4.6 隨身碟儲存活動監控 (Storage Activity)

當設定為複合模式（`ATTACKMODE HID STORAGE`）時，Ducky 可即時偵測目標作業系統是否正在對 MicroSD 進行讀寫存取，藉此精準判定檔案外傳何時完成。

---

### 4.7 鎖定鍵狀態讀取 (Caps/Num/Scroll Lock Keys)

USB 鍵盤協定中，目標主機每次按下 Caps Lock、Num Lock 或 Scroll Lock 時，主機會主動向鍵盤發送 1 個位元組的 HID Output Report 回傳燈號狀態。

USB Rubber Ducky v2 可即時讀取此狀態反饋！這意味著即使目標主機網路斷線、USB 隨身碟讀寫遭完全禁用，目標電腦端仍可透過 PowerShell 快速切換 Caps Lock 狀態，以二進位或摩斯密碼方式將資料回傳給 USB Rubber Ducky！

---

### 4.8 帶外隱蔽外傳技術 (Covert Exfiltration)

結合鎖定鍵狀態回傳或外掛硬體儲存，USB Rubber Ducky 實現了業界首創的無網路、純鍵盤介面資料外傳（Keystroke Exfiltration）。受測主機在未外連網際網路且未插隨身碟的情況下，敏感資料即可由 Ducky 內部記憶體安全截獲。

---

### 4.9 擴充套件系統 (Extensions)

DuckyScript 支援引進社群與原廠提供的擴充功能模組，透過 `EXTENSION` 關鍵字可擴充特化作業系統語意與自動化腳本。

---

### 4.10 條件編譯機制 (Conditional Compilation)

支援依據編譯目標架構或環境旗標進行條件式編譯，使單一程式碼檔案能夠同時適配 Windows、macOS 與 Linux 系統。

---

<!-- section：maintenance -->
## 5. 實戰技巧、常見疑難排解與維護指引

### 5.1 常見問題排查 (Common Issues)

| 異常徵狀 | 潛在成因分析 | 建議排除步驟 |
|---|---|---|
| **插入後完全無擊鍵反應** | 目標主機 USB 列舉速度較慢，或缺少初始延遲 | 在酬載開頭加入 `DELAY 3000` |
| **打字出現亂碼或按鍵錯位** | 目標主機鍵盤設定（Layout）非英文美規 (US) | 確認目標作業系統輸入法已切換為美式鍵盤 |
| **指示燈閃爍紅燈** | MicroSD 卡接觸不良或未找到 `payload.dd` | 重新格式化 MicroSD 為 FAT32 並檢查檔名大小寫 |
| **部分快捷鍵無法觸發** | UAC 權限限制或系統鎖定狀態 | 先行評估目標帳號權限或調整輸入流程 |

---

### 5.2 最佳實踐與實戰技巧 (Tips & Best Practices)

1. **分段測試**：撰寫複雜 DuckyScript 時，善用 `WAIT_FOR_BUTTON_PRESS` 與 `LED` 進行單步斷點偵錯。
2. **合理延遲**：重要視窗快顯指令後，務必給予至少 500 至 1,000 毫秒之系統載入緩衝。
3. **外殼保護**：攜帶時避免金屬異物碰觸裸露之 MicroSD 金手指接觸點。

---

### 5.3 韌體更新與出廠復原指南 (Firmware Updates & Recovery)

若需更新 USB Rubber Ducky v2 內部韌體或進行出廠復原：
1. 長按機身實體按鈕不放。
2. 將裝置插入電腦 USB 連接埠，持續按住按鈕 3 秒後放開。
3. 裝置將列舉為名為 `DUCKY` 的維護隨身碟磁區。
4. 將 Hak5 官方下載之最新韌體二進位檔案複製進該磁區。
5. 待 LED 指示燈呈現紅綠交替閃爍完成後重新插拔即可。
