import sys

result = []
with open('../html_txt/科系/科系列表.txt', 'r') as f:
    for line in f:
        result.append(line.strip('\n'))
    
print(result)
