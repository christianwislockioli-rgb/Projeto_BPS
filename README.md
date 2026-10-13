# 📊 Dashboard Analítico | Banco de Preços em Saúde (BPS) 2020-2026

## 🎯 Objetivo do Projeto
Desenvolver uma solução de Visualização de Dados e Business Intelligence para acompanhar a eficiência das compras de medicamentos e dispositivos médicos registradas no Banco de Preços em Saúde (BPS) entre 2020 e 2026, apoiando a tomada de decisão gerencial na gestão de recursos públicos.

## 🌍 Contextualização do Problema
A gestão eficiente dos recursos em saúde é um dos maiores desafios da administração pública contemporânea. A aquisição de insumos envolve alto volume financeiro e múltiplos atores (secretarias, consórcios, hospitais). Este projeto visa transformar os microdados abertos em indicadores estratégicos, permitindo identificar padrões de consumo, modalidades de compra predominantes e os principais parceiros privados do Estado.

## 🗄️ Fonte dos Dados
Os dados públicos foram extraídos do **Portal Brasileiro de Dados Abertos do Ministério da Saúde** (Datasus), contemplando os arquivos anuais de 2020 a 2026.

## ⚙️ Procedimentos de Extração, Tratamento e Concatenação
Devido ao alto volume de dados, a modelagem foi realizada via script em **Python (Pandas)**:
1.  **Tratamento de Encoding:** Implementação de bloco `try-except` para ler arquivos históricos em `latin1` e arquivos recentes em `utf-8`, evitando a corrupção de caracteres especiais (Mojibake).
2.  **Limpeza de Nulos:** Conversão de strings literais `'NULL'` para `NaN` e preenchimento de vazios com "Não Informado" exclusivamente em colunas de texto (preservando a integridade das colunas de data).
3.  **Tipagem de Dados:** Forçada a conversão numérica de códigos identificadores (`co_pdm`, `co_classe`, etc.) para evitar falhas de carregamento.
4.  **Concatenação:** Junção (`append`/`concat`) dos 7 anos em um arquivo `.csv` unificado.

## 📐 Definição de KPIs e Métricas (DAX)
Os indicadores foram construídos no Power BI visando integridade matemática e relevância de negócio:
*   **Valor Total Registrado:** `SUM(vl_preco_total)`
*   **Quantidade Total de Itens:** `SUM(qt_medicamento)`
*   **Número de Registros:** `COUNTROWS` do modelo consolidado.
*   **Instituições Compradoras:** Contagem distinta pelo `cnpj_instituicao`.
*   **Fornecedores:** Contagem distinta pelo `cnpj_fornecedor`.
*   **Preço Unitário Médio Ponderado:** `DIVIDE(Valor Total Registrado, Qtd Total Itens, 0)` para mitigar erros de divisão.

## 🖥️ Acesso ao Dashboard e Vídeo de Apresentação
*   **Vídeo de Apresentação (Pitch de 5 min):** [Clique aqui para assistir](https://drive.google.com/drive/folders/1K7A_cRiWBXH0nsQwzn2H7kXc4G50WzbG?usp=drive_link)

**Visão Executiva (Capa):**
![Dashboard Capa](Imagens/Dashboard%20Capa.PNG)

**Análise de Fornecedores e Modalidades (Página 1):**
![Dashboard Página 1](Imagens/Dashboard%20Pagina%201.PNG) 

**Análise de Atores e Segmentação (Página 2):**
![Dashboard Página 2](Imagens/Dashboard%20Pagina%202.PNG)

## 💡 Principais Análises e Descobertas
*   **Concentração de Volume:** Produtos como 'Dieta Enteral' e medicamentos de uso crônico lideram o volume financeiro.
*   **Dominância de Modalidade:** A esmagadora maioria dos registros (>90%) ocorre via Pregão, indicando padronização nas licitações.
*   **Principais Compradores:** Secretarias Estaduais de Saúde e Consórcios Intermunicipais são os maiores responsáveis pelas negociações.

## 🚀 Recomendações Baseadas nos Dados
1.  **Ganho de Escala:** Fomentar a ampliação de compras via Consórcios Intermunicipais para medicamentos de alto custo, diluindo valores unitários através do ganho de escala.
2.  **Monitoramento de Estoque:** Como o volume de compras atingiu picos passados, alinhar os editais de Pregão ao fluxo sazonal de demandas crônicas evita desabastecimento e compras emergenciais (que costumam ter sobrepreço).

## ⚠️ Limitações da Análise
*   Diferenças de preços unitários no painel não comprovam necessariamente sobrepreço ou fraude, pois não isolam variáveis logísticas (frete para regiões remotas), flutuações macroeconômicas do período (como impactos da pandemia em 2020/2021) e unidades de fornecimento distintas (caixa vs. ampola).

## 🔄 Instruções para Reprodução
1.  Clone este repositório.
2.  Insira os arquivos `.csv` do BPS na pasta `dados_brutos/`.
3.  Execute `python preparacao_dados.py` para consolidar a base.
4.  Abra o arquivo `.pbix` e atualize a fonte de dados para o arquivo consolidado gerado.