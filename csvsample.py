import csv

#쓰기
f = open('smaple.csv', 'w', encoding='utf-8', newline='') #엑셀 CP040, MS040, EUC_KR

wr = csv.writer(f)  #csv를 불러와 wr변수에 대입
#wr.writerow([1,2,3])
wr.writerows([[1,2,3],[4,5,6], [7,8,9]])
f.close()

#읽기
f = open('smaple.csv', 'r', encoding='utf-8', newline='') #엑셀 CP040, MS040, EUC_KR
rd = csv.reader(f)
for i in rd:
    print(i)
f.close()
