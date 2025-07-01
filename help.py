import time
from colorama import Fore
import pygame

# *** Help Command ***
def display_help():
    """Displays a minimal and slick help screen with grouped commands."""
    
    pygame.mixer.init()
    pygame.mixer.music.load (r'E:\Agents\Test 1\helpbell.mp3')
    pygame.mixer.music.play()

    print(Fore.LIGHTGREEN_EX + """
         ██████  ██████  ███████ ██ ██ ███████ 
        ██    ██ ██   ██ ██      ██ ██ ██      
        ██    ██ ██████  ███████ ██ ██ █████   
        ██    ██ ██           ██ ██ ██ ██      
         ██████  ██      ███████ ██ ██ ███████ 
                                                             
        A Self-Centered Intelligence (SCI) Prototype 
        By ARPA HELLENIC LOGICAL SYSTEMS | Version: 0.3.77 SP | 28 APR 2025
    """)
    time.sleep(1)

    grouped_commands = {
        'Mnemonic Matrix Commands': [
            ('/recall <keyword>', 'Pull relevant context from mnemonic matrix.'),
            ('/forget', 'Exclude the last prompt and response pair from being stored.'),
            ('/memorize <keyword>', 'Save an important message for future reference.')
        ],
        'Agentic Matrix Commands': [
            ('/ask <model> <prompt>', 'Query a specific AI model with a follow-up prompt.'),
            ('/markets <keyword> [extra]', 'Retrieve market data for a sector, company, or currency with optional detailed intel. See /help markets.'),
            ('/read <file_path>', 'Read and analyze files using ARPA File Manager TAF-3000.'),
            ('/voice', 'Enable voice mode. /voiceoff disables it.'),
            ('/imagine <description>', 'Generate an image based on a text description. Use /imagine model for advanced settings.'),
            ('/video <description>', 'Generate a video based on a text description.'),
            ('/music <description>', 'Generate music based on a text description.'),
            ('/dna <sequence>', 'Advanced DNA/RNA/Protein sequence analysis.'),
            ('/room <agents>: <theme>', 'Create a temporal nexus with specified agents and theme.'),
            
            ('vision', 'Use image URLs in your prompts to analyze images.')
        ],
        'Web3 Commands': [
            ('/0x buy <amount> <token> using <token> on <chain>', 'Buy tokens on specified chain'),
            ('/0x sell <amount> <token> for <token> on <chain>', 'Sell tokens on specified chain'),
            ('/0x send <chain> <token> <amount> to <recipient>', 'Send tokens to a known user'),
            ('/0x receive', 'Display wallet addresses'),
            ('/0x gas <low|medium|high>', 'Set gas price strategy'),
            ('/0x new token <name> <chain> <address>', 'Add new token configuration'),
            ('/0x new chain <name> <chain_id> <rpc_url>', 'Add new chain configuration'),
            ('/0x forget token <name>', 'Remove token configuration'),
            ('/0x forget chain <name>', 'Remove chain configuration')
        ],
        'System Commands': [
            ('/mail <emails, subject, and message>', 'Send emails by parsing unstructured prompts. See /help mail.'),
            ('/weblimit <number>', 'Set webpage character extraction limit (500-5000).'),
            ('/status', 'Self-checks and system status update.'),
            ('/soulsig <message>', 'Manage your personalized Soul Signature. See /help soulsig for details.')
        ],
        'BETA Commands': [
            ('/help <command>', 'Get elaborate help for specific commands. e.g., /help imagine')
        ]
    }

    for category, commands in grouped_commands.items():
        print(Fore.LIGHTMAGENTA_EX + f'{category}:\n')
        max_command_length = max(len(cmd[0]) for cmd in commands)
        for command, description in commands:
            print(Fore.LIGHTCYAN_EX + f'{command.ljust(max_command_length)}  {Fore.LIGHTWHITE_EX}{description}\n')
        print()

    print(Fore.LIGHTRED_EX + 'Type "exit" or "quit" without / to terminate the session.\n')

detailed_help_texts = {
    'recall': """
/recall <keyword>

Pull relevant context from past conversations and mnemonic matrix.

**Example:**
    /recall project x

This will retrieve memories related to 'project x' from your previous interactions.
""",
    'forget': """
/forget

Exclude the last prompt and response pair from being stored in the mnemonic matrix.

Use this command if you want to prevent the assistant from remembering the last interaction.
For example, if the agent is hallucinating, or the response accuracy temperature is low, 
you can easily exclude the last pair of prompt and response hustle-free.
""",
    'memorize': """
/memorize <keyword>

Save an important message for future reference.

**Example:**
    /memorize Don't forget to submit the report by Friday.

This will store the message so you can recall it later using /recall.
""",
    'ask': """
/ask <model> <prompt>

Query a specific AI model with a follow-up prompt.

**Available Models:**
- Nyx: ARPA Corporation's specialist agent
  - Expertise: blockchain, AI, biotech, neurotech, quantum computing, DNA
  - Specializes in Python prototyping and proof of concepts
  
- G1 Black: Google's advanced AI agent
  - Standard mode: Technical analysis and problem-solving
  - Live mode: Real-time data access and current information
    Example: `/ask g1 live What's happening with Bitcoin right now?`

**Examples:**
    /ask Nyx Write a Python function that reads URLs.
    /ask G1 Analyze the current state of quantum computing.
    /ask G1 live

**Note:**
- Each agent has their own personality and expertise areas
- Live modes provide access to real-time conversational mode with a specific agent.
""",
    'markets': """
/markets <keyword> [extra]

Retrieve market data for a sector, company, currency, or cryptocurrency, with optional detailed information.

/markets compare <stock1> <stock2>

Compare two stocks across key financial metrics important to venture capitalists, competitors, and regulators.

**Examples:**
    /markets energy
    /markets tesla
    /markets shell statistics
    /markets compare tsla nio
    /markets eur
    /markets btc

**Usage:**

1. **Basic Market Data:**

    `/markets <sector>`

    Retrieve market data and news for a specific sector.

    **Example:**
        /markets energy

    This will display the top stocks in the energy sector with performance data and news.

2. **Company Market Data:**

    `/markets <company>`

    Retrieve market data, performance, price chart, and news for a specific company.

    **Example:**
        /markets tesla

    This will display market data for Tesla, including current price, performance metrics, a price chart, and top news articles.

3. **Currency Market Data:**

    `/markets <currency>`

    Retrieve current exchange rate, performance data, an ASCII chart, and additional volume and range statistics for a currency.

    **Example:**
        /markets usd

    This will display market data for USD, including the current price, performance over different periods, and a simple chart.

4. **Cryptocurrency Market Data:**

    `/markets <crypto>`

    Retrieve the latest price, performance metrics, an ASCII chart, and additional data like market cap and circulating supply for a cryptocurrency.

    **Example:**
        /markets btc

    This will display market data for Bitcoin, including current price, performance metrics, an ASCII chart, and volume details.

5. **Detailed Company Information:**

    `/markets <company> <extra>`

    Retrieve detailed information for a company based on the specified extra command.

    **Extras:**

    - **statistics**: Show key statistics for the company, such as valuation measures and financial highlights.
    - **history**: Display historical price data for the company.
    - **profile**: Show the company's profile, including industry, sector, employee count, and a business summary.
    - **financials**: Display the company's financial statements.
    - **analysis**: Provide analyst recommendations and estimates.
    - **options**: List available options expiration dates and show the options chain.
    - **holders**: Display major and institutional shareholders.
    - **sustainability**: Show sustainability metrics and ESG scores.

    **Examples:**
        /markets shell statistics
        /markets tesla financials
        /markets nio analysis

6. **Compare Two Stocks:**

    `/markets compare <stock1> <stock2>`

    Compare two stocks across the top 10 most important verticals for venture capitalists, competitors, and governments/regulators. The comparison includes metrics such as market capitalization, revenue growth, profit margins, and financial ratios.

    **Example:**
        /markets compare tsla nio

    This will display a side-by-side comparison of Tesla and NIO, highlighting key financial metrics to assess their performance and valuation.

**Note:**
- The `/markets` command provides real-time data pulled from Yahoo Finance.
- Ensure you have an active internet connection for the most up-to-date information.
""",

    'dna': """
/dna <sequence> [options]

GDDA (Genetic Due Diligence Analysis) System v0.21 XP

**Sequence Analysis Types:**
- DNA: Automatic detection of DNA sequences
- RNA: RNA-specific analysis with structure prediction
- Protein: Protein sequence analysis and structure prediction

**Core Features:**
1. Basic Analysis:
   - Sequence type detection
   - Length and composition analysis
   - GC content calculation
   - K-mer frequency analysis
   - Anomaly detection

2. Structure Analysis:
   - DNA: Melting temperature, motif detection
   - RNA: Secondary structure prediction, minimum free energy
   - Protein: Secondary structure (α-helix, β-sheet, coil)

3. Advanced Analysis:
   - Homology search with visual alignment
   - Patent and literature search
   - Database cross-references
   - Regulatory element detection
   - Protein family and domain prediction

4. RNA-Specific Features:
   - miRNA targeting sites
   - siRNA regions
   - RNA structure visualization
   - Regulatory elements detection
   - Database references (Rfam, miRBase, GtRNAdb)

5. Protein-Specific Features:
   - Molecular weight calculation
   - Amino acid composition
   - Cellular localization prediction
   - Protein families and domains
   - Hydrophobicity profile
   - UniProt/Pfam/PROSITE references

**Output Format:**
- Cyberpunk-styled visual reports
- Sequence alignments with identity scores
- Structure visualizations
- Publication and patent references
- Interactive data visualization

**Options:**
  --verbose        Detailed analysis output
  --type TYPE      Force specific sequence type
  --format FORMAT  Input format (default/fasta)
  --export FORMAT  Export format (json/csv/txt)
  --homology      Include sequence similarity search
  --structure     Include structure prediction
  --patents       Include patent database search
  --literature    Include scientific literature search

**Examples:**
  /dna ATGCGTAACGGCATTAGC
  /dna --type rna AUGCGUAACGGCAUUAGC
  /dna --verbose --homology MAKVLISPKQW
  /dna --format fasta --export json sequence.fa
""",

    '0x': """
/0x <subcommand> [arguments]

Web3 Transaction Interface Commands:

1. Buy Tokens:
   /0x buy <amount> <token> using <token> on <chain>
   Example: /0x buy 10 degen using eth on base

2. Sell Tokens:
   /0x sell <amount> <token> for <token> on <chain>
   Example: /0x sell 5 degen for eth on base

3. Send Tokens:
   /0x send <chain> <token> <amount> to <recipient>
   Example: /0x send base eth 0.1 to Ross

4. View Addresses:
   /0x receive
   Shows your and OPSIE's wallet addresses

5. Set Gas Strategy:
   /0x gas <low|medium|high>
   Example: /0x gas medium

6. Add New Token:
   /0x new token <name> <chain> <address>
   Example: /0x new token pepe base 0x123...def

7. Add New Chain:
   /0x new chain <name> <chain_id> <rpc_url>
   Example: /0x new chain avalanche 43114 https://api.avax.network/ext/bc/C/rpc

8. Remove Token:
   /0x forget token <name>
   Example: /0x forget token pepe

9. Remove Chain:
   /0x forget chain <name>
   Example: /0x forget chain avalanche

Notes:
- All transactions require confirmation
- Gas prices adjust based on network conditions
- Use known usernames for recipients
- Base chains (Base, Ethereum, Polygon) cannot be removed
- Token addresses must be valid checksummed addresses
""",

    'receive': """
/receive

Display OPSIE’s and the current user’s public wallet addresses.

Use this command to get the addresses for receiving funds or top up your agent's wallet.
This is a beta function, use with caution.
""",
    'imagine': """
/imagine <description>

Generate an image based on a text description.

**Example:**
    /imagine a futuristic city skyline at sunset

    /imagine model to pull current dream engine.
    
**Advanced Settings:**
    /imagine model <model_name>

Use this to set a specific model for image generation.
Models are specified in a hugging-face fashion.
Default model is FLUX, and looks like "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
You don't have to use the full HF URL when using the command, instead use

/imagine model black-forest-labs/FLUX.1-dev

**Example models:**

# nsfw models
# hakurei/waifu-diffusion                                           
# UnfilteredAI/NSFW-gen-v2
# black-forest-labs/FLUX.1-dev
""",
    'music': """
/music <description>

Generate music based on a text description.

**Example:**
    /music calm piano with soft strings

This will generate music matching your description.
After the generation process the audible specimen will be saved locally and then played back.
""",
    'read': """
/read <file_path>

Read and analyze files (PDF, CSV, TXT, DOCX, XLSX) using ARPA File Manager TAF-3000.

**Example:**
    /read "E:\\Documents\\report.pdf"

This will load the specified file for analysis.
Once you use /read and the file has been successfully loaded, you will enter a temporal data pocket.
During the file query context window, TAF-3000 will be assisting you with your requests.

You can type /close to exit the file query context window and return to default conversational mode.
/open will reload the file if it's still in the temporal memory.
""",
    'open': """
/open

Reopen the last loaded file context for follow-up queries.

Use this command to continue interacting with the last file you loaded.

For more details on file-reading try /help read.
""",
    'close': """
/close

Close the current file context.

This will end the file interaction mode and return to normal conversation.

For more details on file-reading try /help read.
""",
    'weblimit': """
/weblimit <number>

Set webpage character extraction limit (500-5000).

**Example:**
    /weblimit 2000

This sets the character limit to 2000 when extracting text from webpages.
This is particularly helpful when browsing large datasets or public domains to avoid overwhelming logical processes. 
""",
    'status': """
/status

Self-checks and system status update.

Use this command to perform system diagnostics and get a status report.
""",
    'voice': """
/voice

Enable voice mode.

**Additional Options:**
    /voiceoff - Disable voice mode.
    /voice1   - OPSIE responds with voice; you type your input.
    /voice2   - You speak your input; OPSIE responds in text.
""",
    'vision': """
vision (beta)

Use image URLs in your prompts to analyze images.

**Example:**
    Provide an image URL in your prompt, and OPSIE will analyze and describe the image.

Note: This feature is in beta and may not work with all images.
""",
    'mail': """
/mail <emails and message>

Send emails by parsing unstructured prompts.

OPSIE can send emails from its native email account by interpreting your unstructured prompts to extract recipients, subject, and message content.

**Examples:**

1. **Send to a Single Email Address:**

    ```
    /mail x@gmail.com with sub "XYZ" and content "Hey this is a test"
    ```

    This sends an email with subject "XYZ" and body "Hey this is a test" to `x@gmail.com`.

2. **Send to Multiple Email Addresses:**

    ```
    /mail x@gmail.com and y@gmail.com subject "123" content "Hi"
    ```

    This sends an email with subject "123" and body "Hi" to both `x@gmail.com` and `y@gmail.com`.

3. **Send Using Contact Names:**

    ```
    /mail send an email to Nick saying "Sup Nick!" with theme "Hello"
    ```

    This sends an email with subject "Hello" and body "Sup Nick!" to the email address associated with "Nick" in the contacts list.

4. **View Unread Emails:**
    ```
    /mail inbox
    ```
    This command allows you to view and manage your unread emails, including reading and replying to them.

**How It Works:**

- OPSIE parses the prompt to extract email addresses or contact names, subject, and body.
- Email addresses are recognized by their format (e.g., name@example.com).
- Contact names are matched to emails using a known contacts dictionary.
- Keywords for subject include: subject, sub, theme, title, header.
- Keywords for body include: content, body, message, msg, context, main, saying.
- The order of elements in the prompt does not matter.

**Notes:**

- You can send emails to up to 5 recipients at once.
- If required information is missing or unclear, OPSIE will provide an error message with guidance.
- All email interactions are stored in the conversation history for reference.

**Privacy Considerations:**

- Be cautious when including sensitive information in emails.
- OPSIE anonymizes or sanitizes sensitive data when storing conversations.
""",
    'help': """
/help <command>

Get elaborate help for specific commands.

**Example:**
    /help imagine

This will display detailed information and examples for the 'imagine' command.
""",
    'soulsig': """
/soulsig

Soul Signatures are personalized prompts that define your unique interaction with Opsie. Each user has their own Soul Signature, which reflects their preferences, personality traits, and past interactions with Opsie.

**Commands:**

1. **View Your Soul Signature:**
   - `/soulsig`
   - This command displays your current Soul Signature.

2. **Add to Your Soul Signature:**
   - `/soulsig <message>`
   - This command allows you to add a new line to your Soul Signature. For example:
     ```
     /soulsig My favorite color is Lilac.
     /soulsig Do not reply using my middle name.
     /soulsig You are my physics lecturer.
     ```

3. **Wipe Your Soul Signature:**
   - `/soulsig wipe`
   - This command clears your Soul Signature, allowing you to start fresh.
   - Once your SoulSig is wiped, it seizes to live in the mnemonic matrix. Permanent data loss is imminent. Proceed with caution!

4. **Heal Your Soul Signature:**
   - `/soulsig heal`
   - This command restores your Soul Signature from temporary storage if it was wiped. Use this if you change your mind after initiating a wipe.

**Note:** Your Soul Signature is a way for Opsie to remember your preferences and enhance your interactions. This data pocket has the highest informational hierarchy in System Prompt.
""",
    'room': """
/room <agent1, agent2...>: <room theme>

Create a temporal virtual nexus where multiple AI agents collaborate and interact.

**Usage:**
    /room nyx, g1: Brainstorm quantum computing applications
    /room g1: Discuss current AI trends
    
**Features:**
- OPSIE is automatically included in all rooms
- Agents share their system prompts for context awareness
- Real-time collaborative discussion and brainstorming
- Agents can debate, evaluate, and build upon each other's ideas
- Room theme guides the conversation focus

**Commands in Room:**
- Address specific agents by starting message with their name
  Example: "Nyx, what do you think about this approach?"
- `/close` - Exit the room (with option to save conversation)

**Room Storage:**
- When closing a room, you'll be asked to save the conversation
- If saved, conversations are stored as CSV files for future reference

**Note:**
- Multiple agents can participate in the same conversation
- Each agent maintains their unique personality and expertise
- Conversations are contextual and build upon previous messages
""",
    'video': """
/video <description>

Generate a video based on a text description.

**Example:**
    /video a sunset timelapse over a city skyline

This will generate a video matching your description.
After the generation process, the visual sequence will be saved locally and then played back.

Note: Video generation may take longer than other media types due to the complexity of processing.
The generated videos are saved in the OPSIIE Generated Videos directory.
"""
}

def display_detailed_help(command_name):
    """Displays detailed help for a specific command."""
    help_text = detailed_help_texts.get(command_name)
    if help_text:
        print(Fore.LIGHTCYAN_EX + help_text)
    else:
        print(Fore.RED + f"No detailed help found for command: {command_name}")
