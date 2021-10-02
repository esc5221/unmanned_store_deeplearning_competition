test_size = (640, 420)
input_path = "3.1.weak_backsub/"
result_folder = "10.weak/"
class_num = 5


##############################

import matplotlib.pyplot as plt
from matplotlib.image import imread
from PIL import Image
from PIL import ImageDraw
import numpy as np
import os

plt.rcParams['figure.figsize'] = (3, 4)

try: 
    itspy = (os.path.basename(__file__)[-2:] == 'py')
except NameError as e:
    itspy = False

# DRAW BOX - https://wikidocs.net/73720
#   img : Image.open(*)으로 load한 이미지
#   c : list of int
def pil_draw_rect(img, c):
    draw = ImageDraw.Draw(img)
    draw.rectangle(((c[0], c[1]), (c[2], c[3])), outline=(100, 255, 255), width=4)
    return img

# CALCULATE THE COORDINATES OF BOX
#   line : single string
def bx_coord(line, w ,h):
    n_s = line.split()
    n = [float(i) for i in n_s]
    box_f = (w*(n[1]-n[3]/2), h*(n[2]-n[4]/2), w*(n[1]+n[3]/2), h*(n[2]+n[4]/2))
    box = [int(i) for i in box_f]
    return box

# COMBINATION FOR FRAME_1, return x12 sets of x5 numbers
#   class_num : # of classes, default is 60
def combi(n):
    
    cbs = [[],[],[],[],[]]
    cbs[0] = [np.random.randint(1,12) for x in range(5)] 
    #print(cbs[0])
    cbs[1] = [1,2,3,4,5]
    cbs[2] = [1,3,5,7,9]
    cbs[3] = [1,4,7,10,12]
    cbs[4] = [1,6,8,9,11]

    w, h = 5, 12;
    res = [[0 for x in range(w)] for y in range(h)] 

    for k in range(0,12):
        for i in range(0,5):
            res[k][(i-n)%5] = ((cbs[n][i]-1)*5+i+k*5+1)%60    
    return res
        

# CREATE PATH COMBINATION OF IMAGE, return x12 sets of x5 paths
def target_path():
    folder_list = sorted(os.listdir("/home/ai_competition6/"+input_path))
    paths = ["/home/ai_competition6/"+input_path+ folder  \
             for folder in folder_list if os.path.isdir(os.path.join("/home/ai_competition6/"+input_path,folder))]
    target = ["" for i in range(60)]
    classes_list = [ int(p[0:2]) for p in folder_list]
    
    for i in range(60):
        it = i%len(classes_list)
        file_list = sorted(os.listdir(paths[it]))
        l = len(file_list)
        j = np.random.randint(0,l//2)        
        target[i] = paths[it] + "/" + file_list[2*j]

        w, h = 5, 12;
        c_target = [["" for x in range(w)] for y in range(h)] 
        
    if class_num == 60:
        comb = combi(class_num)
        for i in range(12):
            for j in range(5):
                c_target[i][j] = target[comb[i][j]]
                
    elif class_num != 60:
        for i in range(12):
            for j in range(5):
                c_target[i][j] = target[i*5+j]
    
    return c_target

def print_12x5(c_target):
    for i in range(12):
        for j in range(5):
            print(c_target[i][j])
        print("--------------------------------------------------")

    
# RETURN MERGED IMAGE USING FRAME 1 (U3D2)
#   img_paths : list of string (paths of images)
#   typ : integer (type of merge a.k.a number of images for merge)
#   var_1 : float (variable for different horizontal-overlap)
#   var_2 : float (variable for different vertical-overlap)
def merge(img_paths, typ, var_1, var_2, iter_n):
    labels = []
    for i in range(12):
        try:
            # create new empty image
            labels = []
            new_label = ""
            size = test_size
            name = [ 0 for x in range(5)]
            r1 = 150
            r2 = 180
            rand_rgb = (np.random.randint(r1,r2), np.random.randint(r1,r2) ,np.random.randint(r1,r2))
            new_image = Image.new('RGB', size, rand_rgb)

            imgs_size = [ (0,0) for x in range(5)]
            box_size = [[0 for x in range(2)] for y in range(5)] 
            for j in range(5):
                with Image.open(img_paths[i][j]) as img:
                    imgs_size[j] = img.size

            crops = [Image.new('RGBA', (10,10), (255,255,255,0)) for x in range(5)]

            for j in range(5):
                # open iamge and convert to RGBA
                img = Image.open(img_paths[i][j])
                img = img.convert("RGBA")
                datas = img.getdata()

                # make transparent - https://studyforus.com/innisfree/594134
                newData = []
                cutOff = 7
                for item in datas:
                    if item[0] <= cutOff and item[1] <= cutOff and item[2] <= cutOff:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                img.putdata(newData)

                f = open(img_paths[i][j][:-3]+"txt", "r")
                line = f.readlines()
                w, h = imgs_size[j]
                n_s = line[0].split()
                name[j] = int(n_s[0])
                f.close()

                n = [float(i) for i in n_s]
                box_f = (w*(n[1]-n[3]/2), h*(n[2]-n[4]/2), w*(n[1]+n[3]/2), h*(n[2]+n[4]/2))
                box = [int(i) for i in box_f]

                box_size[j][0] = int(w*n[3])
                box_size[j][1] = int(h*n[4])

                # paste test - you should type 'mask' for background transparency
                #   https://stackoverflow.com/questions/38627870/how-to-paste-a-png-image-with-transparency-to-another-image-in-pil-without-white/38629258
                #temp = Image.new('RGBA', (400,400), (105,255,255,255))
                #temp_crop = img.crop(box)
                #temp.paste(temp_crop, (0,0), mask=temp_crop) 
                crops[j] = img.crop(box)

            if(not itspy): 
                plt.figure(figsize=(16, 18))
            for j in range(5):
                resize_wh = (0,0)
                bx = box_size[j][0]
                by = box_size[j][1]
                resize_var = np.random.randint(190,210)
                if bx>by : resize_wh = (resize_var , int(resize_var*(by/bx)) )
                else : resize_wh = (int(resize_var*(bx/by)), resize_var )
                box_size[j] = resize_wh
                resized = crops[j].resize(resize_wh)

                if(not itspy):
                    plt.subplot(1,5,j+1)
                    plt.imshow(resized)

                # set frame
                coord = frame(typ,var_1,var_2, box_size)
                new_image.paste(resized, coord[j], mask=resized) 

                # make label
                t_cen_x = (coord[j][0] + resize_wh[0]/2)/size[0]
                t_cen_y = (coord[j][1] + resize_wh[1]/2)/size[1]
                t_box_w = resize_wh[0]/size[0]
                t_box_h = resize_wh[1]/size[1]
                label = [name[j], t_cen_x, t_cen_y, t_box_w, t_box_h]
                label = map(str, label)
                labels.append(' '.join(label))
                new_label = '\n'.join(labels)
        
        
            i_folder = '{0:04d}'.format(iter_n)
            i_str = '{0:04d}'.format(iter_n)+ '_'+ '{0:02d}'.format(i)

            if not os.path.exists('/home/ai_competition6/'+result_folder+ i_folder):
                os.makedirs('/home/ai_competition6/'+result_folder+ i_folder)

            with open('/home/ai_competition6/'+result_folder+ i_folder + '/'+ i_str + '.txt', 'w') as file:
                file.write(new_label)
            new_image.save('/home/ai_competition6/'+result_folder + i_folder + '/' + i_str +'.jpg')
            
        except Exception as e: 
            print('  except at '+ str(iter_n) + ',' + str(i) )
            print("   -- error is : ", e)
            continue

        
        if(not itspy): 
            plt.show()
            plt.figure(figsize=(40, 30))
            plt.subplot(1,2,1)
            plt.imshow(new_image)
            for kk in img_paths[i]:
                print(kk)
            #print("----------------------------------")
            #print(new_label)
            #print("----------------------------------")
            #print(type(new_label))
            box_new_image = new_image.copy()
            ll = new_label.split("\n")
            for l in ll:
                #print(l[0])
                box_new_image = pil_draw_rect(box_new_image, bx_coord(l,test_size[0],test_size[1]))
            plt.subplot(1,2,2)
            plt.imshow(box_new_image)
       
        
        #paste cropped image to empty image
        #new_image.paste(cropped)
        
        
# RETURN MERGED IMAGE USING FRAME 1 (U3D2)
#   img_paths : list of string (paths of images)
def frame(typ, wx, wy, box_size):
    if typ == 5:
        w, h = 2, typ
        coord =  [[0 for x in range(w)] for y in range(h)] 
        next_x = 47
        next_y = 41

        for j in range(3):
            coord[j][0] = int(next_x)
            coord[j][1] = int(next_y)
            next_x = next_x + box_size[j][0]/wx
            next_y = next_y + (box_size[j][1]) - (box_size[j+1][1])
        for j in range(3,4):
            a = 0
            if box_size[j][0] > box_size[j][1]+100 :
                a = 100

            next_x = 47 + box_size[0][0]/2
            next_y = 41 + box_size[0][1]/wy + a
            coord[j][0] = int(next_x)
            coord[j][1] = int(next_y)+10
        for j in range(4,5):
            coord[j][0] = int(next_x + box_size[j-1][0]/wx)
            coord[j][1] = int(next_y)+10
        return coord
    elif typ == 0:
        coord = [[0 for x in range(2)] for y in range(5)] 
        coord[0] = [0, 0]
        coord[1] = [200, 0]
        coord[2] = [400, 0]
        coord[3] = [100, 210]
        coord[4] = [400, 210]
        return coord

if(not itspy):
    merge(target_path(), 0, 1, 1.2, 1)
else:
    a = int(input('start : '))
    b = int(input('end : '))
    for i in range(a,b):
        print(i)
        merge(target_path(), 0, 1.3, 1.3, i)