# SubtitleMerger

一个用于将中英文SRT字幕合并为双语字幕的Python脚本。

## 特点

- 支持通过时间戳匹配字幕，避免字幕错位。
- 支持选择中文在上或英文在上的显示顺序。
- 提供图形界面，方便选择文件。

## 使用方法
下载merge_srt.exe文件直接使用

# 代码说明

## 导入必要的模块

```python
import pysrt 
import tkinter as tk
from tkinter import filedialog
```

- **`pysrt`**：一个用于读取、操作和保存 SRT 字幕文件的 Python 库。
- **`tkinter`**：Python 内置的 GUI 库，用于创建图形用户界面。
- **`filedialog`**：`tkinter` 的子模块，用于打开文件对话框，让用户选择文件。

---

## 定义读取 SRT 文件的函数

```python
def read_srt(file_path):
    subs = pysrt.open(file_path, encoding='utf-8')
    return subs
```

- **函数功能**：读取指定路径的 SRT 字幕文件。
- **参数**：
  - `file_path`：字幕文件的路径。
- **实现**：
  - 使用 `pysrt.open` 方法打开 SRT 文件，指定编码为 `utf-8`，返回一个 `SubRipFile` 对象，包含所有的字幕条目。

---

## 定义写入 SRT 文件的函数

```python
def write_srt(subs, output_path):
    subs.save(output_path, encoding='utf-8')
```

- **函数功能**：将字幕对象保存到指定路径的 SRT 文件。
- **参数**：
  - `subs`：字幕对象，包含要写入的字幕条目。
  - `output_path`：输出文件的路径。
- **实现**：
  - 使用 `subs.save` 方法，将字幕保存到指定的文件路径，编码为 `utf-8`。

---

## 定义合并字幕的函数

```python
def merge_subtitles(ch_subs, en_subs, max_time_diff=0.5):
    merged_subs = pysrt.SubRipFile()
    en_index = 0
    en_len = len(en_subs)
    
    for ch_sub in ch_subs:
        ch_start_ms = ch_sub.start.ordinal  # 获取开始时间，单位为毫秒
        # 在英文字幕中寻找与当前中文字幕匹配的字幕
        while en_index < en_len and en_subs[en_index].end.ordinal < ch_start_ms - max_time_diff * 1000:
            en_index += 1
        if en_index < en_len and abs(en_subs[en_index].start.ordinal - ch_start_ms) <= max_time_diff * 1000:
            # 合并字幕文本，英文在上，中文在下
            merged_text = f"{en_subs[en_index].text}\n{ch_sub.text}"
            merged_sub = ch_sub
            merged_sub.text = merged_text
            merged_subs.append(merged_sub)
            en_index += 1
        else:
            # 没有匹配的英文字幕，只添加中文字幕
            merged_subs.append(ch_sub)
    return merged_subs
```

### 函数功能

- 将中文和英文字幕按照时间戳匹配，合并为双语字幕。

### 参数

- `ch_subs`：中文字幕列表。
- `en_subs`：英文字幕列表。
- `max_time_diff`：最大时间差，默认为 0.5 秒。

### 实现步骤

1. **初始化合并后的字幕对象和索引**：

   - `merged_subs`：创建一个空的 `SubRipFile` 对象，用于存储合并后的字幕。
   - `en_index`：英文字幕的当前索引，初始化为 0。
   - `en_len`：英文字幕的总数量。

2. **遍历每一条中文字幕**：

   ```python
   for ch_sub in ch_subs:
   ```

3. **获取当前中文字幕的开始时间（毫秒）**：

   ```python
   ch_start_ms = ch_sub.start.ordinal
   ```

4. **在英文字幕中寻找匹配的字幕**：

   - **跳过结束时间早于（中文开始时间 - 最大时间差）的英文字幕**：

     ```python
     while en_index < en_len and en_subs[en_index].end.ordinal < ch_start_ms - max_time_diff * 1000:
         en_index += 1
     ```

   - **检查当前英文字幕是否与中文字幕匹配**：

     ```python
     if en_index < en_len and abs(en_subs[en_index].start.ordinal - ch_start_ms) <= max_time_diff * 1000:
     ```

     - `abs(en_subs[en_index].start.ordinal - ch_start_ms)`：计算英文字幕开始时间与中文字幕开始时间的差值。
     - `<= max_time_diff * 1000`：判断差值是否在允许的最大时间差范围内（转换为毫秒）。

5. **合并匹配的字幕**：

   - **合并文本**：

     ```python
     merged_text = f"{en_subs[en_index].text}\n{ch_sub.text}"
     ```

     - 将英文字幕文本放在上面，中文字幕文本放在下面，用换行符分隔。

   - **创建新的字幕条目**：

     ```python
     merged_sub = ch_sub
     merged_sub.text = merged_text
     merged_subs.append(merged_sub)
     en_index += 1
     ```

     - 使用当前的中文字幕条目作为基础，更新其文本为合并后的文本。
     - 将新的字幕条目添加到 `merged_subs` 列表中。
     - 增加 `en_index`，准备匹配下一条英文字幕。

6. **处理未匹配的中文字幕**：

   - 如果没有找到匹配的英文字幕，直接将中文字幕添加到 `merged_subs` 中：

     ```python
     else:
         merged_subs.append(ch_sub)
     ```

7. **返回合并后的字幕列表**：

   ```python
   return merged_subs
   ```

---

## 定义主函数

```python
def main():
    # 初始化Tkinter主窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 选择中文字幕文件
    ch_path = filedialog.askopenfilename(title="请选择中文字幕文件", filetypes=[("SRT文件", "*.srt")])
    if not ch_path:
        print("未选择中文字幕文件，程序退出。")
        return

    # 选择英文字幕文件
    en_path = filedialog.askopenfilename(title="请选择英文字幕文件", filetypes=[("SRT文件", "*.srt")])
    if not en_path:
        print("未选择英文字幕文件，程序退出。")
        return

    # 选择输出文件保存位置
    output_path = filedialog.asksaveasfilename(title="保存合并后的字幕文件", defaultextension=".srt", filetypes=[("SRT文件", "*.srt")])
    if not output_path:
        print("未选择输出文件路径，程序退出。")
        return

    # 读取字幕文件
    ch_subs = read_srt(ch_path)
    en_subs = read_srt(en_path)

    # 合并字幕
    merged_subs = merge_subtitles(ch_subs, en_subs)

    # 写入合并后的字幕文件
    write_srt(merged_subs, output_path)

    print(f"合并完成，输出文件为：{output_path}")
```

### 实现步骤

1. **初始化 Tkinter 主窗口并隐藏**：

   ```python
   root = tk.Tk()
   root.withdraw()
   ```

   - 创建一个 Tkinter 主窗口 `root`。
   - 使用 `withdraw()` 方法将主窗口隐藏，因为我们只需要文件对话框。

2. **选择中文字幕文件**：

   ```python
   ch_path = filedialog.askopenfilename(title="请选择中文字幕文件", filetypes=[("SRT文件", "*.srt")])
   if not ch_path:
       print("未选择中文字幕文件，程序退出。")
       return
   ```

   - 弹出文件选择对话框，标题为“请选择中文字幕文件”，只显示 `.srt` 文件。
   - 如果用户未选择文件，打印提示信息并退出程序。

3. **选择英文字幕文件**：

   ```python
   en_path = filedialog.askopenfilename(title="请选择英文字幕文件", filetypes=[("SRT文件", "*.srt")])
   if not en_path:
       print("未选择英文字幕文件，程序退出。")
       return
   ```

4. **选择输出文件保存位置**：

   ```python
   output_path = filedialog.asksaveasfilename(
       title="保存合并后的字幕文件",
       defaultextension=".srt",
       filetypes=[("SRT文件", "*.srt")]
   )
   if not output_path:
       print("未选择输出文件路径，程序退出。")
       return
   ```

   - 弹出文件保存对话框，用户可以选择保存合并后字幕文件的位置和名称。
   - 如果用户未选择保存路径，打印提示信息并退出程序。

5. **读取字幕文件**：

   ```python
   ch_subs = read_srt(ch_path)
   en_subs = read_srt(en_path)
   ```

   - 调用 `read_srt` 函数，分别读取中文和英文字幕文件，得到字幕对象。

6. **合并字幕**：

   ```python
   merged_subs = merge_subtitles(ch_subs, en_subs)
   ```

   - 调用 `merge_subtitles` 函数，按照时间戳匹配并合并字幕。

7. **写入合并后的字幕文件**：

   ```python
   write_srt(merged_subs, output_path)
   ```

   - 调用 `write_srt` 函数，将合并后的字幕保存到用户指定的文件路径。

8. **提示完成信息**：

   ```python
   print(f"合并完成，输出文件为：{output_path}")
   ```

   - 打印提示信息，告知用户合并后的字幕文件保存位置。

---

## 程序入口

```python
if __name__ == "__main__":
    main()
```

- 当脚本作为主程序运行时，调用 `main()` 函数。
- 这是一种标准的 Python 程序入口写法，确保模块被导入时不会自动执行主程序。

---

## 注意事项

- **编码问题**：在读取和写入字幕文件时，指定了编码为 `utf-8`，确保程序能够正确处理包含中文字符的文件。

- **时间差参数**：`max_time_diff` 参数控制了在匹配字幕时允许的最大时间差，默认为 0.5 秒。如果发现字幕错位，可以适当调整此参数。

- **合并顺序**：在合并字幕时，默认是英文在上，中文在下。如果需要调整顺序，可以修改以下代码：

  ```python
  merged_text = f"{ch_sub.text}\n{en_subs[en_index].text}"
  ```

- **依赖库安装**：确保在运行程序前安装了必要的库：

  ```bash
  pip install pysrt
  ```

- **GUI 交互**：程序使用了 `tkinter` 库的文件对话框，提供了友好的图形界面，方便用户选择文件。

---

## 总结

该程序通过以下步骤实现了将中文和英文 SRT 字幕文件合并为一个双语字幕文件的功能：

1. **文件选择**：使用 `tkinter` 的文件对话框，让用户方便地选择中文、英文字幕文件和输出文件保存位置。

2. **字幕读取**：使用 `pysrt` 库读取 SRT 字幕文件，得到可操作的字幕对象。

3. **字幕合并**：按照时间戳匹配中文和英文字幕，允许一定的时间差，合并匹配的字幕条目。

4. **字幕保存**：将合并后的字幕保存为新的 SRT 文件，供用户使用。

5. **用户提示**：在关键步骤进行提示，确保用户了解程序的运行状态。

---

## 示例运行流程

1. **运行程序**：执行 `python merge_srt.py`，程序将启动并显示文件选择对话框。

2. **选择文件**：

   - 选择中文字幕文件。
   - 选择英文字幕文件。
   - 选择合并后的字幕文件保存位置。

3. **等待处理**：程序将自动处理字幕文件，合并字幕。

4. **完成提示**：程序完成后，提示合并完成，输出文件的位置。

---

## 扩展功能（可选）

- **支持更多格式**：修改 `filetypes` 参数，支持其他字幕格式，如 `.ass`、`.sub` 等。

- **命令行参数**：添加对命令行参数的支持，允许用户在命令行中指定文件路径。

- **错误处理**：增加对异常情况的处理，如文件格式不正确、文件不存在等。

- **进度显示**：在处理大量字幕时，添加进度条或状态提示。
