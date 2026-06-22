"""Pequena demonstração manual da interpretação local de comandos."""

from intencao import interpretar_local


if __name__ == "__main__":
    for comando in ("pesquise Python", "abra o bloco de notas", "crie arquivo ideias"):
        print(f"{comando!r} -> {interpretar_local(comando)}")
