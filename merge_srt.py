import pysrt
import tkinter as tk
from tkinter import filedialog

def read_srt(file_path):
    subs = pysrt.open(file_path, encoding='utf-8')
    return subs

def write_srt(subs, output_path):
    subs.save(output_path, encoding='utf-8')

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

if __name__ == "__main__":
    main()
