# CONTRIBUIÇÃO

Obrigado por considerar contribuir com o meu projeto Pythoncraft! Este documento explica como o projeto está organizado, os padrões que seguimos e como submeter sua contribuição da forma certa.

## Índice
 
- [Pré-requisitos](#pré-requisitos)
- [Como contribuir](#como-contribuir)
- [Padrões de código](#padrões-de-código)
- [Commits e Pull Requests](#commits-e-pull-requests)
- [Reportando bugs](#reportando-bugs)

## Pré-requisitos
 
- Python **3.10+**
- pip
- Git

## Como contribuir
 
1. **Abra uma issue** antes de começar qualquer coisa grande — discuta a ideia primeiro.
2. **Faça um fork** do repositório e crie uma branch descritiva:
   ```bash
   git checkout -b feature/sistema-de-crafting
   git checkout -b fix/colisao-blocos-superficie
   ```
3. Faça suas alterações seguindo os padrões abaixo.
4. Teste rodando `python main.py` e confirme que nada quebrou.
5. Abra um **Pull Request** com uma descrição clara do que foi feito e por quê.

## Padrões de código
 
- **Idioma do código:** inglês para nomes de variáveis, funções e classes; português para comentários, docstrings e mensagens ao jogador.
- **Tipagem:** use type hints sempre que possível (`def get_block(id: str) -> Block`).
- **Sem dependências extras** sem discussão prévia — o projeto se mantém enxuto intencionalmente.
- Siga o estilo já estabelecido nos módulos existentes: funções de registro (`register_*`), funções de carregamento (`load_all_*`) e getters (`get_*`).

## Commits e Pull Requests
 
Use mensagens de commit curtas e em português:
 
```
feat: adiciona bloco de areia com física
fix: corrige colisão na borda dos chunks
refactor: separa lógica de chunk em core/chunk.py
assets: adiciona textura de madeira de bétula
docs: atualiza CONTRIBUTING com fluxo de entidades
```
 
PRs pequenos e focados são mais fáceis de revisar. Evite misturar features e fixes no mesmo PR.

## Reportando bugs
 
Abra uma issue com:
 
- **O que aconteceu** (comportamento atual)
- **O que deveria acontecer** (comportamento esperado)
- **Como reproduzir** (passo a passo)
- **Versão do Python e sistema operacional**