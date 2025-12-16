import parser
import utils

def gen_lval(node):
  assert node.kind == parser.NodeKind.ND_LVAR, "代入の左辺値が変数ではありません"

  print(" mov rax, rbp")
  print(" sub rax,", node.offset)
  print(" push rax") 

def gen(node):
  # 上のmatchは1つの数字を受け取って１つの数字を返す、それより下は２つオペランドがあるときの処理
  # 引数が１つ：下の処理は行わないため、returnで関数を抜けだす
  match node.kind:
    case parser.NodeKind.ND_NUM:
      print(" push", node.val)
      return
    case parser.NodeKind.ND_LVAR:
      gen_lval(node)
      print(" pop rax")
      print(" mov rax, [rax]")
      print(" push rax")
      return
    case parser.NodeKind.ND_ASSIGN:
      gen_lval(node.lhs)
      gen(node.rhs)
      print(" pop rdi")
      print(" pop rax")
      print(" mov [rax], rdi")
      print(" push rdi")
      return
    case parser.NodeKind.ND_RETURN:
      gen(node.lhs)
      print(" pop rax")
      print(" mov rsp, rbp")
      print(" pop rbp")
      print(" ret")
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
