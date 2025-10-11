import sys
from enum import Enum
#a = sys.stdin.read()

def error(er_msg):
  print(er_msg, file=sys.stderr) #ファイルを指定して書きこむ＝エラーとして出力
  exit(1)

class TokenKind(Enum):
  TK_RESERVED = 1 #記号
  TK_NUM = 2 #整数トークン
  TK_EOF = 3 #入力の終わりを表すトークン

class Token:

  def __init__(self, kind, cur, string): #コンストラクタ
    self.kind = kind # =TokenKind
    self.string = string
    if cur is not None:
       cur.tsugi = self
    # curがNoneなら次の値が分からないのでnextも放っておく

  def expect_number(self):
    #(self.tsugi, suuchi)
    if self.kind != TokenKind.TK_NUM:
      error("数ではありません")
    return (self.tsugi, self.val)
    #次のトークンも戻り値として返す
  
  def at_eof(self):
    return self.kind == TokenKind.TK_EOF
  
  # 文字列が与えられた文字列と一致するかどうかの判定。フェーズ1なので
  def consume(self, op):
    # ここでself, tsugiを返すとmainがアセンブリの出力だけに集中できる
    if self.kind != TokenKind.TK_RESERVED or self.string != op:
      return (self, False)
    else:
      return (self.tsugi, True)
  
  # 
  def expect(self, op):
    if self.kind != TokenKind.TK_RESERVED or self.string != op:
      error(f"{op}ではありません") #エラーを出す
    
    # Trueだとわかってるので不要、次のトークン
    return (self.tsugi)
  
def tokenize(code):
  #ダミーノード
  head = Token(None, None, None)
  cur = head 

  i = 0
  while i != len(code):
    if code[i] == " ":
      i += 1
    elif code[i] == "+" or code[i] == "-":
      cur = Token(TokenKind.TK_RESERVED, cur, code[i])
      #code[i]は＋かーかを見る文だからi+1じゃない
      i += 1
    elif code[i].isdigit():
      cur = Token(TokenKind.TK_NUM, cur, code[i])
      cur.val, i =  strtol(code, i)
    else:
      error("トークナイズできません")
  
  #EOFは意味がないのでNoneを渡す
  Token(TokenKind.TK_EOF, cur, None)
  return head.tsugi

if len(sys.argv) <= 1:
  print("引数の個数が足りません。")
  exit()
  
a = sys.argv[1]
num = []


def strtol(lst, s):
  #print(lst, s)
  num = []
  while s < len(lst) and lst[s].isdigit():
    num.append(lst[s])
    s += 1

  return  "".join(num), s

token = tokenize(a)

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