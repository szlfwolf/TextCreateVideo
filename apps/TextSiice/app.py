#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2023/08/01 11:30
# @file:app.py
import os

from config import file_path


class Main:

    def txt_chapter(self, filepath, pattern='第.{1,4}章'):
        """
        txt文件chapter处理
        :return:
        """    
        path = os.path.join(file_path, filepath)
        if not os.path.exists(path):
            raise FileNotFoundError(f"文件不存在，根路名为{path}")
        file = open(path, 'r', encoding='utf-8')
        content = file.read()
        re.split(pattern, content)
        chapter_list = re.split(pattern, content)
        for index, value in enumerate(chapter_list):
            chapter_path = path.replace('.txt','-{}.txt'.format(str(index)))
            chapter_file = open(chapter_path, 'w')
            content = value.replace('\n', '').replace('\u3000', '').replace('-', '')
            text_list = self.txt_long(content.split('。'))
            text_list = self.txt_short(text_list)
            for line_index, line in enumerate(text_list):
                chapter_file.write("{}:{}{}".format(str(line_index),line,"\n"))
            chapter_file.close()
        return chapter_list

    def txt_handle(self, filepath):
        """
        txt文件处理
        :return:
        """
        path = os.path.join(file_path, filepath)
        if not os.path.exists(path):
            raise FileNotFoundError(f"文件不存在，根路名为{path}")
        file = open(path, 'r', encoding='utf-8')
        content = file.read().replace('\n', '')
        text_list = self.txt_long(content.split('。'))
        return self.txt_short(text_list)

    def txt_short(self, text_list: list):
        """
        处理文本过短的问题
        :return:
        """
        for index, value in enumerate(text_list):
            # 一段话少于15字，则拼接上一段话
            if len(value) < 15 and len(text_list) > 1:
                if index == (len(text_list) - 1):
                    x = False
                elif index == 0:
                    x = True
                else:
                    # 如果该文本的上一句话长度大于下一句话，那么就贴到下一句话头部
                    x = len(text_list[index - 1]) - len(text_list[index + 1]) >= 0
                if index == 0 or x:
                    text_list[index + 1] = f"{value}，" + text_list[index + 1]
                else:
                    text_list[index - 1] = text_list[index - 1] + f"，{value}"
                text_list.pop(index)
        return text_list

    def txt_long(self, text_list: list):
        """
        处理文本过长的问题
        :return:
        """
        new_list = []
        for index, value in enumerate(text_list):
            # print(index, value)
            if len(value) > 60:
                value_list = self.symbol_split(value, ['，', '?'])
                new_list.extend(value_list)
            else:
                new_list.extend([value])
        return new_list

    def recursion(self, value):
        value_list = value.split("，")
        if len(value_list) >= 2:
            for i in value_list:
                if len(i) > 60:
                    return self.recursion(i)
            head_str = ""
            foot_str = ""
            while value_list:
                if len(head_str) > len(foot_str):
                    foot_str += f'{value_list[-1]}，'
                    value_list.pop(-1)
                elif len(head_str) < len(foot_str):
                    head_str += f'{value_list[0]}，'
                    value_list.pop(0)
                else:
                    if len(value_list) > 1:
                        foot_str += f'{value_list[-1]}，'
                        value_list.pop(-1)
                        head_str += f'{value_list[0]}，'
                        value_list.pop(0)
                    else:
                        foot_str += f'{value_list[-1]}，'
                        value_list.pop(-1)
            return [head_str, foot_str]
        else:
            value_list = value[len(value) // 2]
            for i in value_list:
                if len(i) > 60:
                    return self.recursion(i)
            return value_list

    def symbol_split(self, value, symbol_list):
        if not symbol_list:
            return [value]
        value_list = value.split(symbol_list.pop(0))
        for index, value in enumerate(value_list):
            if len(value) > 60:
                return self.symbol_split(value, symbol_list)
        return value_list

    def question_mark_split(self, value):
        value_list = value.split("？")
        for index, value in enumerate(value_list):
            if len(value) > 60:
                value_list = self.recursion(value)
                value_list.pop(index)
                for i, v in enumerate(value_list):
                    value_list.insert(index + i, v)
        return value_list


if __name__ == '__main__':
    Main().txt_handle("道诡异仙.txt")
