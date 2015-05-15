import json
def showjson(filename):
    f = open(filename, 'r')
    j=json.load(f)
    showDict(j, 0)
    return


def showList(x, n):
    for item in x:
        if type(item) is list:
            showList(item, n+1)
        else:
            if type(item) is dict:
                showDict(item, n+1)
            else:
                for i in range(n):
                    print ' ',
                print item
    return

def showDict(x, n):
    for key in x.keys():
        item = x[key]
        if type(item) is list:
            showList(item, n+1)
        else:
            if type(item) is dict:
                showDict(item, n+1)
            else:
                for i in range(n):
                    print ' ',
                print key,
                print ':',
                print item
    return

showjson('./result/user.json')