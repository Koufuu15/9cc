import sys
import parser
import user_input

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