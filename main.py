import sys
import tokenizer
import parser
import codegen

#a = sys.stdin.read()

def main():
  if len(sys.argv) <= 1:
    print("引数の個数が足りません。")
    exit()
  
  token = tokenizer.tokenize()
  '''
  cur = token
  while not cur.at_eof():
    print(cur.kind)
    cur = cur.tsugi
  '''
  code = parser.program(token)

  print(".intel_syntax noprefix")
  print(".globl main")
  print("main:")

  print(" push rbp")
  print(" mov rbp, rsp")
  print(" sub rsp, ", len(parser.lvar) * 8)

  for i in code:
    codegen.gen(i)
    # 何行もの命令の計算結果を一回ごとに取り除いておく
    print(" pop rax")

  # 変数実装には不可欠の2行
  print(" mov rsp, rbp")
  print(" pop rbp")
  print(" ret")

if __name__ == "__main__":
  main()