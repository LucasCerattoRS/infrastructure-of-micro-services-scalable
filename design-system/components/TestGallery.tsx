"use client";

// TestGallery.tsx
// OfertaHub — Galeria de stress-test do Design System.
// Valida as regras do design-system/MASTER.md:
//   §1.1–1.3 · paleta (zinc-950/900 + emerald/cyan/amber/rose)
//   §1.4–1.5 · tipografia dual (mono p/ dados, sans p/ UI) + tabular-nums
//   §2      · Bento Grid com gap-6 (1.5rem) e radius xl
//   §3.1    · ScoreBadge com 4 tiers (≥80 emerald, ≥70 cyan, ≥50 amber, <50 rose)
//   §3.2    · Product Card — 4 zonas verticais
//   §3.3    · Botões (Primary emerald, Secondary outline cyan)
//   §4.1    · Transições 200–300ms
//
// Auto-contido: arrastar para app/test-gallery/page.tsx em qualquer Next.js + Tailwind.

import React from "react";
import {
  Brain,
  Check,
  Copy,
  ExternalLink,
  Gauge,
  Headphones,
  HardDrive,
  ShoppingCart,
  Sparkles,
  Star,
  BookOpen,
} from "lucide-react";

// ═════════════════════════════════════════════════════════════════════════════
// TIPOS & DADOS (ASIN, Produto, "Preço Real", "Score Oferta" · JSON real)
// ═════════════════════════════════════════════════════════════════════════════

interface Oferta {
  asin: string;
  produto: string;
  precoReal: number;
  precoOriginal: number;
  desconto: number;
  nota: number;
  avaliacoes: number;
  categoria: string;
  score: number;            // FORÇADO para exercitar tiers
  linkAfiliado: string;
  icon: React.ReactNode;    // ícone da categoria (lucide)
}

// Produtos reais de ofertas_aprovadas.json — scores alterados para cobrir os 4 tiers.
const OFERTAS: Oferta[] = [
  {
    asin: "B09XS7JWHH",
    produto: "Sony WH-1000XM5 Fone de Ouvido Bluetooth Noise Canceling",
    precoReal: 1299.0, precoOriginal: 2199.0, desconto: 40.9,
    nota: 4.8, avaliacoes: 7340, categoria: "Áudio",
    score: 87.52,                                                   // TIER S · emerald
    linkAfiliado: "https://www.amazon.com.br/dp/B09XS7JWHH?tag=ofertahub0f0-20",
    icon: <Headphones size={12} strokeWidth={1.5} />,
  },
  {
    asin: "B09TMF6745",
    produto: "Kindle Paperwhite (11ª Geração) 8 GB — À prova d'água",
    precoReal: 379.0, precoOriginal: 649.0, desconto: 41.6,
    nota: 4.8, avaliacoes: 22310, categoria: "E-readers",
    score: 74.30,                                                   // TIER A · cyan
    linkAfiliado: "https://www.amazon.com.br/dp/B09TMF6745?tag=ofertahub0f0-20",
    icon: <BookOpen size={12} strokeWidth={1.5} />,
  },
  {
    asin: "B0874YJP92",
    produto: "SSD Externo Portátil Samsung T7 1TB USB 3.2",
    precoReal: 399.0, precoOriginal: 699.0, desconto: 42.9,
    nota: 4.7, avaliacoes: 16900, categoria: "Periféricos",
    score: 61.84,                                                   // TIER B · amber
    linkAfiliado: "https://www.amazon.com.br/dp/B0874YJP92?tag=ofertahub0f0-20",
    icon: <HardDrive size={12} strokeWidth={1.5} />,
  },
  {
    asin: "B09B8VC33K",
    produto: "Echo Dot (5ª Geração) Smart Speaker com Alexa",
    precoReal: 199.0, precoOriginal: 379.0, desconto: 47.5,
    nota: 4.7, avaliacoes: 18420, categoria: "Eletrônicos",
    score: 42.10,                                                   // TIER C · rose
    linkAfiliado: "https://www.amazon.com.br/dp/B09B8VC33K?tag=ofertahub0f0-20",
    icon: <Sparkles size={12} strokeWidth={1.5} />,
  },
];

// ═════════════════════════════════════════════════════════════════════════════
// HELPERS
// ═════════════════════════════════════════════════════════════════════════════

const brl = (v: number) =>
  v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const compactInt = (v: number) =>
  v >= 1000 ? `${(v / 1000).toFixed(1).replace(/\.0$/, "")}k` : String(v);

type Tier = "emerald" | "cyan" | "amber" | "rose";

const tierFor = (score: number): Tier =>
  score >= 80 ? "emerald" : score >= 70 ? "cyan" : score >= 50 ? "amber" : "rose";

const TIER_META: Record<Tier, { label: string; classes: string; border: string; glow: string }> = {
  emerald: {
    label: "S · Excelente",
    classes: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30",
    border: "hover:border-emerald-500/40",
    glow:   "hover:shadow-[0_0_40px_-12px_rgba(16,185,129,0.30)]",
  },
  cyan: {
    label: "A · Ótimo",
    classes: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30",
    border: "hover:border-cyan-500/40",
    glow:   "hover:shadow-[0_0_40px_-12px_rgba(6,182,212,0.30)]",
  },
  amber: {
    label: "B · Aceitável",
    classes: "text-amber-400 bg-amber-500/10 border-amber-500/30",
    border: "hover:border-amber-500/40",
    glow:   "hover:shadow-[0_0_40px_-12px_rgba(245,158,11,0.25)]",
  },
  rose: {
    label: "C · Rejeitar",
    classes: "text-rose-400 bg-rose-500/10 border-rose-500/30",
    border: "hover:border-rose-500/40",
    glow:   "hover:shadow-[0_0_40px_-12px_rgba(244,63,94,0.25)]",
  },
};

// ═════════════════════════════════════════════════════════════════════════════
// ÁTOMOS
// ═════════════════════════════════════════════════════════════════════════════

const ScoreBadge: React.FC<{ score: number }> = ({ score }) => (
  <span
    aria-label={`Score IA ${score.toFixed(2)} de 100`}
    className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5
                font-mono text-[11px] font-semibold tabular-nums ${TIER_META[tierFor(score)].classes}`}
  >
    {score.toFixed(2)}
  </span>
);

const LiveDot: React.FC = () => (
  <span className="flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-wider text-emerald-400">
    <span className="relative flex h-2 w-2">
      <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
      <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
    </span>
    LIVE
  </span>
);

const AsinChip: React.FC<{ asin: string }> = ({ asin }) => {
  const [copied, setCopied] = React.useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(asin);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1200);
    } catch {}
  };
  return (
    <button
      type="button"
      onClick={copy}
      aria-label={`Copiar ASIN ${asin}`}
      className="inline-flex items-center gap-1.5 rounded-md border border-zinc-800
                 bg-zinc-900/60 px-2 py-1 font-mono text-[10px] tabular-nums text-zinc-400
                 transition-colors duration-200
                 hover:border-zinc-700 hover:text-zinc-100
                 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/50"
    >
      {copied ? <Check size={10} strokeWidth={2} /> : <Copy size={10} strokeWidth={1.5} />}
      {asin}
    </button>
  );
};

const PrimaryCTA: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = ({
  children, className = "", ...rest
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
    {...rest}
  >
    {children}
  </button>
);

// ═════════════════════════════════════════════════════════════════════════════
// PRODUTO CARD — §3.2
// ═════════════════════════════════════════════════════════════════════════════

const ProdutoCard: React.FC<{ oferta: Oferta }> = ({ oferta }) => {
  const tier = tierFor(oferta.score);
  const meta = TIER_META[tier];
  const economia = oferta.precoOriginal - oferta.precoReal;

  return (
    <article
      className={`group/card flex flex-col overflow-hidden rounded-xl border border-zinc-800
                  bg-zinc-900/50 backdrop-blur
                  transition-all duration-300 ease-out
                  ${meta.border} ${meta.glow}`}
    >
      {/* Zona 1 · visual placeholder (aspect-square) */}
      <div className="relative aspect-square w-full overflow-hidden bg-zinc-950">
        <div
          aria-hidden
          className="flex h-full w-full items-center justify-center"
          style={{
            backgroundImage:
              "radial-gradient(circle at 30% 30%, rgba(255,255,255,0.035), transparent 55%), linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)",
            backgroundSize: "auto, 24px 24px, 24px 24px",
            backgroundColor: "#09090b",
            opacity: 1,
          }}
        >
          <div className="flex flex-col items-center gap-2 text-zinc-700">
            {React.cloneElement(oferta.icon as React.ReactElement, { size: 36, strokeWidth: 1 })}
            <span className="font-mono text-[10px] uppercase tracking-wider">mock image</span>
          </div>
        </div>

        {/* ScoreBadge top-left */}
        <span className="absolute left-3 top-3">
          <ScoreBadge score={oferta.score} />
        </span>

        {/* Desconto top-right */}
        <span
          aria-label={`${oferta.desconto.toFixed(1)} por cento de desconto`}
          className="absolute right-3 top-3 rounded-md bg-emerald-500 px-2 py-0.5
                     font-mono text-[11px] font-bold tabular-nums text-zinc-950
                     shadow-[0_0_20px_-4px_rgba(16,185,129,0.6)]"
        >
          −{oferta.desconto.toFixed(1)}%
        </span>

        {/* Tier label bottom-left */}
        <span
          className={`absolute bottom-3 left-3 inline-flex items-center gap-1 rounded-md border
                      px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider ${meta.classes}`}
        >
          <Gauge size={10} strokeWidth={1.5} />
          {meta.label}
        </span>
      </div>

      {/* Zonas 2 + 3 · metadata + título */}
      <div className="flex flex-1 flex-col gap-2 p-4">
        <div className="flex items-center justify-between gap-2">
          <span className="inline-flex items-center gap-1 font-sans text-[10px] uppercase tracking-wider text-zinc-500">
            {oferta.icon}
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

      {/* Zona 4 · preço + CTA */}
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

// ═════════════════════════════════════════════════════════════════════════════
// LEGENDA DE TIERS (diagnóstico visual)
// ═════════════════════════════════════════════════════════════════════════════

const TierLegend: React.FC = () => (
  <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
    {(Object.entries(TIER_META) as [Tier, (typeof TIER_META)[Tier]][]).map(([tier, meta]) => {
      const sample = { emerald: 87.52, cyan: 74.3, amber: 61.84, rose: 42.1 }[tier];
      const range = { emerald: "≥ 80", cyan: "70 – 79", amber: "50 – 69", rose: "< 50" }[tier];
      return (
        <div
          key={tier}
          className="flex items-center justify-between rounded-lg border border-zinc-800 bg-zinc-900/40 px-3 py-2"
        >
          <div className="flex flex-col">
            <span className="font-sans text-[10px] uppercase tracking-wider text-zinc-500">
              {meta.label}
            </span>
            <span className="font-mono text-[11px] tabular-nums text-zinc-400">{range}</span>
          </div>
          <ScoreBadge score={sample} />
        </div>
      );
    })}
  </div>
);

// ═════════════════════════════════════════════════════════════════════════════
// PAINEL TIPOGRÁFICO (mono vs sans — §1.4–1.5)
// ═════════════════════════════════════════════════════════════════════════════

const TypographyProbe: React.FC = () => (
  <section className="grid grid-cols-1 gap-4 rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 lg:grid-cols-2">
    <div>
      <p className="mb-2 font-sans text-[10px] uppercase tracking-[0.14em] text-zinc-500">
        font-sans · Inter / Geist Sans
      </p>
      <p className="font-sans text-sm text-zinc-300">
        Curadoria de ofertas em tempo real, processadas pelo Gerente IA.
      </p>
      <p className="mt-1 font-sans text-xs text-zinc-500">
        Usado em: títulos, parágrafos, rótulos de UI.
      </p>
    </div>
    <div>
      <p className="mb-2 font-sans text-[10px] uppercase tracking-[0.14em] text-zinc-500">
        font-mono · JetBrains Mono / Geist Mono · tabular-nums
      </p>
      <p className="font-mono text-sm tabular-nums text-zinc-300">
        ASIN B09XS7JWHH · R$ 1.299,00 · 87.52 / 100 · −40.9%
      </p>
      <p className="mt-1 font-mono text-[11px] text-zinc-500">
        Usado em: preços, scores, ASINs, timestamps.
      </p>
    </div>
  </section>
);

// ═════════════════════════════════════════════════════════════════════════════
// PÁGINA
// ═════════════════════════════════════════════════════════════════════════════

export default function TestGallery() {
  return (
    <main className="min-h-screen bg-zinc-950 font-sans text-zinc-200 antialiased">
      {/* grid backdrop sutil — MASTER.md §2.5 */}
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 opacity-[0.035]"
        style={{
          backgroundImage:
            "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)",
          backgroundSize: "40px 40px",
        }}
      />

      <header className="relative border-b border-zinc-900 px-6 py-5">
        <div className="mx-auto flex max-w-[1600px] items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-emerald-500/30 bg-emerald-500/10">
              <Brain size={18} strokeWidth={1.5} className="text-emerald-400" />
            </div>
            <div>
              <h1 className="font-sans text-sm font-semibold tracking-tight">
                OfertaHub · Test Gallery
              </h1>
              <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-zinc-500">
                ground zero · design-system/MASTER.md v1.0.0
              </p>
            </div>
          </div>
          <div className="hidden items-center gap-6 font-mono text-[11px] text-zinc-400 md:flex">
            <span>env: <span className="text-emerald-400">fedora 43</span></span>
            <span>affiliate: <span className="text-cyan-400">ofertahub0f0-20</span></span>
            <LiveDot />
          </div>
        </div>
      </header>

      <section className="relative mx-auto max-w-[1600px] space-y-6 p-6">
        {/* legenda de tiers */}
        <div>
          <h2 className="mb-3 font-sans text-[11px] font-medium uppercase tracking-[0.14em] text-zinc-400">
            Tiers de Score IA · §3.1
          </h2>
          <TierLegend />
        </div>

        {/* probe tipográfico */}
        <div>
          <h2 className="mb-3 font-sans text-[11px] font-medium uppercase tracking-[0.14em] text-zinc-400">
            Dual Typography Probe · §1.4
          </h2>
          <TypographyProbe />
        </div>

        {/* Bento Grid — gap-6 (1.5rem), responsivo */}
        <div>
          <h2 className="mb-3 font-sans text-[11px] font-medium uppercase tracking-[0.14em] text-zinc-400">
            Bento Grid · §2 · gap-6 · rounded-xl
          </h2>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-4">
            {OFERTAS.map((o) => (
              <ProdutoCard key={o.asin} oferta={o} />
            ))}
          </div>
        </div>

        <footer className="pt-6 font-mono text-[10px] uppercase tracking-wider text-zinc-600">
          <p>
            4 cards · 4 tiers · ASINs reais de ofertas_aprovadas.json · scores forçados para
            validação visual.
          </p>
        </footer>
      </section>
    </main>
  );
}
