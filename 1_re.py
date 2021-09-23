import re

p = re.compile("ca.e")

'''
. : 하나의 문자를 의미 > ca.e  -> care, cafe, case
^ : 시작 문자열을 의미 > ^de -> desk, destination
$ : 끝 문자열을 의미 > se$ -> case, base
'''

def print_match(m):
    if m:
        # print("m.group():", m.group()) # 일치하는 문자열 부문만 반환
        print("m.string:", m.string)   # 일치하는 입력받은 문자열 반환
        # print("m.start():", m.start())   # 일치하는 문자열의 시작 인덱스
        # print("m.end():", m.end())   # 일치하는 문자열의 끝 인뎃스
        # print("m.span():", m.span())   # 일치하는 문자열의 시작과 끝 인덱스
    else:
        print("not matched")

words = ['case', 'super care', 'list', 'cafe', 'careless']

for word in words:
    # m = p.match(word)    # 주어진 문자열의 처음부터 일치하는지 확인
    m = p.search(word)    # 주어진 문자열 중에 일치하는게 있는지 확인
    print_match(m)

print("="*20)

lst = p.findall("we do not care about his careless") # 일치하는 모든 것을 리스트 형태로 반환
print(lst)