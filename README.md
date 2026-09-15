# Calculadora de Incerteza de Medição · ABNT NBR ISO/IEC 17025:2017

[![ISO/IEC 17025:2017](https://img.shields.io/badge/Norma-ISO%2FIEC%2017025%3A2017%20%C2%A7%207.6-blue)](https://www.iso.org/standard/67049.html)
[![GUM JCGM 100:2008](https://img.shields.io/badge/Metrologia-GUM%20%2F%20JCGM%20100-teal)](https://www.bipm.org/en/committees/jc/jcgm/wg1)
[![Eurachem / CITAC](https://img.shields.io/badge/Guia-Eurachem%20%2F%20CITAC%20CG%204-navy)](https://www.eurachem.org/index.php/publications/guides/cum)
[![PWA Offline Ready](https://img.shields.io/badge/PWA-100%25%20Offline%20Ready-success)](#instalação-como-aplicativo-desktop-pwa)
[![Vanilla HTML/JS](https://img.shields.io/badge/Tech-Vanilla%20HTML5%20%2F%20JS-orange)](#desenvolvimento-e-arquitetura)

Aplicação web técnica, autônoma e auditada para a **avaliação e cálculo da incerteza de medição** em ensaios químicos e físico-químicos, em estrita conformidade com o **Requisito 7.6 da ABNT NBR ISO/IEC 17025:2017**, as diretrizes do **GUM (JCGM 100:2008)** e o guia **Eurachem/CITAC CG 4**.

O estudo de caso calibrado de referência implementa o ensaio de **Nitrito por Espectrofotometria UV-Vis (Método Griess · Standard Methods 4500-NO₂⁻ B)**, amplamente utilizado em laboratórios ambientais e de monitoramento da **Eletronuclear**.

---

## 🎯 Destaques e Recursos

* **Cálculo Metrológico Completo:**
  * **Tipo A:** Tratamento de dados mensais com ANOVA (análise de variância) para isolar a repetibilidade dentro da corrida e a precisão intermediária ($s_{IP}$) ao longo do tempo.
  * **Tipo B:** Avaliação de certificados de calibração de padrões (MRC), vidrarias (balões, pipetas), balança analítica e espectrofotômetro, com conversão automática de distribuições (normal com fator $k$, retangular $\sqrt{3}$, triangular $\sqrt{6}$ e resolução $\sqrt{12}$).
  * **Veracidade & Viés (Nordtest TR 537 / Eurachem):** Avaliação de viés contra material de controle independente com teste $t$ de Student e modelo opcional de efeito residual de matriz por recuperação/fortificação.
  * **Orçamento de Incerteza:** Gráficos visuais de contribuição percentual da variância, determinação dos coeficientes de sensibilidade ($c_i$), graus de liberdade efetivos pela fórmula de **Welch-Satterthwaite** e fator de abrangência $k$ para $95,45\%$ de probabilidade de abrangência.
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

### 2. Componente do Viés e Recuperação (Eurachem / Nordtest)
$$u_{\text{viés}}(y) = |y| \cdot \sqrt{\text{viés}^2 + \left(\frac{s_{\text{check}}}{\sqrt{n} \cdot C_{\text{check}}}\right)^2 + u_{\text{rel}}^2(C_{\text{check}})}$$

### 3. Incerteza Combinada e Expandida
A incerteza padrão combinada reúne todas as fontes ortogonais e não redundantes:
$$u_c(y) = \sqrt{\sum_{i=1}^N \left(c_i \cdot u(x_i)\right)^2}$$

Os graus de liberdade efetivos ($\nu_{\text{eff}}$) são calculados pela equação de **Welch-Satterthwaite**:
$$\nu_{\text{eff}} = \frac{u_c^4(y)}{\sum_{i=1}^N \frac{u_i^4(y)}{\nu_i}}$$

A incerteza expandida reportada no laudo oficial é:
$$U = k \cdot u_c(y) \quad (\text{para } 95,45\% \text{ de confiança com } k \approx 2)$$

---

## 📕 Manual Oficial em PDF
O projeto acompanha o manual completo em PDF de **22 páginas ricamente ilustradas** com diagramas de blocos, árvore de fontes, modelo ANOVA e critérios de semáforo de conformidade:  
👉 [`docs/Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf`](docs/Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf)

---

## 📄 Licença e Créditos
* **Normas de referência:** ABNT NBR ISO/IEC 17025:2017, JCGM 100:2008, Eurachem/CITAC Guide CG 4, NIT-DICLA-021.
* **Ambiente de aplicação:** Laboratórios da Eletronuclear / Laboratório de Monitoração Ambiental (LMA).
* Desenvolvido para livre uso em avaliações metrológicas e rotina da garantia da qualidade analítica.
