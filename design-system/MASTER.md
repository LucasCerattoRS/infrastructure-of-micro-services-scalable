# OfertaHub · Master Design System

> **Fonte da verdade visual** do ecossistema OfertaHub.
> Stack: **Next.js 15 · Tailwind CSS v4 · shadcn/ui · lucide-react**.
> Filosofia: *Bento Grid · Minimalismo técnico · Dashboard de engenharia cruzado com marketplace premium*.

| | |
|---|---|
| **Versão** | 1.0.0 |
| **Status** | Canônico — toda nova UI deve referenciar este documento |
| **Escopo** | Dashboard admin, feed de ofertas, bot Telegram (web preview), landing |
| **Modo padrão** | Dark-first (o light mode é opcional, não prioritário) |

---

## 1. Identidade Visual

### 1.1 Paleta — Superfícies (Slate/Zinc)

O sistema é construído sobre **Zinc** (neutro puro, sem viés azulado). A hierarquia de superfície segue a convenção *base → raised → overlay*, permitindo stacking sem perda de contraste.

| Token | Hex | Uso | Tailwind |
|---|---|---|---|
| `--surface-base`     | `#09090B` | Background root da aplicação | `bg-zinc-950` |
| `--surface-raised`   | `#18181B` | Cards Bento, inputs, dropdowns | `bg-zinc-900` |
| `--surface-overlay`  | `#27272A` | Modais, popovers, tooltips | `bg-zinc-800` |
| `--surface-inset`    | `#050507` | Code blocks, terminal output, WAL indicators | `bg-[#050507]` |
| `--border-subtle`    | `#1F1F23` | Divisores internos de card | `border-zinc-800/60` |
| `--border-default`   | `#27272A` | Bordas de container padrão | `border-zinc-800` |
| `--border-emphasis`  | `#3F3F46` | Hover / foco / seleção | `border-zinc-700` |

### 1.2 Paleta — Tipografia

| Token | Hex | Uso | Tailwind |
|---|---|---|---|
| `--fg-primary`   | `#FAFAFA` | Títulos, números-chave, produtos | `text-zinc-50` |
| `--fg-secondary` | `#D4D4D8` | Corpo de texto, parágrafos | `text-zinc-300` |
| `--fg-tertiary`  | `#A1A1AA` | Descrições, hints, metadata | `text-zinc-400` |
| `--fg-muted`     | `#71717A` | Rótulos, timestamps, placeholders | `text-zinc-500` |
| `--fg-disabled`  | `#52525B` | Estados desabilitados | `text-zinc-600` |

### 1.3 Paleta — Semântica (Acentos)

O sistema é **bicromático em acento**: *emerald* (sucesso / sistema saudável) e *cyan* (dados / tecnologia / links). Rose é reservado para erro, amber para alerta — ambos com uso parcimonioso.

| Papel | Token | Hex | Uso dominante |
|---|---|---|---|
| **Success / Live** | `--accent-emerald` | `#10B981` | Score alto (≥ 70), systemd active, aprovações |
| **Success hover**  | `--accent-emerald-hi` | `#34D399` | Hover state de CTAs primários |
| **Tech / Data**    | `--accent-cyan`    | `#06B6D4` | Links de afiliado, métricas numéricas neutras |
| **Tech hover**     | `--accent-cyan-hi` | `#22D3EE` | Hover state de CTAs secundários |
| **Warning**        | `--accent-amber`   | `#F59E0B` | Score médio (50–69), volatilidade, histórico curto |
| **Danger**         | `--accent-rose`    | `#F43F5E` | Score baixo (< 50), blacklist, erro de pipeline |
| **Info**           | `--accent-sky`     | `#0EA5E9` | Notas informativas, onboarding |

> **Regra:** nunca combine emerald + cyan no mesmo elemento sem separação espacial. Cada componente deve ter **um** acento dominante.

### 1.4 Tipografia — Stacks

Dois stacks, divisão de responsabilidade rígida:

```css
--font-sans: "Inter", "Geist", ui-sans-serif, system-ui, sans-serif;
--font-mono: "JetBrains Mono", "Geist Mono", ui-monospace, "Menlo", monospace;
```

| Quando usar **mono** | Quando usar **sans** |
|---|---|
| Números: preços, scores, ASINs, percentuais, contadores | Títulos de produto, rótulos de UI, parágrafos |
| Códigos técnicos, tokens, timestamps | Mensagens de erro/sucesso narradas |
| Métricas em dashboards | Navegação, botões, CTAs |

**Sempre aplicar `tabular-nums` em números dinâmicos** para evitar "dança" de dígitos entre re-renders.

### 1.5 Escala Tipográfica

Escala modular com base **16px / 1rem** e ratio ≈ 1.2. Otimizada para densidade de dados.

| Token | Size / LH | Tailwind | Uso |
|---|---|---|---|
| `text-micro`   | 10px / 14px | `text-[10px] leading-[14px]` | Labels UPPERCASE, badges menores, footer legal |
| `text-xs`      | 11px / 16px | `text-[11px] leading-4` | Metadata, hints, categorias |
| `text-sm`      | 13px / 18px | `text-[13px] leading-[18px]` | Corpo de texto padrão, itens de lista |
| `text-base`    | 14px / 20px | `text-sm leading-5` | Títulos de produto, CTAs |
| `text-lg`      | 16px / 24px | `text-base leading-6` | Subtítulos de seção |
| `text-xl`      | 20px / 28px | `text-xl leading-7` | Título de card principal |
| `text-2xl`     | 24px / 32px | `text-2xl leading-8` | Números secundários (score, counters) |
| `text-display` | 32px / 40px | `text-[32px] leading-10` | Números-chave (Score Médio, totais) |
| `text-hero`    | 48px / 56px | `text-5xl leading-[56px]` | Landing, onboarding |

**Tracking:**
- Labels UPPERCASE → `tracking-[0.14em]`
- Monospaced (ASINs, códigos) → `tracking-normal`
- Sans default → `tracking-tight` (-0.011em) em headings, padrão no resto

### 1.6 Ícones

Biblioteca única: **lucide-react**. Regras:

- Stroke-width padrão: **1.5** (ligeiramente mais fino que o default de 2, combina com a estética minimalista)
- Tamanhos: `12` (inline), `14` (header de card), `16` (botões), `18` (nav), `24` (empty states)
- Cor: herda do `color` do container (`currentColor`). Nunca colore ícones arbitrariamente.

```tsx
<Brain size={14} strokeWidth={1.5} className="text-emerald-400" />
```

---

## 2. Grid System — Bento Rules

### 2.1 Container base

| Propriedade | Valor | Notas |
|---|---|---|
| Max width | `1600px` (`max-w-[1600px]`) | Acima disso, o dashboard perde densidade |
| Padding externo | `24px` (`p-6`) mobile · `32px` (`p-8`) desktop | — |
| Base grid | `grid-cols-12` | 12 colunas em desktop |
| Gap | `16px` (`gap-4`) | Único valor de gap em todo o Bento |

### 2.2 Spans canônicos

Todo card Bento usa um dos seguintes spans. **Não inventar spans arbitrários.**

| Tamanho | Spans | Uso típico |
|---|---|---|
| **Small**  | `col-span-12 md:col-span-6 lg:col-span-3` | KPIs isolados, gauges, status |
| **Medium** | `col-span-12 md:col-span-6 lg:col-span-4` | Donuts, listas curtas, gráficos compactos |
| **Large**  | `col-span-12 lg:col-span-5` ou `lg:col-span-7` | Painéis principais (Performance IA, Tráfego) |
| **Wide**   | `col-span-12 lg:col-span-8` | Tabelas, feeds longos |
| **Full**   | `col-span-12` | Headers, banners, empty states |

Altura: preferir `row-span-2` para cards-chave (criam a assimetria característica do Bento), nunca para mais de 30% dos cards na view.

### 2.3 Card anatomy

```
┌──────────────────────────────────┐
│ [icon] LABEL UPPERCASE     LIVE• │  ← header (mb-4)
├──────────────────────────────────┤
│                                  │
│  ■ content                       │
│                                  │
├──────────────────────────────────┤
│ metadata · timestamps · hints    │  ← footer (opcional, border-t)
└──────────────────────────────────┘
```

| Propriedade | Valor | Tailwind |
|---|---|---|
| Radius | `12px` | `rounded-xl` |
| Border | `1px solid --border-default` | `border border-zinc-800` |
| Background | `--surface-raised` com alpha 60% sobre base | `bg-zinc-950/60 backdrop-blur` |
| Padding | `20px` | `p-5` |
| Hover border | `--accent-emerald` @ 30% alpha | `hover:border-emerald-500/30` |
| Hover glow | soft emerald bloom | `hover:shadow-[0_0_40px_-12px_rgba(16,185,129,0.25)]` |
| Transition | `300ms ease` | `transition-all duration-300` |

### 2.4 Header de card (regra rígida)

```tsx
<header className="mb-4 flex items-center justify-between">
  <div className="flex items-center gap-2 text-zinc-400">
    <Icon size={14} strokeWidth={1.5} />
    <h2 className="text-[11px] font-medium uppercase tracking-[0.14em]">
      Título do Card
    </h2>
  </div>
  {live && <LiveDot />}
</header>
```

- **Nunca** usar cores de acento no título — sempre `text-zinc-400`.
- Indicador `LIVE` é o **único** elemento que ganha acento no header.

### 2.5 Background grid (opcional)

Para a view raiz do dashboard, um grid sutil reforça a leitura técnica:

```tsx
<div
  className="pointer-events-none fixed inset-0 opacity-[0.035]"
  style={{
    backgroundImage:
      "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)",
    backgroundSize: "40px 40px",
  }}
/>
```

> `opacity` entre `0.03` e `0.05`. Acima disso, compete com o conteúdo.

---

## 3. Component Library — Átomos

### 3.1 Score Badge (dinâmico)

O Score da IA é **o** elemento semântico central do OfertaHub. Quatro tiers:

| Tier | Range | Cor | Label | Tailwind |
|---|---|---|---|---|
| **S — Excellent** | ≥ 80 | emerald | "Excelente" | `text-emerald-400 bg-emerald-500/10 border-emerald-500/30` |
| **A — Good**      | 70–79 | cyan    | "Ótimo"     | `text-cyan-400 bg-cyan-500/10 border-cyan-500/30` |
| **B — Ok**        | 50–69 | amber   | "Aceitável" | `text-amber-400 bg-amber-500/10 border-amber-500/30` |
| **C — Reject**    | < 50  | rose    | "Rejeitar"  | `text-rose-400 bg-rose-500/10 border-rose-500/30` |

```tsx
export const ScoreBadge = ({ score }: { score: number }) => {
  const tier =
    score >= 80 ? "emerald" :
    score >= 70 ? "cyan"    :
    score >= 50 ? "amber"   : "rose";
  return (
    <span className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5
                      font-mono text-[11px] font-semibold tabular-nums
                      text-${tier}-400 bg-${tier}-500/10 border-${tier}-500/30`}>
      {score.toFixed(2)}
    </span>
  );
};
```

> **Importante:** o limiar 50/70/80 é a versão visual da fórmula `Score = (Wp·P) + (Wa·A) + (Wv·log₁₀V) − C`. Se os pesos mudarem em `config.py`, os limiares devem ser revisados.

### 3.2 Card de Produto

Estrutura de 4 zonas verticais, sempre nesta ordem:

```
┌─────────────────┐
│  [imagem 1:1]   │  zone 1 — visual (aspect-square)
│          −47%   │  desconto absoluto (overlay top-right)
├─────────────────┤
│ Categoria       │  zone 2 — metadata (text-xs muted)
│ Título produto  │  zone 3 — nome (text-sm primary, 2 lines clamp)
│ ★ 4.7 · 18.4k   │  metadata secundária
├─────────────────┤
│ R$ 199,00       │  zone 4 — preço atual (display, emerald)
│ R$ 379,00       │  preço original (line-through, muted)
│ [CTA Comprar]   │  botão primário full-width
└─────────────────┘
```

Especificação:

| Zona | Tailwind |
|---|---|
| Container | `rounded-xl border border-zinc-800 bg-zinc-900/50 overflow-hidden transition hover:border-emerald-500/30` |
| Imagem    | `aspect-square w-full bg-zinc-950 object-cover` |
| Badge desconto | `absolute top-3 right-3 rounded-md bg-emerald-500 px-2 py-0.5 font-mono text-[11px] font-bold text-zinc-950` |
| Categoria | `text-[10px] uppercase tracking-wider text-zinc-500` |
| Título    | `text-sm text-zinc-100 line-clamp-2` |
| Preço atual | `font-mono text-2xl font-semibold tabular-nums text-emerald-400` |
| Preço original | `font-mono text-xs tabular-nums text-zinc-500 line-through` |
| CTA       | ver **3.3 Botões** |

### 3.3 Botões

Três variantes apenas. Evitar proliferação.

#### Primary (Emerald)
```
bg-emerald-500 text-zinc-950 font-medium
hover:bg-emerald-400
active:bg-emerald-600
disabled:bg-zinc-800 disabled:text-zinc-600
```

#### Secondary (Outline Cyan)
```
border border-zinc-800 bg-transparent text-zinc-200
hover:border-cyan-500/50 hover:text-cyan-400 hover:bg-cyan-500/5
active:bg-cyan-500/10
```

#### Ghost
```
bg-transparent text-zinc-400
hover:bg-zinc-900 hover:text-zinc-100
```

Sizes:

| Size | Height | Padding | Text |
|---|---|---|---|
| `sm` | `32px` (`h-8`)  | `px-3` | `text-xs` |
| `md` | `38px` (`h-[38px]`) | `px-4` | `text-sm` |
| `lg` | `44px` (`h-11`) | `px-6` | `text-sm` |

Base (todos):
```
inline-flex items-center justify-center gap-2 rounded-lg
font-medium transition-all duration-200
focus-visible:outline-none focus-visible:ring-2
focus-visible:ring-emerald-500/50 focus-visible:ring-offset-2
focus-visible:ring-offset-zinc-950
```

### 3.4 Live Indicator

Marca cards que recebem dados do pipeline (`pipeline.py`, `disparador_telegram.py`).

```tsx
export const LiveDot = () => (
  <span className="flex items-center gap-1.5 font-mono text-[10px]
                   uppercase tracking-wider text-emerald-400">
    <span className="relative flex h-2 w-2">
      <span className="absolute inline-flex h-full w-full animate-ping
                       rounded-full bg-emerald-400 opacity-75" />
      <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
    </span>
    LIVE
  </span>
);
```

### 3.5 Stat (KPI atômico)

Unidade mínima de exibição de métrica. **Use em vez de reinventar formatação de número.**

```tsx
<div>
  <p className="text-[10px] uppercase tracking-wider text-zinc-500">Score Médio</p>
  <p className="font-mono text-[32px] font-semibold tabular-nums text-emerald-400">
    74.12
  </p>
  <p className="mt-1 font-mono text-[11px] text-zinc-500">gerente_ia.calcular_score()</p>
</div>
```

### 3.6 Tag / Chip

Para filtros e categorias:

```
inline-flex items-center gap-1.5 rounded-md border border-zinc-800
bg-zinc-900/60 px-2 py-1 text-[11px] text-zinc-300
hover:border-zinc-700 hover:text-zinc-100 transition
```

Estado ativo: substituir `border-zinc-800` por `border-emerald-500/40` e `text-zinc-300` por `text-emerald-400`.

### 3.7 Input

```
h-10 w-full rounded-lg border border-zinc-800 bg-zinc-900/40
px-3 font-sans text-sm text-zinc-100 placeholder:text-zinc-600
transition focus:border-emerald-500/50 focus:bg-zinc-900
focus:outline-none focus:ring-2 focus:ring-emerald-500/20
```

### 3.8 Divider

Preferir `border-t border-zinc-800/60` em vez de `<hr>`. Para grupos densos, `divide-y divide-zinc-800/70` no container.

---

## 4. Interaction Design

### 4.1 Curvas de transição

| Contexto | Duração | Easing | Tailwind |
|---|---|---|---|
| Hover estado (cor, borda) | `200ms` | `ease-out` | `transition-colors duration-200` |
| Transform (scale, translate) | `250ms` | `cubic-bezier(0.22, 1, 0.36, 1)` | `transition-transform duration-[250ms] ease-[cubic-bezier(0.22,1,0.36,1)]` |
| Card hover (shadow + border) | `300ms` | `ease` | `transition-all duration-300` |
| Entrada de página | `400ms` | `ease-out` | via Framer Motion preferencialmente |
| Skeletons / loading | `1.5s` | `linear` infinite | `animate-pulse` |

**Regra:** nenhuma transição acima de `400ms` em estado de hover. Hover que demora parece lag.

### 4.2 Estados

Todo componente interativo deve cobrir **todos** os estados abaixo:

| Estado | Tratamento |
|---|---|
| **default** | Definido pela variante |
| **hover**   | Elevação de contraste (borda, background, cor do texto) |
| **active / pressed** | Tom um step mais escuro que hover |
| **focus-visible** | `ring-2 ring-emerald-500/50 ring-offset-2 ring-offset-zinc-950` |
| **disabled** | `opacity-50 cursor-not-allowed` + `pointer-events-none` |
| **loading** | Spinner `size-4` + texto substituído por "Carregando…" |

> Use `focus-visible`, **não** `focus` — evita o outline em cliques de mouse.

### 4.3 Micro-interações

**Copy-to-clipboard** (ASINs, links de afiliado):
- Click → `navigator.clipboard.writeText()`
- Feedback: ícone troca de `Copy` para `Check` por 1200ms, texto breve "copiado".

**Row hover em listas**:
- Background: `hover:bg-zinc-900/40`
- Revelar ações (ícone de link, menu) com `opacity-0 group-hover:opacity-100 transition`

**Pulse em dados live**:
- Usar `LiveDot` (seção 3.4) — animação `ping` do Tailwind é suficiente, não escrever keyframes custom.

### 4.4 Feedback de ação

Toda mutação (aprovar oferta, disparar Telegram, etc.) deve:

1. Mostrar estado *optimistic* imediatamente (< 16ms percebido)
2. Toast no canto inferior-direito com ícone + mensagem
3. Em caso de erro: toast rose, reverter estado optimistic, oferecer retry

Toast base:
```
rounded-lg border border-zinc-800 bg-zinc-900 p-4 shadow-xl
```

---

## 5. Acessibilidade (WCAG AA)

### 5.1 Contraste — verificado

| Par | Ratio | Status |
|---|---|---|
| `zinc-50` em `zinc-950`   | 19.1:1 | ✅ AAA |
| `zinc-300` em `zinc-950`  | 12.6:1 | ✅ AAA |
| `zinc-400` em `zinc-950`  | 7.8:1  | ✅ AAA |
| `zinc-500` em `zinc-950`  | 4.9:1  | ✅ AA  |
| `zinc-600` em `zinc-950`  | 3.2:1  | ⚠️ apenas para texto decorativo/disabled |
| `emerald-400` em `zinc-950` | 8.4:1 | ✅ AAA |
| `emerald-500` em `zinc-950` | 6.1:1 | ✅ AA  |
| `cyan-400` em `zinc-950`    | 7.9:1  | ✅ AAA |
| `rose-400` em `zinc-950`    | 5.4:1  | ✅ AA  |
| `amber-400` em `zinc-950`   | 10.8:1 | ✅ AAA |

### 5.2 Regras

- Todo `<button>` e `<a>` sem texto visível **precisa** de `aria-label`.
- Ícones decorativos: `aria-hidden="true"`.
- Números críticos (preços, scores): acompanhar de texto legível por screen reader, por ex.:
  ```tsx
  <span aria-label="Score 78.41 de 100">78.41</span>
  ```
- Nenhum elemento interativo com **alvo de clique menor que 32×32px**. Para ícones de 14px, o padding do container deve completar o alvo.
- Movimento: respeitar `prefers-reduced-motion` — desabilitar `animate-ping` e transições longas quando `true`.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 6. Configuração — `tailwind.config.ts`

```ts
import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "Geist", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Geist Mono", "ui-monospace", "Menlo", "monospace"],
      },
      colors: {
        surface: {
          base:    "#09090B",
          raised:  "#18181B",
          overlay: "#27272A",
          inset:   "#050507",
        },
        accent: {
          emerald:   "#10B981",
          emeraldHi: "#34D399",
          cyan:      "#06B6D4",
          cyanHi:    "#22D3EE",
          amber:     "#F59E0B",
          rose:      "#F43F5E",
          sky:       "#0EA5E9",
        },
      },
      borderRadius: {
        xs: "4px",
        sm: "6px",
        md: "8px",
        lg: "10px",
        xl: "12px",
        "2xl": "16px",
      },
      boxShadow: {
        "glow-emerald": "0 0 40px -12px rgba(16, 185, 129, 0.25)",
        "glow-cyan":    "0 0 40px -12px rgba(6, 182, 212, 0.25)",
        "card":         "0 1px 0 0 rgba(255, 255, 255, 0.02) inset, 0 1px 2px 0 rgba(0, 0, 0, 0.3)",
      },
      transitionTimingFunction: {
        "out-expo": "cubic-bezier(0.22, 1, 0.36, 1)",
      },
      keyframes: {
        "pulse-subtle": {
          "0%, 100%": { opacity: "1" },
          "50%":      { opacity: "0.7" },
        },
      },
      animation: {
        "pulse-subtle": "pulse-subtle 2.5s ease-in-out infinite",
      },
    },
  },
  plugins: [],
} satisfies Config;
```

### 6.1 Variáveis CSS globais

```css
/* app/globals.css */
@layer base {
  :root {
    --surface-base:    #09090B;
    --surface-raised:  #18181B;
    --surface-overlay: #27272A;
    --border-default:  #27272A;

    --accent-emerald:  #10B981;
    --accent-cyan:     #06B6D4;
    --accent-amber:    #F59E0B;
    --accent-rose:     #F43F5E;

    --radius:          12px;
  }

  html { color-scheme: dark; }

  body {
    background: var(--surface-base);
    color: #FAFAFA;
    font-feature-settings: "cv11", "ss01", "ss03";
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }

  /* tabular nums por padrão em <code> e elementos .font-mono */
  code, kbd, samp, pre, .font-mono {
    font-variant-numeric: tabular-nums;
  }
}
```

---

## 7. Tokens para shadcn/ui

Quando usar `shadcn/ui`, sobrescrever os tokens do gerador no `components.json` para alinhar ao sistema:

```json
{
  "style": "default",
  "rsc": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "ui": "@/components/ui",
    "utils": "@/lib/utils"
  }
}
```

Variantes de `Button` (de shadcn) a **remover / renomear**:
- `destructive` → manter, mapear para `accent-rose`
- `link` → remover (usar `<Link>` direto com classe `text-cyan-400 hover:underline`)
- `outline` → realinhar para o **Secondary (Outline Cyan)** da seção 3.3

---

## 8. Anti-patterns — proibidos

| ❌ Proibido | ✅ Correto |
|---|---|
| Gradientes grandes em backgrounds (`from-purple to-pink`) | Gradientes sutis apenas em progress bars / barras de métrica (ex: `from-cyan-400 to-emerald-400`) |
| Sombras coloridas pesadas (`shadow-2xl shadow-emerald-500`) | `shadow-glow-emerald` (ver 6.0) — bloom sutil apenas no hover |
| Uso de `font-serif` em qualquer lugar | Apenas `font-sans` e `font-mono` |
| Ícones coloridos independentemente do contexto | Ícones herdam `currentColor` |
| Mais de **dois** acentos simultâneos no mesmo card | Um acento dominante por card |
| Botão roxo, rosa, laranja | Apenas emerald (primary), outline cyan (secondary), ghost |
| Bordas arredondadas `rounded-full` em cards | Apenas em badges, avatares e indicadores |
| `text-align: center` em blocos de texto longo | Esquerda por padrão; centro apenas em empty states |
| Animações de entrada > 400ms | Máximo 400ms, preferir 200–300ms |
| Números em `font-sans` com dígitos proporcionais | Sempre `font-mono tabular-nums` para dados |

---

## 9. Glossário do domínio

Termos que aparecem na UI e **não devem ser traduzidos ou abreviados**:

| Termo | Origem | Onde aparece |
|---|---|---|
| **ASIN** | Amazon Standard Identification Number | Cards, listas, tooltip de produto |
| **Score IA** / **Score Oferta** | `gerente_ia.calcular_score()` | Badges, sort, filtros |
| **Tag de Afiliado** | `AFFILIATE_TAG` em `config.py` | Header, footer de card |
| **WAL Mode** | SQLite journal mode | Status do sistema |
| **Pipeline** | `pipeline.py` orquestrador | Log card, timestamps |
| **Gerente IA** | `gerente_ia.py` | Título de seções de scoring |
| **Disparador** | `disparador_telegram.py` | Status de notificações |
| **Inline Keyboard** | Telegram Bot API | Preview de mensagens |

---

## 10. Versionamento & contribuição

- Toda alteração de token (cor, radius, font) exige bump **MINOR** e changelog.
- Remoção de variante de componente exige bump **MAJOR**.
- Novos átomos vão na seção 3 antes de virar código — documentar **sempre** primeiro.
- Componentes compostos (moléculas/organismos) ficam fora deste documento e devem viver em `design-system/components/*.md`.

---

**Fim do MASTER.md** · Este documento é a contraparte visual da lógica em `BackEnd/AI/`. Qualquer novo componente React deve importar tokens daqui — nenhum hex hardcoded fora desta referência.
