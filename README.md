# Steam Top 1000: Análise de Dados

Análise exploratória dos **1000 jogos mais bem avaliados da Steam**, cobrindo todo o pipeline de dados — da coleta à clusterização.

## Pipeline de Dados

```
SteamDB (web scraping)
        │
        ▼
   IGDB API (enriquecimento)
        │
        ▼
   Limpeza & Transformação
        │
        ▼
   EDA + K-Means
```

### Coleta de Dados

- **Webscraping do SteamDB** (`src/ingestion/webscraping/`): raspagem do ranking dos 1000 jogos mais bem avaliados usando BeautifulSoup, extraindo avaliações positivas/negativas e percentual de aprovação.
- **API do IGDB** (`src/ingestion/igdb_api/`): enriquecimento via API REST da Internet Game Database (autenticação OAuth2 via Twitch), coletando gêneros, plataformas, perspectivas, engine, notas de críticos e datas de lançamento. Taxa de 4 req/s (~4 min para os 1000 jogos).

### Limpeza do Dataset

Duas rodadas de limpeza documentadas em `src/cleaning/`:
- **v1**: normalização de strings, remoção de vírgulas em campos numéricos, tratamento de backslashes em listas (plataformas/gêneros).
- **v2**: re-rating de jogos com dados faltantes, consolidação do JSON final.

## Perguntas de Análise

1. Quais gêneros têm as melhores classificações médias?
2. Quais plataformas concentram mais jogos entre os 1000 mais bem avaliados?
3. Popularidade (total de reviews) implica melhor avaliação?

## Análises Realizadas

| Seção | Conteúdo |
|---|---|
| Medidas de Centralidade | Médias e medianas de reviews (SteamDB + IGDB), modas por modo de jogo, plataforma, engine e perspectiva |
| Medidas de Dispersão | Boxplots, desvio padrão, detecção de outliers via z-score |
| Gráficos | Histogramas de plataformas por ano, correlação entre popularidade e avaliação, ranking de gêneros (público vs crítica) |
| Sistema de Score | Score composto combinando nota Steam, nota IGDB e volume de reviews |
| K-Means | Clusterização em 4 grupos por features numéricas + ano de lançamento |

## Principais Achados

- Correlação quase nula (0,007) entre total de reviews e percentual de aprovação — popularidade não implica qualidade.
- Roguelike lidera tanto no ranking do público quanto da crítica.
- Outliers em volume: Terraria (1,3M reviews), Garry's Mod (1,1M), Elden Ring (968k).
- Cluster dominante (852 jogos): lançamentos pós-2018, studios independentes, média de 10k avaliações positivas.

## Tecnologias

- **Python** — pandas, scikit-learn, matplotlib, seaborn, BeautifulSoup, requests
- **Jupyter Notebook**
- **APIs**: IGDB (OAuth2/Twitch)
- **Dados**: SteamDB + IGDB → `data/games_data.csv`

## Estrutura

```
├── data/                        # Dataset final (CSV + JSON)
├── notebooks/
│   └── analysis.ipynb           # Notebook principal
├── src/
│   ├── ingestion/
│   │   ├── webscraping/         # Scraper do SteamDB
│   │   └── igdb_api/            # Wrapper + scripts de requisição IGDB
│   └── cleaning/
│       ├── v1/                  # Primeira rodada de limpeza
│       └── v2/                  # Segunda rodada (dataset final)
└── assets/                      # Imagens e capturas de tela
```
