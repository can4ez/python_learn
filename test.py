s = "bccfcafan"
pos_1 = 0
pos_2 = 0
max_l = 0
for i in range(len(s)): 
    p = s.rfind(s[i]) + 1
    l = len(s[i:p])
    if l > max_l:
        pos_1 = i
        pos_2 = p
        max_l = l

print(s[pos_1:pos_2]) # ccfc
print(pos_1 + 1, pos_2, sep=' ') # 2 5
print(max_l) # 4