# Timbrado Maker

**Timbrado Maker** é uma API desenvolvida em **FastAPI + Python** para gerar **PDFs timbrados automaticamente** a partir de arquivos `.txt`.  
A ferramenta aplica um **modelo de timbrado fixo (PDF base)** sobre o conteúdo recebido e retorna um arquivo final timbrado — ideal para automação de documentos oficiais e padronizados.

---

## Funcionalidades

- Recebe arquivos `.txt` e converte em PDF formatado.  
- Aplica automaticamente o **timbrado padrão** configurado.  
- Retorna o PDF final já timbrado para download.  
- Estrutura modular, fácil de adaptar para outros timbrados e layouts.  
- Desenvolvido com **FastAPI**, pronto para integração com automações (ex: n8n, bots, etc).

---

## Estrutura do Projeto

    Timbrado_Maker/
    │
    ├── api_process.py # Lógica principal de timbragem dos PDFs
    ├── main.py # API FastAPI (endpoints de upload e resposta)
    ├── timbrado/ # Pasta com o modelo de timbrado (timbrado.pdf)
    └── requirements.txt # Dependências do projeto