import parser
import utils
from user_input import user_input

class Token:

  def __init__(self, kind, cur, index, length=1): #コンストラクタ
    self.kind = kind # =TokenKind
    self.index = index  # self.index：クラス変数　index：引数
    if cur is not None:
       cur.tsugi = self
    # curがNoneなら次の値が分からないのでnextも放っておく
    
    self.length = length

  def expect_number(self):
    #(self.tsugi, suuchi)
    if self.kind != parser.TokenKind.TK_NUM:
      utils.error_at("数ではありません", self.index)
    return (self.tsugi, self.val)
    #次のトークンも戻り値として返す
  
  def at_eof(self):
    return self.kind == parser.TokenKind.TK_EOF
  
  # 文字列が与えられた文字列と一致するかどうかの判定。フェーズ1なので
  def consume(self, op):
    # ここでself, tsugiを返すとmainがアセンブリの出力だけに集中できる
    if self.kind != parser.TokenKind.TK_RESERVED or user_input[self.index : self.index+self.length] != op:
      return (self, False)
    else:
      return (self.tsugi, True)
  
  # 
  def expect(self, op):
    if self.kind != parser.TokenKind.TK_RESERVED or user_input[self.index : self.index+self.length] != op:
      utils.error_at(f"{op}ではありません", self.index) #エラーを出す
    
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
    # 比較の演算子が使われている場合
    elif user_input[i] in "!=<>":
      # 二文字分の場合がある
      match user_input[i : i + 2]:
        case "==" | "!=" | "<=" | ">=":
          cur = Token(parser.TokenKind.TK_RESERVED, cur, i, 2)
          i += 2
        case _:
          # 一文字
          if user_input[i] == ">" or user_input[i] == "<":
            cur = Token(parser.TokenKind.TK_RESERVED, cur, i)
            i += 1
          else:
            # 現時点で'!', '='に対応する文法が存在しないため棄却しておく
            utils.error_at("不明なトークンです", i)
    elif user_input[i] in "+-*/()":
      cur = Token(parser.TokenKind.TK_RESERVED, cur, i)
      #code[i]は＋かーかを見る文だからi+1じゃない
      i += 1
    elif user_input[i].isdigit():
      cur = Token(parser.TokenKind.TK_NUM, cur, i)
      cur.val, i =  utils.strtol(user_input, i)
    else:
      utils.error_at("トークナイズできません", i)
  
  #EOFは意味がないのでNoneを渡す
  Token(parser.TokenKind.TK_EOF, cur, None)
  return head.tsugi

"""
elif user_input[index] in "!=<>":
            # 二文字分の場合がある
            match user_input[index : index + 2]:
                case "==" | "!=" | "<=" | ">=":
                    cur = Token(TokenKind.TK_RESERVED, cur, index, 2)
                    index += 2
                case _:
                    # 一文字
                    if user_input[index] == ">" or user_input[index] == "<":
                        cur = Token(TokenKind.TK_RESERVED, cur, index)
                        index += 1
                    else:
                        # 現時点で'!', '='に対応する文法が存在しないため棄却しておく
                        error_at("不明なトークンです", index)
"""
