import re
import string as _str  # Не знаю почему, но на простой импорт он ругается и вместо string подставляет str ..
import pickle


def get_words(txt):
    result = {}

    # Чистим от знаков препинания, они не относятся к словам
    for p in _str.punctuation:
        txt = txt.replace(p, ' ')

    words = txt.split()
    for w in words:
        result[w] = len(w)

    return result


def get_words_count(s):
    for p in _str.punctuation:
        s = s.replace(p, ' ')

    return len(s.split())


def get_suggestions(txt):
    result = {}

    # suggestions = re.split("[.!?]\s*", txt)

    # Чтобы сохранился символ окончания строки
    suggestions = re.split(r'(?<=[.!?]) ', txt)

    for s in suggestions:
        c = get_words_count(s)
        if c != 0:
            result[s] = c

    return result


def get_punctuations(txt):
    result = {}

    for p in _str.punctuation:
        c = txt.count(p)
        if c != 0:
            result[p] = c

    return result


def dump_result(result, path):
    with open(path, 'wb') as f:
        pickle.dump(result, f)


def dump_text(result, path):
    with open(path, 'w', encoding='UTF-8') as f:
        for r in result:
            f.write(r + '\n')


def result_print(result):
    for key in result:
        if isinstance(result[key], dict):
            print(key, '', sep=': ')
            for sub in result[key]:
                print('\t' + sub, result[key][sub], sep=': ')
        else:
            print(key, result[key], sep=': ')

        print("\n")


def gen_paragrapths(items, n):
    result = []
    i = 0
    c = 0

    for s in items:

        if c == 0:
            result.append(s)
        else:
            result[i] += ' ' + s
        c += 1

        if c == n:
            c = 0
            i += 1

    return result


def input_num(text):
    return 2

    while 1:
        n = input(text)
        try:
            n = int(n)
        except ValueError as ex:
            print("Ошибка ввода: а что за символ был введен? Это точно не число!", "Попробуй еще раз!", sep="\n")
            continue

        return n


def sort_paragrapths(paragraphs):
    # Т.к. по заданию нужна сортировка по возростанию количества СЛОВ
    # то используем созданную функцию get_words() для получения списка слов и расчета их количества
    return sorted(paragraphs, key=lambda x: len(get_words(x)))


def print_paragraphs(sorted_paragraphs, n):
    print("Текст после разбиения на абзацы по "+str(n)+" предложения и сортировки их по числу слов:")
    for s in sorted_paragraphs:
        print(s)


def parse_text(txt):
    print('Исходный текст: ' + txt)

    result = {"Всего слов": 0, "Всего предложений": 0, "Предложения": 0, "Слова": 0, "Знаки препинания": 0}

    result['Предложения'] = get_suggestions(txt)
    result['Всего предложений'] = len(result['Предложения'])

    result['Слова'] = get_words(txt)
    result['Всего слов'] = len(result['Слова'])

    result['Знаки препинания'] = get_punctuations(txt)

    result_print(result)

    dump_result(result, 'data.pickle')

    n = input_num("А еще, я умею разбивать тект по предложениям.\nКакого размера создать обзацы? (n): ")
    paragraphs = gen_paragrapths(result['Предложения'], n)
   
    sorted_paragraphs = sort_paragrapths(paragraphs)
    print_paragraphs(sorted_paragraphs, n)
    dump_text(sorted_paragraphs, 'data.txt')



if __name__ == '__main__':
    string = 'Захотелось мне как-то сделать более надёжной передачу информации через радиоканал. ' \
             'Это не какой-то промышленный проект, или что-то другое серьёзное. ' \
             'Это скорее для хобби и саморазвития.'
    parse_text(string)
