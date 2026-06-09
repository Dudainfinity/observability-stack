# Stack de Observabilidade com Prometheus + Grafana

Uma aplicação instrumentada sendo monitorada de ponta a ponta: **métricas
coletadas pelo Prometheus**, **dashboards no Grafana** e um **alerta que dispara
quando o serviço cai**. Tudo sobe com um único `docker compose up`.

> Projeto de portfólio com foco em **Observabilidade e Monitoramento** — o que
> separa "fazer subir" de "operar em produção de verdade".

---

## 🧩 Arquitetura

```
┌──────────┐   scrape    ┌────────────┐   alertas   ┌──────────────┐
│   App    │ ──/metrics─▶│ Prometheus │ ───────────▶│ Alertmanager │
│ (Flask)  │             │            │             │              │
└──────────┘             └─────┬──────┘             └──────────────┘
                               │ query
                               ▼
                         ┌───────────┐
                         │  Grafana  │  (dashboard provisionado)
                         └───────────┘
```

| Serviço | Porta | Função |
|---|---|---|
| **app** | 8000 | Aplicação Flask instrumentada, expõe métricas em `/metrics` |
| **Prometheus** | 9090 | Coleta as métricas e avalia as regras de alerta |
| **Alertmanager** | 9093 | Recebe e roteia os alertas disparados |
| **Grafana** | 3000 | Dashboards (datasource e painel já provisionados) |

---

## 🚀 Como subir

Pré-requisito: Docker e Docker Compose.

```bash
docker compose up -d --build
```

Depois acesse:

| O quê | URL | Login |
|---|---|---|
| Aplicação | http://localhost:8000 | — |
| Métricas da app | http://localhost:8000/metrics | — |
| Prometheus | http://localhost:9090 | — |
| Alertas no Prometheus | http://localhost:9090/alerts | — |
| Grafana | http://localhost:3000 | admin / admin |

No Grafana, o dashboard **"Monitoramento da Aplicação"** já aparece pronto
(datasource Prometheus configurado automaticamente).

Para derrubar tudo:

```bash
docker compose down
```

---

## 🔔 Testando o alerta "serviço caiu"

O alerta `AppForaDoAr` dispara quando a aplicação fica sem responder por 30s.
Para ver na prática:

```bash
# Derruba só a aplicação
docker compose stop app

# Aguarde ~30-45s e veja o alerta ficar "FIRING" em:
#   http://localhost:9090/alerts

# Suba de volta
docker compose start app
```

Também existe o alerta `TaxaDeErroAlta`, que dispara se muitos erros 500
acontecerem — gere alguns acessando http://localhost:8000/erro várias vezes.

---

## 📊 O que o dashboard mostra

- **Aplicação no ar (up)** — verde "NO AR" / vermelho "FORA".
- **Requisições por segundo** — taxa de requests por endpoint e status.
- **Latência (p95)** — tempo de resposta no percentil 95.

---

## 📁 Estrutura

```
observability-stack/
├── docker-compose.yml          # Orquestra os 4 serviços
├── app/                        # Aplicação Flask instrumentada
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── prometheus/
│   ├── prometheus.yml          # Configuração de scrape
│   └── alert.rules.yml         # Regras de alerta
├── alertmanager/
│   └── alertmanager.yml        # Roteamento dos alertas
└── grafana/
    └── provisioning/           # Datasource + dashboard automáticos
        ├── datasources/datasource.yml
        └── dashboards/
            ├── dashboards.yml
            └── app-dashboard.json
```

---

## 🧰 Stack

`Docker` · `Docker Compose` · `Prometheus` · `Grafana` · `Alertmanager` · `Python (Flask)` · `Linux`

---

Feito por **Maria Eduarda** — foco em DevOps & Cloud (AWS).
[GitHub](https://github.com/Dudainfinity)
