import os

num = [1,2,3,4,5,6,7]
paths = ["/home/ai_competition6/1.competition_trainset/"+ str(i) +"_dataset/" for i in num]
length = []
file_lists = []
for path in paths:
    file_list = sorted(os.listdir(path))
    file_lists.append(file_list)
    # jpg파일과 txt파일 개수 합친 것
    length.append(len(file_list)//2)
    print('number of images in', '"'+path[21:]+'"', 'is', length[-1])

dict_name = {}
for i in range(60):
    dict_name[i] = []

for p in enumerate(paths):
    if p[0] == 0:
        continue
    file_list = sorted(os.listdir(p[1]))
    for idx in range(length[p[0]]):
        with open(p[1] + file_list[idx*2 + 1], "r") as f:
            text = f.readlines()
            x = text[0].split(' ')
            dict_name[int(x[0])].append((p[1]+file_list[idx*2 + 1])[:-4])

for i in range(60):
    val = '\n'.join(dict_name[i])    
    with open("/home/ai_competition6/name/" + str(i) + ".txt", "w") as  f:
            f.write(val)
