import argparse
import logging
import shutil
from pathlib import Path

from quarentena import DOWNLOADS, QUARENTENA, calcular_sha256, configurar_log, destino_unico

# fora da raiz de Downloads, para o monitor não pegar o arquivo de novo
LIBERADOS = DOWNLOADS / "Liberados"


def listar_arquivos() -> list[Path]:
    if not QUARENTENA.exists():
        return []
    return sorted(p for p in QUARENTENA.iterdir() if p.is_file())


def achar(nome: str) -> Path | None:
    caminho = QUARENTENA / nome
    # segurança: o arquivo precisa estar direto dentro da quarentena
    if caminho.resolve().parent != QUARENTENA.resolve() or not caminho.is_file():
        print(f"Arquivo não encontrado na quarentena: {nome}")
        return None
    return caminho


def listar() -> None:
    arquivos = listar_arquivos()
    if not arquivos:
        print("Quarentena vazia.")
        return
    for i, arquivo in enumerate(arquivos, start=1):
        kb = arquivo.stat().st_size / 1024
        print(f"{i}. {arquivo.name} ({kb:.1f} KB)")
        try:
            print(f"   SHA-256: {calcular_sha256(arquivo)}")
        except OSError as erro:
            print(f"   Não consegui calcular o hash: {erro}")


def liberar(nome: str) -> None:
    arquivo = achar(nome)
    if not arquivo:
        return
    LIBERADOS.mkdir(exist_ok=True)
    destino = destino_unico(LIBERADOS / arquivo.name)
    shutil.move(str(arquivo), str(destino))
    logging.info(f"Liberado: {arquivo.name} -> {destino}")


def deletar(nome: str) -> None:
    arquivo = achar(nome)
    if not arquivo:
        return
    resposta = input(f"Apagar '{arquivo.name}' para sempre? (s/n): ")
    if resposta.strip().lower() != "s":
        print("Cancelado.")
        return
    arquivo.unlink()
    logging.info(f"Apagado: {arquivo.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerencia a quarentena de downloads")
    sub = parser.add_subparsers(dest="comando", required=True)

    sub.add_parser("listar", help="lista os arquivos em quarentena com o hash SHA-256")

    p_liberar = sub.add_parser("liberar", help="move o arquivo para Downloads\\Liberados")
    p_liberar.add_argument("nome", help="nome do arquivo (use aspas se tiver espaços)")

    p_deletar = sub.add_parser("deletar", help="apaga o arquivo da quarentena")
    p_deletar.add_argument("nome", help="nome do arquivo (use aspas se tiver espaços)")

    args = parser.parse_args()
    configurar_log()

    if args.comando == "listar":
        listar()
    elif args.comando == "liberar":
        liberar(args.nome)
    elif args.comando == "deletar":
        deletar(args.nome)


if __name__ == "__main__":
    main()