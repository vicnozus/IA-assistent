msg = input("Digite seu comando: ")

if msg.startswith("http"):
    print("Isso parece um link, vou abrir no navegador!")
elif msg.startswith("pesquisar"):
    print("Isso é uma busca, vou formatar o texto primeiro.")
else:
    print("Não entendi o que você quer fazer.")