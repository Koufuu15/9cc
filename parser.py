from enum import Enum

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