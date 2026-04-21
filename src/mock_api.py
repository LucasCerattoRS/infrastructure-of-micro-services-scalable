"""
Mock da Amazon Product Advertising API.
ASINs verificados na Amazon.com.br — produtos com histórico estável de vendas.
Cobre todos os caminhos da lógica de filtragem: aprovados, rejeitados por cada critério.
"""

import random

_PRODUTOS_MOCK = [
    # ── APROVADOS ──────────────────────────────────────────────────────────
    {
        "asin": "B09B8VC33K",   # Echo Dot (5ª Geração) — Amazon BR
        "titulo": "Echo Dot (5ª Geração) Smart Speaker com Alexa",
        "preco_atual": 199.00,
        "preco_original": 379.00,
        "nota": 4.7,
        "total_avaliacoes": 18420,
        "categoria": "Eletrônicos",
    },
    {
        "asin": "B0BJ3BNVDM",   # Fire TV Stick 4K Max (2ª Geração)
        "titulo": "Fire TV Stick 4K Max com Alexa Voice Remote",
        "preco_atual": 269.00,
        "preco_original": 449.00,
        "nota": 4.6,
        "total_avaliacoes": 9870,
        "categoria": "Eletrônicos",
    },
    {
        "asin": "B0BSXW3FGF",   # Kindle (11ª Geração) — sem luz
        "titulo": "Kindle (11ª Geração) 16 GB — o Kindle mais leve",
        "preco_atual": 299.00,
        "preco_original": 499.00,
        "nota": 4.7,
        "total_avaliacoes": 14650,
        "categoria": "E-readers",
    },
    {
        "asin": "B09TMF6745",   # Kindle Paperwhite (11ª Geração)
        "titulo": "Kindle Paperwhite (11ª Geração) 8 GB — À prova d'água",
        "preco_atual": 379.00,
        "preco_original": 649.00,
        "nota": 4.8,
        "total_avaliacoes": 22310,
        "categoria": "E-readers",
    },
    {
        "asin": "B09XS7JWHH",   # Sony WH-1000XM5
        "titulo": "Sony WH-1000XM5 Fone de Ouvido Bluetooth Noise Canceling",
        "preco_atual": 1299.00,
        "preco_original": 2199.00,
        "nota": 4.8,
        "total_avaliacoes": 7340,
        "categoria": "Áudio",
    },
    {
        "asin": "B09KRDPQTZ",   # JBL Flip 6
        "titulo": "JBL Flip 6 Caixa de Som Bluetooth À Prova d'Água",
        "preco_atual": 499.00,
        "preco_original": 849.00,
        "nota": 4.6,
        "total_avaliacoes": 11230,
        "categoria": "Áudio",
    },
    {
        "asin": "B09TM3TFJM",   # Logitech G502 X
        "titulo": "Mouse Gamer Logitech G502 X 25600 DPI LIGHTFORCE",
        "preco_atual": 379.00,
        "preco_original": 649.00,
        "nota": 4.7,
        "total_avaliacoes": 4820,
        "categoria": "Periféricos",
    },
    {
        "asin": "B0874YJP92",   # Samsung T7 SSD Portátil 1TB
        "titulo": "SSD Externo Portátil Samsung T7 1TB USB 3.2",
        "preco_atual": 399.00,
        "preco_original": 699.00,
        "nota": 4.7,
        "total_avaliacoes": 16900,
        "categoria": "Periféricos",
    },
    {
        "asin": "B07VGBBQ2Q",   # TP-Link Tapo C200
        "titulo": "Câmera de Segurança Wi-Fi TP-Link Tapo C200 Full HD 360°",
        "preco_atual": 159.00,
        "preco_original": 279.00,
        "nota": 4.4,
        "total_avaliacoes": 8650,
        "categoria": "Segurança",
    },
    {
        "asin": "B08384MFKP",   # iRobot Roomba 692
        "titulo": "Robô Aspirador iRobot Roomba 692 Wi-Fi com Alexa",
        "preco_atual": 1399.00,
        "preco_original": 2499.00,
        "nota": 4.3,
        "total_avaliacoes": 3210,
        "categoria": "Eletrodomésticos",
    },

    # ── REJEITADOS (cobrem todos os critérios de triagem) ──────────────────
    {
        "asin": "B0C3QBX3PT",
        "titulo": "Cabo USB-C sem Marca 1m Carga Rápida",   # marca bloqueada "sem marca"
        "preco_atual": 24.90,
        "preco_original": 39.90,
        "nota": 4.2,
        "total_avaliacoes": 310,
        "categoria": "Acessórios",
    },
    {
        "asin": "B0CJLVJQS3",
        "titulo": "Tablet Samsung Galaxy Tab A9+ 11'' 128GB",
        "preco_atual": 1599.00,
        "preco_original": 1749.00,  # desconto 8.6% — abaixo de 20%
        "nota": 4.5,
        "total_avaliacoes": 2140,
        "categoria": "Eletrônicos",
    },
    {
        "asin": "B0B9X9QGKZ",
        "titulo": "Fone de Ouvido In-Ear Importado S/ Garantia BR",
        "preco_atual": 79.90,
        "preco_original": 159.00,
        "nota": 3.1,               # nota 3.1 — abaixo de 4.0
        "total_avaliacoes": 890,
        "categoria": "Áudio",
    },
    {
        "asin": "B0CKWQHX3R",
        "titulo": "Suporte Articulado para Monitor Dual",
        "preco_atual": 89.90,
        "preco_original": 159.00,
        "nota": 4.3,
        "total_avaliacoes": 28,    # apenas 28 avaliações — abaixo de 50
        "categoria": "Periféricos",
    },
]


def buscar_produtos(categoria: str = "geral", limite: int = 20) -> list[dict]:
    """Simula resposta paginada da API retornando produtos brutos."""
    return random.sample(_PRODUTOS_MOCK, min(limite, len(_PRODUTOS_MOCK)))
