from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from urllib import request, parse
import json
import hashlib
import asyncio

translation_cache = {}


async def translate_word(en_str, language):
    normalized_en_str = en_str.strip()
    if (normalized_en_str, language) in translation_cache:
        return translation_cache[(normalized_en_str, language)]
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    from_data = {
        'from': 'auto',
        'to': language,
        'q': normalized_en_str,
        'appid': 'your_appid',
        'salt': 'your_salt'
    }
    key = 'your_key'
    m = from_data['appid'] + normalized_en_str + from_data['salt'] + key
    m_MD5 = hashlib.md5(m.encode('utf8'))
    from_data['sign'] = m_MD5.hexdigest()
    data = parse.urlencode(from_data).encode('utf-8')
    try:
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: request.urlopen(url, data))
        html = await asyncio.get_event_loop().run_in_executor(None, response.read)
        translate_results = json.loads(html.decode('utf-8'))
        translate_results = translate_results['trans_result'][0]['dst']
    except Exception as e:
        messagebox.showerror("错误", f"翻译失败{str(e)}")
        return None
    translation_cache[(normalized_en_str, language)] = translate_results
    return translate_results


class TranslationApp:
    def __init__(self):
        self.root = Tk()
        self.root.title('基于百度翻译工具')
        self.root.geometry('520x270')
        self.root.resizable(False, False)  # 禁止改变窗口大小
        self.root.iconbitmap('F:/Python/爬虫翻译器/icon.ico')  # 设置窗口图标
        # 标签和输入框
        self.frame1 = ttk.Frame(self.root, style='TFrame')
        self.frame1.place(x=10, y=10, width=410, height=100)
        self.label1 = Label(self.frame1, text='输入要翻译的内容:', width=20, font=('Microsoft YaHei UI', 10))
        self.label1.grid(row=0, column=0, padx=5, pady=5)
        self.entry1 = Text(self.frame1, width=30, height=5, wrap='word', font=('Microsoft YaHei UI', 10))
        self.entry1.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.label3 = Label(self.frame1, text='翻译语言:', width=20, font=('Microsoft YaHei UI', 10))
        self.label3.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.language_var = StringVar()
        self.language_dropdown = ttk.Combobox(self.frame1, textvariable=self.language_var, width=10)
        self.language_dropdown['values'] = ('auto', 'en', 'es', 'fr')  # 添加支持的语言类型，可根据需要进行修改
        self.language_dropdown.current(0)  # 设置默认选项
        self.language_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.frame2 = ttk.Frame(self.root, style='TFrame')
        self.frame2.place(x=10, y=120, width=410, height=100)
        self.label2 = Label(self.frame2, text='翻译结果:', width=20, font=('Microsoft YaHei UI', 10))
        self.label2.grid(row=0, column=0, padx=5, pady=5)
        self.entry2 = Text(self.frame2, width=30, height=5, wrap='word', state='disabled',
                           font=('Microsoft YaHei UI', 10))
        self.entry2.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # 翻译按钮和清空按钮
        self.translate_button = Button(self.root, text='翻译', width=8, command=self.translate_button_click,
                                       font=('Microsoft YaHei UI', 10))
        self.translate_button.place(x=150, y=230)
        self.clear_button = Button(self.root, text='清空', width=8, command=self.clear_button_click,
                                   font=('Microsoft YaHei UI', 10))
        self.clear_button.place(x=250, y=230)

        # 作者标签
        self.author_label = Label(self.root, text='by @tcy', font=('Microsoft YaHei UI', 8))
        self.author_label.place(relx=1, rely=1, anchor='se')

    def translate_button_click(self):
        en_str = self.entry1.get(1.0, END)
        language = self.language_var.get()
        if en_str.strip():
            loop = asyncio.get_event_loop()
            vText = loop.run_until_complete(translate_word(en_str, language))
            if vText:
                self.entry2.config(state='normal')  # 允许修改状态
                self.entry2.delete(1.0, END)
                self.entry2.insert(1.0, vText)
                self.entry2.config(state='disabled')  # 设置为只读状态
        else:
            messagebox.showinfo("提示", "请输入要翻译的内容")

    def clear_button_click(self):
        self.entry1.delete(1.0, END)
        self.entry2.config(state='normal')  # 允许修改状态
        self.entry2.delete(1.0, END)
        self.entry2.config(state='disabled')  # 设置为只读状态

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = TranslationApp()
    app.run()
