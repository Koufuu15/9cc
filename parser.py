from enum import Enum
import parser
import tokenizer

lvar = {}

class NodeKind(Enum):
  ND_ADD = 1
  ND_SUB = 2
  ND_MUL = 3
  ND_DIV = 4
  ND_ASSIGN = 5  #lhsにrhsを代入する式
  ND_LVAR = 6  #変数
  ND_EQ = 7
  ND_NE = 8
  ND_LT = 9
  ND_LE = 10
  ND_NUM = 11
  ND_RETURN = 12
  ND_IF = 13

# コンストラクタを1つに統合　～self に情報を詰めているため、returnが要らない
class Node:
  def __init__(self, kind, nodes, val):
    self.kind = kind
    if kind == NodeKind.ND_NUM:
      self.val = val
    elif kind == NodeKind.ND_LVAR:
      self.offset = val
    elif kind == NodeKind.ND_RETURN:
      #ここで変数宣言できる
      self.lhs = nodes
    elif kind == NodeKind.ND_IF:
      self.cand, self.if_block, self.else_block = nodes 
    else:
      self.lhs, self.rhs = nodes

def program(cur):
  code = []
  while(not cur.at_eof()):
    node, cur = stmt(cur)
    code.append(node)
  return code

def stmt(cur):  
  #returnなら
  cur, bln = cur.consume_tokenKind(tokenizer.TokenKind.TK_RETURN)
  if bln:
    node, cur = expr(cur)
    node = parser.Node(parser.NodeKind.ND_RETURN, node, None)
    cur = cur.expect(";")
    return [node, cur]
  
  #ifなら
  cur, bln = cur.consume_tokenKind(tokenizer.TokenKind.TK_IF)
  if bln:
    cur = cur.expect("(")
    cand, cur = expr(cur)
    cur = cur.expect(")")
    if_block, cur = stmt(cur)
    #print(if_block)
    
    cur, bln = cur.consume_tokenKind(tokenizer.TokenKind.TK_ELSE)
    if bln:
      else_block, cur = stmt(cur)
    else:
      else_block = None
      
    node = parser.Node(parser.NodeKind.ND_IF, [cand, if_block, else_block], None)
    return [node, cur]
  
  node, cur = expr(cur)
  cur = cur.expect(";")
  return [node, cur]

def expr(cur):
  node, cur = assign(cur)
  return [node, cur]


def assign(cur):
  node, cur = equality(cur)

  cur, bln = cur.consume("=")
  if bln:
    rhs, cur = assign(cur)
    node = parser.Node(parser.NodeKind.ND_ASSIGN, [node, rhs], None)
  
  return [node, cur]
      

def equality(cur):
  node, cur = relational(cur)
  
  while True:
    cur, bln = cur.consume("==")
    if bln:
      rhs, cur = relational(cur)
      node = parser.Node(parser.NodeKind.ND_EQ, [node, rhs], None)
      continue
    
    cur, bln = cur.consume("!=")
    if bln:
      rhs, cur = relational(cur)
      node = parser.Node(parser.NodeKind.ND_NE, [node, rhs], None)
      continue

    return [node, cur]


def relational(cur):
  node, cur = add(cur)
  while True:
    cur, bln = cur.consume("<")
    if bln:
      rhs, cur = add(cur)
      node = parser.Node(parser.NodeKind.ND_LT, [node, rhs], None)
      continue
    
    cur, bln = cur.consume("<=")
    if bln:
      rhs, cur = add(cur)
      node = parser.Node(parser.NodeKind.ND_LE, [node, rhs], None)
      continue

    cur, bln = cur.consume(">")
    if bln:
      lhs, cur = add(cur)
      node = parser.Node(parser.NodeKind.ND_LT, [lhs, node], None)
      continue
    
    cur, bln = cur.consume(">=")
    if bln:
      lhs, cur = add(cur)
      node = parser.Node(parser.NodeKind.ND_LE, [lhs, node], None)
      continue
  
    return [node, cur]


def add(cur):
  node, cur = mul(cur)
  while True:
    cur, bln = cur.consume("+")
    if bln:
      rhs, cur = mul(cur)
      node = parser.Node(parser.NodeKind.ND_ADD, [node, rhs], None)
      continue
    
    cur, bln = cur.consume("-")
    if bln:
      rhs, cur = mul(cur)
      node = parser.Node(parser.NodeKind.ND_SUB, [node, rhs], None)
      continue
    
    return [node, cur]
  

def mul(cur):
  node, cur = unary(cur)

  while True:
    cur, bln = cur.consume('*')
    if bln:
      rhs, cur = unary(cur)
      node = parser.Node(parser.NodeKind.ND_MUL, [node, rhs], None)
      continue
    
    cur, bln = cur.consume('/')
    if bln:
      rhs, cur = unary(cur)
      node = parser.Node(parser.NodeKind.ND_DIV, [node, rhs], None)
      continue
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
    zero = parser.Node(parser.NodeKind.ND_NUM, [None, None], 0)
    node = parser.Node(parser.NodeKind.ND_SUB, [zero, node], cur)
    return [node, cur]
  
  #  return [node, cur] unaryをスキップ
  return primary(cur)


def primary(cur):
  cur, bln = cur.consume('(')
  if bln:
    node, cur = expr(cur)
    cur = cur.expect(')')
    return [node, cur]
  
  cur, bln, varname = cur.consume_ident()
  if bln:
    if varname not in lvar:
      lvar[varname] = (len(lvar) + 1) * 8
    node = parser.Node(parser.NodeKind.ND_LVAR, [varname, None], lvar[varname])
    return [node, cur]

  cur, val = cur.expect_number()
  # 数字のノードを作る。左辺と右辺はなし。
  node = parser.Node(parser.NodeKind.ND_NUM, [None, None], val)
  return [node, cur]