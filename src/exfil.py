LETTERS = "0123456789abcdefghijklmnopqrstuvwxyz"


def decode(domain: str) -> bytes:
    # TODO: implement this function
    ...


class Exfil:
    def __init__(self, server: str = "127.0.0.53", port: int = 53):
        self.maxlen = 253

    def encode(self, data: bytes) -> list[str]:
        # 253 bytes max per DNS query
        # some of those bytes are used for `.`s separating the labels
        out = []
        currentQuery = []
        temp = ""
        for idx, char in enumerate(data):
            n = char
            while n:
                n, r = divmod(n, 36)
                temp += LETTERS[r]
                if len(temp) + 1 == 63:
                    currentQuery.append(temp)
                    temp = ""
                    if len(currentQuery) == 4:
                        out.append(".".join(currentQuery))
                        currentQuery = []
                    elif len(currentQuery) > 4:
                        print(f"{currentQuery= }")
                        raise ValueError("Too many labels!")
                elif len(temp) + 1 > 63:
                    print(f"{temp= }")
                    print(f"{len(temp)= }")
                    print(f"{char= }")
                    print(f"{idx= }")
                    raise ValueError("Data too long!")
        # cleanup leftovers
        if temp:
            currentQuery.append(temp)
        if currentQuery:
            out.append(".".join(currentQuery))

        return out

    def exfil(self, server, port): ...


if __name__ == "__main__":
    with open("data/example.txt", "rb") as f:
        data = f.read()

    exfil = Exfil()
    encoded = exfil.encode(data)
    print(encoded)
    for query in encoded:
        print(decode(query))
