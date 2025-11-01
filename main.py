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

class NodeKind(Enum):
  ND_ADD = 1
  ND_SUB = 2
  ND_MUL = 3
  ND_DIV = 4
  ND_NUM = 5

# コンストラクタを1つに統合　～self に情報を詰めているため、returnが要らない
class Node:
  def __init__(self, kind, lhs, rhs, val):
    self.kind = kind
    if kind == NodeKind.ND_NUM:
      self.val = val
    else:
      self.lhs = lhs
      self.rhs = rhs

def expr(cur):
  node, cur = mul(cur)

  while True:
    cur, bln = cur.consume('+')
    if bln:
      # mulは返り値が２つあるので引数にできない
      rhs, cur = mul(cur)
      # 現在見ているノードが演算子なら、必ずその右(rhs)にはノードがある
      node = Node(NodeKind.ND_ADD, node, rhs, None)
      continue
    
    # consumeは返り値が２つあるので直接引数にできない
    cur, bln = cur.consume('-')
    if bln:
      rhs, cur = mul(cur)
      node = Node(NodeKind.ND_SUB, node, rhs, None)
      continue
    return [node, cur]
      
def mul(cur):
  node, cur = unary(cur)

  while True:
    cur, bln = cur.consume('*')
    if bln:
      rhs, cur = unary(cur)
      node = Node(NodeKind.ND_MUL, node, rhs, None)
      continue
    
    cur, bln = cur.consume('/')
    if bln:
      rhs, cur = unary(cur)
      node = Node(NodeKind.ND_DIV, node, rhs, None)
      continue
    return [node, cur]
      
def primary(cur):
  cur, bln = cur.consume('(')
  if bln:
    node, cur = expr(cur)
    cur = cur.expect(')')
    return [node, cur]
  else:
    cur, val = cur.expect_number()
    # 数字のノードを作る。左辺と右辺はなし。
    node = Node(NodeKind.ND_NUM, None, None, val)
    return [node, cur]

def unary(cur):
  cur, bln = cur.consume('+')
  if bln:
    node, cur = primary(cur)
    return [node, cur]
  
  # 次に見るべきトークン cur 上書きすればずっと見とけばいい
  cur, bln = cur.consume('-')
  if bln:
    node, cur = primary(cur)
    zero = Node(NodeKind.ND_NUM, None, None, 0)
    node = Node(NodeKind.ND_SUB, zero, node, cur)
    return [node, cur]
  
  #  return [node, cur] unaryをスキップ
  return primary(cur)

class Token:

  def __init__(self, kind, cur, index): #コンストラクタ
    self.kind = kind # =TokenKind
    self.index = index  # self.index：クラス変数　index：引数
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
    elif user_input[i] in "+-*/()":
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

def gen(node):
  if node.kind == NodeKind.ND_NUM:
    print(" push", node.val)
    return
  
  # 右辺と左辺が計算済みなら計算できる
  gen(node.lhs)
  gen(node.rhs)

  # main関数のアセンブリなのでインデントが入る。
  print(" pop rdi")
  print(" pop rax")

  match node.kind:
    case NodeKind.ND_ADD:
      print(" add rax, rdi")
    case NodeKind.ND_SUB:
      print(" sub rax, rdi")
    case NodeKind.ND_MUL:
      print(" imul rax, rdi")
    case NodeKind.ND_DIV:
      print(" cqo")
      print(" idiv rax, rdi")
  
  print(" push rax")

def strtol(lst, s):
  #print(lst, s)
  num = []
  while s < len(lst) and lst[s].isdigit():
    num.append(lst[s])
    s += 1

  return  "".join(num), s

# 入力値をグローバル変数に
user_input = sys.argv[1]
num = []

def main():
  if len(sys.argv) <= 1:
    print("引数の個数が足りません。")
    exit()
  
  token = tokenize()
  node, _ = expr(token)

  print(".intel_syntax noprefix")
  print(".globl main")
  print("main:")

  gen(node)

  print(" pop rax")
  print(" ret")

if __name__ == "__main__":
  main()