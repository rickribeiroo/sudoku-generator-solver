# Sudoku generator and solver with visual feedback using Python
📝 Descrição

✨ Este projeto implementa um gerador e solucionador de Sudoku 9x9 completo com feedback visual, com capacidade para:

    Gerar tabuleiros 9x9 de Sudoku válidos

    Resolver tabuleiros 9x9 criados

    Visualizar o processo em tempo real usando 'matplotlib'

O algoritmo usado em ambos os casos é o 'backtracking' e, sendo assim, às vezes o programa pode demorar um pouco mais para criar/resolver o Sudoku.

📝 Output

O programa gera:

    complete_table.csv - Tabela completa com os números esperados
    table.csv - Tabela com os espaços vazios
    solution.csv - Tabela com a solução encontrada pelo 'sudoku_solver.py'
### ⚙️ Fluxo de Geração
```mermaid
graph TD
    A[Início] --> B[Tabuleiro Vazio]
    B --> C[Preenchimento Recursivo]
    C --> D{Valido?}
    D -- Sim --> E[Próxima Célula]
    D -- Não --> F[Backtrack]
    E --> G[Completo?]
    G -- Não --> C
    G -- Sim --> H[Remove Números]
    H --> I[Puzzle Final]
```
### 🧩 Fluxo de Solução
```mermaid
graph TD
    A[Início] --> B[Carrega Tabuleiro]
    B --> C[Identifica Células Vazias]
    C --> D[Calcula Possibilidades]
    D --> E[Ordena por Menos Opções]
    E --> F{Próxima Célula?}
    F -- Sim --> G[Tenta Número]
    G --> H{Validação}
    H -- Válido --> I[Atualiza Tabuleiro]
    I --> J[Remove de Células Relacionadas]
    J --> K[Reordena Lista]
    K --> L[Próxima Posição]
    L --> F
    H -- Inválido --> M[Backtrack]
    M --> N[Restaura Valor]
    N --> O[Restaura Possibilidades]
    O --> F
    F -- Não --> P{Tabuleiro Completo?}
    P -- Sim --> Q[Salva Solução]
    P -- Não --> R[Sem Solução]
```
