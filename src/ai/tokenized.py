import glob

import us
import nltk

import re
import regex

nltk.download('words')

files = glob.glob('/home/amin/Downloads/temp_text/*')
files.sort()

month_all = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']
month_abv = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
state_all = [str(i0) for i0 in us.states.STATES]
state_abv = [str(i0.abbr) for i0 in us.states.STATES]
key_words = ['agreement', 'grantor', 'grantee', 'county', 'parish', 'right of way']


def fun_clean(data):
    fun_clean1 = lambda elem: re.sub(r"$ (@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem)
    # fun_clean2 = lambda elem: re.sub(r"\d+", "", elem)
    data = fun_clean1(data)
    data = data.replace('rn', ' ')

    data = " ".join(data.split())

    return data


def fun_token(data, l_value=40):
    df = {}
    for i0 in key_words:
        ind_case = [m.start() for m in re.finditer(i0.lower(), data.lower())]
        # df[i0 + '_index'] = ind_case
        df[i0] = []
        for i1 in ind_case:
            val = data[i1 - l_value: i1 + l_value + 10]
            if i0 == 'agreement' and 'as agreement' not in val.lower() and 'this agreement' not in val.lower() and 'reference agreement' not in val.lower() and 'by agreement' not in val.lower() and 'the agreement' not in val.lower() and 'and agreement' not in val.lower() and 'or agreement' not in val.lower():
                val = " ".join([w for w in val.split() if w[0] != w[0].lower()])
                if len(val) != 0: df[i0].append(val)

            try:
                a = 2

                if i0 == 'county' or i0 == 'parish':
                    val_norm = val.split()
                    val_lower = val.lower().split()

                    try:
                        ind_county = val_lower.index('county')
                    except:
                        ind_county = val_lower.index('parish')

                    print(i0, ind_county)

                    if val_lower[ind_county + 1] == 'of':
                        '''
            it might be gabeurish when you call val_norm[ind_county: ind_county + 3]
            we can cross examine it by a list of counties if we know the state
            '''
                        val_county = " ".join(val_norm[ind_county: ind_county + 3])
                        if len(val_county) != 0: df['county'].append(val_county.title())

                    else:

                        val_case = val_norm[ind_county - 1: ind_county + 1]
                        if val_case[0][0] != val_case[0][0].lower():
                            val_county = " ".join(val_case)
                            if len(val_county) != 0: df['county'].append(val_county.title())

                        '''
            it might be gabeurish when you call val_norm[ind_county: ind_county + 3]
            we can cross examine it by a list of counties if we know the state
            '''

                if i0 == 'grantee':
                    val_norm = val.split()
                    val_lower = val.lower().split()
                    ind_grantee = val_lower.index('grantee')
                    val_case = val_norm[:ind_grantee]
                    val_case = [m for m in val_case if m[0] != m[0].lower()]

                    val_case = " ".join(val_case)

                    val_case = val_case.replace('Grantee', '')
                    val_case = val_case.replace('Grantor', '')

                    if len(val_case) != 0: df[i0].append(val_case.title())

                if i0 == 'grantor':
                    val_norm = val.split()
                    val_lower = val.lower().split()
                    ind_grantor = val_lower.index('grantor')
                    val_case = val_norm[:ind_grantor]
                    val_case = [m for m in val_case if m[0] != m[0].lower()]

                    val_case = " ".join(val_case)

                    val_case = val_case.replace('Grantee', '')
                    val_case = val_case.replace('Grantor', '')

                    if len(val_case) != 0: df[i0].append(val_case.title())

            except:
                pass

            # if i0 != 'agreement':
            #   if len(val) != 0: df[i0].append(val)

    state = []
    for i0 in state_all:
        ind_case = [m.start() for m in re.finditer(i0.lower(), data.lower())]

        for i1 in ind_case:
            state.append(data[i1: i1 + len(i0)].title())

    df['state'] = state

    date = []
    for i0 in month_abv:
        ind_case = [m.start() for m in re.finditer(i0, data)]

        for i1 in ind_case:
            val = data[i1 - l_value: i1 + l_value + 10]
            year = [i2 for i2 in range(1800, 2022) if '{}'.format(i2) in val]
            # print(year)

            for i2 in range(max(len(year), 1)):
                if len(year) == 0:
                    date.append(i0.title())
                else:
                    date.append("{} - {}".format(i0.title(), year[i2]))

    df['date'] = date

    return df


def fun_money(df, data, l_value):
    money = []
    for i0 in ["\$"]:
        ind_case = [m.start() for m in re.finditer("\$", data)]

        for i1 in ind_case:
            val = data[i1: i1 + 15]
            val_final = fun_digit(val)
            if len(val_final) > 1:
                money.append(val_final)

    df['money'] = money
    return df


def fun_digit(val):
    fun = lambda elem: regex.sub(r"([^\d.]|(?<=\..*)\.)", "", elem)
    val = fun(val)
    out = ['$']
    val = "".join(val.split())

    for i0 in range(len(val)):
        if val[i0].isdigit():
            out.append(val[i0])
        elif val[i0] == '.':
            if i0 != 0 and i0 != len(val) - 1:
                if val[i0 - 1].isdigit() and val[i0 + 1].isdigit():
                    out.append(val[i0])
        elif val[i0] == ',' and i0 != len(val) - 1:
            if i0 != 0:
                if val[i0 - 1].isdigit() and val[i0 + 1].isdigit():
                    out.append(val[i0])
        else:
            pass

    return "".join(out)


def run(text):
    data_case = fun_clean(text)
    df = fun_token(data_case, 75)
    df = fun_money(df, text, 75)
    res = dict()
    for i0 in df.keys():
        for i in range(len(df[i0])):
            res[df[i0][i]] = i0

    return res

