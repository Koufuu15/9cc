import parser

def gen(node):
  if node.kind == parser.NodeKind.ND_NUM:
    print(" push", node.val)
    return
  
  # 右辺と左辺が計算済みなら計算できる
  gen(node.lhs)
  gen(node.rhs)

  # main関数のアセンブリなのでインデントが入る。
  print(" pop rdi")
  print(" pop rax")

  match node.kind:
    case parser.NodeKind.ND_ADD:
      print(" add rax, rdi")
    case parser.NodeKind.ND_SUB:
      print(" sub rax, rdi")
    case parser.NodeKind.ND_MUL:
      print(" imul rax, rdi")
    case parser.NodeKind.ND_DIV:
      print(" cqo")
      print(" idiv rax, rdi")
    case parser.NodeKind.ND_EQ:
      print(" cmp rax, rdi")
      print(" sete al")
      print(" movzb rax, al")
    case parser.NodeKind.ND_NE:
      print(" cmp rax, rdi")
      print(" setne al")
      print(" movzb rax, al")
    case parser.NodeKind.ND_LT:
      print(" cmp rax, rdi")
      print(" setl al")
      print(" movzb rax, al")
    case parser.NodeKind.ND_LE:
      print(" cmp rax, rdi")
      print(" setle al")
      print(" movzb rax, al")
  
  print(" push rax")
