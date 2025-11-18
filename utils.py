import sys
import user_input

def error_at(er_msg, pos):
  print(user_input, file=sys.stderr)
  print(" " * pos + "^ " + er_msg, file=sys.stderr) #ファイルを指定して書きこむ＝エラーとして出力
  exit(1)

def strtol(lst, s):
  #print(lst, s)
  num = []
  while s < len(lst) and lst[s].isdigit():
    num.append(lst[s])
    s += 1

  return  "".join(num), s