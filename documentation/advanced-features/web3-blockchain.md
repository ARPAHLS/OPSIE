# Web3 & Blockchain

Multi-chain Web3 operations on Base, Ethereum, and Polygon networks.

## 🔗 Overview

Web3 capabilities:
- Token trading (buy/sell)
- Token transfers
- Multi-chain support
- Gas strategy control
- Custom token/chain addition
- DEX integration

## 🌐 Supported Chains

**Base** (Chain ID: 8453)
- Native: ETH
- Explorer: basescan.org

**Ethereum** (Chain ID: 1)
- Native: ETH
- Explorer: etherscan.io

**Polygon** (Chain ID: 137)
- Native: MATIC
- Explorer: polygonscan.com

## 💰 Supported Tokens

**Degen**: Base network
**USDC**: Base, Ethereum, Polygon

## 📝 Commands

### Buy Tokens
```bash
/0x buy <amount> <token> using <token> on <chain>
```

**Examples:**
```bash
/0x buy 10 degen using eth on base
/0x buy 100 usdc using eth on ethereum
/0x buy 50 degen using usdc on base
```

### Sell Tokens
```bash
/0x sell <amount> <token> for <token> on <chain>
```

**Examples:**
```bash
/0x sell 5 degen for eth on base
/0x sell 100 usdc for eth on polygon
/0x sell 10 degen for usdc on base
```

### Send Tokens
```bash
/0x send <chain> <token> <amount> to <recipient>
```

**Examples:**
```bash
/0x send base eth 0.1 to Ross
/0x send polygon usdc 100 to Alice
/0x send base degen 50 to R001
```

Recipients resolved from kun.py contacts.

### View Addresses
```bash
/0x receive
```

Shows wallet addresses and supported assets.

### Gas Strategy
```bash
/0x gas <low|medium|high>
```

**Levels:**
- **low**: 80% of current gas
- **medium**: 100% (default)
- **high**: 150%

### Add Custom Token
```bash
/0x new token <name> <chain> <address>
```

**Example:**
```bash
/0x new token pepe base 0x123...def
```

### Add Custom Chain
```bash
/0x new chain <name> <chain_id> <rpc_url>
```

**Example:**
```bash
/0x new chain avalanche 43114 https://api.avax.network/ext/bc/C/rpc
```

### Remove Configuration
```bash
/0x forget token <name>
/0x forget chain <name>
```

**Note:** Base chains (Base, Ethereum, Polygon) cannot be removed.

## 🔧 Configuration

### Required in .env
```env
AGENT_PRIVATE_KEY=0x...
BASE_RPC_URL=https://...
ETHEREUM_RPC_URL=https://...
POLYGON_RPC_URL=https://...
```

### OPSIIE Wallet
```python
AGENT_WALLET = {
    'private_key': AGENT_PRIVATE_KEY,
    'public_key': '0x89A7f83Db9C1919B89370182002ffE5dfFc03e21'
}
```

## 💡 Transaction Flow

1. Parse command intent
2. Get price quote from DEX
3. Display preview with USD values
4. Request confirmation
5. Execute on-chain
6. Display explorer link

### Price Quotes
- Best price from DEX routers
- Exchange rates calculated
- USD values shown
- Slippage tolerance: 0.5%

### DEX Routers
- **Base**: BaseSwap
- **Ethereum**: Uniswap V2
- **Polygon**: QuickSwap

## 🚨 Troubleshooting

**Insufficient balance:** Check wallet funds
**Transaction failed:** Increase gas, check approvals
**Invalid address:** Use checksummed addresses
**RPC error:** Verify RPC URLs in .env

## 🎯 Use Cases

**Token Trading:**
```bash
/0x buy 10 degen using eth on base
/0x sell 5 degen for eth on base
```

**Transfers:**
```bash
/0x send base eth 0.1 to Ross
```

**Portfolio Management:**
```bash
/0x receive  # View holdings
/0x gas high  # Priority transactions
```

## 🔐 Security

- Private keys in .env (never commit)
- Transaction confirmation required
- Checksummed addresses enforced
- Gas limit protections

## 📊 Access Control

**R-Grade Required** for all /0x features

---


**Decentralized finance at your command.** 🔗

**For an advanced self-sustainable version of Opsie's Web3 Capabilities, check [Hermes3 (H3)](https://github.com/arpahls/h3/) who specializes in Web3 Operations, can perform everything Opsie does in Web3 and more, and all in dynamic abstract NLP**
