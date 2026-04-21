// ProductCard.tsx
// OfertaHub — Card de Produto
// Segue estritamente MASTER.md §3.1 (ScoreBadge), §3.2 (Product Card) e §3.3 (Botões).
//
// Dados: espelham a estrutura de BackEnd/AI/ofertas_aprovadas.json
// {
//   ASIN, Produto, "Preço Real", "Preço Original", Desconto,
//   "Nota de Avaliação", "Total de Avaliações", Categoria, "Score Oferta", "Link de Afiliado"
// }
//
// Requisitos: React 18+, Tailwind (tokens do MASTER.md §6), lucide-react.

import React from "react";
import { ShoppingCart, Star, Copy, Check, ExternalLink } from "lucide-react";

// ─────────────────────────────────────────────────────────────────────────────
// Tipos (canônicos — reutilizar em qualquer consumidor)
// ─────────────────────────────────────────────────────────────────────────────

export interface Oferta {
  asin: string;
  produto: string;
  precoReal: number;
  precoOriginal: number;
  desconto: number;       // percentual, ex: 47.5
  nota: number;           // 0–5
  avaliacoes: number;
  categoria: string;
  score: number;          // 0–100, do gerente_ia.calcular_score()
  linkAfiliado: string;
  imagem?: string;        // opcional; fallback é placeholder neutro
}

// ─────────────────────────────────────────────────────────────────────────────
// Helpers (formato pt-BR + tiers do Score — §3.1)
// ─────────────────────────────────────────────────────────────────────────────

const brl = (v: number) =>
  v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const compactInt = (v: number) =>
  v >= 1000 ? `${(v / 1000).toFixed(1).replace(/\.0$/, "")}k` : String(v);

type ScoreTier = "emerald" | "cyan" | "amber" | "rose";

const tierFor = (score: number): ScoreTier =>
  score >= 80 ? "emerald" : score >= 70 ? "cyan" : score >= 50 ? "amber" : "rose";

// Classes completas por tier (Tailwind não suporta interpolação dinâmica — MASTER.md §3.1).
const TIER_CLASSES: Record<ScoreTier, string> = {
  emerald: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
  cyan:    "text-cyan-400 bg-cyan-500/10 border-cyan-500/30",
  amber:   "text-amber-400 bg-amber-500/10 border-amber-500/30",
  rose:    "text-rose-400 bg-rose-500/10 border-rose-500/30",
};

// ─────────────────────────────────────────────────────────────────────────────
// ScoreBadge — §3.1
// ─────────────────────────────────────────────────────────────────────────────

export const ScoreBadge: React.FC<{ score: number }> = ({ score }) => (
  <span
    aria-label={`Score IA ${score.toFixed(2)} de 100`}
    className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5
                font-mono text-[11px] font-semibold tabular-nums ${TIER_CLASSES[tierFor(score)]}`}
  >
    {score.toFixed(2)}
  </span>
);

// ─────────────────────────────────────────────────────────────────────────────
// Botão Primary — §3.3
// ─────────────────────────────────────────────────────────────────────────────

const PrimaryCTA: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = ({
  children,
  className = "",
  ...props
}) => (
  <button
    className={`inline-flex h-[38px] w-full items-center justify-center gap-2 rounded-lg
                bg-emerald-500 px-4 text-sm font-medium text-zinc-950
                transition-all duration-200 ease-out
                hover:bg-emerald-400 active:bg-emerald-600
                disabled:bg-zinc-800 disabled:text-zinc-600 disabled:pointer-events-none
                focus-visible:outline-none focus-visible:ring-2
                focus-visible:ring-emerald-500/50 focus-visible:ring-offset-2
                focus-visible:ring-offset-zinc-950 ${className}`}
    {...props}
  >
    {children}
  </button>
);

// ─────────────────────────────────────────────────────────────────────────────
// ASIN chip com copy-to-clipboard — §4.3 (micro-interação)
// ─────────────────────────────────────────────────────────────────────────────

const AsinChip: React.FC<{ asin: string }> = ({ asin }) => {
  const [copied, setCopied] = React.useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(asin);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1200);
    } catch {
      /* silencioso — clipboard pode estar bloqueado em iframe */
    }
  };

  return (
    <button
      type="button"
      onClick={copy}
      aria-label={`Copiar ASIN ${asin}`}
      className="inline-flex items-center gap-1.5 rounded-md border border-zinc-800
                 bg-zinc-900/60 px-2 py-1 font-mono text-[10px] tabular-nums text-zinc-400
                 transition hover:border-zinc-700 hover:text-zinc-100
                 focus-visible:outline-none focus-visible:ring-2
                 focus-visible:ring-emerald-500/50"
    >
      {copied ? <Check size={10} strokeWidth={2} /> : <Copy size={10} strokeWidth={1.5} />}
      {asin}
    </button>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// ProductCard — §3.2
// ─────────────────────────────────────────────────────────────────────────────

export const ProductCard: React.FC<{ oferta: Oferta }> = ({ oferta }) => {
  const economia = oferta.precoOriginal - oferta.precoReal;

  return (
    <article
      className="group/card flex flex-col overflow-hidden rounded-xl border border-zinc-800
                 bg-zinc-900/50 backdrop-blur
                 transition-all duration-300 ease-out
                 hover:border-emerald-500/30
                 hover:shadow-[0_0_40px_-12px_rgba(16,185,129,0.25)]
                 focus-within:border-emerald-500/40"
    >
      {/* ── Zona 1 · visual ─────────────────────────────────────────────── */}
      <div className="relative aspect-square w-full overflow-hidden bg-zinc-950">
        {oferta.imagem ? (
          <img
            src={oferta.imagem}
            alt={oferta.produto}
            loading="lazy"
            className="h-full w-full object-cover transition-transform duration-[250ms]
                       ease-[cubic-bezier(0.22,1,0.36,1)] group-hover/card:scale-[1.03]"
          />
        ) : (
          <div
            aria-hidden
            className="flex h-full w-full items-center justify-center font-mono text-[10px]
                       uppercase tracking-wider text-zinc-700"
          >
            sem imagem
          </div>
        )}

        {/* Badge de desconto (top-right) — §3.2 zona 1 */}
        <span
          aria-label={`${oferta.desconto.toFixed(1)} por cento de desconto`}
          className="absolute right-3 top-3 rounded-md bg-emerald-500 px-2 py-0.5
                     font-mono text-[11px] font-bold tabular-nums text-zinc-950
                     shadow-[0_0_20px_-4px_rgba(16,185,129,0.6)]"
        >
          −{oferta.desconto.toFixed(1)}%
        </span>

        {/* ScoreBadge sobreposto (top-left) */}
        <span className="absolute left-3 top-3">
          <ScoreBadge score={oferta.score} />
        </span>
      </div>

      {/* ── Zonas 2 + 3 · metadata + título ─────────────────────────────── */}
      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="flex items-center justify-between gap-2">
          <span className="font-sans text-[10px] uppercase tracking-wider text-zinc-500">
            {oferta.categoria}
          </span>
          <AsinChip asin={oferta.asin} />
        </div>

        <h3 className="line-clamp-2 font-sans text-sm font-medium leading-[18px] text-zinc-100">
          {oferta.produto}
        </h3>

        <div className="mt-auto flex items-center gap-2 font-mono text-[11px] text-zinc-500">
          <Star size={12} strokeWidth={1.5} className="text-amber-400" aria-hidden />
          <span className="tabular-nums text-zinc-300">{oferta.nota.toFixed(1)}</span>
          <span aria-hidden>·</span>
          <span className="tabular-nums">{compactInt(oferta.avaliacoes)} avaliações</span>
        </div>
      </div>

      {/* ── Zona 4 · preço + CTA ────────────────────────────────────────── */}
      <div className="border-t border-zinc-800/70 p-4">
        <div className="flex items-baseline gap-2">
          <span className="font-mono text-2xl font-semibold tabular-nums text-emerald-400">
            R$ {brl(oferta.precoReal)}
          </span>
          <span className="font-mono text-xs tabular-nums text-zinc-500 line-through">
            R$ {brl(oferta.precoOriginal)}
          </span>
        </div>
        <p className="mt-0.5 font-mono text-[10px] uppercase tracking-wider text-zinc-500">
          economia de <span className="text-zinc-300">R$ {brl(economia)}</span>
        </p>

        <PrimaryCTA
          className="mt-3"
          onClick={() => window.open(oferta.linkAfiliado, "_blank", "noopener,noreferrer")}
        >
          <ShoppingCart size={14} strokeWidth={1.5} aria-hidden />
          Comprar na Amazon
          <ExternalLink size={12} strokeWidth={1.5} className="opacity-70" aria-hidden />
        </PrimaryCTA>
      </div>
    </article>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Grid wrapper — demonstra uso em Bento (§2.2 small/medium spans)
// ─────────────────────────────────────────────────────────────────────────────

export const ProductGrid: React.FC<{ ofertas: Oferta[] }> = ({ ofertas }) => (
  <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    {ofertas.map((o) => (
      <ProductCard key={o.asin} oferta={o} />
    ))}
  </div>
);

// ─────────────────────────────────────────────────────────────────────────────
// Mock — reflete BackEnd/AI/ofertas_aprovadas.json
// ─────────────────────────────────────────────────────────────────────────────

export const MOCK_OFERTAS: Oferta[] = [
  {
    asin: "B09B8VC33K",
    produto: "Echo Dot (5ª Geração) Smart Speaker com Alexa",
    precoReal: 199.0, precoOriginal: 379.0, desconto: 47.5,
    nota: 4.7, avaliacoes: 18420, categoria: "Eletrônicos", score: 78.41,
    linkAfiliado: "https://www.amazon.com.br/dp/B09B8VC33K?tag=ofertahub0f0-20",
  },
  {
    asin: "B09TMF6745",
    produto: "Kindle Paperwhite (11ª Geração) 8 GB — À prova d'água",
    precoReal: 379.0, precoOriginal: 649.0, desconto: 41.6,
    nota: 4.8, avaliacoes: 22310, categoria: "E-readers", score: 76.6,
    linkAfiliado: "https://www.amazon.com.br/dp/B09TMF6745?tag=ofertahub0f0-20",
  },
  {
    asin: "B0874YJP92",
    produto: "SSD Externo Portátil Samsung T7 1TB USB 3.2",
    precoReal: 399.0, precoOriginal: 699.0, desconto: 42.9,
    nota: 4.7, avaliacoes: 16900, categoria: "Periféricos", score: 75.97,
    linkAfiliado: "https://www.amazon.com.br/dp/B0874YJP92?tag=ofertahub0f0-20",
  },
  {
    asin: "B09XS7JWHH",
    produto: "Sony WH-1000XM5 Fone de Ouvido Bluetooth Noise Canceling",
    precoReal: 1299.0, precoOriginal: 2199.0, desconto: 40.9,
    nota: 4.8, avaliacoes: 7340, categoria: "Áudio", score: 82.33,
    linkAfiliado: "https://www.amazon.com.br/dp/B09XS7JWHH?tag=ofertahub0f0-20",
  },
];

export default ProductCard;
