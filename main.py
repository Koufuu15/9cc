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
  node, _ = parser.expr(token)

  print(".intel_syntax noprefix")
  print(".globl main")
  print("main:")

  codegen.gen(node)

  print(" pop rax")
  print(" ret")

if __name__ == "__main__":
  main()