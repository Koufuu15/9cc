import sys
from user_input import user_input
import string

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

def keyword(index):
  val = ""
  while user_input[index] in string.ascii_lowercase or user_input[index] in string.ascii_uppercase or user_input[index] == "_":
    val += user_input[index]
    index += 1
  
  return val