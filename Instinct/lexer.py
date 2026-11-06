class Token:
    def __init__(self, _type, value=None) -> None:
        self.type = _type
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}({self.value})"
        return f"{self.type}"

#comment

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = ""
        self.advance()

        self.lex()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
    def peek(self):
        return self.text[self.pos+1] if self.pos+1 < len(self.text) else None

    def lex(self):
        tokens = []

        while self.current_char != None:
            if self.current_char == "+":
                pass

            if self.current_char == "-":
                pass

            if self.current_char == "*":
                pass

            if self.current_char == "/":
                if peek()=="/":
                    tokens.append(Token("SLASH"))
                pass

            if self.current_char == "":
                pass

            if self.current_char == "":
                pass

            if self.current_char == "":
                pass

            if self.current_char == "":
                pass

            if self.current_char == "":
                pass

            if self.current_char == "":
                pass

            if self.current_char == "":
                pass

            if self.current_char == "":
                pass

            if self.current_char == "":
                pass

        return tokens
