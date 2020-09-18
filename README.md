# ftp_file_md5sum

input python3 ftp_file_list_md5.py [a] [b] [c]
[a] (mode):
  0 is caculate the all files md5 and save the md5 to [b] file
  1 is compared c dir all files with b md5 file.
[b] (md5_file) : save md5 value.
[c] (dir): destnate dir.



**example 1:** python3 ftp_file_list_md5.py 0 hello.txt /data/ssss
caculate the /data/ssss all files md5 and write to hello.txt.

**example 2:** python3 ftp_file_list_md5.py 1 hello.txt /data/ssss
caclaute the /data/ssss all files md5 and compared with reading hello.txt all md5.