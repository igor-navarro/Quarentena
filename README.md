# Quarentena

Ferramenta pessoal para Windows que vigia a pasta Downloads e move cada arquivo novo para uma pasta de quarentena antes de liberar o acesso. Cada arquivo recebe um hash SHA-256, base para a consulta futura em serviços de reputação como o VirusTotal, e tudo o que acontece é registrado em um log.

## Status

- [x] Monitor da pasta Downloads
- [x] Quarentena automática dos arquivos baixados
- [x] Listar, liberar e deletar arquivos da quarentena
- [x] Hash SHA-256 de cada arquivo
- [x] Log em arquivo de tudo que entra, sai ou é apagado da quarentena
- [ ] Consulta na nuvem (VirusTotal)
- [ ] Escaneamento local (ClamAV)
- [ ] Liberar automaticamente após o scan

## Como rodar

1. Instale as dependências:

```
pip install -r requirements.txt
```

2. Inicie o monitor:

```
python quarentena.py
```

Enquanto ele estiver rodando, todo arquivo que terminar de ser baixado em `Downloads` é movido para `C:\Users\<usuario>\Quarentena`.

## Gerenciar a quarentena

Em outro terminal, enquanto o monitor roda (ou com ele parado):

```
python gerenciar.py listar
python gerenciar.py liberar nome_do_arquivo.zip
python gerenciar.py deletar nome_do_arquivo.zip
```

- `listar` mostra nome, tamanho e SHA-256 de cada arquivo em quarentena.
- `liberar` move o arquivo para `Downloads\Liberados`.
- `deletar` apaga o arquivo para sempre, depois de pedir confirmação.

Se o nome tiver espaços, use aspas: `python gerenciar.py liberar "meu arquivo.zip"`.

## Por que os arquivos liberados vão para Downloads\Liberados?

O monitor vigia a raiz da pasta Downloads. Se o arquivo fosse devolvido direto para lá, ele seria capturado de novo e voltaria para a quarentena, num ciclo infinito. Na subpasta `Liberados` isso não acontece.

## Por que SHA-256?

O hash funciona como uma impressão digital do arquivo: qualquer alteração, mesmo de um byte, gera um hash totalmente diferente. Serviços como o VirusTotal identificam arquivos por esse valor, então dá para consultar a reputação de um arquivo sem precisar enviá-lo. O programa lê o arquivo em blocos de 1 MB, então funciona bem mesmo com arquivos grandes.

## Log

Tudo que acontece é registrado em `quarentena.log`, na pasta do projeto, com data e hora:

```
2026-10-26 21:12:57 | Em quarentena: relatorio.pdf | 52310 bytes | SHA-256: 9f86d0...
2026-10-26 21:13:18 | Liberado: relatorio.pdf -> C:\Users\...\Downloads\Liberados\relatorio.pdf
2026-10-26 21:14:02 | Apagado: instalador.exe
```

O arquivo de log não é enviado para o GitHub (está no `.gitignore`), porque contém os nomes dos arquivos baixados.

## Estrutura do projeto

```
Quarentena/
├── quarentena.py     # monitor de downloads (quarentena, hash e log)
├── gerenciar.py      # comandos listar, liberar e deletar
├── requirements.txt  # dependências
├── README.md         # documentação
└── .gitignore        # ignora venv, cache e logs
```

## Tecnologias

- Python 3.10+
- [watchdog](https://pypi.org/project/watchdog/)
- hashlib, logging e argparse (biblioteca padrão)
