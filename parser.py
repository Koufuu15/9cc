from enum import Enum
import parser

class TokenKind(Enum):
  TK_RESERVED = 1 #記号
  TK_NUM = 2 #整数トークン
  TK_EOF = 3 #入力の終わりを表すトークン

class NodeKind(Enum):
  ND_ADD = 1
  ND_SUB = 2
  ND_MUL = 3
  ND_DIV = 4
  ND_EQ = 6
  ND_NE = 7
  ND_LT = 8
  ND_LE = 9
  ND_NUM = 10

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
  node, cur = equality(cur)

  while True:
    cur, bln = cur.consume('+')
    if bln:
      # mulは返り値が２つあるので引数にできない
      rhs, cur = equality(cur)
      # 現在見ているノードが演算子なら、必ずその右(rhs)にはノードがある
      node = parser.Node(parser.NodeKind.ND_ADD, node, rhs, None)
      continue
    
    # consumeは返り値が２つあるので直接引数にできない
    cur, bln = cur.consume('-')
    if bln:
      rhs, cur = equality(cur)
      node = parser.Node(parser.NodeKind.ND_SUB, node, rhs, None)
      continue
    return [node, cur]
      
def mul(cur):
  node, cur = unary(cur)

  while True:
    cur, bln = cur.consume('*')
    if bln:
      rhs, cur = unary(cur)
      node = parser.Node(parser.NodeKind.ND_MUL, node, rhs, None)
      continue
    
    cur, bln = cur.consume('/')
    if bln:
      rhs, cur = unary(cur)
      node = parser.Node(parser.NodeKind.ND_DIV, node, rhs, None)
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
    node = parser.Node(parser.NodeKind.ND_NUM, None, None, val)
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
    zero = parser.Node(parser.NodeKind.ND_NUM, None, None, 0)
    node = parser.Node(parser.NodeKind.ND_SUB, zero, node, cur)
    return [node, cur]
  
  #  return [node, cur] unaryをスキップ
  return primary(cur)

def equality(cur):
  node, cur = relational(cur)
  
  while True:
    cur, bln = cur.consume("==")
    if bln:
      rhs, cur = relational(cur)
      node = parser.Node(parser.NodeKind.ND_EQ, node, rhs, None)
      continue
    
    cur, bln = cur.consume("!=")
    if bln:
      rhs, cur = relational(cur)
      node = parser.Node(parser.NodeKind.ND_NE, node, rhs, None)
      continue

    return [node, cur]

def relational(cur):
  node, cur = add(cur)
  while True:
    cur, bln = cur.consume("<")
    if bln:
      rhs, cur = add(cur)
      node = parser.Node(parser.NodeKind.ND_LT, node, rhs, None)
      continue
    
    cur, bln = cur.consume("<=")
    if bln:
      rhs, cur = add(cur)
      node = parser.Node(parser.NodeKind.ND_LE, node, rhs, None)
      continue

    cur, bln = cur.consume(">")
    if bln:
      lhs, cur = add(cur)
      node = parser.Node(parser.NodeKind.ND_LT, lhs, node, None)
      continue
    
    cur, bln = cur.consume(">=")
    if bln:
      lhs, cur = add(cur)
      node = parser.Node(parser.NodeKind.ND_LE, lhs, node, None)
      continue
  
    return [node, cur]

def add(cur):
  node, cur = mul(cur)
  while True:
    cur, bln = cur.consume("+")
    if bln:
      rhs, cur = mul(cur)
      node = parser.Node(parser.NodeKind.ND_ADD, node, rhs, None)
      continue
    
    cur, bln = cur.consume("-")
    if bln:
      rhs, cur = mul(cur)
      node = parser.Node(parser.NodeKind.ND_SUB, node, rhs, None)
      continue
    
    return [node, cur]