import parser
import utils

label_count = 0

def gen_lval(node):
  assert node.kind == parser.NodeKind.ND_LVAR, "代入の左辺値が変数ではありません"

  print(" mov rax, rbp")
  print(" sub rax,", node.offset)
  print(" push rax") 

def gen(node):
  global label_count #複数回globalを書くとエラーになるのでここで書く
  # 上のmatchは1つの数字を受け取って１つの数字を返す、それより下は２つオペランドがあるときの処理
  # 引数が１つ：下の処理は行わないため、returnで関数を抜けだす
  #print(node)
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
    case parser.NodeKind.ND_IF:
      gen(node.cand)
      print(" pop rax")
      print(" cmp rax, 0")
      label_now = label_count
      label_count += 1
      
      if node.else_block is not None:
        print(f" je .Lelse{label_now}")
        gen(node.if_block)
        label_count += 1
        print(f" jmp .Lend{label_now}")
        print(f".Lelse{label_now}:")
        gen(node.else_block)
        print(f".Lend{label_now}:")
      else:
        print(f" je .Lend{label_now}")
        gen(node.if_block)
        print(f".Lend{label_now}:")

      print(" push rax")
      return
    case parser.NodeKind.ND_WHILE:
      label_now = label_count
      print(f".Lbegin{label_now}:")
      gen(node.cand)
      print(" pop rax")
      print(" cmp rax, 0")
      print(f" je .Lend{label_now}")
      gen(node.while_block)
      print(f" jmp .Lbegin{label_now}")
      print(f".Lend{label_now}:")
      
      #1つのブロックで１つの値を返さないと壊れるため、raxにpush(=出力)しておく
      print(" push rax")
      return
    case parser.NodeKind.ND_FOR:
      gen(node.expr1)
      label_now = label_count
      print(f".Lbegin{label_now}:")
      gen(node.expr2)
      print(" pop rax")
      print(" cmp rax, 0")
      print(f" je .Lend{label_now}")
      gen(node.for_block)
      gen(node.expr3)
      print(f" jmp .Lbegin{label_now}")
      print(f".Lend{label_now}:")
      print(" push rax")
      return
    case parser.NodeKind.ND_BLOCK:
      for n in node.nodes:
        gen(n)
      print(" push rax")
      return
    case parser.NodeKind.ND_FUNCTION:
      cnt = len(parser.lvar) + utils.pop_cnt - utils.push_cnt
      if cnt % 2 == 1:
        print("sub 8, rsp")

      print(f" call {node.func_name}")

      if cnt % 2 == 1:
        print("add 8, rsp")
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
