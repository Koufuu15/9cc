import sys
#a = sys.stdin.read()
if len(sys.argv) <= 1:
  print("引数の個数が足りません。")
  exit()
  
a = sys.argv[1]
num = []
first = 0
start = 0

def strtol(lst, s):
  #print(lst, s)
  num = []
  while s < len(lst) and lst[s].isdigit():
    num.append(lst[s])
    s += 1

  return  "".join(num), s

first, start = strtol(a, 0)

print(".intel_syntax noprefix")
print(".globl main")
print("main:")
print(f"  mov rax, ", first)

i = start
while i != len(a):
  if a[i] == "+":
    num, i = strtol(a, i+1)
    print("  add rax, ", num)
  elif a[i] == "-":
    num, i = strtol(a, i+1)
    print("  sub rax, ", num)
  else:
    print("予期しない文字です", i)
    exit()
  
  #break

print(" ret")

'''
for j in range(0,len(a)):
  isBreak = False
  for k in a[0:j]:
    if k in str == False:
      first = a[0:j]
      start = j

for i in range(len(a)):
  if a[i] == "+":
    print("  add rax, ", a[start:i-1])
    start = i + 1
    i += 1
  elif a[i] == "-":
    print(" sub rax, ", a[start:i-1])
    start = i + 1
    i += 1
  else:
    print("予期しない文字です", i)
    exit()

for j in range(0,len(a)):
  if a[j] == "+" or a[j] == "-":
    first = a[0:j-1]
    start = j+1
'''