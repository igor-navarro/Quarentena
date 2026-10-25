# Quarentena

Ferramenta pessoal para Windows que vigia a pasta Downloads e move cada arquivo novo para uma pasta de quarentena antes de liberar o acesso. Cada arquivo recebe um hash SHA-256, base para a consulta futura em serviços de reputação como o VirusTotal.

## Status

- [x] Monitor da pasta Downloads
- [x] Quarentena automática dos arquivos baixados
- [x] Listar, liberar e deletar arquivos da quarentena
- [x] Hash SHA-256 de cada arquivo
- [ ] Consulta na nuvem (VirusTotal)
- [ ] Escaneamento local (ClamAV)
- [ ] Liberar automaticamente após o scan

## Como rodar

```
pip install -r requirements.txt
python quarentena.py
```

## Gerenciar a quarentena

Em outro terminal, enquanto o monitor roda (ou com ele parado):

```
python gerenciar.py listar
python gerenciar.py liberar nome_do_arquivo.zip
python gerenciar.py deletar nome_do_arquivo.zip
```

O `listar` mostra nome, tamanho e SHA-256 de cada arquivo. Arquivos liberados vão para `Downloads\Liberados`.

## Por que SHA-256?

O hash funciona como uma impressão digital do arquivo: qualquer alteração, mesmo de um byte, gera um hash totalmente diferente. Serviços como o VirusTotal identificam arquivos por esse valor, então dá para consultar a reputação de um arquivo sem precisar enviá-lo. O programa lê o arquivo em blocos de 1 MB, então funciona bem mesmo com arquivos grandes.

## Tecnologias

- Python 3.10+
- [watchdog](https://pypi.org/project/watchdog/)
- hashlib (biblioteca padrão)
