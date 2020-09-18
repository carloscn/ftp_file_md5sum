import os,sys,hashlib,argparse

# input python3 ftp_file_list_md5.py [a] [b] [c]
# [a] (mode):
#   0 is caculate the all files md5 and save the md5 to [b] file
#   1 is compared c dir all files with b md5 file.
# [b] (md5_file) : save md5 value.
# [c] (dir): destnate dir.

# example 1: python3 ftp_file_list_md5.py 0 hello.txt /data/ssss
# caculate the /data/ssss all files md5 and write to hello.txt.

# example 2: python3 ftp_file_list_md5.py 1 hello.txt /data/ssss
# caclaute the /data/ssss all files md5 and compared with reading hello.txt all md5.

file_name_list = []
file_md5_list = []

def match(file_path,Bytes=1024):
    md5_1 = hashlib.md5()
    with open(file_path,'rb') as f:
        while 1:
            data =f.read(Bytes)
            if data:
                md5_1.update(data)
            else:
                break
    ret = md5_1.hexdigest()
    return ret

def read_dir_file_list(dir):
    file_name_list = os.listdir(dir)
    file_name_list.sort()
    print("[inf_log]: file list is:", file_name_list)
    return file_name_list

def calc_md5(dir, file_name_list):
    count = 0
    file_md5_list = []
    for file_name in file_name_list:
        file_md5_list.append(match(str(dir + "/" + file_name)))
        print("[inf_log]: calc file [",file_name, "] md5 is [", file_md5_list[count] ,"]")
        count = count + 1
    return file_md5_list

def write_file_md5_to_file(file_out_name, file_name_list, file_md5_list):
    output = open(file_out_name, 'w+')
    if len(file_name_list) != len(file_md5_list):
        print("[err_log]: file list and md5 len not match!\n")
        assert 0
    for i in range(len(file_name_list)):
        output.write(file_name_list[i])
        output.write("$$")
        output.write(file_md5_list[i])
        output.write("$$")
        output.write("\n")
    output.close()

def read_filelist_from_file(file_in_name):
    input = open(file_in_name, 'r+')
    file_name_list = []
    list = input.readlines()
    for i in range(len(list)):
        file_name_list.append(list[i])
        file_name_list[i] = file_name_list[i].split("$$")[0]
    return file_name_list

def read_md5_from_file(file_in_name):
    input = open(file_in_name, 'r+')
    file_md5_list = []
    list = input.readlines()
    for i in range(len(list)):
        file_md5_list.append(list[i])
        file_md5_list[i] = file_md5_list[i].split("$$")[1]
    return file_md5_list

parser = argparse.ArgumentParser()
parser.description='please enter two parameters md5_file and files dir ...'
parser.add_argument("-w", "--work", help="this is parameter work mode", dest="work", type=int, default="0")
parser.add_argument("-m", "--md5f", help="this is parameter md5 file", dest="md5f", type=str, default="hello.txt")
parser.add_argument("-d", "--dir", help="this is parameter dir",  dest="dir", type=str, default="./data")
args = parser.parse_args()

print("[inf_log]: parameter a is :", args.work)
print("[inf_log]: parameter b is :", args.md5f)
print("[inf_log]: parameter c is :", args.dir)
work_mode = int(args.work)
md5f = str(args.md5f)
dir = str(args.dir)
# check work mode
if (work_mode >= int(2)):
    print("[err_log]: -w parameter is wrong, 1 or 0 is true, your value is %d" % work_mode)
    assert 0
# check dir
ret = os.path.exists(dir)
if ret == False:
    print("[err_log]: -d parameter is wrong, no dir [%s] is exist." % dir)
    assert 0
# check dir empty
files = os.listdir(dir)
if len(files) == False:
    print("[err_log]: -d parameter is wrong, dir [%s] is empty." % dir)
    assert 0

if (work_mode == 0):
    pass
    file_name_list = read_dir_file_list(dir)
    file_md5_list = calc_md5(dir, file_name_list)
    write_file_md5_to_file(md5f, file_name_list, file_md5_list)
    file_name_list = []
    file_md5_list = []
    print("[inf_log]: save [%s] file ok !" % (md5f))

elif (work_mode == 1):
    if os.path.isfile(md5f) == False:
        print("[err_log]: md5f [%s] is not exist" % md5f)
        assert 0
    print("[inf_log]: read [%s] file ok !" % md5f)
    f_file_name_list = read_filelist_from_file(md5f)
    f_file_md5_list = read_md5_from_file(md5f)
    l_file_name_list = read_dir_file_list(dir)
    l_file_md5_list = calc_md5(dir, l_file_name_list)
    file_error_list = []
    md5_error_list_local = []
    md5_error_list_remote = []
    error_count = 0
    if (len(l_file_md5_list) != len(f_file_md5_list)):
        print("[err_log]: mdfile list and local filelist len not match!")
        assert 0
    print("[inf_log]: compare md5 and filename..")
    for i in range(len(l_file_name_list)):
        print("[inf_log]: %d times: compare filename [%s] | [%s] , compare hash [%s] | [%s] " %(i ,f_file_name_list[i] ,l_file_name_list[i] ,f_file_md5_list[i] ,l_file_md5_list[i]))
        if (f_file_name_list[i] != l_file_name_list[i]):
            print("[err_inf]: compare name error! -> remote name: [%s] | local name: [%s] " %(f_file_name_list[i], l_file_name_list[i]))
            assert 0
    for i in range(len(l_file_md5_list)):
        if (f_file_md5_list[i] != l_file_md5_list[i]):
            print("[err_inf]: compare md5 error! -> remote md5: [%s] | local md5: [%s] " % (f_file_md5_list[i], l_file_md5_list[i]))
            file_error_list.append(f_file_name_list[i])
            md5_error_list_local.append(l_file_md5_list[i])
            md5_error_list_remote.append(f_file_md5_list[i])
            error_count = error_count + 1
    if error_count == 0:
        print("[inf_log]: All files have been passed md5 check!! Goodbye!-------->>>")
    else :
        print("[err_log]: MD5 check failed, there are files md5 not match total %d, please check it on err_list.txt !! Goodbye!-------->>>" %error_count)
        for i in range(error_count):
            print("[err_log]: file [%s] md5 check failed." %file_error_list[i])
        output = open("err_list.txt", 'w+')
        output.write(str("--------------md5 match error list total %d-------------------\n" %error_count))
        for i in range(error_count):
            output.write("file "+ str(i) + " | name:[")
            output.write(file_error_list[i])
            output.write("] -> remote md5:[%s] & local md5:[%s] " %(md5_error_list_remote[i], md5_error_list_local[i]))
            output.write("\n")
        output.write("-------------------------------------------------------------")
        output.close()

else:
    pass