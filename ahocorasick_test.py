# JiangHao
# coding:utf-8
import ahocorasick


def make_AC(AC, word_set):
    for word in word_set:
        AC.add_word(word, word)
    return AC


def test_ahocorasick():
    '''
    ahocosick：自动机的意思
    可实现自动批量匹配字符串的作用，即可一次返回该条字符串中命中的所有关键词
    '''
    key_list = ["苹果", "香蕉", "梨", "橙子", "柚子", "火龙果", "柿子", "猕猴挑"]
    AC_KEY = ahocorasick.Automaton()
    AC_KEY = make_AC(AC_KEY, set(key_list))
    AC_KEY.make_automaton()
    test_str_list = ["我最喜欢吃的水果有：苹果、梨和香蕉", "我也喜欢吃香蕉，但是我不喜欢吃梨"]
    for content in test_str_list:
        name_list = set()
        for item in AC_KEY.iter(content):  # 将AC_KEY中的每一项与content内容作对比，若匹配则返回
            name_list.add(item[1])
        name_list = list(name_list)
        if len(name_list) > 0:
            print(content, "--->命中的关键词有：", "\t".join(name_list))


if __name__ == "__main__":
    test_ahocorasick()
