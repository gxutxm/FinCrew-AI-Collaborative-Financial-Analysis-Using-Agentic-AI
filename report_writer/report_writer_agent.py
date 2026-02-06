def validate_inputs(market_data, quant_data):
    required_market = ["sentiment", "confidence_score", "key_risks", "summary"]
    required_quant = ["volatility", "avg_return", "RSI", "max_drawdown"]

    for key in required_market:
        if key not in market_data:
            raise ValueError(f"Missing market field: {key}")

    for key in required_quant:
        if key not in quant_data:
            raise ValueError(f"Missing quant field: {key}")

    return True


def generate_full_report(market_data, quant_data):
    validate_inputs(market_data, quant_data)

    report = f"""
FINANCIAL ANALYSIS REPORT

Market Sentiment:
{market_data['sentiment']} (Confidence: {market_data['confidence_score']})

Summary:
- {'; '.join(market_data['summary'])}

Quantitative Metrics:
- Average Return: {quant_data['avg_return']}
- Volatility: {quant_data['volatility']}
- RSI: {quant_data['RSI']}
- Max Drawdown: {quant_data['max_drawdown']}

Key Risks:
- {'; '.join(market_data['key_risks'])}

Disclaimer:
This report is generated automatically and is not financial advice.
"""
    return report


if __name__ == "__main__":
    market_example = {
        "sentiment": "Bullish",
        "confidence_score": 0.72,
        "key_risks": ["Inflation", "Regulatory pressure"],
        "summary": ["Strong earnings", "Positive outlook"]
    }

    quant_example = {
        "volatility": 0.21,
        "avg_return": 0.015,
        "RSI": 62,
        "max_drawdown": -0.18
    }

    print(generate_full_report(market_example, quant_example))

