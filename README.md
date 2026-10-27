# vigia-de-arquivos

Roda um comando toda vez que um arquivo muda, só com stdlib

Código do carrossel publicado no [@python_brasil](https://instagram.com/python_brasil).

## Como rodar

```bash
python main.py --help
```

```bash
python main.py "pytest -q"
python main.py "python app.py" --pasta src --ext .py .html
```

## O que este código NÃO faz

- varre a pasta a cada intervalo; em projeto com dezenas de milhares de arquivos, prefira o `watchdog`
- não observa alteração de permissão, só de conteúdo e data

---

Feito pela comunidade [@python_brasil](https://instagram.com/python_brasil).
