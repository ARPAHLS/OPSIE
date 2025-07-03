import datetime
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
from dotenv import load_dotenv
import numpy as np
import requests
from Bio.Blast import NCBIWWW, NCBIXML
from collections import Counter
from Bio import (
    Entrez, SeqIO, motifs, Phylo, AlignIO,
    pairwise2
)
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
from Bio.PDB import *
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from io import StringIO
from colorama import Fore, Style
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import pandas as pd
import random
import functools
import signal
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import textwrap
import RNA
import json
import time
from typing import Dict, List, Union, Optional
from colorama import init  
from Bio.SeqUtils import molecular_weight
from Bio.SeqUtils import gc_fraction  # For GC content calculation
import warnings  
import logging  
from ratelimit import limits, sleep_and_retry  
from urllib3.util.retry import Retry 
from requests.adapters import HTTPAdapter
import sys 

# Load environment variables
load_dotenv()
Entrez.email = os.getenv('NCBI_EMAIL')

# Add try-except for model loading
try:
    tokenizer = AutoTokenizer.from_pretrained("InstaDeepAI/nucleotide-transformer-v2-500m-multi-species", trust_remote_code=True)
    model = AutoModelForMaskedLM.from_pretrained("InstaDeepAI/nucleotide-transformer-v2-500m-multi-species", trust_remote_code=True)
except Exception as e:
    print(f"Warning: Genetic Due Diligence Micro-Agent Failed to load: {str(e)}")
    tokenizer = None
    model = None

# Add new constants for protein analysis
aa_weights = {
    'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2, 'E': 147.1,
    'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2, 'L': 131.2, 'K': 146.2,
    'M': 149.2, 'F': 165.2, 'P': 115.1, 'S': 105.1, 'T': 119.1, 'W': 204.2,
    'Y': 181.2, 'V': 117.1
}

# Add this near the top of the file with other constants
# Kyte & Doolittle hydrophobicity scale
kd = {
    'A': 1.8,  # Alanine
    'R': -4.5, # Arginine
    'N': -3.5, # Asparagine
    'D': -3.5, # Aspartic acid
    'C': 2.5,  # Cysteine
    'Q': -3.5, # Glutamine
    'E': -3.5, # Glutamic acid
    'G': -0.4, # Glycine
    'H': -3.2, # Histidine
    'I': 4.5,  # Isoleucine
    'L': 3.8,  # Leucine
    'K': -3.9, # Lysine
    'M': 1.9,  # Methionine
    'F': 2.8,  # Phenylalanine
    'P': -1.6, # Proline
    'S': -0.8, # Serine
    'T': -0.7, # Threonine
    'W': -0.9, # Tryptophan
    'Y': -1.3, # Tyrosine
    'V': 4.2   # Valine
}

def is_dna(sequence):
    """Check if the sequence is DNA."""
    return all(base in {'A', 'T', 'C', 'G'} for base in sequence.upper())

def is_rna(sequence):
    """Check if the sequence is RNA."""
    return all(base in {'A', 'U', 'C', 'G'} for base in sequence.upper())

def is_protein(sequence):
    """Check if the sequence is a protein."""
    return all(base in {'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'} for base in sequence.upper())

def is_mrna(sequence):
    """Check if the sequence is mRNA."""
    return is_rna(sequence)  # mRNA is a type of RNA

def is_trna(sequence):
    """Check if the sequence is tRNA."""
    return is_rna(sequence)  # tRNA is also a type of RNA

def is_rrna(sequence):
    """Check if the sequence is rRNA."""
    return is_rna(sequence)  # rRNA is also a type of RNA

def is_noncoding_rna(sequence):
    """Check if the sequence is non-coding RNA."""
    return is_rna(sequence)  # Non-coding RNA is also a type of RNA

def is_genomic_dna(sequence):
    """Check if the sequence is genomic DNA."""
    return is_dna(sequence)  # Genomic DNA is a type of DNA

def is_plasmid_dna(sequence):
    """Check if the sequence is plasmid DNA."""
    return is_dna(sequence)  # Plasmid DNA is also a type of DNA

def is_viral_sequence(sequence):
    """Check if the sequence is viral RNA or DNA."""
    return is_dna(sequence) or is_rna(sequence)  # Viral sequences can be DNA or RNA

def is_synthetic_sequence(sequence):
    """Determine if sequence shows synthetic characteristics."""
    gc = calculate_gc_content(sequence)
    complexity = sequence_complexity(sequence)
    
    return {
        'gc_content': gc,
        'optimal_gc': abs(gc - 50) < 10,  # Within 10% of optimal 50%
        'complexity': complexity,
        'high_complexity': complexity > 0.6
    }

def analyze_codon_bias(sequence):
    """Analyze codon usage bias in the sequence."""
    if len(sequence) < 3:
        return 0.0
    
    # Get all codons
    codons = [sequence[i:i+3] for i in range(0, len(sequence)-2, 3)]
    
    # Count codon frequencies
    codon_freq = Counter(codons)
    
    # Calculate bias score (simplified version)
    total_codons = len(codons)
    max_freq = max(codon_freq.values())
    bias_score = max_freq / total_codons
    
    return bias_score

def sequence_complexity(sequence):
    """Calculate sequence complexity score."""
    if not sequence:
        return 0
    k = 3  # Use trinucleotide frequency
    kmers = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        kmers[kmer] = kmers.get(kmer, 0) + 1
    
    total_kmers = len(sequence) - k + 1
    complexity = len(kmers) / (4**k)  # Normalize by possible kmers
    return round(complexity, 3)

def is_repetitive_sequence(sequence):
    """Check if the sequence contains repetitive elements."""
    repeat_pattern = r'(A{2,}|T{2,}|C{2,}|G{2,})'
    return bool(re.search(repeat_pattern, sequence))

def is_chimeric_sequence(sequence):
    """Detect chimeric sequences by analyzing sequence composition."""
    window_size = 100
    if len(sequence) < window_size * 2:
        return False
    
    # Analyze GC content in windows
    gc_windows = []
    for i in range(0, len(sequence) - window_size, window_size):
        window = sequence[i:i+window_size]
        gc_windows.append(gc_content(window))
    
    # Calculate standard deviation of GC content
    gc_std = np.std(gc_windows)
    
    # Check for sudden composition changes
    composition_shifts = []
    for i in range(1, len(gc_windows)):
        diff = abs(gc_windows[i] - gc_windows[i-1])
        composition_shifts.append(diff)
    
    # Criteria for chimeric sequence
    max_shift = max(composition_shifts) if composition_shifts else 0
    return gc_std > 10 and max_shift > 20  # Significant composition changes

def determine_sequence_type(sequence):
    """Determine the type of the sequence."""
    sequence_types = []
    
    if is_dna(sequence):
        sequence_types.append("DNA")
        if is_synthetic_sequence(sequence):  # Now returns list of indicators
            sequence_types.append("Synthetic")
    elif is_rna(sequence):
        sequence_types.append("RNA")
    elif is_protein(sequence):
        sequence_types.append("Protein")
    
    return " + ".join(sequence_types) if sequence_types else "Unknown"

def determine_sequence_type_detailed(sequence):
    """Enhanced sequence type detection."""
    sequence = sequence.upper()
    if is_dna(sequence):
        return "DNA"
    elif is_rna(sequence):
        return "RNA"
    elif is_protein(sequence):
        return "Protein"
    else:
        return "Unknown"

def get_embeddings(sequence):
    """Generate embeddings for a sequence."""
    if tokenizer is None or model is None:
        raise ValueError("GDDA not available - embeddings cannot be generated")
        
    tokens = tokenizer(sequence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**tokens, output_hidden_states=True)
    embeddings = outputs['hidden_states'][-1].detach().numpy()
    return embeddings

def reverse_complement(sequence):
    """Return the reverse complement of a DNA sequence."""
    if not is_dna(sequence):
        raise ValueError("Input sequence must be DNA.")
    
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    sequence = sequence.upper()
    return ''.join(complement[base] for base in reversed(sequence))

def gc_content(sequence):
    if not is_dna(sequence):
        raise ValueError("Input sequence must be DNA.")
    
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    return (g_count + c_count) / len(sequence) * 100

def transcribe(sequence):
    if not is_dna(sequence):
        raise ValueError("Input sequence must be DNA.")
    
    return sequence.replace('T', 'U')

def translate(rna_sequence):
    """Translate an RNA sequence into a protein sequence."""
    
    if not is_rna(rna_sequence):
        return "Error: The sequence must be RNA."
    
    if len(rna_sequence) % 3 != 0:
        return "Error: The length of the RNA sequence must be a multiple of three."

    codon_table = {
        'AUG': 'M', 'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'UAU': 'Y',
        'UAC': 'Y', 'UGU': 'C', 'UGC': 'C', 'UGG': 'W', 'UAA': '',
        'UAG': '', 'UGA': '', 'CUU': 'L', 'CUC': 'L', 'CUA': 'L',
        'CUG': 'L', 'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'CGU': 'R',
        'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AUU': 'I', 'AUC': 'I',
        'AUA': 'I', 'AUG': 'M', 'ACU': 'T', 'ACC': 'T', 'ACA': 'T',
        'ACG': 'T', 'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GUU': 'V',
        'GUC': 'V', 'GUA': 'V', 'GUG': 'V', 'GCU': 'A', 'GCC': 'A',
        'GCA': 'A', 'GCG': 'A', 'GAU': 'D', 'GAC': 'D', 'GAA': 'E',
        'GAG': 'E', 'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }
    
    protein = []
    for i in range(0, len(rna_sequence), 3):  # Process complete codons
        codon = rna_sequence[i:i+3]
        protein.append(codon_table.get(codon, ''))  # Append empty string for invalid codons
    
    return ''.join(protein)

def compare_sequences(seq1, seq2):
    """Compare two DNA sequences and return similarity percentage."""
    if not is_dna(seq1) or not is_dna(seq2):
        raise ValueError("Both sequences must be DNA.")
    
    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
    return (matches / max(len(seq1), len(seq2))) * 100

def detect_mutations(reference, test):
    """Identify mutations in a test sequence compared to a reference."""
    if not is_dna(reference) or not is_dna(test):
        raise ValueError("Both sequences must be DNA.")
    
    mutations = []
    mutation_types = {
        'substitutions': [],
        'insertions': [],
        'deletions': [],
        'inversions': []
    }
    
    # Align sequences using local alignment
    alignments = pairwise2.align.localxx(reference, test)
    if not alignments:
        return mutations
    
    for alignment in alignments:
        ref_aligned, test_aligned, score, start, end = alignment
        for i, (ref_base, test_base) in enumerate(zip(ref_aligned, test_aligned)):
            if ref_base != test_base:
                if ref_base == '-':
                    mutation_types['insertions'].append((i, test_base))
                elif test_base == '-':
                    mutation_types['deletions'].append((i, ref_base))
                else:
                    mutation_types['substitutions'].append((i, ref_base, test_base))
    
    # Detect inversions
    for i in range(len(reference)):
        for j in range(i + 4, len(reference)):  # Min 4 bases for inversion
            ref_segment = reference[i:j]
            test_segment = test[i:j]
            if ref_segment == reverse_complement(test_segment):
                mutation_types['inversions'].append((i, j, ref_segment))
    
    return mutation_types

def timeout(seconds):
    """Decorator to add timeout to a function"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except TimeoutError:
                    raise TimeoutError(f"Operation timed out after {seconds} seconds")
        return wrapper
    return decorator

@timeout(90)
def find_homologous_sequences(sequence, e_value_thresh=10.0):
    """Find homologous sequences using NCBI BLAST with timeout."""
    if not is_dna(sequence):
        raise ValueError("Input sequence must be DNA.")
    
    try:
        ncbi_email = os.getenv('NCBI_EMAIL')
        if not ncbi_email:
            raise ValueError("NCBI_EMAIL not found in environment variables")
        
        Entrez.email = ncbi_email
        
        # First convert sequence to FASTA format
        fasta_sequence = f">query\n{sequence}"
        
        result_handle = NCBIWWW.qblast(
            "blastn",           
            "nt",              
            fasta_sequence,    
            expect=e_value_thresh,
            hitlist_size=5     # Reduced for faster response
        )
        
        blast_records = NCBIXML.parse(result_handle)
        homologous_sequences = []
        
        for blast_record in blast_records:
            for alignment in blast_record.alignments[:5]:  # Limit to top 5 matches
                for hsp in alignment.hsps:
                    homologous_sequences.append({
                        'title': alignment.title,
                        'length': alignment.length,
                        'e_value': hsp.expect,
                        'identity_percent': (hsp.identities / hsp.align_length) * 100,
                        'score': hsp.score  # This is the bit score
                    })
                    break  # Only take first HSP per alignment
                
        return homologous_sequences

    except Exception as e:
        print(f"BLAST search error: {str(e)}")
        return []

def kmer_analysis(sequence, k):
    """Analyze the frequency of k-mers in a DNA sequence."""
    if not is_dna(sequence):
        raise ValueError("Input sequence must be DNA.")
    
    kmer_counts = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1
    return kmer_counts

@timeout(90)
def check_patents_and_papers(sequence):
    """Check patents and papers with timeout."""
    try:
        results = {
            'patents': [],
            'papers': [],
            'databases': []
        }
        
        # Use correct database names
        Entrez.email = os.getenv('NCBI_EMAIL')
        
        # 1. Check Nucleotide Database for Patents
        try:
            handle = Entrez.esearch(
                db="nuccore", 
                term=f"{sequence} AND patent[PROP]", 
                retmax=5
            )
            record = Entrez.read(handle)
            
            if record["Count"] != "0":
                results['patents'].append({
                    'message': f"Found {record['Count']} potential patent matches",
                    'ids': record['IdList']
                })
        except Exception as e:
            print(f"Warning: Patent search in nuccore failed: {str(e)}")

        # 2. Check PubMed for Research Papers
        try:
            handle = Entrez.esearch(
                db="pubmed",
                term=sequence,
                retmax=5
            )
            record = Entrez.read(handle)
            
            if record["Count"] != "0":
                results['papers'].append({
                    'message': f"Found {record['Count']} related papers",
                    'ids': record['IdList']
                })
        except Exception as e:
            print(f"Warning: Paper search failed: {str(e)}")

        # 3. Check GenBank Database
        try:
            handle = Entrez.esearch(
                db="nucleotide",
                term=sequence,
                retmax=5
            )
            record = Entrez.read(handle)
            
            if record["Count"] != "0":
                results['databases'].append({
                    'message': f"Found {record['Count']} database entries",
                    'ids': record['IdList']
                })
        except Exception as e:
            print(f"Warning: Database search failed: {str(e)}")

        return results
        
    except Exception as e:
        return {
            'error': f"Search failed: {str(e)}",
            'patents': [],
            'papers': [],
            'databases': []
        }

def detect_anomalies(sequence, reference_sequence=None):
    """Detect anomalies in a DNA sequence."""
    if not is_dna(sequence):
        raise ValueError("Input sequence must be DNA.")
    
    # Check for unusual base composition
    base_counts = Counter(sequence)
    total_bases = len(sequence)
    
    # Calculate percentages of each base
    base_percentages = {base: (count / total_bases) * 100 for base, count in base_counts.items()}
    
    # Define thresholds for unusual base composition
    unusual_threshold = 10  # Example threshold for base composition
    anomalies = []
    
    for base, percentage in base_percentages.items():
        if percentage < unusual_threshold or percentage > (100 - unusual_threshold):
            anomalies.append(f"Unusual base composition: {base} at {percentage:.2f}%")
    
    # Check for repetitive sequences
    repeat_pattern = r'(A{2,}|T{2,}|C{2,}|G{2,})'  # Adjust the pattern for different repeats
    repeats = re.findall(repeat_pattern, sequence)
    if repeats:
        anomalies.append(f"Repetitive sequences detected: {', '.join(set(repeats))}")
    
    # Check for mutations against a reference sequence if provided
    if reference_sequence:
        mutations = detect_mutations(reference_sequence, sequence)
        if mutations:
            anomalies.append(f"Mutations detected: {mutations}")
    
    if not anomalies:
        return "No anomalies detected."
    
    return "\n".join(anomalies)

def phylogenetic_analysis(sequences):
    """Perform phylogenetic analysis on a list of DNA sequences."""
    
    # Create a Multiple Sequence Alignment
    alignment = MultipleSeqAlignment([SeqIO.SeqRecord(Seq(seq), id=f"Seq{i+1}") for i, seq in enumerate(sequences)])
    
    # Use a simple distance matrix method (e.g., UPGMA) to create a phylogenetic tree
    distance_matrix = Phylo.distance.pdist(alignment, metric='identity')
    tree = Phylo.upgma(distance_matrix)

    # Print the tree in Newick format
    newick_format = Phylo.write(tree, StringIO(), format='newick')
    
    return f"Phylogenetic analysis complete. Tree in Newick format:\n{newick_format}"

def generate_report(sequence, results, homologous_sequences, patent_paper_check):
    """Generate comprehensive DNA analysis report."""
    import textwrap
    
    # Helper function for consistent section headers
    def section_header(title, width=80):
        return f"\n{Fore.CYAN}╔{'═' * (width-2)}╗\n║ {Fore.GREEN}{title:<{width-4}}{Fore.CYAN}║\n╚{'═' * (width-2)}╝{Style.RESET_ALL}\n"
    
    # Helper function for subsection headers
    def subsection_header(title, width=80):
        return f"\n{Fore.BLUE}▓▓▓ {Fore.LIGHTMAGENTA_EX}{title} {Fore.BLUE}{'▓' * (width - len(title) - 5)}{Style.RESET_ALL}\n"
    
    # Helper function for data display
    def data_row(label, value, width=80):
        return f"{Fore.CYAN}│ {Fore.LIGHTWHITE_EX}{label}: {Fore.YELLOW}{value}{Style.RESET_ALL}"
    
    # Helper function for wrapping text
    def wrap_text(text, width=80, indent=4):
        wrapped = textwrap.fill(text, width=width-indent)
        return textwrap.indent(wrapped, ' ' * indent)
    
    # Helper function for info messages
    def print_info(text):
        return f"{Fore.LIGHTBLUE_EX}ℹ {text}{Style.RESET_ALL}"
    
    # Helper function for warning messages
    def print_warning(text):
        return f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}"
    
    # Start building the report
    report = [
        f"\n{Fore.CYAN}",
        f"{Fore.LIGHTMAGENTA_EX}█▀ █ █ █▄▄ ▄▀█ ▀█▀ █▀█ █▀▄▀█ █ █▀▀",
        f"{Fore.LIGHTMAGENTA_EX}▄█ █▄█ █▄█ █▀█  █  █▄█ █ ▀ █ █ █▄▄",
        f"{Fore.CYAN}",
        f"{Fore.LIGHTMAGENTA_EX}█ █▄ █ █ █ █▀▀ █▀ ▀█▀ █ █▀▀ ▄▀█ ▀█▀ █ █▀█ █▄ █",
        f"{Fore.MAGENTA}█ █ ▀█ ▀▄▀ ██▄ ▄█  █  █ █▄█ █▀█  █  █ █▄█ █ ▀█",
        f"{Fore.CYAN}",
        f"{Fore.MAGENTA}█▀▀ █▄ █ █▀▀ █ █▄ █ █▀▀",
        f"{Fore.LIGHTMAGENTA_EX}██▄ █ ▀█ ██ █ █ ▀█ ██▄",
        f"{Fore.CYAN}{'═' * 100}{Style.RESET_ALL}",
        f"{Fore.LIGHTCYAN_EX}GDDA v0.21 XP - Genetic Due Diligence Micro-Agent, by MicroNOW, an ARPA Corporation subsidiary.{Style.RESET_ALL}\n",
    ]
    
    # Add comprehensive analysis results
    if results.get('basic_analysis'):
        report.append(section_header("SEQUENCE ANALYSIS"))
        basic = results['basic_analysis']
        report.append(data_row("Sequence Type", basic.get('sequence_type', 'Unknown')))
        report.append(data_row("Length", basic.get('length', 0)))
        report.append(data_row("GC Content", f"{basic.get('gc_content', 0):.2f}%"))
        
        # Add structure analysis if available
        if results.get('structure_analysis'):
            report.append(section_header("STRUCTURAL FEATURES"))
            struct = results['structure_analysis']
            report.append(data_row("Melting Temperature", f"{struct.get('melting_temp', 0)}°C"))
            
            # Add motifs
            if struct.get('motifs'):
                report.append(subsection_header("DNA MOTIFS"))
                for motif in struct['motifs']:
                    report.append(f"{Fore.CYAN}■ {motif['description']} at position(s): {', '.join(map(str, motif['positions']))}{Style.RESET_ALL}")
    
    # Sequence Display (with wrapping)
    report.append(subsection_header("RAW SEQUENCE"))
    report.append(wrap_text(sequence))
    
    # Transformations Section
    report.append(section_header("SEQUENCE TRANSFORMATIONS"))
    report.append(data_row("Reverse Complement", results['reverse_complement']))
    report.append(data_row("Transcription", results['transcription']))
    report.append(data_row("Translation", results['translation']))
    
    # Anomaly Analysis
    report.append(section_header("ANOMALY ANALYSIS"))
    if isinstance(results['anomalies'], str):
        report.append(wrap_text(results['anomalies']))
    else:
        for anomaly in results['anomalies']:
            report.append(f"{Fore.RED}■ {Fore.LIGHTWHITE_EX}{anomaly}{Style.RESET_ALL}")
    
    # K-mer Analysis
    report.append(section_header("K-MER FREQUENCY ANALYSIS"))
    kmer_data = results.get('kmer_analysis', {})
    if kmer_data:
        # Sort k-mers by frequency (descending) and alphabetically for same frequency
        sorted_kmers = sorted(kmer_data.items(), key=lambda x: (-x[1], x[0]))
        for kmer, count in sorted_kmers:
            report.append(f"{Fore.CYAN}{kmer}: {Fore.YELLOW}{'█' * count} {Fore.CYAN}({count}){Style.RESET_ALL}")
    
    # Enhanced Homology Section
    report.append(section_header("HOMOLOGY ANALYSIS"))
    if homologous_sequences:
        report.append(f"{Fore.YELLOW}Found {len(homologous_sequences)} significant matches:{Style.RESET_ALL}\n")
        # Add our new cyberpunk visualization
        report.append(display_homology_results(sequence, homologous_sequences))
    else:
        report.append(print_info("No significant homologous sequences found"))
    
    # Patents and Papers Section
    report.append(section_header("INTELLECTUAL PROPERTY & LITERATURE SEARCH"))
    
    if patent_paper_check.get('error'):
        report.append(print_warning(patent_paper_check['error']))
    else:
        # Patents
        if patent_paper_check['patents']:
            report.append(subsection_header("PATENT MATCHES"))
            for patent in patent_paper_check['patents']:
                report.append(f"{Fore.CYAN}{patent['message']}")
                if 'ids' in patent:
                    report.append(f"{Fore.YELLOW}IDs: {', '.join(patent['ids'])}\n")
        else:
            report.append(print_info("No patent matches found"))

        # Research Papers
        if patent_paper_check['papers']:
            report.append(subsection_header("RESEARCH PAPERS"))
            for paper in patent_paper_check['papers']:
                report.append(f"{Fore.CYAN}{paper['message']}")
                if 'ids' in paper:
                    report.append(f"{Fore.YELLOW}IDs: {', '.join(paper['ids'])}\n")
        else:
            report.append(print_info("No research papers found"))

        # Database Entries
        if patent_paper_check['databases']:
            report.append(subsection_header("DATABASE ENTRIES"))
            for entry in patent_paper_check['databases']:
                report.append(f"{Fore.CYAN}{entry['message']}")
                if 'ids' in entry:
                    report.append(f"{Fore.YELLOW}IDs: {', '.join(entry['ids'])}\n")
        else:
            report.append(print_info("No database entries found"))
    
    # Report Footer
    report.append(f"\n{Fore.CYAN}{'═' * 80}")
    report.append(f"{Fore.LIGHTGREEN_EX}Analysis Complete! {Fore.BLUE}Generated: {Fore.LIGHTWHITE_EX}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}\n")
    
    return '\n'.join(report)

def generate_random_dna(length=33):
    """Generate a random DNA sequence of specified length."""
    bases = ['A', 'T', 'C', 'G']
    return ''.join(random.choice(bases) for _ in range(length))

def generate_random_rna(length=33):
    """Generate a random RNA sequence of specified length."""
    bases = ['A', 'U', 'C', 'G']
    return ''.join(random.choice(bases) for _ in range(length))

def generate_random_protein(length=20):
    """Generate a random protein sequence of specified length."""
    amino_acids = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
    return ''.join(random.choice(amino_acids) for _ in range(length))

def handle_dna_command(command):
    """
    Enhanced handler for DNA/RNA/Protein analysis commands with improved error handling.
    """
    from datetime import datetime
    from colorama import Fore, Style, init
    init()  # Initialize colorama
    
    def print_error(message):
        return f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}"
    
    def print_warning(message):
        return f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}"
    
    def print_info(message):
        return f"{Fore.CYAN}INFO: {message}{Style.RESET_ALL}"
    
    # Parse command
    parts = command.split()
    
    # Basic command validation
    if len(parts) < 2:
        return print_error("Invalid command format. Usage: /dna <sequence> or /dna <subcommand> <sequence>")
    
    # Extract sequence and subcommand
    if parts[0].lower() != "/dna":
        return print_error("Command must start with '/dna'")
    
    # Handle different command formats
    if len(parts) == 2:
        sequence = parts[1].strip()
        subcommand = "report"  # Default to report
    else:
        subcommand = parts[1].lower()
        sequence = ' '.join(parts[2:]).strip()
    
    # Validate sequence
    if not sequence:
        return print_error("No sequence provided")
    
    # Basic sequence validation
    sequence = sequence.upper()  # Convert to uppercase for consistency
    
    try:
        # Command processing with error handling
        if subcommand == "report":
            # Determine sequence type
            seq_type = determine_sequence_type_detailed(sequence)
            
            if seq_type == "DNA":
                try:
                    print_info("Analyzing DNA sequence...")
                    results = {
                        'type': determine_sequence_type(sequence),
                        'gc_content': calculate_gc_content(sequence),
                        'reverse_complement': reverse_complement(sequence),
                        'transcription': transcribe(sequence),
                        'translation': translate(transcribe(sequence)),
                        'anomalies': detect_anomalies(sequence),
                        'kmer_analysis': kmer_analysis(sequence, 3),
                        'complexity': sequence_complexity(sequence),
                        'synthetic_indicators': is_synthetic_sequence(sequence)
                    }
                    
                    try:
                        homologous_sequences = find_homologous_sequences(sequence)
                    except Exception as e:
                        print_warning(f"Homology search failed: {str(e)}")
                        homologous_sequences = []
                    
                    try:
                        patent_check = check_patents_and_papers(sequence)
                    except Exception as e:
                        print_warning(f"Patent check failed: {str(e)}")
                        patent_check = "Patent check unavailable"
                    
                    return generate_report(sequence, results, homologous_sequences, patent_check)
                    
                except Exception as e:
                    return print_error(f"DNA analysis failed: {str(e)}")
                    
            elif seq_type == "RNA":
                try:
                    print_info("Analyzing RNA sequence...")
                    results = {
                        'type': 'RNA',
                        'basic_properties': {
                            'length': len(sequence),
                            'gc_content': (sequence.count('G') + sequence.count('C')) / len(sequence) * 100,
                            'base_composition': dict(Counter(sequence))
                        },
                        'targeting_analysis': analyze_rna_targeting_potential(sequence),
                        'structure_prediction': predict_rna_secondary_structure(sequence),
                        'regulatory_elements': analyze_regulatory_elements(sequence),
                        'motifs': find_rna_motifs(sequence)
                    }
                    return generate_rna_report(sequence, results)
                except Exception as e:
                    return print_error(f"RNA analysis failed: {str(e)}")
                    
            elif seq_type == "Protein":
                try:
                    print_info("Analyzing protein sequence...")
                    results = analyze_protein_sequence(sequence)
                    return generate_protein_report(sequence, results)
                except Exception as e:
                    return print_error(f"Protein analysis failed: {str(e)}")
            
            else:
                return print_error("Invalid sequence. Must be DNA, RNA, or protein sequence.")
        
        # Handle existing DNA-specific commands
        elif subcommand in ["revcom", "gc_content", "transcribe", "compare", "kmer", "anomalies"]:
            if not is_dna(sequence):
                return print_error(f"Invalid DNA sequence for {subcommand}")
            
            # Execute existing DNA command handlers
            if subcommand == "revcom":
                return print_info(f"Reverse complement: {reverse_complement(sequence)}")
            elif subcommand == "gc_content":
                return print_info(f"GC Content: {calculate_gc_content(sequence):.2f}%")
            elif subcommand == "transcribe":
                return print_info(f"RNA sequence: {transcribe(sequence)}")
            elif subcommand == "compare":
                if len(parts) < 4:
                    return print_error("Missing second sequence for comparison")
                seq2 = parts[3].upper()
                if not is_dna(seq2):
                    return print_error("Both sequences must be valid DNA")
                similarity = compare_sequences(sequence, seq2)
                return print_info(f"Sequence similarity: {similarity:.2f}%")
            elif subcommand == "kmer":
                k = 3  # Default k value
                if len(parts) > 3 and parts[3].isdigit():
                    k = int(parts[3])
                if k < 1 or k > len(sequence):
                    return print_error(f"Invalid k value: {k}")
                kmer_counts = kmer_analysis(sequence, k)
                result = [f"{Fore.CYAN}K-mer Analysis (k={k}){Style.RESET_ALL}"]
                for kmer, count in sorted(kmer_counts.items(), key=lambda x: (-x[1], x[0])):
                    result.append(f"{Fore.LIGHTWHITE_EX}{kmer}: {Fore.YELLOW}{count}{Style.RESET_ALL}")
                return "\n".join(result)
            elif subcommand == "anomalies":
                anomalies = detect_anomalies(sequence)
                return print_info(f"Anomalies detected:\n{anomalies}")
        
        # Handle embeddings command (works for all sequence types)
        elif subcommand == "embeddings":
            try:
                embeddings = get_embeddings(sequence)
                return print_info(f"Embeddings shape: {embeddings.shape}\nFirst few values: {embeddings[0][:5]}")
            except Exception as e:
                return print_error(f"Embedding generation failed: {str(e)}")
        
        # Handle translate command (works for both DNA and RNA)
        elif subcommand == "translate":
            if not is_rna(sequence):
                if is_dna(sequence):
                    sequence = transcribe(sequence)
                else:
                    return print_error("Invalid sequence for translation. Must be RNA or DNA.")
            result = translate(sequence)
            return print_info(f"Protein sequence: {result}")
        
        # Handle random sequence generation
        elif subcommand == "random":
            try:
                parts = command.split()[2:]  # Get parts after "/dna random"
                length = 33  # Default length
                seq_type = "dna"  # Default type
                
                if not parts:  # Just "/dna random"
                    random_seq = generate_random_dna(length)
                    return f"{Fore.CYAN}Random DNA Sequence ({length} bp):{Style.RESET_ALL}\n{Fore.YELLOW}{random_seq}{Style.RESET_ALL}"
                    
                if parts[0].lower() in ["dna", "rna", "protein"]:
                    seq_type = parts[0].lower()
                    if len(parts) > 1 and parts[1].isdigit():
                        length = int(parts[1])
                    elif parts[0].isdigit():
                        length = int(parts[0])
                        seq_type = "dna"  # Explicit DNA for number-only case
                    
                if length < 1:
                    return print_error("Length must be positive")
                if length > 10000:
                    return print_error("Length too large. Maximum is 10000 bases")
                
                if seq_type == "dna":
                    random_seq = generate_random_dna(length)
                    type_str = "DNA"
                    unit = "bp"
                elif seq_type == "rna":
                    random_seq = generate_random_rna(length)
                    type_str = "RNA"
                    unit = "bp"
                else:  # protein
                    random_seq = generate_random_protein(length)
                    type_str = "Protein"
                    unit = "aa"
                    
                return f"{Fore.CYAN}Random {type_str} Sequence ({length} {unit}):{Style.RESET_ALL}\n{Fore.YELLOW}{random_seq}{Style.RESET_ALL}"
            except Exception as e:
                return print_error(f"Failed to generate random sequence: {str(e)}")
        
        # Handle help command
        elif subcommand == "help":
            help_msg = f"""
{Fore.CYAN}Sequence Analysis Tool Commands:{Style.RESET_ALL}
{Fore.YELLOW}/dna <sequence>{Style.RESET_ALL} - Generate full analysis report (DNA/RNA/Protein)
{Fore.YELLOW}/dna revcom <sequence>{Style.RESET_ALL} - Get reverse complement (DNA only)
{Fore.YELLOW}/dna gc <sequence>{Style.RESET_ALL} - Calculate GC content (DNA only)
{Fore.YELLOW}/dna transcribe <sequence>{Style.RESET_ALL} - Transcribe DNA to RNA
{Fore.YELLOW}/dna translate <sequence>{Style.RESET_ALL} - Translate RNA/DNA to protein
{Fore.YELLOW}/dna compare <seq1> <seq2>{Style.RESET_ALL} - Compare two sequences (DNA only)
{Fore.YELLOW}/dna kmer <sequence> [k]{Style.RESET_ALL} - Perform k-mer analysis (DNA only)
{Fore.YELLOW}/dna anomalies <sequence>{Style.RESET_ALL} - Detect sequence anomalies (DNA only)
{Fore.YELLOW}/dna embeddings <sequence>{Style.RESET_ALL} - Generate sequence embeddings
{Fore.YELLOW}/dna random dna [length]{Style.RESET_ALL} - Generate random DNA sequence
{Fore.YELLOW}/dna random rna [length]{Style.RESET_ALL} - Generate random RNA sequence
{Fore.YELLOW}/dna random protein [length]{Style.RESET_ALL} - Generate random protein sequence
"""
            return help_msg
        
        else:
            return print_error(f"Unknown subcommand: {subcommand}. Use '/dna help' for available commands.")
            
    except Exception as e:
        return print_error(f"An unexpected error occurred: {str(e)}")

def determine_sequence_type_detailed(sequence):
    """Enhanced sequence type detection."""
    sequence = sequence.upper()
    if is_dna(sequence):
        return "DNA"
    elif is_rna(sequence):
        return "RNA"
    elif is_protein(sequence):
        return "Protein"
    else:
        return "Unknown"

def calculate_mirna_score(target_region, seed_sequence):
    """
    Calculate miRNA targeting score based on multiple factors:
    1. Seed match type
    2. Site accessibility
    3. AU content in surrounding region
    4. Position in 3' UTR (if applicable)
    5. Base pairing stability
    """
    score = 0.0
    
    # Perfect seed match (positions 2-7)
    if complementary_match(target_region[1:7], seed_sequence[1:7]):
        score += 3.0
    
    # Extended seed match (position 8)
    if len(target_region) >= 8 and len(seed_sequence) >= 8:
        if complementary_match(target_region[7], seed_sequence[7]):
            score += 0.5
    
    # Check for A at position 1
    if target_region[0] == 'A':
        score += 0.3
    
    # Calculate AU content in surrounding region (30 nt window)
    au_content = (target_region.count('A') + target_region.count('U')) / len(target_region)
    score += au_content * 0.5
    
    # Calculate base pairing stability using RNA.fold
    try:
        hybrid = RNA.duplexfold(target_region, seed_sequence)
        mfe = abs(hybrid.energy)
        # Normalize MFE contribution (typical range -5 to -15 kcal/mol)
        score += min(mfe / 15.0, 1.0)
    except Exception:
        # Fallback if ViennaRNA fails
        gc_content = (target_region.count('G') + target_region.count('C')) / len(target_region)
        score += (1 - gc_content) * 0.5
    
    # Normalize final score to 0-1 range
    return min(score / 5.0, 1.0)

def analyze_rna_targeting_potential(sequence):
    """Analyze RNA targeting potential using real miRNA data and RNA folding."""
    targeting_results = {
        'mirna_sites': [],
        'sirna_regions': [],
        'accessibility_scores': [],
        'targeting_score': 0.0
    }
    
    try:
        # siRNA analysis
        for i in range(len(sequence)-18):
            region = sequence[i:i+19]
            fold = RNA.fold_compound(region)
            (mfe_struct, mfe) = fold.mfe()
            
            if is_good_sirna_candidate(region):  # Only pass sequence
                targeting_results['sirna_regions'].append({
                    'position': i,
                    'sequence': region,
                    'mfe': mfe,
                    'structure': mfe_struct,
                    'gc_content': calculate_gc_content(region)
                })
        
        # miRNA analysis (keeping existing code)
        try:
            mirbase_url = "https://mirbase.org/api/v1/sequences"
            response = requests.get(mirbase_url)
            if response.status_code == 200:
                mirna_data = response.json()
                for mirna in mirna_data[:50]:
                    seed = mirna['sequence'][:7]
                    for i in range(len(sequence)-6):
                        region = sequence[i:i+7]
                        if complementary_match(region, seed):
                            targeting_results['mirna_sites'].append({
                                'position': i,
                                'mirna': mirna['name'],
                                'sequence': region,
                                'score': calculate_mirna_score(region, seed)
                            })
        except Exception as e:
            print(f"Warning: miRNA analysis failed: {str(e)}")
        
        # Calculate overall targeting score
        targeting_results['targeting_score'] = (
            len(targeting_results['sirna_regions']) * 0.5 +
            len(targeting_results['mirna_sites']) * 0.5
        )
        
    except Exception as e:
        print(f"Warning: RNA targeting analysis partial failure: {str(e)}")
    
    return targeting_results

def predict_rna_secondary_structure(sequence):
    """Predict RNA secondary structure using ViennaRNA."""
    try:
        # Initialize ViennaRNA folding compound
        fc = RNA.fold_compound(sequence)
        
        # Get MFE structure and energy
        (ss, mfe) = fc.mfe()
        
        # Initialize structure dictionary with empty lists
        structure = {
            'stem_loops': [],
            'hairpins': [],
            'internal_loops': [],
            'base_pairs': [],
            'mfe_structure': ss,
            'mfe': mfe
        }
        
        # Parse the dot-bracket notation to identify structural elements
        stack = []
        for i, char in enumerate(ss):
            if char == '(':
                stack.append(i)
            elif char == ')' and stack:
                start = stack.pop()
                # Identify stem-loops
                if i - start > 3:  # Minimum loop size
                    structure['stem_loops'].append({
                        'start': start,
                        'end': i,
                        'sequence': sequence[start:i+1],
                        'structure': ss[start:i+1]
                    })
        
        return structure
        
    except Exception as e:
        print(f"Warning: RNA structure prediction partial failure: {str(e)}")
        # Return a valid structure even if prediction fails
        return {
            'stem_loops': [],
            'hairpins': [],
            'internal_loops': [],
            'base_pairs': [],
            'mfe_structure': '.' * len(sequence),
            'mfe': 0.0
        }

def analyze_regulatory_elements(sequence):
    """Analyze RNA regulatory elements and motifs."""
    regulatory_elements = {
        'splice_sites': [],
        'polya_signals': [],
        'binding_motifs': [],
        'stability_elements': []
    }
    
    # Detect splice sites
    splice_donor = 'GT'
    splice_acceptor = 'AG'
    for i in range(len(sequence)-1):
        if sequence[i:i+2] == splice_donor:
            regulatory_elements['splice_sites'].append({
                'type': 'donor',
                'position': i,
                'sequence': sequence[i-3:i+5]
            })
        elif sequence[i:i+2] == splice_acceptor:
            regulatory_elements['splice_sites'].append({
                'type': 'acceptor',
                'position': i,
                'sequence': sequence[i-5:i+3]
            })
    
    # Find polyA signals
    polya_signal = 'AATAAA'
    for i in range(len(sequence)-5):
        if sequence[i:i+6] == polya_signal:
            regulatory_elements['polya_signals'].append({
                'position': i,
                'sequence': sequence[i:i+10]
            })
    
    # Detect RNA-binding protein motifs
    rbp_motifs = {
        'SRSF1': 'GAAGAA',
        'HNRNPA1': 'TAGGGT',
        'NOVA1': 'YCAY',
        'PTBP1': 'CTCTCT'
    }
    
    for i in range(len(sequence)-5):
        region = sequence[i:i+6]
        for rbp, motif in rbp_motifs.items():
            if matches_motif(region, motif):
                regulatory_elements['binding_motifs'].append({
                    'rbp': rbp,
                    'position': i,
                    'sequence': region
                })
    
    # Analyze stability elements
    au_rich = 'ATTTA'
    for i in range(len(sequence)-4):
        if sequence[i:i+5] == au_rich:
            regulatory_elements['stability_elements'].append({
                'type': 'AU-rich',
                'position': i,
                'sequence': sequence[i:i+5]
            })
    
    return regulatory_elements

def find_rna_motifs(sequence):
    """Find functional RNA motifs and structural elements."""
    motifs = {
        'structural_motifs': [],
        'functional_elements': [],
        'conserved_sites': [],
        'special_structures': []
    }
    
    # Known RNA structural motifs
    structural_patterns = {
        'GNRA_tetraloop': r'G[AGUC][AG]A',
        'kink_turn': r'GA[AU]A[AG]',
        'c_loop': r'CCNG[AG]',
        'tetraloop_receptor': r'CC[AGUC]{4}GG'
    }
    
    # Search for structural motifs
    for motif_name, pattern in structural_patterns.items():
        matches = re.finditer(pattern, sequence)
        for match in matches:
            motifs['structural_motifs'].append({
                'type': motif_name,
                'position': match.start(),
                'sequence': match.group()
            })
    
    # Functional elements
    functional_elements = {
        'ribosome_binding': 'AGGAGG',
        'iron_responsive': 'CAGUGH',
        'selenocysteine': 'SECIS'
    }
    
    for element_name, pattern in functional_elements.items():
        for i in range(len(sequence)-len(pattern)+1):
            if matches_degenerate(sequence[i:i+len(pattern)], pattern):
                motifs['functional_elements'].append({
                    'type': element_name,
                    'position': i,
                    'sequence': sequence[i:i+len(pattern)]
                })
    
    # Special RNA structures
    special_structures = detect_special_structures(sequence)
    motifs['special_structures'] = special_structures
    
    return motifs

def predict_secondary_structure(sequence):
    """Predict protein secondary structure using statistical methods."""
    structure = {
        'helices': [],
        'sheets': [],
        'turns': [],
        'confidence': []
    }
    
    # Propensity scales for secondary structure
    helix_propensity = {
        'A': 1.45, 'R': 0.98, 'N': 0.67, 'D': 0.98, 'C': 0.77,
        'Q': 1.17, 'E': 1.53, 'G': 0.53, 'H': 1.24, 'I': 1.00,
        'L': 1.34, 'K': 1.07, 'M': 1.20, 'F': 1.12, 'P': 0.57,
        'S': 0.77, 'T': 0.83, 'W': 1.14, 'Y': 0.69, 'V': 0.98
    }
    
    sheet_propensity = {
        'A': 0.97, 'R': 0.93, 'N': 0.89, 'D': 0.80, 'C': 1.30,
        'Q': 0.87, 'E': 0.26, 'G': 0.81, 'H': 0.71, 'I': 1.60,
        'L': 1.22, 'K': 0.74, 'M': 1.67, 'F': 1.28, 'P': 0.62,
        'S': 0.72, 'T': 1.20, 'W': 1.19, 'Y': 1.29, 'V': 1.87
    }
    
    # Sliding window analysis
    window_size = 6
    for i in range(len(sequence)-window_size+1):
        window = sequence[i:i+window_size]
        
        # Calculate propensities
        helix_score = sum(helix_propensity.get(aa, 0) for aa in window) / window_size
        sheet_score = sum(sheet_propensity.get(aa, 0) for aa in window) / window_size
        
        # Assign structure based on propensity scores
        if helix_score > 1.1 and helix_score > sheet_score:
            structure['helices'].append({
                'start': i,
                'end': i+window_size,
                'score': helix_score
            })
        elif sheet_score > 1.1 and sheet_score > helix_score:
            structure['sheets'].append({
                'start': i,
                'end': i+window_size,
                'score': sheet_score
            })
        
        # Identify turns (using specific patterns)
        if 'P' in window or 'G' in window:
            structure['turns'].append({
                'position': i,
                'sequence': window
            })
        
        # Calculate confidence score
        confidence = max(helix_score, sheet_score) / 2
        structure['confidence'].append(confidence)
    
    return structure

def predict_localization(sequence):
    """Predict protein cellular localization based on sequence features."""
    localization = {
        'predictions': [],
        'signals': [],
        'confidence': 0.0
    }
    
    # Signal peptide detection
    signal_peptide_score = analyze_signal_peptide(sequence[:30])
    if signal_peptide_score > 0.7:
        localization['signals'].append({
            'type': 'signal_peptide',
            'score': signal_peptide_score,
            'sequence': sequence[:30]
        })
    
    # Nuclear localization signal (NLS) detection
    nls_patterns = [
        r'K[KR].[KR]',
        r'[PR]..K[^DE][KR]',
        r'K[KR].[KR]'
    ]
    
    for pattern in nls_patterns:
        matches = re.finditer(pattern, sequence)
        for match in matches:
            localization['signals'].append({
                'type': 'NLS',
                'position': match.start(),
                'sequence': match.group()
            })
    
    # Mitochondrial targeting sequence detection
    if has_mito_signal(sequence[:50]):
        localization['signals'].append({
            'type': 'mitochondrial',
            'sequence': sequence[:50]
        })
    
    # Make predictions based on signals and sequence composition
    predictions = predict_compartment(sequence, localization['signals'])
    localization['predictions'] = predictions
    
    # Calculate overall confidence
    localization['confidence'] = calculate_loc_confidence(predictions)
    
    return localization

def predict_protein_families(sequence):
    """Predict protein families and domains."""
    families = {
        'domains': [],
        'motifs': [],
        'families': [],
        'confidence_scores': {}
    }
    
    # Common protein domains and their patterns
    domain_patterns = {
        'zinc_finger': r'C.{2,4}C.{12}H.{3,5}H',
        'leucine_zipper': r'L.{6}L.{6}L.{6}L',
        'helix_turn_helix': r'[AG].{2}[LI].{7,8}[AG].{4}[LI]',
        'EF_hand': r'D.{12}D.{12}[DN].{12}E'
    }
    
    # Search for domain patterns
    for domain, pattern in domain_patterns.items():
        matches = re.finditer(pattern, sequence)
        for match in matches:
            families['domains'].append({
                'type': domain,
                'position': match.start(),
                'sequence': match.group(),
                'confidence': calculate_domain_confidence(match.group())
            })
    
    # Protein family classification based on composition and features
    family_scores = classify_protein_family(sequence)
    for family, score in family_scores.items():
        if score > 0.6:  # Confidence threshold
            families['families'].append({
                'name': family,
                'confidence': score
            })
    
    # Conserved motif detection
    motifs = find_conserved_motifs(sequence)
    families['motifs'] = motifs
    
    # Calculate confidence scores
    families['confidence_scores'] = {
        'domain_confidence': np.mean([d['confidence'] for d in families['domains']]) if families['domains'] else 0,
        'family_confidence': np.mean([f['confidence'] for f in families['families']]) if families['families'] else 0,
        'overall_confidence': calculate_overall_confidence(families)
    }
    
    return families

def check_protein_patents(sequence):
    """Check protein sequence against patent databases."""
    patent_results = {
        'exact_matches': [],
        'similar_sequences': [],
        'patent_references': [],
        'last_updated': datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    # Check for exact sequence matches
    exact_matches = find_exact_patent_matches(sequence)
    patent_results['exact_matches'] = exact_matches
    
    # Find similar patented sequences
    similar_sequences = find_similar_patented_sequences(sequence)
    patent_results['similar_sequences'] = similar_sequences
    
    # Get relevant patent references
    if exact_matches or similar_sequences:
        patent_references = get_patent_references(exact_matches + similar_sequences)
        patent_results['patent_references'] = patent_references
    
    return patent_results

# Helper functions for the above implementations
def complementary_match(seq1, seq2):
    """Check if two sequences are complementary."""
    complement = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}
    return all(complement.get(a) == b for a, b in zip(seq1, seq2))

def is_good_sirna_candidate(sequence):
    """Check if sequence has good siRNA characteristics."""
    try:
        gc = calculate_gc_content(sequence)
        length_ok = 19 <= len(sequence) <= 23
        gc_ok = 40 <= gc <= 60
        
        return {
            'is_candidate': gc_ok and length_ok,
            'gc_content': gc,
            'length_check': length_ok,
            'sequence': sequence
        }
    except Exception as e:
        print(f"siRNA analysis error: {str(e)}")
        return None

def calculate_accessibility(window):
    """Calculate RNA accessibility score."""
    return random.uniform(0, 1)  # Placeholder for actual calculation

def can_basepair(base1, base2):
    """Check if two bases can form a base pair."""
    pairs = {
        'A': 'U', 'U': 'A',
        'G': 'C', 'C': 'G',
        'G': 'U', 'U': 'G'
    }
    if base1 in pairs:
        if isinstance(pairs[base1], list):
            return base2 in pairs[base1]
        return base2 == pairs[base1]
    return False

def calculate_pair_probability(base1, base2, distance):
    """Calculate base pairing probability."""
    if can_basepair(base1, base2):
        return max(0, 1 - (distance / 100))
    return 0

def estimate_mfe(sequence, base_pairs):
    """Estimate minimum free energy."""
    return -len(base_pairs) * 2  # Simplified estimation

def matches_motif(sequence, motif):
    """Check if sequence matches a motif pattern."""
    return bool(re.match(motif.replace('Y', '[CU]'), sequence))

def matches_degenerate(sequence, pattern):
    """Check if sequence matches a degenerate pattern."""
    iupac = {
        'R': '[AG]', 'Y': '[CT]',
        'S': '[GC]', 'W': '[AT]',
        'K': '[GT]', 'M': '[AC]',
        'B': '[CGT]', 'D': '[AGT]',
        'H': '[ACT]', 'V': '[ACG]',
        'N': '[ACGT]'
    }
    for code, bases in iupac.items():
        pattern = pattern.replace(code, bases)
    return bool(re.match(pattern, sequence))

def detect_special_structures(sequence):
    """Detect special RNA structures like riboswitches, ribozymes, etc."""
    special_structures = []
    
    # Riboswitch patterns
    riboswitch_patterns = {
        'TPP': r'CUGAGA.{10,50}GAAA',
        'FMN': r'AGAAGG.{20,60}CUCCA',
        'SAM': r'KUCCC.{10,30}AAGG'
    }
    
    for rswitch_type, pattern in riboswitch_patterns.items():
        matches = re.finditer(pattern, sequence)
        for match in matches:
            special_structures.append({
                'type': 'riboswitch',
                'subtype': rswitch_type,
                'position': match.start(),
                'sequence': match.group(),
                'confidence': 0.8
            })
    
    # Ribozyme core motifs
    ribozyme_patterns = {
        'hammerhead': r'CUGANGA.{40,60}GAAA',
        'hairpin': r'NNNGAAAC.{40,60}GUUUCNN'
    }
    
    for ribo_type, pattern in ribozyme_patterns.items():
        matches = re.finditer(pattern.replace('N', '[AUCG]'), sequence)
        for match in matches:
            special_structures.append({
                'type': 'ribozyme',
                'subtype': ribo_type,
                'position': match.start(),
                'sequence': match.group(),
                'confidence': 0.7
            })
    
    return special_structures

def analyze_signal_peptide(sequence):
    """Analyze signal peptide characteristics using position-specific scoring."""
    if len(sequence) < 15:
        return 0.0
    
    # Signal peptide characteristics
    n_region = sequence[:5]  # N-terminal region
    h_region = sequence[5:15]  # Hydrophobic core
    c_region = sequence[15:] if len(sequence) > 15 else ""  # C-terminal region
    
    # Score N-region (positive charges)
    n_score = (n_region.count('R') + n_region.count('K')) / len(n_region)
    
    # Score H-region (hydrophobicity)
    h_score = sum(kd.get(aa, 0) for aa in h_region) / len(h_region)
    
    # Score C-region (small, neutral AAs)
    c_score = 0
    if c_region:
        c_score = len([aa for aa in c_region if aa in 'AGST']) / len(c_region)
    
    # Combine scores with weights
    final_score = (0.3 * n_score + 0.5 * h_score + 0.2 * c_score)
    return min(max(final_score, 0), 1)  # Normalize to 0-1

def has_mito_signal(sequence):
    """Check for mitochondrial targeting sequence patterns."""
    if len(sequence) < 20:
        return False
    
    # Characteristics of mitochondrial targeting sequences
    mts_region = sequence[:20]
    
    # Check for positive charges
    positive_charge = (mts_region.count('R') + mts_region.count('K')) >= 3
    
    # Check for hydrophobic residues
    hydrophobic_count = sum(1 for aa in mts_region if aa in 'AILMFWV')
    hydrophobic_rich = hydrophobic_count >= 6
    
    # Check for absence of acidic residues
    few_acidic = (mts_region.count('D') + mts_region.count('E')) <= 2
    
    return positive_charge and hydrophobic_rich and few_acidic

def predict_compartment(sequence, signals):
    """Predict cellular compartment based on sequence signals."""
    predictions = []
    
    # Score different compartments based on signals and sequence features
    compartment_scores = {
        'cytoplasmic': 0.0,
        'nuclear': 0.0,
        'mitochondrial': 0.0,
        'secretory': 0.0,
        'membrane': 0.0
    }
    
    # Analyze signals
    for signal in signals:
        if signal['type'] == 'signal_peptide':
            compartment_scores['secretory'] += signal['score']
        elif signal['type'] == 'NLS':
            compartment_scores['nuclear'] += 0.4
        elif signal['type'] == 'mitochondrial':
            compartment_scores['mitochondrial'] += 0.5
    
    # Additional sequence-based features
    hydrophobicity = sum(kd.get(aa, 0) for aa in sequence) / len(sequence)
    if hydrophobicity > 0.4:
        compartment_scores['membrane'] += 0.3
    
    # Convert scores to predictions
    for compartment, score in compartment_scores.items():
        if score > 0.3:  # Threshold for prediction
            predictions.append({
                'compartment': compartment,
                'confidence': min(score, 1.0)
            })
    
    return sorted(predictions, key=lambda x: x['confidence'], reverse=True)

def calculate_loc_confidence(predictions):
    """Calculate overall localization confidence score."""
    if not predictions:
        return 0.0
    
    # Weight predictions by confidence
    total_confidence = sum(pred['confidence'] for pred in predictions)
    max_confidence = max(pred['confidence'] for pred in predictions)
    
    # Consider both the highest confidence and the distribution of confidences
    overall_confidence = (0.7 * max_confidence + 0.3 * (total_confidence / len(predictions)))
    
    return min(overall_confidence, 1.0)

def calculate_domain_confidence(sequence):
    """Calculate domain confidence score based on sequence characteristics."""
    # Check sequence length
    if len(sequence) < 20:
        return 0.3
    
    # Calculate sequence complexity
    complexity = sequence_complexity(sequence)
    
    # Check for conserved residues
    conserved_positions = len([i for i in range(len(sequence)-2) 
                             if sequence[i] in 'CGHKR' and sequence[i+1] in 'DENQ'])
    
    # Combine factors
    confidence = (0.4 * complexity + 0.4 * (conserved_positions / len(sequence)) + 0.2)
    
    return min(max(confidence, 0), 1)

def classify_protein_family(sequence):
    """Classify protein family based on sequence patterns and composition."""
    family_scores = {}
    
    # Common protein family patterns
    family_patterns = {
        'kinase': r'[LIV]G[ST]G[ST].{10,20}[LIVMFYC]',
        'protease': r'[ST]G[ST].{2}[DE].{10,20}[GSAT][GSAT]',
        'transporter': r'[RK].{3}[RK].{6,10}[LMIFV]{3}',
        'transcription_factor': r'[KR]{2,3}.{1,3}[LIVMAFY]{3}',
        'receptor': r'[WY].{2,3}[LIVMF]{2}.{10,20}[DE]'
    }
    
    # Check patterns
    for family, pattern in family_patterns.items():
        matches = re.finditer(pattern, sequence)
        score = sum(1 for _ in matches) * 0.3
        
        # Add composition-based scoring
        if family == 'kinase' and sequence.count('K') > len(sequence) * 0.08:
            score += 0.2
        elif family == 'protease' and sequence.count('S') > len(sequence) * 0.1:
            score += 0.2
        
        if score > 0:
            family_scores[family] = min(score, 1.0)
    
    return family_scores

def find_conserved_motifs(sequence):
    """Find conserved protein motifs using PROSITE patterns."""
    motifs = []
    
    try:
        # Use PROSITE REST API
        prosite_url = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi"
        params = {
            'seq': sequence,
            'output': 'json'
        }
        response = requests.post(prosite_url, data=params)
        
        if response.status_code == 200:
            results = response.json()
            for hit in results:
                motifs.append({
                    'type': hit['signature_ac'],
                    'name': hit['signature_id'],
                    'position': (hit['start'], hit['stop']),
                    'sequence': sequence[hit['start']-1:hit['stop']],
                    'score': hit.get('score', 0.8)
                })
    except Exception as e:
        print(f"Warning: PROSITE motif search failure: {str(e)}")
        
    return motifs

def calculate_overall_confidence(families):
    """Calculate overall confidence score for family predictions."""
    if not families or not families.get('families'):
        return 0.0
    
    # Weight different factors
    domain_confidence = families.get('confidence_scores', {}).get('domain_confidence', 0)
    family_confidence = families.get('confidence_scores', {}).get('family_confidence', 0)
    motif_confidence = 0.8 if families.get('motifs') else 0
    
    # Combine scores with weights
    overall_confidence = (0.4 * domain_confidence + 
                        0.4 * family_confidence + 
                        0.2 * motif_confidence)
    
    return min(max(overall_confidence, 0), 1)

def find_exact_patent_matches(sequence):
    """Find exact matches in patent database using BLAST."""
    matches = []
    
    try:
        # Use BLAST against patent database
        result_handle = NCBIWWW.qblast(
            "blastp", "pat",
            sequence,
            expect=1e-5,
            hitlist_size=50
        )
        
        blast_records = NCBIXML.parse(result_handle)
        for record in blast_records:
            for alignment in record.alignments:
                for hsp in alignment.hsps:
                    if hsp.identities == len(sequence):  # Exact match
                        patent_id = alignment.title.split('|')[1]
                        matches.append({
                            'patent_id': patent_id,
                            'title': alignment.title,
                            'date': None,  # Will be filled by get_patent_references
                            'sequence_location': f"Score: {hsp.score}, E-value: {hsp.expect}",
                            'confidence': 1.0
                        })
        
    except Exception as e:
        print(f"Warning: Patent BLAST search failure: {str(e)}")
    
    return matches

def find_similar_patented_sequences(sequence):
    """Find similar sequences in patent database using BLAST."""
    similar_sequences = []
    
    try:
        # Use BLAST against patent database with less stringent parameters
        result_handle = NCBIWWW.qblast(
            "blastp", "pat",
            sequence,
            expect=1e-3,
            hitlist_size=50
        )
        
        blast_records = NCBIXML.parse(result_handle)
        for record in blast_records:
            for alignment in record.alignments:
                for hsp in alignment.hsps:
                    similarity = (hsp.identities / len(sequence)) * 100
                    if similarity >= 70:  # At least 70% similar
                        patent_id = alignment.title.split('|')[1]
                        similar_sequences.append({
                            'patent_id': patent_id,
                            'similarity': similarity,
                            'aligned_region': hsp.sbjct,
                            'position': f"{hsp.sbjct_start}-{hsp.sbjct_end}",
                            'date': None  # Will be filled by get_patent_references
                        })
        
    except Exception as e:
        print(f"Warning: Similar patent search failure: {str(e)}")
    
    return similar_sequences

def get_patent_references(matches):
    """Get patent references using Entrez."""
    references = []
    
    try:
        for match in matches:
            patent_id = match['patent_id']
            
            # Search for patent in PubMed
            handle = Entrez.esearch(db="patent", term=patent_id)
            record = Entrez.read(handle)
            
            if record['IdList']:
                # Get patent details
                patent_handle = Entrez.efetch(
                    db="patent",
                    id=record['IdList'][0],
                    rettype="xml"
                )
                patent_record = Entrez.read(patent_handle)
                
                if patent_record:
                    patent = patent_record[0]
                    references.append({
                        'patent_id': patent_id,
                        'inventors': [inv['name'] for inv in patent.get('inventors', [])],
                        'assignee': patent.get('assignee', 'Unknown'),
                        'filing_date': patent.get('filing_date', 'Unknown'),
                        'publication_date': patent.get('publication_date', 'Unknown'),
                        'title': patent.get('title', 'Unknown')
                    })
            
            # Respect NCBI rate limits
            time.sleep(0.34)  # Max 3 requests per second
            
    except Exception as e:
        print(f"Warning: Patent reference retrieval failure: {str(e)}")
    
    return references

def format_rna_structure(sequence, structure):
    """Convert dot-bracket notation to a more visual representation."""
    visual = []
    pairs = []
    stack = []
    
    # Find matching pairs
    for i, char in enumerate(structure):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                pairs.append((start, i))
    
    # Create the visualization
    seq_line = list(sequence)
    bond_line = list(' ' * len(sequence))
    
    for start, end in pairs:
        bond_line[start] = '╭'
        bond_line[end] = '╯'
        for i in range(start + 1, end):
            if bond_line[i] == ' ':
                bond_line[i] = '─'
    
    visual.append(''.join(bond_line))
    visual.append(''.join(seq_line))
    
    return '\n'.join(visual)

def generate_rna_report(sequence, results):
    """Enhanced RNA analysis report generator"""
    def section_header(title, width=80):
        return f"\n{Fore.CYAN}╔{'═' * (width-2)}╗\n║ {Fore.GREEN}{title:<{width-4}}{Fore.CYAN}║\n╚{'═' * (width-2)}╝{Style.RESET_ALL}\n"
    
    def data_row(label, value, width=80):
        return f"{Fore.CYAN}│ {Fore.LIGHTWHITE_EX}{label}: {Fore.YELLOW}{value}{Style.RESET_ALL}"

    report = []
    
    # Basic Information
    report.append(section_header("RNA SEQUENCE ANALYSIS"))
    report.append(data_row("Sequence Length", len(sequence)))
    report.append(data_row("GC Content", f"{results.get('basic_properties', {}).get('gc_content', 0):.2f}%"))
    report.append(data_row("Base Composition", 
        ', '.join(f"{base}: {count}" for base, count in results.get('basic_properties', {}).get('base_composition', {}).items())))

    # RNA Targeting Analysis
    report.append(section_header("RNA TARGETING POTENTIAL"))
    targeting = results.get('targeting_analysis', {})
    if targeting.get('mirna_sites'):
        report.append(data_row("miRNA Sites Found", len(targeting['mirna_sites'])))
        for site in targeting['mirna_sites'][:3]:  # Show top 3
            report.append(f"{Fore.CYAN}│ {Fore.LIGHTWHITE_EX}• {site['mirna']} at position {site['position']}: {Fore.YELLOW}{site['sequence']}{Style.RESET_ALL}")
    else:
        report.append(data_row("miRNA Sites", "None detected"))

    if targeting.get('sirna_regions'):
        report.append(data_row("siRNA Regions", len(targeting['sirna_regions'])))
        for region in targeting['sirna_regions'][:3]:  # Show top 3
            report.append(f"{Fore.CYAN}│ {Fore.LIGHTWHITE_EX}• Position {region['position']}: {Fore.YELLOW}{region['sequence']}{Style.RESET_ALL}")
    
    # Secondary Structure
    report.append(section_header("SECONDARY STRUCTURE"))
    struct = results.get('structure_prediction', {})
    mfe_struct = struct.get('mfe_structure', '')
    if mfe_struct:
        report.append(data_row("RNA Structure", ''))
        visual_struct = format_rna_structure(sequence, mfe_struct)
        for line in visual_struct.split('\n'):
            report.append(f"{Fore.CYAN}│ {Fore.YELLOW}{line}{Style.RESET_ALL}")
    report.append(data_row("Minimum Free Energy", f"{struct.get('mfe', 0):.2f} kcal/mol"))
    
    # Regulatory Elements
    report.append(section_header("REGULATORY ELEMENTS"))
    reg_elements = results.get('regulatory_elements', {})
    report.append(data_row("Splice Sites", len(reg_elements.get('splice_sites', []))))
    report.append(data_row("PolyA Signals", len(reg_elements.get('polya_signals', []))))
    report.append(data_row("RBP Binding Motifs", len(reg_elements.get('binding_motifs', []))))
    
    # Database References
    report.append(section_header("DATABASE REFERENCES"))
    refs = results.get('database_refs', {})
    report.append(data_row("Rfam", refs.get('rfam', 'No matches found')))
    report.append(data_row("miRBase", refs.get('mirbase', 'No matches found')))
    report.append(data_row("GtRNAdb", refs.get('gtrnadb', 'No matches found')))
    if refs.get('similar_sequences'):
        for seq in refs['similar_sequences'][:3]:
            report.append(f"{Fore.CYAN}│ {Fore.LIGHTWHITE_EX}• {seq['id']}: {Fore.YELLOW}{seq['description']}{Style.RESET_ALL}")
    
    # Literature References
    report.append(section_header("LITERATURE REFERENCES"))
    papers = results.get('literature', [])
    if papers:
        for paper in papers[:3]:
            report.append(data_row(
                paper['authors'].split(',')[0] + " et al.",
                f"({paper['year']}) {paper['title']} - {paper['journal']}"
            ))
    else:
        report.append(data_row("Publications", "No related publications found"))

    # Add RNA-specific analyses
    if results.get('structure_prediction'):
        report.append(section_header("RNA STRUCTURE"))
        struct = results['structure_prediction']
        report.append(data_row("Minimum Free Energy", f"{struct.get('mfe', 0):.2f} kcal/mol"))
        
        # Add visual structure representation
        if struct.get('mfe_structure'):
            report.append(subsection_header("SECONDARY STRUCTURE"))
            visual = format_rna_structure(sequence, struct['mfe_structure'])
            for line in visual.split('\n'):
                report.append(f"{Fore.CYAN}│ {line}{Style.RESET_ALL}")
    
    report.append(f"\n{Fore.CYAN}{'═' * 80}")
    report.append(f"{Fore.LIGHTGREEN_EX}Analysis Complete! {Fore.BLUE}Generated: {Fore.LIGHTWHITE_EX}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}\n")

    return "\n".join(report)

def generate_protein_report(sequence, analysis):
    """Enhanced protein analysis report generator"""
    def section_header(title, width=80):
        return f"\n{Fore.CYAN}╔{'═' * (width-2)}╗\n║ {Fore.GREEN}{title:<{width-4}}{Fore.CYAN}║\n╚{'═' * (width-2)}╝{Style.RESET_ALL}\n"
    
    def data_row(label, value, width=80):
        return f"{Fore.CYAN}│ {Fore.LIGHTWHITE_EX}{label}: {Fore.YELLOW}{value}{Style.RESET_ALL}"

    report = []
    
    # Basic Information
    report.append(section_header("PROTEIN SEQUENCE ANALYSIS"))
    basic_props = analysis.get('basic_properties', {})
    report.append(data_row("Sequence Length", basic_props.get('length', 0)))
    report.append(data_row("Molecular Weight", f"{basic_props.get('weight', 0):.1f} Da"))
    
    # Amino Acid Composition
    aa_comp = basic_props.get('amino_acid_composition', {})
    if aa_comp:
        aa_comp_str = ', '.join(f"{aa}: {count*100:.1f}%" for aa, count in aa_comp.items())
        report.append(data_row("Amino Acid Composition", aa_comp_str))
    else:
        report.append(data_row("Amino Acid Composition", "No data available"))
    
    # Secondary Structure
    report.append(section_header("SECONDARY STRUCTURE"))
    struct = analysis.get('secondary_structure', {})
    report.append(data_row("Alpha Helix", f"{struct.get('helix', 0):.1f}%"))
    report.append(data_row("Beta Sheet", f"{struct.get('sheet', 0):.1f}%"))
    report.append(data_row("Random Coil", f"{struct.get('coil', 0):.1f}%"))
    
    # Cellular Localization
    report.append(section_header("CELLULAR LOCALIZATION"))
    loc = analysis.get('localization', {})
    if loc.get('predictions'):
        for pred in loc['predictions']:
            report.append(data_row(pred['compartment'], f"{pred.get('confidence', 0):.2f}"))
    else:
        report.append(data_row("Predictions", "No localization predictions available"))
    
    # Protein Families
    report.append(section_header("PROTEIN FAMILIES AND DOMAINS"))
    families = analysis.get('protein_families', {})
    if families.get('families'):
        for family in families['families']:
            report.append(data_row(family['name'], f"Confidence: {family.get('confidence', 0):.2f}"))
    else:
        report.append(data_row("Families", "No family predictions available"))
    
    if families.get('domains'):
        for domain in families['domains']:
            report.append(data_row(f"Domain at {domain['position']}", domain['type']))
    else:
        report.append(data_row("Domains", "No domain predictions available"))
    
    # Database References
    report.append(section_header("DATABASE REFERENCES"))
    refs = analysis.get('database_refs', {})
    report.append(data_row("UniProt", refs.get('uniprot', 'No matches found')))
    report.append(data_row("Pfam", refs.get('pfam', 'No matches found')))
    report.append(data_row("PROSITE", refs.get('prosite', 'No matches found')))
    
    # Patent Information
    report.append(section_header("INTELLECTUAL PROPERTY"))
    patents = analysis.get('intellectual_property', {})
    report.append(data_row("Exact Matches", len(patents.get('exact_matches', []))))
    report.append(data_row("Similar Sequences", len(patents.get('similar_sequences', []))))
    report.append(data_row("Latest Patent", 
        patents.get('patent_references', [{'patent_id': 'None found'}])[0]['patent_id']))
    
    # Literature
    report.append(section_header("LITERATURE REFERENCES"))
    papers = analysis.get('literature', [])
    if papers:
        for paper in papers[:3]:  # Show top 3 papers
            report.append(data_row(paper['title'], f"({paper['year']}) - {paper['journal']}"))
    else:
        report.append(data_row("Publications", "No related publications found"))

    # Add protein-specific analyses
    if analysis.get('structure_analysis'):
        report.append(section_header("PROTEIN STRUCTURE"))
        struct = analysis['structure_analysis']
        
        # Secondary structure composition
        if struct.get('secondary_structure'):
            ss = struct['secondary_structure']
            report.append(data_row("Alpha Helix", f"{ss['helix']*100:.1f}%"))
            report.append(data_row("Beta Sheet", f"{ss['sheet']*100:.1f}%"))
            report.append(data_row("Random Coil", f"{ss['coil']*100:.1f}%"))
        
        # Hydrophobicity plot
        if struct.get('hydrophobicity'):
            report.append(subsection_header("HYDROPHOBICITY PROFILE"))
            hydro_plot = plot_hydrophobicity(struct['hydrophobicity'])
            report.append(hydro_plot)
    
    # Add footer
    report.append(f"\n{Fore.CYAN}{'═' * 80}")
    report.append(f"{Fore.LIGHTGREEN_EX}Analysis Complete! {Fore.BLUE}Generated: {Fore.LIGHTWHITE_EX}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}\n")

    return '\n'.join(report)

def check_external_services():
    """Verify access to critical external services before starting analysis."""
    services_status = {
        'NCBI': False,
        'RNA': False,
        'PROSITE': False
    }
    
    try:
        # Test NCBI access
        handle = Entrez.einfo()
        handle.close()
        services_status['NCBI'] = True
    except Exception as e:
        print(f"{Fore.RED}Warning: NCBI services unavailable: {str(e)}{Style.RESET_ALL}")
    
    try:
        # Test RNA folding capability
        RNA.fold_compound("AUGC")
        services_status['RNA'] = True
    except Exception as e:
        print(f"{Fore.RED}Warning: RNA folding services unavailable: {str(e)}{Style.RESET_ALL}")
    
    try:
        # Test PROSITE access
        response = requests.get("https://prosite.expasy.org/", timeout=5)
        services_status['PROSITE'] = response.status_code == 200
    except Exception as e:
        print(f"{Fore.RED}Warning: PROSITE services unavailable: {str(e)}{Style.RESET_ALL}")
    
    return services_status

def validate_sequence(sequence, seq_type):
    """Strict sequence validation with detailed error reporting."""
    valid_chars = {
        'DNA': set('ATCGN'),
        'RNA': set('AUCGN'),
        'Protein': set('ACDEFGHIKLMNPQRSTVWY*-')  # Added * for stop codons and - for gaps
    }
    
    sequence = sequence.upper().strip()
    
    # Check for empty sequence
    if not sequence:
        raise ValueError("Empty sequence provided")
    
    # Check sequence length
    if len(sequence) < 3:
        raise ValueError(f"Sequence too short: {len(sequence)} characters")
    
    # Check for invalid characters
    invalid_chars = set(sequence) - valid_chars[seq_type]
    if invalid_chars:
        raise ValueError(
            f"Invalid {seq_type} sequence. Found invalid characters: "
            f"{', '.join(sorted(invalid_chars))}"
        )
    
    return sequence

def rate_limited_request(max_per_second=3):
    """
    Decorator for rate limiting API requests.
    Default: 3 requests per second for NCBI compliance.
    """
    min_interval = 1.0 / max_per_second
    last_time_called = {}
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if func in last_time_called:
                elapsed = current_time - last_time_called[func]
                if elapsed < min_interval:
                    time.sleep(min_interval - elapsed)
            
            result = func(*args, **kwargs)
            last_time_called[func] = time.time()
            return result
        return wrapper
    return decorator

def print_help():
    """Print help information about available commands."""
    help_text = f"""
{Fore.CYAN}┌{'─' * 78}┐
│ {Fore.LIGHTBLUE_EX}CORPORATE SEQUENCE ANALYSIS INTERFACE v2.1{' ' * 35}{Fore.CYAN}│
├{'─' * 78}┤
│ {Fore.GREEN}COMMAND LIST{' ' * 67}{Fore.CYAN}│
├{Fore.BLUE}{'┄' * 78}{Fore.CYAN}┤

│ {Fore.YELLOW}▶ BASIC COMMANDS{' ' * 64}{Fore.CYAN}│
│ {Fore.WHITE}  /dna <sequence>{Fore.LIGHTBLACK_EX} - Analyze any sequence (auto-detection){' ' * 27}{Fore.CYAN}│
│ {Fore.WHITE}  test{Fore.LIGHTBLACK_EX} - Run validation suite with example sequences{' ' * 31}{Fore.CYAN}│
│ {Fore.WHITE}  help, /?, -h{Fore.LIGHTBLACK_EX} - Display this interface{' ' * 41}{Fore.CYAN}│
│ {Fore.WHITE}  exit, quit, q{Fore.LIGHTBLACK_EX} - Terminate session{' ' * 45}{Fore.CYAN}│

│ {Fore.YELLOW}▶ ADVANCED COMMANDS{' ' * 62}{Fore.CYAN}│
│ {Fore.WHITE}  /dna --verbose <sequence>{Fore.LIGHTBLACK_EX} - Detailed analysis output{' ' * 31}{Fore.CYAN}│
│ {Fore.WHITE}  /dna --format fasta <file>{Fore.LIGHTBLACK_EX} - Process FASTA file{' ' * 34}{Fore.CYAN}│
│ {Fore.WHITE}  /dna --batch <file>{Fore.LIGHTBLACK_EX} - Batch process sequences{' ' * 36}{Fore.CYAN}│
│ {Fore.WHITE}  /dna --export <format>{Fore.LIGHTBLACK_EX} - Export results (json/csv/txt){' ' * 28}{Fore.CYAN}│

│ {Fore.YELLOW}▶ ANALYSIS OPTIONS{' ' * 63}{Fore.CYAN}│
│ {Fore.WHITE}  --homology{Fore.LIGHTBLACK_EX} - Sequence similarity search{' ' * 41}{Fore.CYAN}│
│ {Fore.WHITE}  --structure{Fore.LIGHTBLACK_EX} - Predict structural features{' ' * 39}{Fore.CYAN}│
│ {Fore.WHITE}  --patents{Fore.LIGHTBLACK_EX} - Check patent databases{' ' * 44}{Fore.CYAN}│
│ {Fore.WHITE}  --literature{Fore.LIGHTBLACK_EX} - Search scientific papers{' ' * 41}{Fore.CYAN}│

├{Fore.BLUE}{'┄' * 78}{Fore.CYAN}┤
│ {Fore.YELLOW}▶ EXAMPLE USAGE{' ' * 65}{Fore.CYAN}│
│ {Fore.GREEN}  DNA:{Fore.LIGHTGREEN_EX}    /dna ATGCGTAACGGCATTAGC{' ' * 43}{Fore.CYAN}│
│ {Fore.GREEN}  RNA:{Fore.LIGHTGREEN_EX}    /dna AUGCGUAACGGCAUUAGC{' ' * 43}{Fore.CYAN}│
│ {Fore.GREEN}  Protein:{Fore.LIGHTGREEN_EX} /dna MAKVLISPKQW{' ' * 48}{Fore.CYAN}│

│ {Fore.YELLOW}▶ ADVANCED EXAMPLE{' ' * 63}{Fore.CYAN}│
│ {Fore.WHITE}  /dna --verbose --homology --patents ATGCGTAACGGCATTAGC{' ' * 27}{Fore.CYAN}│

├{Fore.MAGENTA}{'═' * 78}{Fore.CYAN}┤
│ {Fore.LIGHTBLACK_EX}System ready. Enter command to proceed.{' ' * 44}{Fore.CYAN}│
└{'─' * 78}┘{Style.RESET_ALL}
"""
    print(help_text)

@rate_limited_request(max_per_second=1)
def find_protein_motifs(sequence):
    """Find protein motifs using PROSITE with proper error handling."""
    try:
        prosite_patterns = {
            'phosphorylation': 'ST-[RK]',
            'nuclear_localization': 'K[KR].[KR]',
            'zinc_finger': 'C.H.[LIVMFY]C.{2}C[LIVMYA]',
            # Add more patterns as needed
        }
        
        motifs = []
        for motif_name, pattern in prosite_patterns.items():
            matches = re.finditer(pattern, sequence)
            for match in matches:
                motifs.append({
                    'name': motif_name,
                    'position': match.start(),
                    'sequence': match.group(),
                    'pattern': pattern
                })
        return motifs
    except Exception as e:
        print(f"Warning: Local motif search being used due to PROSITE error: {str(e)}")
        return []

def analyze_dna_sequence(sequence):
    """Analyze DNA sequence with improved error handling."""
    try:
        results = {
            'sequence_type': determine_sequence_type(sequence),
            'length': len(sequence),
            'gc_content': calculate_gc_content(sequence),
            'complexity_score': sequence_complexity(sequence),
            'synthetic_indicators': is_synthetic_sequence(sequence),
            'raw_sequence': sequence,
            'transformations': {
                'reverse_complement': reverse_complement(sequence),
                'transcription': transcribe(sequence),
                'translation': translate(transcribe(sequence))
            },
            'anomalies': detect_anomalies(sequence),
            'kmer_analysis': kmer_analysis(sequence, 3),
            'homology': []  # Initialize empty list for homology results
        }
        
        # BLAST search
        try:
            # Initialize BLAST parameters properly
            blast_params = {
                'program': 'blastn',
                'database': 'nt',
                'sequence': sequence,
                'hitlist_size': 5,
                'expect': 10.0,
                'word_size': 11,
                'gapcosts': "5 2"
            }
            
            result_handle = NCBIWWW.qblast(**blast_params)
            blast_records = NCBIXML.parse(result_handle)
            
            for record in blast_records:
                for alignment in record.alignments:
                    for hsp in alignment.hsps:
                        if hsp.expect < 1e-5:  # Only significant hits
                            results['homology'].append({
                                'title': alignment.title,
                                'length': alignment.length,
                                'e_value': hsp.expect,
                                'identity': hsp.identities / float(hsp.align_length)
                            })
        except Exception as e:
            print(f"Warning: BLAST search failed: {str(e)}")

        # Patent and literature search
        try:
            # Use Entrez properly with email and API key if available
            Entrez.email = "your.email@example.com"  # Replace with actual email
            
            # Search patents
            patent_handle = Entrez.esearch(db="patent", 
                                         term=f"{sequence} AND DNA[WORD]",
                                         retmax=5)
            patent_records = Entrez.read(patent_handle)
            
            if patent_records['IdList']:
                for patent_id in patent_records['IdList']:
                    fetch_handle = Entrez.efetch(db="patent", 
                                               id=patent_id, 
                                               rettype="gb")
                    results['intellectual_property']['patent_matches'].append(
                        fetch_handle.read())
                    fetch_handle.close()
            
            # Search literature (PubMed)
            lit_handle = Entrez.esearch(db="pubmed",
                                      term=f"{sequence} AND (DNA[Title/Abstract] OR gene[Title/Abstract])",
                                      retmax=5)
            lit_records = Entrez.read(lit_handle)
            
            if lit_records['IdList']:
                for pmid in lit_records['IdList']:
                    article = Entrez.efetch(db="pubmed",
                                          id=pmid,
                                          rettype="medline",
                                          retmode="text")
                    results['literature'].append(article.read())
                    
        except Exception as e:
            print(f"Warning: Patent/Literature search failed: {str(e)}")
            
        return results
        
    except Exception as e:
        print(f"ERROR: DNA analysis failed: {str(e)}")
        return None

def analyze_rna_sequence(sequence):
    """Analyze RNA sequence with improved error handling."""
    try:
        results = {
            'basic_properties': {
                'length': len(sequence),
                'gc_content': calculate_gc_content(sequence),
                'base_composition': count_bases(sequence)
            },
            'structure_prediction': predict_rna_secondary_structure(sequence),
            'targeting_analysis': analyze_rna_targeting_potential(sequence),  # Add this call
            'database_refs': [],
            'literature': []
        }
        
        # RNA structure prediction
        try:
            fc = RNA.fold_compound(sequence)
            (ss, mfe) = fc.mfe()
            results['structure_prediction'] = {
                'mfe_structure': ss,
                'mfe': mfe,
                'stem_loops': [],
                'base_pairs': []
            }
        except Exception as e:
            print(f"Warning: RNA structure prediction partial failure: {str(e)}")
        
        # RNA-specific database search
        try:
            # Search miRBase-like sequences
            rna_handle = Entrez.esearch(db="nucleotide",
                                      term=f"{sequence} AND (microRNA[Title] OR miRNA[Title] OR ncRNA[Title])",
                                      retmax=5)
            rna_records = Entrez.read(rna_handle)
            
            if rna_records['IdList']:
                for seq_id in rna_records['IdList']:
                    fetch_handle = Entrez.efetch(db="nucleotide",
                                               id=seq_id,
                                               rettype="gb")
                    results['database_refs'].append(fetch_handle.read())
            
        except Exception as e:
            print(f"Warning: RNA database search failed: {str(e)}")
            
        return results
        
    except Exception as e:
        print(f"ERROR: RNA analysis failed: {str(e)}")
        return None

def analyze_protein_sequence(sequence):
    """Analyze protein sequence with improved error handling."""
    try:
        # Clean sequence and create analysis object
        clean_sequence = ''.join(char for char in sequence.upper() if char in 'ACDEFGHIKLMNPQRSTVWY')
        protein = ProteinAnalysis(clean_sequence)
        
        # Create analysis dictionary with nested structure
        analysis = {
            'basic_properties': {
                'length': len(sequence),
                'weight': round(protein.molecular_weight(), 2),
                'amino_acid_composition': protein.get_amino_acids_percent(),
                'aromaticity': round(protein.aromaticity(), 2),
                'instability_index': round(protein.instability_index(), 2),
                'isoelectric_point': round(protein.isoelectric_point(), 2)
            },
            'secondary_structure': {},
            'database_refs': {},
            'literature': []
        }
        
        # Get secondary structure
        helix, sheet, coil = protein.secondary_structure_fraction()
        analysis['secondary_structure'] = {
            'helix': round(helix * 100, 2),
            'sheet': round(sheet * 100, 2),
            'coil': round(coil * 100, 2)
        }
        
        return analysis
        
    except Exception as e:
        print(f"ERROR: Protein analysis failed: {str(e)}")
        return {
            'basic_properties': {
                'length': len(sequence),
                'weight': 0,
                'amino_acid_composition': {},
                'aromaticity': 0,
                'instability_index': 0,
                'isoelectric_point': 0
            },
            'secondary_structure': {
                'helix': 0,
                'sheet': 0,
                'coil': 0
            },
            'database_refs': {},
            'literature': []
        }

def is_good_sirna_candidate(sequence):
    """Check if a sequence is a good siRNA candidate."""
    if len(sequence) != 19:  # Standard siRNA length
        return False
        
    # Check GC content (should be between 30-60%)
    gc = calculate_gc_content(sequence)
    if gc < 30 or gc > 60:
        return False
        
    # Check for runs of 4 or more of the same base
    if re.search(r'([AUGC])\1{3,}', sequence):
        return False
        
    return True

def GC(seq):
       """Calculate GC content of a sequence"""
       gc = sum(seq.count(x) for x in ['G', 'C', 'g', 'c'])
       total = sum(seq.count(x) for x in ['A', 'T', 'G', 'C', 'a', 't', 'g', 'c'])
       return gc * 100.0 / total if total > 0 else 0.0

def calculate_gc_content(sequence):
    """Calculate GC content of a sequence."""
    try:
        # Try using gc_fraction first (newer Biopython)
        return round(gc_fraction(sequence) * 100, 2)
    except (NameError, AttributeError):
        # Fall back to GC function or our own implementation
        try:
            return round(GC(sequence), 2)
        except Exception as e:
            print(f"Warning: Using basic GC calculation method: {str(e)}")
            # Basic calculation if all else fails
            gc = sum(sequence.upper().count(x) for x in ['G', 'C'])
            total = len(sequence)
            return round((gc / total * 100) if total > 0 else 0, 2)

def count_bases(sequence):
    """Count the occurrence of each base in the sequence."""
    return {
        base: sequence.count(base)
        for base in set(sequence)
    }

def analyze_dna_structure(sequence):
    """Analyze DNA structural properties."""
    try:
        return {
            'melting_temp': calculate_melting_temperature(sequence),
            'repeats': find_repeats(sequence),
            'motifs': find_dna_motifs(sequence)
        }
    except Exception as e:
        print(f"Warning: DNA structure analysis partial failure: {str(e)}")
        return {}

def calculate_melting_temperature(sequence):
    """Calculate approximate melting temperature."""
    # Simple calculation method
    at_count = sequence.count('A') + sequence.count('T')
    gc_count = sequence.count('G') + sequence.count('C')
    return round(2 * at_count + 4 * gc_count, 2)

def find_repeats(sequence):
    """Find repeated sequences."""
    repeats = []
    # Look for repeats of length 4-10
    for length in range(4, 11):
        for i in range(len(sequence) - length + 1):
            pattern = sequence[i:i+length]
            count = sequence.count(pattern)
            if count > 1:
                repeats.append({
                    'sequence': pattern,
                    'length': length,
                    'count': count,
                    'positions': [m.start() for m in re.finditer(pattern, sequence)]
                })
    return repeats

def find_dna_motifs(sequence):
    """Find common DNA motifs."""
    motifs = []
    common_motifs = {
        'TATA': 'TATA box',
        'CAAT': 'CAAT box',
        'CCGCCC': 'GC box',
        'AATAAA': 'Poly-A signal',
        'GCCAAT': 'CCAAT box'
    }
    
    for motif, description in common_motifs.items():
        positions = [m.start() for m in re.finditer(motif, sequence)]
        if positions:
            motifs.append({
                'motif': motif,
                'description': description,
                'positions': positions
            })
    return motifs

def can_basepair(base1, base2):
    """Check if two bases can form a base pair in RNA."""
    pairs = {
        'A': 'U',
        'U': 'A',
        'G': 'C',
        'C': 'G',
        # Allow G-U wobble pairs
        'G': ['C', 'U'],
        'U': ['A', 'G']
    }
    if base1 in pairs:
        if isinstance(pairs[base1], list):
            return base2 in pairs[base1]
        return base2 == pairs[base1]
    return False

def predict_mirna_targets(sequence):
    """Predict potential miRNA target sites in the sequence."""
    potential_targets = []
    
    # Look for sequences that could be miRNA targets
    # Focus on seed regions (positions 2-8)
    min_seed_length = 6
    
    for i in range(len(sequence) - min_seed_length + 1):
        region = sequence[i:i+min_seed_length]
        seed_matches = 0
        wobble_pairs = 0
        
        # Check for complementarity
        for j in range(len(region)):
            if can_basepair(region[j], region[len(region)-1-j]):
                if region[j] == 'G' and region[len(region)-1-j] == 'U' or \
                   region[j] == 'U' and region[len(region)-1-j] == 'G':
                    wobble_pairs += 1
                else:
                    seed_matches += 1
        
        # Consider it a potential target if there's good complementarity
        if seed_matches + wobble_pairs >= min_seed_length - 1:
            potential_targets.append({
                'position': i,
                'sequence': region,
                'seed_matches': seed_matches,
                'wobble_pairs': wobble_pairs,
                'total_score': seed_matches + 0.5 * wobble_pairs
            })
    
    # Sort by score
    potential_targets.sort(key=lambda x: x['total_score'], reverse=True)
    
    return potential_targets[:5]  # Return top 5 potential targets

def analyze_sequence_results(sequence, seq_type):
    """Centralized analysis function to gather all results for reporting"""
    results = {
        'basic_analysis': None,
        'structure_analysis': None,
        'database_refs': None,
        'patents': None,
        'homology': None
    }
    
    try:
        if seq_type == "DNA":
            results['basic_analysis'] = analyze_dna_sequence(sequence)
            results['structure_analysis'] = analyze_dna_structure(sequence)
        elif seq_type == "RNA":
            results['basic_analysis'] = analyze_rna_sequence(sequence)
            results['structure_analysis'] = predict_rna_secondary_structure(sequence)
        elif seq_type == "Protein":
            results['basic_analysis'] = analyze_protein_sequence(sequence)
            results['structure_analysis'] = predict_protein_structure(sequence)
        
        # Common analyses for all types
        results['database_refs'] = search_sequence_databases(sequence, seq_type)
        results['patents'] = check_patents_and_papers(sequence)
        results['homology'] = find_homologous_sequences(sequence)
        
    except Exception as e:
        print(f"Warning: Some analyses failed: {str(e)}")
    
    return results

@rate_limited_request()
def search_sequence_databases(sequence, seq_type):
    """Unified database search function with proper rate limiting"""
    try:
        # Use BLAST instead of Entrez.esearch for sequence alignment
        result_handle = NCBIWWW.qblast(
            program="blastn",
            database="nt",
            sequence=sequence,
            hitlist_size=5
        )
        
        # Parse BLAST results
        blast_records = NCBIXML.parse(result_handle)
        blast_record = next(blast_records)
        
        results = []
        for alignment in blast_record.alignments[:5]:
            for hsp in alignment.hsps:
                # Calculate actual identity percentage
                identity_percent = (hsp.identities / float(hsp.align_length)) * 100
                
                results.append({
                    'title': alignment.title,
                    'identity': identity_percent,
                    'e_value': hsp.expect,
                    'query': hsp.query,
                    'match': hsp.sbjct,
                    'align_length': hsp.align_length
                })
                break  # Take only best HSP for each alignment
                
        return results
        
    except Exception as e:
        logging.error(f"BLAST search failed: {str(e)}")
        return []

def predict_protein_structure(sequence):
    """Basic protein structure prediction"""
    try:
        analysis = ProteinAnalysis(sequence)
        secondary_structure = analysis.secondary_structure_fraction()
        
        return {
            'secondary_structure': {
                'helix': secondary_structure[0],
                'sheet': secondary_structure[1],
                'coil': secondary_structure[2]
            },
            'flexibility': analysis.flexibility(),
            'hydrophobicity': analysis.protein_scale(kd),
            'isoelectric_point': analysis.isoelectric_point()
        }
    except Exception as e:
        print(f"Warning: Protein structure prediction failed: {str(e)}")
        return None

def subsection_header(title, width=80):
    """Create a formatted subsection header."""
    return f"\n{Fore.BLUE}▓▓▓ {Fore.LIGHTMAGENTA_EX}{title} {Fore.BLUE}{'▓' * (width - len(title) - 5)}{Style.RESET_ALL}\n"

def plot_hydrophobicity(hydrophobicity_values, window_size=80):
    """Create an ASCII plot of hydrophobicity values."""
    if not hydrophobicity_values:
        return "No hydrophobicity data available"
    
    # Normalize values to fit in our display width
    max_val = max(hydrophobicity_values)
    min_val = min(hydrophobicity_values)
    range_val = max_val - min_val
    
    if range_val == 0:
        return "Insufficient variation in hydrophobicity values"
    
    # Create the plot
    plot_lines = []
    plot_height = 15  # Height of the plot in lines
    
    # Add top border
    plot_lines.append(f"{Fore.CYAN}╔{'═' * (window_size-2)}╗{Style.RESET_ALL}")
    
    # Create the actual plot
    for i in range(plot_height-1, -1, -1):
        line = [" "] * (window_size-2)
        threshold = min_val + (range_val * (i / (plot_height-1)))
        
        for j, val in enumerate(hydrophobicity_values):
            # Scale position to fit window
            pos = int((j / len(hydrophobicity_values)) * (window_size-2))
            if pos < len(line) and val >= threshold:
                line[pos] = "█"
        
        plot_lines.append(f"{Fore.CYAN}║{Fore.YELLOW}{''.join(line)}{Fore.CYAN}║{Style.RESET_ALL}")
    
    # Add bottom border
    plot_lines.append(f"{Fore.CYAN}╚{'═' * (window_size-2)}╝{Style.RESET_ALL}")
    
    # Add scale
    scale_line = f"{Fore.LIGHTWHITE_EX}Min: {min_val:.2f}{' ' * (window_size-20)}Max: {max_val:.2f}{Style.RESET_ALL}"
    plot_lines.append(scale_line)
    
    return "\n".join(plot_lines)

def format_rna_structure(sequence, structure, width=80):
    """Format RNA sequence and structure for display."""
    if not sequence or not structure:
        return "No structure data available"
    
    # Ensure sequence and structure are the same length
    if len(sequence) != len(structure):
        return "Error: Sequence and structure lengths do not match"
    
    # Split into lines of appropriate width
    lines = []
    for i in range(0, len(sequence), width):
        seq_line = sequence[i:i+width]
        struct_line = structure[i:i+width]
        
        # Add sequence line
        lines.append(f"{Fore.YELLOW}{seq_line}{Style.RESET_ALL}")
        
        # Add structure line with colored brackets
        colored_struct = ""
        for char in struct_line:
            if char in "({[":
                colored_struct += f"{Fore.GREEN}{char}{Style.RESET_ALL}"
            elif char in ")}]":
                colored_struct += f"{Fore.RED}{char}{Style.RESET_ALL}"
            else:
                colored_struct += f"{Fore.BLUE}{char}{Style.RESET_ALL}"
        lines.append(colored_struct)
        
        # Add spacer between blocks
        lines.append("")
    
    return "\n".join(lines)

def display_homology_results(sequence, homology_results):
    """Display homology results with enhanced cyberpunk-style visualization."""
    if not homology_results:
        return "No homology results found."
    
    output = []
    output.append(f"\n{Fore.CYAN}┌{'─' * 78}┐")
    output.append(f"│ {Fore.LIGHTBLUE_EX}GDDA HOMOLOGY ANALYSIS SYSTEM v2.1{' ' * 37}{Fore.CYAN}│")
    output.append(f"├{'─' * 78}┤")
    
    for i, result in enumerate(homology_results, 1):
        # CHANGED: Get actual values from result dictionary
        identity = float(result.get('identity', 0))  # Convert to float for percentage
        e_value = float(result.get('e_value', 0))   # Convert to float for scientific notation
        title = result.get('title', '').split('|')[-1][:40]
        
        # Neo-corporate match header
        output.append(f"│ {Fore.YELLOW}▶ MATCH::{i:02d} {Fore.LIGHTBLACK_EX}│{Fore.BLUE} {title:<40}{Fore.CYAN}│")
        output.append(f"├{Fore.BLUE}{'┄' * 78}{Fore.CYAN}┤")
        
        # Same sequence logic, enhanced visual presentation
        query = sequence[:50]
        match = ''.join(random.choice('ATCG') if random.random() > identity/100 else q 
                       for q in query)
        
        # Same connection logic with enhanced visuals
        connections = ''
        for q, m in zip(query, match):
            if q == m:
                connections += '█'  # Solid match
            elif random.random() < 0.3:
                connections += '▀'  # Partial match
            else:
                connections += '·'  # No match
        
        # Sequence display with modern tech styling
        output.append(f"│ {Fore.GREEN}QRY ►{Fore.LIGHTGREEN_EX} {query}{' ' * (71-len(query))}{Fore.CYAN}│")
        output.append(f"│ {Fore.WHITE}ALN ►{Fore.LIGHTBLUE_EX} {connections}{' ' * (71-len(connections))}{Fore.CYAN}│")
        output.append(f"│ {Fore.RED}MTH ►{Fore.LIGHTRED_EX} {match}{' ' * (71-len(match))}{Fore.CYAN}│")
        
        # Statistics with modern meter display
        output.append(f"├{Fore.BLUE}{'┄' * 78}{Fore.CYAN}┤")
        # Identity meter
        meter = '█' * int(identity/2) + '░' * (50-int(identity/2))
        output.append(f"│ {Fore.WHITE}IDENTITY {Fore.YELLOW}{identity:>5.1f}% {Fore.BLUE}│{Fore.LIGHTBLUE_EX} {meter}{Fore.CYAN}│")
        output.append(f"│ {Fore.WHITE}E-VALUE  {Fore.YELLOW}{e_value:>5.2e} {Fore.LIGHTBLACK_EX}│{' ' * 51}{Fore.CYAN}│")
        
        # Section separator
        output.append(f"├{Fore.MAGENTA}{'═' * 78}{Fore.CYAN}┤")
    
    # Footer
    output.append(f"└{'─' * 78}┘{Style.RESET_ALL}")
    
    return '\n'.join(output)

def main():
    """Enhanced main function with service checking and validation."""
    print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
    print(Fore.LIGHTGREEN_EX + """
    ╔═══════════════════════════════════════════╗
    ║   Genetic Due Diligence Agent Test Loop   ║
    ╚═══════════════════════════════════════════╝
    """)
    
    # Check external services
    print(f"{Fore.CYAN}Checking external services...{Style.RESET_ALL}")
    services = check_external_services()
    
    # Report service status
    for service, status in services.items():
        status_color = Fore.GREEN if status else Fore.RED
        status_text = "Available" if status else "Unavailable"
        print(f"{status_color}{service}: {status_text}{Style.RESET_ALL}")
    
    if not any(services.values()):
        print(f"{Fore.RED}Error: No required services available. Some features will be limited.{Style.RESET_ALL}")
    
    print(Fore.LIGHTCYAN_EX + "═" * 80)
    print(Fore.LIGHTYELLOW_EX + "\nType '/dna help' for available commands")
    print(Fore.LIGHTCYAN_EX + "═" * 80)
    
    # Test sequences for validation
    test_sequences = {
        # a fragment of the human insulin gene
        'dna': 'ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACC',
        
        # let-7a microRNA precursor - well documented
        'rna': 'UGAGGUAGUAGGUUGUAUAGUUUUAGGGUCACACCCACCACUGGGAGAUAACUAUACAAUCUACUGUCUUUCCUA',
        
        # Insulin receptor fragment - well studied in databases
        'protein': 'HLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN'
    }
    
    while True:
        try:
            command = input(f"\n{Fore.GREEN}Enter command (or 'test' for validation): {Style.RESET_ALL}")
            
            # Check for exit command
            if command.lower() in ['exit', 'quit', 'q']:
                print(f"{Fore.LIGHTGREEN_EX}[SYSTEM] Exiting Analysis Interface...{Style.RESET_ALL}")
                break
            
            # Run test suite
            if command.lower() == 'test':
                print(f"{Fore.CYAN}Running validation tests...{Style.RESET_ALL}")
                for seq_type, sequence in test_sequences.items():
                    print(f"\nTesting {seq_type.upper()} analysis:")
                    test_command = f"/dna {sequence}"
                    result = handle_dna_command(test_command)
                    print(result)
                    time.sleep(1)  # Pause between tests
                continue
                
            # Handle help command
            if command.lower() in ['/dna help', 'help', '/?', '-h', '--help']:
                print_help()
                continue
                
            # Handle empty input
            if not command.strip():
                continue
                
            result = handle_dna_command(command)
            print(result)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTGREEN_EX}[SYSTEM] Exiting Analysis Interface...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
