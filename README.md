# Quarentena de Downloads

Ferramenta pessoal para Windows que vigia a pasta Downloads e move cada arquivo novo para uma pasta de quarentena antes de liberar o acesso.

## Status

- [x] Monitor da pasta Downloads
- [x] Quarentena automática dos arquivos baixados
- [ ] Escaneamento local (ClamAV)
- [ ] Consulta na nuvem (VirusTotal)
- [ ] Liberar ou deletar após o scan

## Como rodar

```
pip install -r requirements.txt
python quarentena.py
```

## Tecnologias

- Python 3.10+
- [watchdog](https://pypi.org/project/watchdog/)
