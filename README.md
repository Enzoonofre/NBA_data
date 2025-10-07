# NBA Data Analysis Project

Este projeto tem como objetivo coletar, processar e analisar dados da NBA através de sua API não oficial, criando um pipeline completo de dados desde a extração até a análise preditiva.

## 📋 Sobre o Projeto

O projeto está em desenvolvimento e atualmente foca nas temporadas de 2010 até 2024 da NBA. O objetivo final é criar um pipeline completo que inclui:

- Extração de dados da API não oficial da NBA sobre cada time
- Armazenamento dos dados em nuvem
- Análise visual dos dados
- Modelos preditivos usando machine learning
- Expansão para múltiplas temporadas

## 🗂️ Estrutura do Projeto

```
NBA_data/
├── app.py          # Página Home dos dados
│
├── pages/          # Páginas web para analise de dados
│   ├── front.py
├── tests/          # Arquivos do Google Colab para testes
│   ├── NBA_colab.ipynb
├── data/                # Dados do projeto
│   ├── raw/            # Dados brutos da API
│   └── processed/      # Dados processados
├── src/                # Código fonte em Python
│   └── main.py         # Arquivo principal para extração dos dados
├── .gitignore          # Arquivo para ignorar variáveis de ambiente e arquivos da IDE
└── requirements.txt    # Dependências do projeto
```

## 🚀 Como Executar

1. Clone o repositório
2. Navegue até a pasta do projeto:
   ```bash
   cd NBA_data
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Extraia os dados da NBA:
   ```bash
   python src/main.py
   ```
5. Execute a análise e visualize os dados no dashboard:
   ```bash
   streamlit run app.py
   ```

## 📊 Funcionalidades Atuais

- [x] Conexão com a API da NBA
- [x] Extração de dados dos times da temporada 2010-2024
- [x] Estrutura inicial para processamento de dados
- [ ] Upload para armazenamento em nuvem
- [x] Dashboard interativo com gráficos e estatísticas
- [ ] Modelos preditivos de machine learning

## 🔮 Próximos Passos

- Implementar pipeline completo de ETL
- Adicionar visualizações de dados
- Desenvolver modelos preditivos
- Expandir análises históricas e insights avançados

## 🤝 Contribuição

Este projeto está em construção. Novas funcionalidades e melhorias serão implementadas gradualmente.
