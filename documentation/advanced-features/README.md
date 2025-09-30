# Advanced Features

Specialized capabilities for R-Grade users including AI agents, DNA analysis, financial intelligence, and Web3.

## 🚀 Feature Overview

### [Agentic Network](agentic-network.md) 🤖
Multi-agent collaboration with Nyx, G1 Black, and Kronos.
- `/ask <agent>` - Query AI agents
- `/ask g1 live` - Real-time voice
- `/room` - Collaboration spaces

### [DNA Analysis](dna-analysis.md) 🧬
GDDA bioinformatics system.
- `/dna <sequence>` - Analyze DNA/RNA/Protein
- Structure prediction
- Homology search
- Database cross-refs

### [Financial Intelligence](financial-intelligence.md) 📊
Real-time market data via Yahoo Finance.
- `/markets <stock>` - Stock data
- `/markets <crypto>` - Crypto prices
- `/markets compare` - Stock comparison

### [Web3 & Blockchain](web3-blockchain.md) 🔗
Multi-chain operations on Base, Ethereum, Polygon.
- `/0x buy/sell` - Token trading
- `/0x send` - Transfers
- `/0x receive` - View wallets

## ⚠️ Access Requirements

**All advanced features require R-Grade (Master) access.**

R-Grade users have `arpa_id` starting with 'R' in kun.py:
```python
'arpa_id': 'R001'  # R-Grade Master access
```

A-Grade users (`arpa_id` starting with 'A') cannot access these features.

## 🚀 Quick Examples

**Agentic Network:**
```bash
/ask Nyx Design a blockchain voting system
/ask g1 live
/room nyx, g1: Quantum computing
```

**DNA Analysis:**
```bash
/dna ATGCGTAACGGCATTAGC
/dna --verbose --homology MAKVLISPKQW
```

**Financial:**
```bash
/markets tesla
/markets btc
/markets compare tsla nio
```

**Web3:**
```bash
/0x buy 10 degen using eth on base
/0x send base eth 0.1 to Ross
/0x receive
```

## 📖 Learn More

- [Command Reference](../api-reference/command-reference.md)
- [System Architecture](../system-architecture/core-components.md)

---

**Advanced features for power users.** ⚡