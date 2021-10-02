import os
import sys
import gspread

def write(tp_list):
    gc = gspread.service_account(filename="/home/ai_competition6/gs_api.json")
    sh = gc.open("분석").worksheet("from_server")
    r = len(tp_list)
    sh.update('A1:B'+str(r), tp_list)


ver = input("""version (3 or 4) : """)
isTiny = input("""is tiny? (y or n) : """)
isUsual = input("""usual mode? (y or n) : """)
st_from = input("""start from? (default is 0) : """)
st_from = int(st_from)
path = input("""path (put / at the end, just press enter if weights are in current directory) : """ )+"""backup/"""
print(path)
try: 
    if (ver=="3" or ver=="4") and (isTiny == "y" or isTiny == "n"):
        pass
    else: 
        raise
    
    os.system("ls "+path+ " > map_temp.txt") 
    f = open("map_temp.txt", "r")
    text = f.readlines()
    tp_text = []
    for line in text:
        try: 
            line = ( int(line.split("_")[1].split(".")[0]), line.rstrip("\n"))
            tp_text.append(line)
        except:
            continue
    
    tp_text.sort(key=lambda x: x[0])
    if not st_from == 0 :
        i = [y[0] for y in tp_text].index(st_from)
        tp_text = tp_text[i:]
    
    for l in tp_text:
        print(l)
    
    if ver=="3" and isTiny=="y": a = "3-tiny.cfg"
    elif ver=="3" and isTiny=="n": a = "3.cfg"
    elif ver=="4" and isTiny=="y": a = "4-tiny-custom.cfg"
    elif ver=="4" and isTiny=="n": a = "4-custom.cfg"
    
    cmd_1 = "./darknet detector map yolov" + ver + ".data cfg/yolov" + a + " " + path
    
    q = 0
    try : 
        os.system("rm map_temp.txt")
    except : 
        print("its okay...")
        pass


    for tp in tp_text:
        cmd = cmd_1 + tp[1]
        #print(cmd)
        q = q+1
        if isUsual == "n":
            os.system("""echo "mean average precision (mAP@0.50) = 0.970368, or 97.04--""" + str(tp[0]) + """ ">> map_temp.txt """) 
        elif isUsual == "y":
            os.system(cmd + " | grep mAP@ >> map_temp.txt ") 
    
    tp_res = []
    f = open("map_temp.txt", "r")
    text = f.readlines()
    
    i=0
    for line in text:
        t1 = (tp_text[i][0])
        t2 = float(line.split("= ")[1].split(",")[0])
        tp_res.append([t1, t2])
        i = i+1
    
    #"./darknet detector map yolov4.data cfg/yolov4-custom.cfg backup/yolov4-custom_10000.weight"
    write(tp_res)
    
except Exception as e:
    print("wrong : ", e)
    
print("end of program")

