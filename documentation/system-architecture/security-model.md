# Security Model

OPSIIE security architecture.

## 🔐 Authentication

**Facial Recognition**: OpenCV, MSE matching
**Threshold**: 1000 (configurable)
**Photo**: kun.py user['picture']

## 🔑 Access Control

**R-Grade**: ARPA ID R### (full access)
**A-Grade**: ARPA ID A### (core only)

## 🔒 Secret Management

**.env**: API keys, DB credentials, private keys
**kun.py**: User profiles, public data only

**Best Practices**:
- Use .env.example template
- Rotate keys quarterly
- Gmail: App password (not account password)
- Never commit .env

## 🌐 Network Security

**Web3**: Private key protected, checksum addresses
**APIs**: HTTPS only, keys in headers
**Email**: App password, 2FA required

## 💾 Data Security

**PostgreSQL**: Password protected, local only
**Files**: Local access only, no uploads
**Privacy**: No telemetry, local system only

## 🛡️ Security Checklist

- [ ] .env from example, unique keys
- [ ] Gmail app password
- [ ] PostgreSQL password secured
- [ ] Web3 private key secured
- [ ] ARPA IDs verified
- [ ] Regular key rotation

---

**Security by design.** 🛡️
