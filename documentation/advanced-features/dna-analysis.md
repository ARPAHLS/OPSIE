# DNA Analysis - GDDA System

Genetic Due Diligence Analysis (GDDA) v0.21 XP for bioinformatics.

## 🧬 Command

### /dna - Analyze Sequence
```bash
/dna <sequence> [options]
```

**Examples:**
```bash
/dna ATGCGTAACGGCATTAGC        # DNA
/dna AUGCGUAACGGCAUUAGC        # RNA
/dna MAKVLISPKQW               # Protein
/dna --verbose ATGCGTAACGGC    # Detailed
/dna --homology MAKVLISPKQW    # With search
```

## 🔬 Features

**Basic**: Type detection, GC content, k-mer frequency
**Structure**: DNA melting temp, RNA secondary, protein prediction
**Advanced**: Homology search, patents, literature
**RNA**: miRNA sites, siRNA regions, Rfam/miRBase refs
**Protein**: Weight, localization, UniProt/Pfam refs

## ⚙️ Options

`--verbose` `--type` `--format` `--export` `--homology` `--structure` `--patents` `--literature`

## 🔧 Setup

```env
NCBI_EMAIL=your_email@example.com
```

**R-Grade Required**

---

**Bioinformatics intelligence.** 🧬
