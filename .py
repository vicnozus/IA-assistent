def caca_palavras(comando):
    comando = comando.lower().strip()
    palavras_proibida = ["droga", "droguinha", "rapazzzzz", "dolinho", "danonão"]
    palavras_boas = ["bom", "fusca", "balinha", "guarana"]

    if any(p in comando for p in palavras_proibida):
        print("me ta o fora daqui, ta ligado mermão")

    elif any(p in comando for p in palavras_boas):
        print("agora sim eu curti")

    else:
        print("eu vou dar o fora ta ligado")

nem_te_conto = input("diz ai parça, como ta?\n> ")

caca_palavras(nem_te_conto)