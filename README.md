# Calculadora de Incerteza de Medição · ABNT NBR ISO/IEC 17025:2017

[![ISO/IEC 17025:2017](https://img.shields.io/badge/Norma-ISO%2FIEC%2017025%3A2017%20%C2%A7%207.6-blue)](https://www.iso.org/standard/67049.html)
[![GUM JCGM 100:2008](https://img.shields.io/badge/Metrologia-GUM%20%2F%20JCGM%20100-teal)](https://www.bipm.org/en/committees/jc/jcgm/wg1)
[![Eurachem / CITAC](https://img.shields.io/badge/Guia-Eurachem%20%2F%20CITAC%20CG%204-navy)](https://www.eurachem.org/index.php/publications/guides/cum)
[![PWA Offline Ready](https://img.shields.io/badge/PWA-100%25%20Offline%20Ready-success)](#instalação-como-aplicativo-desktop-pwa)
[![Vanilla HTML/JS](https://img.shields.io/badge/Tech-Vanilla%20HTML5%20%2F%20JS-orange)](#desenvolvimento-e-arquitetura)

Aplicação web técnica, autônoma e auditada para a **avaliação e cálculo da incerteza de medição** em ensaios químicos e físico-químicos, em estrita conformidade com o **Requisito 7.6 da ABNT NBR ISO/IEC 17025:2017**, as diretrizes do **GUM (JCGM 100:2008)**, o guia **Eurachem/CITAC CG 4** e o relatório técnico **Nordtest TR 537**.

Ao iniciar, a aplicação abre diretamente em uma tela de seleção (Hub Metrológico) apresentando cards pré-configurados e a possibilidade de cadastrar ensaios analíticos personalizados sob medida:

1. **Nitrito ($\text{N-NO}_2^-$)** — Estudo de caso calibrado de referência por Espectrofotometria UV-Vis (Método Griess · Standard Methods 4500-NO₂⁻ B), utilizado no monitoramento ambiental da **Eletronuclear**.
2. **Amônia ($\text{N-NH}_3$)** — Espectrofotometria UV-Vis pelo método do Fenato/Salicilato (Standard Methods 4500-NH₃ F) em 640 nm.
3. **Hidrazina ($\text{N}_2\text{H}_4$)** — Sequestrante de oxigênio em circuitos secundários de reatores nucleares e caldeiras por p-DAB (ASTM D1385) em 458 nm.
4. **Carbono Orgânico Total (TOC)** — Oxidação catalítica a 680 °C e detecção por NDIR (Standard Methods 5310 B) para águas ultrapuras.
5. **pH (Potenciometria Direta)** — Eletrodo combinado de vidro com compensação automática de temperatura ATC (Standard Methods 4500-H⁺ B).
6. **Card `+` (Adicionar Novo Ensaio)** — Construtor interativo de métodos analíticos com configuração de mensurando, técnica, faixas operacionais, tolerâncias de check e seleção de fontes padrão de incerteza Tipo B (MRC primário, Balança analítica, Balões Classe A, Micropipetas, Equipamento e Variação Térmica). Ensaios personalizados são salvos localmente e podem ser exportados/importados em JSON.

---

## 🎯 Destaques e Recursos

* **Cálculo Metrológico Completo:**
  * **Tipo A:** Tratamento de dados mensais com ANOVA (análise de variância) para isolar a repetibilidade dentro da corrida e a precisão intermediária ($s_{IP}$) ao longo do tempo.
  * **Tipo B:** Avaliação de certificados de calibração de padrões (MRC), vidrarias (balões, pipetas), balança analítica e espectrofotômetro, com conversão automática de distribuições (normal com fator $k$, retangular $\sqrt{3}$ e resolução $\sqrt{12}$).
  * **Veracidade & Viés (Nordtest TR 537 / Eurachem):** Avaliação de viés contra material de controle independente (check), com o viés integrado ao orçamento como componente de incerteza, sem correção do resultado.
  * **Orçamento de Incerteza:** Gráficos visuais de contribuição percentual da variância, determinação dos coeficientes de sensibilidade ($c_i$) e fator de abrangência $k$ declarado pelo analista, com o resultado expresso como $y \pm U$.
  * **Ajuda nos campos:** passe o mouse (ou foque com Tab) no rótulo de qualquer campo para ver, no próprio formulário, o que digitar ali — sem "onde encontrar": só a instrução.
  * **Menos digitação:** no histórico do controle só **data, corrida, preparação e resultado** são obrigatórios; analista, equipamento e lote permanecem disponíveis como registro opcional de rastreabilidade.
* **Memória de Cálculo Auditável:** Geração instantânea de relatório técnico para impressão e exportação em PDF (folha A4) contendo o equacionamento formal e a trilha de auditoria completa.
* **Glossário Interativo:** Mais de 40 termos metrológicos fundamentados com definições conceituais acionáveis por clique ou sobreposição (*hover*).
* **Importação & Exportação:**
  * Salve e recarregue estudos completos em formato `.json`.
  * Exporte e importe tabelas de corridas e precisão intermediária em `.csv`.
  * Leitura e auditoria de relatórios instrumentais em PDF (espectrofotômetro Cary UV-Vis).

---

## 🏗️ Arquitetura: 100% HTML Puro (Zero Dependências)

Este projeto adota a premissa de **máxima simplicidade operacional e portabilidade metrológica**:
* **Sem frameworks pesados:** Não utiliza React, Angular, Vue, Webpack, Vite ou Node.js em tempo de execução.
* **Sem build:** O código-fonte é o próprio código executado.
* **Segurança total:** Nenhum dado sai do navegador do usuário; todos os cálculos são executados estritamente na máquina local (*client-side*).

### Estrutura de Arquivos
```text
calculadora-incerteza-iso17025/
├── index.html         # Aplicação completa (HTML5 + CSS3 + JavaScript ES6)
├── manifest.json      # Manifesto PWA para instalação desktop/mobile
├── sw.js              # Service Worker para cache e uso 100% offline
├── icons/             # Ícones do aplicativo (SVG, 192px, 512px)
├── docs/              # Manual e documentação oficial em PDF (22 páginas)
│   └── Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf
├── exemplos/          # Estudos de caso prontos em JSON para treinamento
│   └── estudo_exemplo_nitrito.json
├── tests/             # Suíte de testes automatizados de exatidão numérica
│   └── nitrito_calculadora.cjs
└── README.md          # Esta documentação
```

---

## 🚀 Como Utilizar

### 1. Execução Local Imediata
Basta abrir o arquivo [`index.html`](index.html) dando um **duplo clique** ou arrastando-o para qualquer navegador moderno (Chrome, Edge, Firefox, Safari, Brave).

### 2. Instalação como Aplicativo Desktop (PWA)
1. Abra o arquivo no **Google Chrome** ou **Microsoft Edge**.
2. Na barra de endereços (à direita), clique no ícone **"Instalar Aplicativo"** (ou acerte em `Configurações > Aplicativos > Instalar esta página como aplicativo`).
3. O software ganhará uma janela limpa e dedicada, atalho próprio na Área de Trabalho e funcionará **completamente offline** mesmo se o computador estiver desconectado da rede.

### 3. Publicação no GitHub Pages (Opção 1)
Para disponibilizar a calculadora online na internet ou na intranet do laboratório:
1. Crie um novo repositório no GitHub (ex.: `calculadora-incerteza-iso17025`).
2. Suba os arquivos do projeto:
   ```bash
   git init
   git add .
   git commit -m "feat: lancamento da calculadora de incerteza ISO 17025"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/calculadora-incerteza-iso17025.git
   git push -u origin main
   ```
3. No GitHub, acesse **Settings > Pages > Branch: main / (root) > Save**.
4. Em menos de 1 minuto, a aplicação estará publicada e acessível em `https://SEU-USUARIO.github.io/calculadora-incerteza-iso17025/`.

---

## 📐 Formulação Matemática de Referência

O mensurando direto é a concentração de analito determinada pela curva de calibração:
$$y = C_{\text{leitura}} \quad [\text{mg/L de } \text{N-NO}_2^-]$$

### 1. Componente da Precisão (Tipo A)
A partir da precisão intermediária obtida por ANOVA balanceada com $m$ preparações independentes por corrida:
$$s_{IP} = \sqrt{MS_{\text{dentro}} + \max\left(0, \frac{MS_{\text{entre}} - MS_{\text{dentro}}}{m}\right)}$$
$$u_{\text{precisão}}(y) = |y| \cdot \frac{s_{IP}}{|\bar{x}|}$$

### 2. Componente do Viés (Eurachem / Nordtest)
O viés é avaliado contra um material de check independente e entra no orçamento como incerteza (não há correção do resultado):
$$u_{\text{viés}}(y) = |y| \cdot \sqrt{\text{viés}^2 + \left(\frac{s_{\text{check}}}{\sqrt{n} \cdot C_{\text{check}}}\right)^2 + u_{\text{rel}}^2(C_{\text{check}})}$$

#### 🔄 Modos Operacionais do Padrão de Check (Aba 03 - Controle de Qualidade):
* **Situação 1 (Recomendada / Prática de Rotina Integrada):**
  * O **mesmo material de controle/check** lido nas corridas analíticas diárias (ex.: Check $0{,}100\text{ mg/L}$) é utilizado simultaneamente para avaliar a **Precisão Intermediária** ($s_{IP}$ por ANOVA) e a **Veracidade / Viés** ($u_{\text{viés}}$ por recuperação), tudo reunido na **Aba 03**.
  * A calculadora mantém **sincronização contínua e reativa**: qualquer alteração nas leituras da tabela de corridas atualiza instantaneamente as leituras do check, recalculando o viés ($b$), o desvio do check ($s_{\text{check}}$) e sua incerteza ($u_{\text{viés}}$).
  * O assistente de diluição de estoque ($1000$ ou $100\text{ mg/L} \to 0{,}100\text{ mg/L}$) padroniza o nome do grupo e calcula $C_{\text{ref}} \pm U_{\text{ref}}$ com distribuição triangular de vidraria volumétrica Classe A.
* **Situação 2 (Material de Referência Independente):**
  * A Precisão Intermediária é estimada com uma amostra de controle de rotina (ex.: amostra fortificada ou duplicatas de clientes), enquanto a Veracidade é avaliada com um MRC externo independente ou ensaio de proficiência.
  * O analista desmarca a caixa de sincronização e insere manualmente as leituras do MRC.

#### ⚙️ Gaveta "Configurações avançadas do controle e premissas da ISO 17025"
* **Grupo do controle:** campo com lista dos grupos já lançados na tabela de corridas; o indicador ao lado mostra quantas leituras estão vinculadas. Se o nome não corresponder a nenhuma linha, aparece o aviso *"nenhuma leitura usa este grupo"* com o botão **usar o grupo da tabela**, que realinha o estudo em um clique e evita o falso erro "pelo menos dois resultados são necessários".
* **Corrida automática:** o código de corrida é gerado de **Data + Analista** no padrão `ANA_ddMMMyy NO2- XX` e exibido em campo somente-leitura. Códigos informados manualmente (importações antigas ou identificações próprias do laboratório) são preservados. Duas sessões do mesmo dia, com o mesmo analista e a mesma preparação recebem os sufixos `s2`, `s3`…, mantendo a rastreabilidade sem identificação duplicada.
* **Premissas do controle:** um único controle declara as duas premissas normativas (estabilidade/comparabilidade do controle no período e origem independente do check). Desmarcar exige a **justificativa técnica do desvio**: com a justificativa preenchida o estudo continua calculado e o desvio sai registrado como aviso na memória de cálculo; sem justificativa, o cálculo permanece bloqueado.

### 3. Incerteza Combinada e Expandida
A incerteza padrão combinada reúne todas as fontes ortogonais e não redundantes:
$$u_c(y) = \sqrt{\sum_{i=1}^N \left(c_i \cdot u(x_i)\right)^2}$$

O fator de abrangência ($k$) é **declarado pelo analista** na aba 05: $k = 2$ corresponde a aproximadamente $95,45\%$ quando a distribuição é aproximadamente normal e o número de graus de liberdade é suficiente. Recomenda-se registrar essa justificativa no próprio estudo.

A incerteza expandida reportada no laudo é:
$$U = k \cdot u_c(y) \quad (\text{para } 95,45\% \text{ de confiança com } k \approx 2)$$

---

## 📥 Importação Universal de Corridas e Laudos Cary (PDF, BCN, CSV)

A calculadora possui motor de extração direta de relatórios e arquivos brutos gerados pelo software **Varian / Agilent Cary WinUV Concentration (Cary 300 / Cary 50 / Cary 60)**:

* **Formatos Suportados:**
  * **`.BCN` (Batch Concentration File):** Arquivo binário nativo do equipamento. Extrai simultaneamente os **5 padrões da curva de calibração** (concentração e absorbância com cálculo automático de inclinação, intercepto e $R^2$), a leitura do branco/zero, data/hora da corrida e as duplicatas de medição.
  * **`.PDF` (Concentration Analysis Report):** Laudos instrumentais exportados diretamente da bancada.
  * **`.CSV / .TXT / .ASC / .DAT`:** Tabelas e dados exportados pelo comando *Save As ASCII*.
* **Reconhecimento Automático:**
  * **Analito por comprimento de onda / lote:** Nitrito ($\approx 543\text{ nm}$), Amônia ($\approx 630\text{--}640\text{ nm}$), Hidrazina ($\approx 447\text{ nm}$).
  * **Matriz:** Água do Mar (salinidade $\approx 35\text{ g/L}$), Água Subterrânea (poços de monitoramento `PM-01` a `PM-06`), Água Doce / Caldeira.
  * **Padrões de Check e CQ:** `CHECK 0.1`, `Check - 0,1`, `PD CHECK 0,1`, `PD1`, `PD 0,1 ppm`, etc.
  * **Amostras:** `AM6`, `AM7`, `AM8`, poços `PM-01`..`PM-06`, e séries de diluição (`0.5:100` a `4:100`).

### 🔬 O que o laudo do equipamento fornece vs. O que falta para a ISO/IEC 17025

| Parâmetro | No Arquivo Cary (`.PDF` / `.BCN`) | O que AINDA FALTA para o cálculo de incerteza ($u_c$ e $U$) |
| :--- | :--- | :--- |
| **Leitura Instrumental ($C_{\text{leitura}}$)** | ✅ Fornecida diretamente (amostra e duplicatas). | — |
| **Curva de Calibração** | ✅ Padrões e absorbâncias (em `.BCN`). | Avaliação do resíduo e incerteza da calibração ($s_{x0}$). |
| **Repetibilidade da Corrida** | ✅ Desvio padrão entre réplicas da mesma cubeta. | **Precisão Intermediária a Longo Prazo ($s_{IP}$ - Aba 03):** requer controle medido ao longo de dias e analistas distintos (ANOVA de longo prazo). |
| **Leitura do Padrão de Check** | ✅ Concentração medida do check (ex.: $0{,}102\text{ mg/L}$). | **Certificado Rastreável do MRC ($C_{\text{ref}}$, $U_{\text{ref}}$, $k$ - Aba 03):** o equipamento não conhece a incerteza do frasco do padrão nem sua validade. |
| **Efeito de Matriz (Água do Mar / Subterrânea)** | ⚠️ Apenas concentração aparente. | **Estudo de Recuperação / Fortificação (Spike):** em água do mar ($\approx 35\text{ g/L}$ de sais) e água subterrânea (interferentes e matéria orgânica), é indispensável o ensaio de spike na matriz real para avaliar $u_{\text{matriz}}$ sem duplicações. |
| **Volumetria / Diluições** | ⚠️ Alíquotas registradas no nome (ex.: `0.5:100`). | **Incerteza Tipo B de Balões e Micropipetas (Aba 02):** tolerâncias e calibrações dos materiais volumétricos utilizados. |
| **Regra de Decisão e Conformidade** | ❌ Não fornecida pelo espectrofotômetro. | **Critério Regulatório (Aba 05):** limites da Resolução CONAMA 357 (água do mar) ou CONAMA 396 (água subterrânea) e definição do fator $k$ com banda de guarda ($y + U \le L$). |

### 🚀 Resolução dos 3 Pilares Metrológicos Solicitados

1. **Variação Temporal e Reprodutibilidade Intralaboratorial (Item 1):**
   * A calculadora permite seleção múltipla de arquivos (`.BCN` ou `.PDF`) de uma só vez.
   * O modal de importação em lote compõe automaticamente a tabela da **Aba 03 (Controle de Qualidade: Precisão Intermediária)** distribuindo as réplicas de controle por dias de análise, analistas distintos (`CE`, `AP`, `JR`) e lotes de reagentes.
   * A ANOVA balanceada ou desbalanceada (Nordtest / ISO 17025) calcula instantaneamente a repetibilidade dentro da corrida ($s_r$), a variância entre dias ($s_{\text{entre}}$) e o desvio padrão da precisão intermediária ($s_{IP}$).

2. **Preparo e Diluição Manual do Check a partir de Estoque 1000 ou 100 mg/L (Item 2):**
   * Na **Aba 03 (Controle de Qualidade: Padrão de Check e Viés)**, um painel dedicado (`#checkDilutionDetails`) calcula a concentração nominal ($C_{\text{ref}}$) e a incerteza expandida ($U_{\text{ref}}$):
     $$C_{\text{ref}} = C_{\text{estoque}} \times \frac{V_{\text{pipeta}}}{V_{\text{balão}}}$$
     $$u_{\text{rel}}(C_{\text{ref}}) = \sqrt{\left(\frac{u(C_{\text{estoque}})}{C_{\text{estoque}}}\right)^2 + \left(\frac{\text{Tol}_{\text{pip}}}{\sqrt{6} \cdot V_{\text{pip}}}\right)^2 + \left(\frac{\text{Tol}_{\text{bal}}}{\sqrt{6} \cdot V_{\text{bal}}}\right)^2}$$
   * Botões de atalho rápido para estoque concentrado **1000 mg/L** ($0{,}100\text{ mL} \to 1000\text{ mL}$) e **100 mg/L** ($1{,}000\text{ mL} \to 1000\text{ mL}$), com propagação de incerteza por distribuição triangular ($\sqrt{6}$) de vidraria volumétrica Classe A (Eurachem CG 4).
   * O botão *"✓ Aplicar Valores ao Check"* preenche automaticamente $C_{\text{ref}}$, $U_{\text{ref}}$ e a rastreabilidade do certificado.

3. **Parâmetros Instrumentais Cary Enriquecidos no HTML (Item 3):**
   * Os dados técnicos da corrida instrumental são extraídos e apresentados em cards estruturados no HTML da aplicação e na memória de cálculo:
     * **Instrumento e Software:** Varian Cary 300 UV-Vis, Cary WinUV Concentration v4.20, Firmware v12.00.
     * **Parâmetros Ópticos:** Comprimento de onda ($\lambda = 543\text{ nm}$ Nitrito, $630\text{--}640\text{ nm}$ Amônia, $447\text{ nm}$ Hidrazina), Largura de Fenda Espectral (SBW $= 1{,}5\text{ nm}$ / $2{,}0\text{ nm}$), Tempo de Média (Ave Time $= 0{,}100\text{ s}$ / $0{,}500\text{ s}$), Modo de Feixe (Duplo feixe auto-select) e Leitura do Branco / Zero ($0{,}0000$).
     * **Rastreabilidade de Arquivos:** Nome do método de bancada (`.MCN`) e nome do arquivo de lote (`.BCN`).
     * **Curva de Calibração Completa:** Tabela de 5 padrões (`Std 1` a `Std 5`), concentrações nominais, absorbâncias medidas, equação linear de regressão ($y = ax + b$) e coeficiente de determinação ($R^2 > 0{,}999$).
     * **Condições de Matriz:** Indicação de matriz marinha salina ($\approx 35\text{ PSU}$ com compensação de cloretos) ou matriz de água subterrânea.
4. **Atalhos Regulatórios Ambientais (Aba 05):**
   * Botões diretos para limites CONAMA:
     * 🌊 **CONAMA 357 — Água do Mar Classe 1:** $0{,}07\text{ mg/L}$
     * 🌊 **CONAMA 357 — Água do Mar Classe 2:** $0{,}20\text{ mg/L}$
     * ⛰️ **CONAMA 396 — Água Subterrânea:** $1{,}0\text{ mg/L}$

---

## 📕 Manual Oficial em PDF
O projeto acompanha o manual completo em PDF de **22 páginas ricamente ilustradas** com diagramas de blocos, árvore de fontes, modelo ANOVA e critérios de semáforo de conformidade:  
👉 [`docs/Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf`](docs/Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf)

---

## 📄 Licença e Créditos
* **Normas de referência:** ABNT NBR ISO/IEC 17025:2017, JCGM 100:2008, Eurachem/CITAC Guide CG 4, NIT-DICLA-021.
* **Ambiente de aplicação:** Laboratórios da Eletronuclear / Laboratório de Monitoração Ambiental (LMA).
* Desenvolvido para livre uso em avaliações metrológicas e rotina da garantia da qualidade analítica.
