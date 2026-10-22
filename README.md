# Quarentena

Ferramenta pessoal para Windows que vigia a pasta Downloads e move cada arquivo novo para uma pasta de quarentena antes de liberar o acesso.

## Status

- [x] Monitor da pasta Downloads
- [x] Quarentena automática dos arquivos baixados
- [x] Listar, liberar e deletar arquivos da quarentena
- [ ] Escaneamento local (ClamAV)
- [ ] Consulta na nuvem (VirusTotal)
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

Arquivos liberados vão para `Downloads\Liberados`.

## Tecnologias

- Python 3.10+
- [watchdog](https://pypi.org/project/watchdog/)
