symbols = ["BTC", "BNB", "ETH", "SOL"]
results = []


def calcular_ema(closes, periodo):
    k = 2 / (periodo + 1)
    ema = sum(closes[:periodo]) / periodo
    for preco in closes[periodo:]:
        ema = preco * k + ema * (1 - k)
    return ema


def calcular_rsi(closes, periodo=14):
    ganhos = []
    perdas = []
    for j in range(1, periodo + 1):
        diff = closes[j] - closes[j - 1]
        if diff >= 0:
            ganhos.append(diff)
            perdas.append(0)
        else:
            ganhos.append(0)
            perdas.append(abs(diff))
    media_ganho = sum(ganhos) / periodo
    media_perda = sum(perdas) / periodo
    if media_perda == 0:
        return 100
    rs = media_ganho / media_perda
    return 100 - (100 / (1 + rs))


def calcular_macd(closes):
    ema12 = calcular_ema(closes, 12)
    ema26 = calcular_ema(closes, 26)
    macd_line = ema12 - ema26
    ema12_prev = calcular_ema(closes[:-1], 12)
    ema26_prev = calcular_ema(closes[:-1], 26)
    macd_prev = ema12_prev - ema26_prev
    signal = (macd_line + macd_prev) / 2
    histogram = macd_line - signal
    return histogram


for i, symbol in enumerate(symbols):
    candles = [item["json"] for item in _items[i * 30: (i + 1) * 30]]
    closes = [float(candle[4]) for candle in candles]
    preco_brl = closes[-1]
    ema20 = calcular_ema(closes, 20)
    forca_relativa = calcular_rsi(closes)
    tendencia_mercado = calcular_macd(closes)
    preco_brl_fmt = f"R$ {preco_brl:,.2f}"
    ema20_fmt = f"R$ {ema20:,.2f}"
    rsi_fmt = f"{forca_relativa:.1f}"
    hora_utc = ""

    sep = "━" * 26
    if forca_relativa < 25:
        emoji = "🔵"
        titulo = f"QUEDA INTENSA — {symbol}/USDT"
        macd_txt = "Momentum negativo forte"
        tendencia = "Possível fundo se formando"
        conclusao = "⚡ Entrada especulativa de risco alto"

    elif forca_relativa < 35 and preco_brl < ema20 and tendencia_mercado > 0:
        emoji = "🟢"
        titulo = f"COMPRA FORTE — {symbol}/USDT"
        macd_txt = "Cruzamento altista"
        tendencia = f"Abaixo da EMA20 ({ema20_fmt})"
        conclusao = "✅ Ativo subvalorizado com reversão"

    elif 50 < forca_relativa < 65 and tendencia_mercado < 0:
        emoji = "🟡"
        titulo = f"ATENÇÃO — {symbol}/USDT"
        macd_txt = "Histograma negativo"
        tendencia = "Força compradora diminuindo"
        conclusao = "⚠️  Tendência virando — fique alerta"

    elif forca_relativa > 65 and preco_brl > ema20 and tendencia_mercado < 0:
        emoji = "🔴"
        titulo = f"VENDA — {symbol}/USDT"
        macd_txt = "Divergência baixista"
        tendencia = f"Acima da EMA20 ({ema20_fmt})"
        conclusao = "🚨 Sobrecomprado — considere realizar"

    else:
        emoji = "⚪"
        titulo = f"NEUTRO — {symbol}/USDT"
        macd_txt = "Sem sinal claro"
        tendencia = "Mercado lateral"
        conclusao = "💤 Aguardando confirmação"

    # ── Monta a mensagem formatada ───────────────────────────
    sinal = (
        f"{emoji} *{titulo}*\n"
        f"{sep}\n"
        f"💰 Preço atual:  *{preco_brl_fmt}*\n"
        f"📊 RSI (14):     *{rsi_fmt}*\n"
        f"📈 MACD:         {macd_txt}\n"
        f"📉 EMA20:        {tendencia}\n"
        f"{sep}\n"
        f"{conclusao}\n"
        f"🕐 {hora_utc}"
    )

    results.append({
        "json": {
            "moeda": symbol,
            "preco_brl": preco_brl,
            "rsi": forca_relativa,
            "sinal": sinal,
        }
    })

return results
