import sys
from enum import Enum
#a = sys.stdin.read()

global user_input

def error_at(er_msg, pos):
  print(user_input, file=sys.stderr)
  print(" " * pos + "^ " + er_msg, file=sys.stderr) #ファイルを指定して書きこむ＝エラーとして出力
  exit(1)

class TokenKind(Enum):
  TK_RESERVED = 1 #記号
  TK_NUM = 2 #整数トークン
  TK_EOF = 3 #入力の終わりを表すトークン

class Token:

  def __init__(self, kind, cur, index): #コンストラクタ
    self.kind = kind # =TokenKind
    self.index = index
    if cur is not None:
       cur.tsugi = self
    # curがNoneなら次の値が分からないのでnextも放っておく

  def expect_number(self):
    #(self.tsugi, suuchi)
    if self.kind != TokenKind.TK_NUM:
      error_at("数ではありません", self.index)
    return (self.tsugi, self.val)
    #次のトークンも戻り値として返す
  
  def at_eof(self):
    return self.kind == TokenKind.TK_EOF
  
  # 文字列が与えられた文字列と一致するかどうかの判定。フェーズ1なので
  def consume(self, op):
    # ここでself, tsugiを返すとmainがアセンブリの出力だけに集中できる
    if self.kind != TokenKind.TK_RESERVED or user_input[self.index] != op:
      return (self, False)
    else:
      return (self.tsugi, True)
  
  # 
  def expect(self, op):
    if self.kind != TokenKind.TK_RESERVED or user_input[self.index] != op:
      error_at(f"{op}ではありません", self.index) #エラーを出す
    
    # Trueだとわかってるので不要、次のトークン
    return (self.tsugi)
  
def tokenize():
  global user_input
  #ダミーノード
  head = Token(None, None, None)
  cur = head 

  i = 0
  while i != len(user_input):
    if user_input[i] == " ":
      i += 1
    elif user_input[i] == "+" or user_input[i] == "-":
      cur = Token(TokenKind.TK_RESERVED, cur, i)
      #code[i]は＋かーかを見る文だからi+1じゃない
      i += 1
    elif user_input[i].isdigit():
      cur = Token(TokenKind.TK_NUM, cur, i)
      cur.val, i =  strtol(user_input, i)
    else:
      error_at("トークナイズできません", i)
  
  #EOFは意味がないのでNoneを渡す
  Token(TokenKind.TK_EOF, cur, None)
  return head.tsugi

if len(sys.argv) <= 1:
  print("引数の個数が足りません。")
  exit()
  
# 入力値をグローバル変数に
user_input = sys.argv[1]
num = []


def strtol(lst, s):
  #print(lst, s)
  num = []
  while s < len(lst) and lst[s].isdigit():
    num.append(lst[s])
    s += 1

  return  "".join(num), s

token = tokenize()

print(".intel_syntax noprefix")
print(".globl main")
print("main:")
token , j = token.expect_number()
print("  mov rax,", j)

while (not token.at_eof()):
  # +かどうか
  token, bln = token.consume("+")
  if bln:
    token , j = token.expect_number()
    print("  add rax, ", j)
    continue #次のループへ
  
  token = token.expect("-")
  token , j = token.expect_number()
  print("  sub rax, ", j)

print(" ret")