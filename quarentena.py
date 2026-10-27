import hashlib
import logging
import shutil
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

DOWNLOADS = Path.home() / "Downloads"
QUARENTENA = Path.home() / "Quarentena"
# o log fica na pasta do projeto, fora da quarentena (senão apareceria no "listar")
LOG = Path(__file__).parent / "quarentena.log"
# extensões de arquivos que ainda estão sendo baixados
IGNORAR = {".crdownload", ".part", ".tmp", ".download"}


def configurar_log() -> None:
    """Mostra as mensagens no terminal e grava todas no quarentena.log."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG, encoding="utf-8", delay=True),
        ],
    )


def calcular_sha256(caminho: Path) -> str:
    """Calcula o hash SHA-256 lendo o arquivo em blocos (funciona com arquivos grandes)."""
    sha256 = hashlib.sha256()
    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            sha256.update(bloco)
    return sha256.hexdigest()


def download_terminou(caminho: Path, tentativas: int = 30, intervalo: float = 1.0) -> bool:
    """Espera o tamanho do arquivo parar de mudar (sinal de que o download acabou)."""
    tamanho_anterior = -1
    for _ in range(tentativas):
        try:
            tamanho = caminho.stat().st_size
        except FileNotFoundError:
            return False
        if tamanho == tamanho_anterior:
            return True
        tamanho_anterior = tamanho
        time.sleep(intervalo)
    return False


def destino_unico(destino: Path) -> Path:
    """Evita sobrescrever: arquivo.zip -> arquivo (1).zip"""
    contador = 1
    novo = destino
    while novo.exists():
        novo = destino.with_name(f"{destino.stem} ({contador}){destino.suffix}")
        contador += 1
    return novo


class MonitorDownloads(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.processar(Path(event.src_path))

    def on_moved(self, event):
        # navegadores baixam como .crdownload e depois renomeiam
        if not event.is_directory:
            self.processar(Path(event.dest_path))

    def processar(self, caminho: Path) -> None:
        if caminho.suffix.lower() in IGNORAR:
            return
        if not download_terminou(caminho):
            logging.warning(f"Não consegui confirmar o fim do download: {caminho.name}")
            return

        destino = destino_unico(QUARENTENA / caminho.name)
        try:
            shutil.move(str(caminho), str(destino))
        except OSError as erro:
            logging.warning(f"Erro ao mover {caminho.name}: {erro}")
            return

        try:
            tamanho = destino.stat().st_size
            hash_arquivo = calcular_sha256(destino)
        except OSError as erro:
            logging.warning(f"Em quarentena: {destino.name} | não consegui calcular o hash: {erro}")
            return

        logging.info(f"Em quarentena: {destino.name} | {tamanho} bytes | SHA-256: {hash_arquivo}")


if __name__ == "__main__":
    configurar_log()
    QUARENTENA.mkdir(exist_ok=True)

    observer = Observer()
    observer.schedule(MonitorDownloads(), str(DOWNLOADS), recursive=False)
    observer.start()
    logging.info(f"Monitor iniciado em {DOWNLOADS} (Ctrl+C para parar)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Monitor encerrado")
    observer.join()