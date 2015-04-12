
N = 5000
f1 = open('verified_online.xml','r')
f2 = open('Black.xml','w')

for i in range(N):
    f2.write(f1.readline())

f1.close()
f2.close()
