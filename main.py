import sys
#a = sys.stdin.read()
if len(sys.argv) <= 1:
  print("引数の個数が足りません。")
  exit()
  
a = sys.argv[1]

print(".intel_syntax noprefix")
print(".globl main")
print("main:")
print(f"  mov rax, {int(a)}")
print("  ret")