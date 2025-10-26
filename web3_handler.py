# web3.py
# For the more advanced and self-sustainable version of the Web3 Handler with dynamic NLP execution, check: https://github.com/arpahls/hermes3

import os
import re
import json
from decimal import Decimal
from dotenv import load_dotenv
from web3 import Web3
from colorama import Fore, Style
from kun import known_user_names
import time
import requests

# Load environment variables from .env
load_dotenv()

# Retrieve the agent's private key and RPC URLs from the environment
AGENT_PRIVATE_KEY = os.getenv("AGENT_PRIVATE_KEY")
BASE_RPC_URL = os.getenv("BASE_RPC_URL")
ETHEREUM_RPC_URL = os.getenv("ETHEREUM_RPC_URL")
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL")

# Error handling if environment variables are missing
if not AGENT_PRIVATE_KEY or not BASE_RPC_URL or not ETHEREUM_RPC_URL or not POLYGON_RPC_URL:
    print(Fore.RED + "Error: Missing environment variables. Check your .env file.")
    exit()

# Initialize Web3 Connections for multiple chains
CHAIN_INFO = {
    'Base': {
        'chain_id': 8453,
        'rpc_url': BASE_RPC_URL,
        'symbol': 'ETH',
        'decimals': 18,
        'explorer_url': 'https://basescan.org',
    },
    'Ethereum': {
        'chain_id': 1,
        'rpc_url': ETHEREUM_RPC_URL,
        'symbol': 'ETH',
        'decimals': 18,
        'explorer_url': 'https://etherscan.io',
    },
    'Polygon': {
        'chain_id': 137,
        'rpc_url': POLYGON_RPC_URL,
        'symbol': 'MATIC',
        'decimals': 18,
        'explorer_url': 'https://polygonscan.com',
    },
}

# Token dictionary with human-readable names
TOKENS = {
    'Degen': {
        'Base': '0x4ed4e862860bed51a9570b96d89af5e1b0efefed',
        'Ethereum': '0xABCDEF1234567890ABCDEF1234567890ABCDEF12',
        'Polygon': '0x1234567890ABCDEF1234567890ABCDEF12345678'
    },
    'USDC': {
        'Base': '0x7F5c764cBc14f9669B88837ca1490cCa17c31607',
        'Ethereum': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606EB48',
        'Polygon': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
    },
}

# Web3 connection object and gas strategy
web3_connection = None
gas_strategy = 'medium'

# Token ABI for ERC20 tokens (simplified)
TOKEN_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Add this near the top of the file with other constants
ROUTER_ABI = [
    # Quotes
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"}
        ],
        "name": "getAmountsIn",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"}
        ],
        "name": "getAmountsOut",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    # Swapping
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactETHForTokens",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactTokensForETH",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    # Factory
    {
        "inputs": [],
        "name": "factory",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    # WETH
    {
        "inputs": [],
        "name": "WETH",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class Web3Handler:
    def __init__(self, known_user_names):
        """Initialize Web3Handler with user data"""
        self.known_user_names = known_user_names
        self.web3_connection = None
        self.current_chain = None
        
        # Use the code's dictionaries as primary source
        self.CHAIN_INFO = CHAIN_INFO.copy()
        self.TOKENS = TOKENS.copy()
        
        # Get the directory for temporary JSON storage
        self.config_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.gas_strategy = 'medium'
        self.AGENT_WALLET = {
            'private_key': AGENT_PRIVATE_KEY,
            'public_key': Web3.to_checksum_address('0x89A7f83Db9C1919B89370182002ffE5dfFc03e21')
        }
        # Initialize connection to default chain
        self.connect_to_chain('Base')

    def save_chain_config(self):
        """Save chain configuration to JSON file"""
        with open('chain_config.json', 'w') as f:
            json.dump(self.CHAIN_INFO, f, indent=4)

    def save_token_config(self):
        """Save token configuration to JSON file"""
        with open('token_config.json', 'w') as f:
            json.dump(self.TOKENS, f, indent=4)

    def add_chain(self):
        """Add a new chain configuration"""
        try:
            print(Fore.YELLOW + "\nAdding new chain configuration:")
            
            # Get chain details
            chain_name = input("Chain name: ").strip()
            if chain_name in self.CHAIN_INFO:
                print(Fore.RED + "Chain already exists!")
                return

            try:
                chain_id = int(input("Chain ID: ").strip())
                rpc_url = input("RPC URL: ").strip()
                symbol = input("Native token symbol: ").strip()
                explorer_url = input("Block explorer URL: ").strip()

                # Test connection
                web3 = Web3(Web3.HTTPProvider(rpc_url))
                if not web3.is_connected():
                    raise ValueError("Unable to connect to RPC URL")

                # Update runtime dictionary
                self.CHAIN_INFO[chain_name] = {
                    'chain_id': chain_id,
                    'rpc_url': rpc_url,
                    'symbol': symbol,
                    'decimals': 18,
                    'explorer_url': explorer_url
                }

                # Save to temporary JSON for persistence until code is updated
                self.save_chain_config()

                # Update the Python file
                self._update_python_file_chain(chain_name)

                print(Fore.GREEN + f"\nChain {chain_name} added successfully!")

            except Exception as e:
                raise ValueError(f"Failed to add chain: {str(e)}")

        except Exception as e:
            raise ValueError(f"Failed to add chain: {str(e)}")

    def add_token(self):
        """Interactive token addition"""
        print(Fore.YELLOW + "\nAdding new token configuration:")
        
        # Get token details
        token_name = input("Token name: ").strip()
        chain_name = input("Chain name: ").strip()
        
        if chain_name not in self.CHAIN_INFO:
            print(Fore.RED + f"Chain {chain_name} not supported!")
            return

        try:
            contract_address = input("Contract address: ").strip()
            contract_address = Web3.to_checksum_address(contract_address)
            
            # Verify contract
            web3 = Web3(Web3.HTTPProvider(self.CHAIN_INFO[chain_name]['rpc_url']))
            contract = web3.eth.contract(address=contract_address, abi=TOKEN_ABI)
            
            # Try to get token symbol
            symbol = contract.functions.symbol().call()
            
            # Add token
            if token_name not in self.TOKENS:
                self.TOKENS[token_name] = {}
            
            self.TOKENS[token_name][chain_name] = contract_address
            self.TOKENS[token_name]['symbol'] = symbol
            
        
            print(Fore.GREEN + f"\nToken {token_name} ({symbol}) added successfully on {chain_name}!")

        except Exception as e:
            print(Fore.RED + f"Error adding token: {str(e)}")

    def connect_to_chain(self, chain_name):
        """Establish a connection to the specified blockchain."""
        if chain_name not in self.CHAIN_INFO:
            print(Fore.RED + f"Error: Chain '{chain_name}' not supported.")
            return False

        chain = self.CHAIN_INFO[chain_name]
        try:
            provider = Web3.HTTPProvider(chain['rpc_url'])
            self.web3_connection = Web3(provider)
            
            if self.web3_connection.is_connected():
                self.current_chain = chain_name
                return True
            else:
                print(Fore.RED + f"Failed to connect to {chain_name}")
                return False
            
        except Exception as e:
            print(Fore.RED + f"Error connecting to {chain_name}: {str(e)}")
            return False

    def get_gas_price(self):
        """Return gas price based on the current strategy (low, medium, high)."""
        if self.gas_strategy == 'low':
            return self.web3_connection.eth.gas_price * 0.8
        elif self.gas_strategy == 'high':
            return self.web3_connection.eth.gas_price * 1.5
        else:  # medium is default
            return self.web3_connection.eth.gas_price

    def set_gas_strategy(self, level):
        """Set the gas strategy for transactions."""
        if level in ['low', 'medium', 'high']:
            self.gas_strategy = level
            print(Fore.GREEN + f"Gas strategy set to {self.gas_strategy}.")
        else:
            print(Fore.RED + "Error: Invalid gas level. Choose 'low', 'medium', or 'high'.")

    def get_recipient_address(self, recipient_name):
        """Fetch recipient's public Ethereum address by matching full_name or call_name."""
        for user in self.known_user_names.values():
            if user['full_name'].lower() == recipient_name.lower() or user['call_name'].lower() == recipient_name.lower():
                return user['public0x']
        return None

    def confirm_transaction(self):
        """Ask the user for confirmation before committing the transaction."""
        print(Fore.LIGHTRED_EX + "Please confirm the transaction by typing or saying 'confirm' or cancel by typing 'cancel'.")
        user_input = input().strip().lower()
        if user_input == 'confirm':
            return True
        elif user_input == 'cancel':
            print(Fore.RED + "Transaction cancelled.")
            return False
        else:
            print(Fore.RED + "Invalid input. Transaction cancelled.")
            return False

    def get_transaction_url(self, chain_name, tx_hash):
        """Returns the appropriate URL for viewing the transaction based on the chain."""
        if chain_name in self.CHAIN_INFO and 'explorer_url' in self.CHAIN_INFO[chain_name]:
            base_url = self.CHAIN_INFO[chain_name]['explorer_url'].rstrip('/')
            return f"{base_url}/tx/{tx_hash}"
        return f"Unknown chain: {chain_name}"

    def send_tokens(self, chain, token_name, amount, recipient_name):
        # First, ensure connection to the right chain
        if not self.connect_to_chain(chain):
            print(Fore.RED + f"Error: Failed to connect to {chain}.")
            return

        recipient_address = self.get_recipient_address(recipient_name)
        if not recipient_address:
            print(Fore.RED + f"Error: Recipient '{recipient_name}' not found or has no known public address.")
            return

        # Set default token as native token if not specified
        if token_name == '':
            token_name = self.CHAIN_INFO[chain]['symbol']

        chain_data = self.CHAIN_INFO[chain]

        print(Fore.LIGHTYELLOW_EX + f"Preparing to send {amount} {token_name} to {recipient_name} ({recipient_address}) on {chain} network.")
        
        if not self.confirm_transaction():
            return

        if token_name == chain_data['symbol']:  # Native token
            amount_in_wei = self.web3_connection.to_wei(amount, 'ether')
            transaction = {
                'from': self.AGENT_WALLET['public_key'],
                'to': recipient_address,
                'value': amount_in_wei,
                'gas': 21000,
                'gasPrice': self.get_gas_price(),
                'chainId': chain_data['chain_id'],
            }

            signed_txn = self.web3_connection.eth.account.sign_transaction(
                transaction, 
                private_key=self.AGENT_WALLET['private_key']
            )
            tx_hash = self.web3_connection.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Get transaction URL and print success message
            tx_url = self.get_transaction_url(chain, self.web3_connection.to_hex(tx_hash))
            print(Fore.LIGHTGREEN_EX + f"Transaction sent! View it on explorer: {tx_url}")

        else:  # ERC-20 token
            token_address = self.TOKENS.get(token_name, {}).get(chain)
            if not token_address:
                print(Fore.RED + f"Error: Token '{token_name}' is not supported on {chain}.")
                return

            token_contract = self.web3_connection.eth.contract(
                address=Web3.to_checksum_address(token_address), 
                abi=TOKEN_ABI
            )
            amount_in_wei = self.web3_connection.to_wei(amount, 'ether')

            transaction = token_contract.functions.transfer(
                recipient_address, 
                amount_in_wei
            ).build_transaction({
                'from': self.AGENT_WALLET['public_key'],
                'gas': 100000,
                'gasPrice': self.get_gas_price(),
                'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                'chainId': chain_data['chain_id'],
            })

            signed_txn = self.web3_connection.eth.account.sign_transaction(
                transaction,
                private_key=self.AGENT_WALLET['private_key']
            )
            tx_hash = self.web3_connection.eth.send_raw_transaction(signed_txn.raw_transaction)

            # Get transaction URL and print success message
            tx_url = self.get_transaction_url(chain, self.web3_connection.to_hex(tx_hash))
            print(Fore.LIGHTGREEN_EX + f"Transaction sent! View it on explorer: {tx_url}")

    def handle_send_command(self, command, agent_voice_active=False, voice_mode_active=False, speak_response=None):
        """Handle the /send command logic."""
        try:
            match = re.match(r'(?:/send|/0x\s+send)\s+(\w+)\s+([\w|\'\']+)\s+(\d+(\.\d+)?)\s+to\s+(\w+)', command)
            if not match:
                raise ValueError("Invalid command format. Use: /send <chain> <token|''> <amount> to <recipient>.")
            
            chain = match.group(1).capitalize()
            token_name = match.group(2).capitalize()
            amount = float(match.group(3))
            recipient_name = match.group(5)
            
            if chain not in self.CHAIN_INFO:
                chain_matches = [c for c in self.CHAIN_INFO.keys() if c.lower() == chain.lower()]
                if chain_matches:
                    chain = chain_matches[0]
                else:
                    raise ValueError(f"Chain '{chain}' is not supported.")

            # Check if token exists (case-insensitive)
            if token_name and token_name not in self.TOKENS:  # Fix: Use global TOKENS
                token_matches = [t for t in self.TOKENS.keys() if t.lower() == token_name.lower()]
                if token_matches:
                    token_name = token_matches[0]
                else:
                    raise ValueError(f"Token '{token_name}' is not supported.")

            self.send_tokens(chain, token_name, amount, recipient_name)

        except ValueError as ve:
            error_message = f"Error: {ve}"
            print(Fore.RED + error_message)
            if agent_voice_active or voice_mode_active and speak_response:
                speak_response(error_message)

    def handle_gas_command(self, command):
        """Handle the /send gas command."""
        try:
            args = command.split()
            if len(args) < 2:
                raise ValueError("Invalid format. Use: /send gas <low|medium|high>.")

            gas_level = args[2]
            self.set_gas_strategy(gas_level)

        except ValueError as ve:
            print(Fore.RED + f"Error: {ve}")

    def handle_receive_command(self, current_user=None):
        """Display wallet addresses and supported tokens/chains"""
        print(Fore.LIGHTMAGENTA_EX + "\nWallet Information & Supported Assets")
        print("=" * 50)

        # Display wallet addresses
        if current_user and current_user in self.known_user_names:
            user_wallet = self.known_user_names[current_user]['public0x']
            print(Fore.LIGHTYELLOW_EX + f"\n{current_user}'s Wallet:")
            print(f"Address: {user_wallet}")
        
        print(Fore.LIGHTYELLOW_EX + "\nOPSIE's Wallet:")
        print(f"Address: {self.AGENT_WALLET['public_key']}")

        # Display supported chains
        print(Fore.LIGHTYELLOW_EX + "\nSupported Chains:")
        for chain_name, chain_data in self.CHAIN_INFO.items():  # Fix: Use global CHAIN_INFO
            print(f"\n{chain_name}:")
            print(f"  Native Token: {chain_data['symbol']}")
            print(f"  Explorer: {chain_data['explorer_url']}")

        # Display supported tokens per chain
        print(Fore.LIGHTYELLOW_EX + "\nSupported Tokens:")
        for chain_name in self.CHAIN_INFO.keys():  # Fix: Use global CHAIN_INFO
            print(f"\n{chain_name} Tokens:")
            chain_tokens = [token for token, data in self.TOKENS.items()  # Fix: Use global TOKENS
                           if chain_name in data]
            for token in chain_tokens:
                contract = self.TOKENS[token].get(chain_name)  # Fix: Use global TOKENS
                print(f"  {token}: {contract}")

        print("\n" + "=" * 50)

    def parse_transaction_intent(self, command):
        """Parse user's natural language input into transaction parameters"""
        if not command:
            return None
        
        # Normalize input
        command = command.lower().strip()
        
        # Initialize parameters
        params = {
            'action': None,      # buy, sell
            'amount': None,      # numeric amount, 'all', 'half', '50%', etc.
            'token': None,       # token to buy/sell
            'chain': None,       # chain to operate on
            'using_token': None, # token to pay with (for buy) or receive (for sell)
            'amount_is_target': False  # True if amount refers to using_token instead of main token
        }

        # Extract chain (look for "on <chain>")
        chain_match = re.search(r'on\s+(\w+)', command)
        if chain_match and chain_match.group(1):
            chain_name = chain_match.group(1).capitalize()
            if chain_name in self.CHAIN_INFO:  # Fix: Use global CHAIN_INFO
                params['chain'] = chain_name

        # Determine action
        if 'sell' in command:
            params['action'] = 'sell'
        elif 'buy' in command:
            params['action'] = 'buy'

        # Extract amount and token
        amount_patterns = [
            r'(all)(?:\s+my)?\s+(\w+)',
            r'(half)(?:\s+of)?\s+(?:my)?\s+(\w+)',
            r'(\d+(?:\.\d+)?%?)(?:\s+of)?\s+(?:my)?\s+(\w+)',
            r'(\d+(?:\.\d+)?)\s+(\w+)'
        ]

        for pattern in amount_patterns:
            match = re.search(pattern, command)
            if match:
                amount_str, token_name = match.groups()
                
                # Process amount
                if amount_str == 'all':
                    params['amount'] = 'all'
                elif amount_str == 'half':
                    params['amount'] = '50%'
                elif '%' in amount_str:
                    params['amount'] = amount_str
                else:
                    try:
                        params['amount'] = float(amount_str)
                    except ValueError:
                        continue

                # Find matching token
                for trusted_token in self.TOKENS:  # Fix: Use global TOKENS
                    if trusted_token.lower() == token_name.lower():
                        params['token'] = trusted_token
                        break
                
                # Check if it's a native token
                for chain_name, chain_data in self.CHAIN_INFO.items():  # Fix: Use global CHAIN_INFO
                    if chain_data.get('symbol', '').lower() == token_name.lower():
                        params['token'] = chain_data['symbol']
                        break
                
                if params['token']:
                    break

        # Handle target token amount (e.g., "sell degen for 0.1 eth")
        for pattern in [r'for\s+(\d+(?:\.\d+)?)\s+(\w+)', r'using\s+(\d+(?:\.\d+)?)\s+(\w+)']:
            match = re.search(pattern, command)
            if match:
                amount_str, token_name = match.groups()
                try:
                    params['amount'] = float(amount_str)
                    params['amount_is_target'] = True
                    
                    # Check if it's a native token
                    for chain_name, chain_data in self.CHAIN_INFO.items():  # Fix: Use global CHAIN_INFO
                        if chain_data.get('symbol', '').lower() == token_name.lower():
                            params['using_token'] = chain_data['symbol']
                            break
                    
                    # If not native, check trusted tokens
                    if not params['using_token']:
                        for trusted_token in self.TOKENS:  # Fix: Use global TOKENS
                            if trusted_token.lower() == token_name.lower():
                                params['using_token'] = trusted_token
                                break
                except ValueError:
                    continue

        # If no target amount found, look for target token
        if not params['using_token']:
            for pattern in [r'for\s+(\w+)', r'using\s+(\w+)']:
                match = re.search(pattern, command)
                if match and match.group(1):
                    token_name = match.group(1)
                    # Check native tokens
                    for chain_name, chain_data in self.CHAIN_INFO.items():  # Fix: Use global CHAIN_INFO
                        if chain_data.get('symbol', '').lower() == token_name.lower():
                            params['using_token'] = chain_data['symbol']
                            break
                    # Check trusted tokens
                    if not params['using_token']:
                        for trusted_token in self.TOKENS:  # Fix: Use global TOKENS
                            if trusted_token.lower() == token_name.lower():
                                params['using_token'] = trusted_token
                                break

        return params

    def validate_and_complete_transaction(self, params):
        """Validate transaction parameters and prompt for missing information"""
        if not params:
            raise ValueError("Could not understand transaction intent. Please try again.")

        # Validate/prompt for chain
        if not params['chain']:
            print(Fore.YELLOW + "\nAvailable chains:")
            for chain in self.CHAIN_INFO.keys():
                print(f"- {chain}")
            chain_input = input("Which chain would you like to use? ").strip()
            if chain_input.capitalize() in self.CHAIN_INFO:
                params['chain'] = chain_input.capitalize()
            else:
                raise ValueError(f"Unsupported chain: {chain_input}")

        # Validate/prompt for token
        if not params['token']:
            print(Fore.YELLOW + f"\nAvailable tokens on {params['chain']}:")
            available_tokens = [token for token, data in self.TOKENS.items() 
                              if params['chain'] in data]
            for token in available_tokens:
                print(f"- {token}")
            token_input = input("Which token would you like to trade? ").strip().upper()
            if token_input in [t.upper() for t in available_tokens]:
                params['token'] = next(t for t in available_tokens if t.upper() == token_input)
            else:
                raise ValueError(f"Unsupported token: {token_input}")

        # For buy/sell operations, validate/prompt for using_token
        if params['action'] in ['buy', 'sell'] and not params['using_token']:
            print(Fore.YELLOW + f"\nAvailable tokens to trade with:")
            # Get available tokens excluding the one being traded
            available_tokens = [token for token, data in self.TOKENS.items() 
                              if params['chain'] in data and token != params['token']]
            # Add native token
            native_token = self.CHAIN_INFO[params['chain']]['symbol']
            available_tokens.append(native_token)
            
            for token in available_tokens:
                print(f"- {token}")
            token_input = input(f"Which token would you like to {'pay with' if params['action'] == 'buy' else 'receive'}? ").strip().upper()
            
            if token_input in [t.upper() for t in available_tokens]:
                params['using_token'] = next(t for t in available_tokens if t.upper() == token_input)
            else:
                raise ValueError(f"Unsupported token: {token_input}")

        # Validate/prompt for amount
        if not params['amount'] and params['amount'] != 0:
            amount_input = input("How much would you like to trade? (or 'all' for entire balance) ").strip()
            if amount_input.lower() == 'all':
                params['amount'] = 'all'
            else:
                try:
                    params['amount'] = float(amount_input)
                except ValueError:
                    raise ValueError("Invalid amount specified")

        return params

    def format_transaction_preview(self, params, price_data):
        """Format transaction details for user confirmation"""
        preview = []
        
        if params['action'] in ['buy', 'sell']:
            # Token amounts
            if params['action'] == 'buy':
                preview.extend([
                    "Price Quotes:",
                    "Best Price from DEX:",
                    f"  You give: {price_data['amount_in_formatted']} {params['using_token']}",
                    f"  You get:  {price_data['amount_out_formatted']} {params['token']}"
                ])
            else:  # sell remains unchanged
                preview.extend([
                    "Price Quotes:",
                    "Best Price from DEX:",
                    f"  You give: {params['amount']} {params['token']}",
                    f"  You get:  {price_data['amount_out_formatted']} {params['using_token']}"
                ])

            # Exchange rate
            if params['action'] == 'buy':
                preview.extend([
                    "",
                    "Exchange Rate:",
                    f"  1 {params['using_token']} = {1/price_data['exchange_rate']:.6f} {params['token']}"
                ])
            else:  # sell remains unchanged
                preview.extend([
                    "",
                    "Exchange Rate:",
                    f"  1 {params['token']} = {price_data['exchange_rate']:.6f} {params['using_token']}"
                ])

            # Rest of the preview formatting remains the same
            preview.extend([
                "",
                "USD Values:",
                f"  Input:  ${price_data['usd_values']['input']:.2f}",
                f"  Output: ${price_data['usd_values']['output']:.2f}",
                f"  Price Impact: {((price_data['usd_values']['output'] - price_data['usd_values']['input']) / price_data['usd_values']['input'] * 100):.2f}%",
                "",
                "Available Routes:"
            ])
            for route in price_data['all_quotes']['dexes']:
                preview.append(f"  - {route['name']} via {route['router']}")

        return "\n".join(preview)

    def get_best_price(self, params):
        """Get best price across multiple DEXes with USD values"""
        try:
            # Ensure we have a connection
            if not self.web3_connection or not self.web3_connection.is_connected():
                if not self.connect_to_chain(params['chain']):
                    raise ValueError(f"Failed to connect to {params['chain']}")

            router = self.get_dex_router(params['chain'])
            
            token_address = Web3.to_checksum_address(self.TOKENS[params['token']][params['chain']])
            using_token_address = (self.get_weth_address(params['chain']) 
                                 if params['using_token'] == self.CHAIN_INFO[params['chain']]['symbol']
                                 else Web3.to_checksum_address(self.TOKENS[params['using_token']][params['chain']]))

            if params['action'] == 'buy':
                # Get token decimals
                token_contract = self.web3_connection.eth.contract(
                    address=token_address,
                    abi=TOKEN_ABI
                )
                token_decimals = token_contract.functions.decimals().call()
                
                # Calculate the target amount of tokens we want to buy
                amount_out = int(float(params['amount']) * (10 ** token_decimals))
                # Get amounts from router using getAmountsIn()
                amounts = router.functions.getAmountsIn(
                    amount_out,  # Amount of tokens we want to receive
                    [using_token_address, token_address]  # Path: ETH -> Token
                ).call()
                
                amount_in = amounts[0]  # This is how much ETH we need to pay
                
                # Format amounts for display
                amount_in_formatted = Web3.from_wei(amount_in, 'ether')
                amount_out_formatted = float(params['amount'])
                
                # Get USD values
                eth_price = self.get_token_usd_price('ETH', params['chain'])
                input_usd = float(amount_in_formatted) * eth_price
                output_usd = input_usd  # Simplified for now

                return {
                    'source': 'DEX',
                    'amount_in': amount_in,
                    'amount_in_formatted': amount_in_formatted,
                    'amount_out': amount_out,
                    'amount_out_formatted': amount_out_formatted,
                    # For display purposes, we want to show how many tokens per ETH
                    'exchange_rate': float(amount_in_formatted) / float(amount_out_formatted),
                    'decimals': {
                        'from': 18,  # ETH decimals
                        'to': token_decimals
                    },
                    'usd_values': {
                        'input': input_usd,
                        'output': output_usd
                    },
                    'quote': {
                        'router': router.address,
                        'path': [using_token_address, token_address]
                    },
                    'all_quotes': {
                        'dexes': [{
                            'name': 'BaseSwap',
                            'router': router.address
                        }]
                    }
                }
            else:  # sell
                # Get token decimals
                token_contract = self.web3_connection.eth.contract(
                    address=token_address,
                    abi=TOKEN_ABI
                )
                token_decimals = token_contract.functions.decimals().call()
                
                # Calculate amount in wei
                amount_in = int(float(params['amount']) * (10 ** token_decimals))
                
                # Get amounts from router
                amounts = router.functions.getAmountsOut(
                    amount_in,
                    [token_address, using_token_address]
                ).call()
                
                amount_out = amounts[1]
                
                # Format amounts for display
                amount_in_formatted = float(params['amount'])
                amount_out_formatted = Web3.from_wei(amount_out, 'ether')
                
                # Calculate exchange rate
                exchange_rate = float(amount_out_formatted) / float(amount_in_formatted)
                
                # Get USD values
                eth_price = self.get_token_usd_price('ETH', params['chain'])
                output_usd = float(amount_out_formatted) * eth_price
                input_usd = output_usd  # Simplified for now

                return {
                    'source': 'DEX',
                    'amount_in': amount_in,
                    'amount_in_formatted': amount_in_formatted,
                    'amount_out': amount_out,
                    'amount_out_formatted': amount_out_formatted,
                    'exchange_rate': exchange_rate,
                    'decimals': {
                        'from': token_decimals,
                        'to': 18  # ETH decimals
                    },
                    'usd_values': {
                        'input': input_usd,
                        'output': output_usd
                    },
                    'quote': {
                        'router': router.address,
                        'path': [token_address, using_token_address]
                    },
                    'all_quotes': {
                        'dexes': [{
                            'name': 'UniswapV2',
                            'router': router.address
                        }]
                    }
                }

        except Exception as e:
            raise ValueError(f"Failed to get price: {str(e)}")

    def execute_buy(self, params):
        """Execute a buy transaction with additional validation"""
        try:
            if not self.connect_to_chain(params['chain']):
                raise ValueError(f"Failed to connect to {params['chain']}")

            # Get price quote first
            price_quote = self.get_best_price(params)
            
            token_address = Web3.to_checksum_address(self.TOKENS[params['token']][params['chain']])
            using_token_address = (self.get_weth_address(params['chain']) 
                                 if params['using_token'] == self.CHAIN_INFO[params['chain']]['symbol']
                                 else Web3.to_checksum_address(self.TOKENS[params['using_token']][params['chain']]))
            
            router = self.get_dex_router(params['chain'])
            
            # Calculate slippage and deadline
            slippage = 0.005  # 0.5% slippage tolerance
            amount_out_min = int(price_quote['amount_out'] * (1 - slippage))
            deadline = int(time.time()) + 300  # 5 minutes

            if params['using_token'] == self.CHAIN_INFO[params['chain']]['symbol']:
                # Check ETH balance
                balance = self.web3_connection.eth.get_balance(self.AGENT_WALLET['public_key'])
                if balance < price_quote['amount_in']:
                    raise ValueError(f"Insufficient ETH balance. Need {Web3.from_wei(price_quote['amount_in'], 'ether')} ETH")

                # Execute ETH swap
                swap_tx = router.functions.swapExactETHForTokens(
                    amount_out_min,  # minimum amount of tokens to receive
                    [using_token_address, token_address],  # path
                    self.AGENT_WALLET['public_key'],  # recipient
                    deadline
                ).build_transaction({
                    'from': self.AGENT_WALLET['public_key'],
                    'value': price_quote['amount_in'],  # amount of ETH to send
                    'gas': 250000,
                    'gasPrice': self.get_gas_price(),
                    'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                    'chainId': self.web3_connection.eth.chain_id
                })

            else:
                # Handle ERC20 token
                token_contract = self.web3_connection.eth.contract(
                    address=using_token_address,
                    abi=TOKEN_ABI
                )
                
                # Check token balance
                balance = token_contract.functions.balanceOf(self.AGENT_WALLET['public_key']).call()
                if balance < price_quote['amount_in']:
                    raise ValueError(f"Insufficient {params['using_token']} balance")

                # Approve tokens if needed
                allowance = token_contract.functions.allowance(
                    self.AGENT_WALLET['public_key'],
                    router.address
                ).call()
                
                if allowance < price_quote['amount_in']:
                    approve_tx = token_contract.functions.approve(
                        router.address,
                        price_quote['amount_in']
                    ).build_transaction({
                        'from': self.AGENT_WALLET['public_key'],
                        'gas': 100000,
                        'gasPrice': self.get_gas_price(),
                        'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                        'chainId': self.web3_connection.eth.chain_id
                    })
                    
                    signed_tx = self.web3_connection.eth.account.sign_transaction(
                        approve_tx,
                        private_key=self.AGENT_WALLET['private_key']
                    )
                    tx_hash = self.web3_connection.eth.send_raw_transaction(signed_tx.raw_transaction)
                    self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)

                # Execute token swap
                swap_tx = router.functions.swapExactTokensForTokens(
                    price_quote['amount_in'],  # amount of tokens to send
                    amount_out_min,  # minimum amount of tokens to receive
                    [using_token_address, token_address],  # path
                    self.AGENT_WALLET['public_key'],  # recipient
                    deadline
                ).build_transaction({
                    'from': self.AGENT_WALLET['public_key'],
                    'gas': 250000,
                    'gasPrice': self.get_gas_price(),
                    'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                    'chainId': self.web3_connection.eth.chain_id
                })

            # Sign and send transaction
            signed_tx = self.web3_connection.eth.account.sign_transaction(
                swap_tx,
                private_key=self.AGENT_WALLET['private_key']
            )
            tx_hash = self.web3_connection.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)

            if receipt['status'] == 1:
                success_message = (
                    f"\nBought {price_quote['amount_out_formatted']} {params['token']} "
                    f"using {price_quote['amount_in_formatted']} {params['using_token']} "
                    f"at rate 1 {params['using_token']} = {1/price_quote['exchange_rate']:.8f} {params['token']} "
                    f"via UniswapV2 pool"
                )
                print(Fore.GREEN + success_message)
                print(f"View on explorer: {self.CHAIN_INFO[params['chain']]['explorer_url']}/tx/{self.web3_connection.to_hex(tx_hash)}")
            else:
                raise ValueError("Swap transaction failed!")

        except Exception as e:
            raise ValueError(f"Buy transaction failed: {str(e)}")

    def execute_sell(self, params):
        """Execute a sell transaction on DEX"""
        try:
            if not self.connect_to_chain(params['chain']):
                raise ValueError(f"Failed to connect to {params['chain']}")

            # Get price quote first
            price_quote = self.get_best_price(params)
            
            token_address = Web3.to_checksum_address(self.TOKENS[params['token']][params['chain']])
            using_token_address = (self.get_weth_address(params['chain']) 
                                 if params['using_token'] == self.CHAIN_INFO[params['chain']]['symbol']
                                 else Web3.to_checksum_address(self.TOKENS[params['using_token']][params['chain']]))
            
            router = self.get_dex_router(params['chain'])
            
            # Create token contract
            token_contract = self.web3_connection.eth.contract(
                address=token_address,
                abi=TOKEN_ABI
            )

            decimals = token_contract.functions.decimals().call()
            amount_in_wei = int(params['amount'] * (10 ** decimals))
            
            # Calculate minimum tokens out with slippage
            slippage = 0.005  # 0.5% slippage tolerance
            min_tokens_out = int(price_quote['amount_out'] * (1 - slippage))
            deadline = int(time.time()) + 300  # 5 minutes

            # Approve tokens first
            approve_tx = token_contract.functions.approve(
                router.address,
                amount_in_wei
            ).build_transaction({
                'from': self.AGENT_WALLET['public_key'],
                'gas': 100000,
                'gasPrice': self.get_gas_price(),
                'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                'chainId': self.web3_connection.eth.chain_id
            })

            # Sign and send approval
            signed_approve = self.web3_connection.eth.account.sign_transaction(
                approve_tx,
                private_key=self.AGENT_WALLET['private_key']
            )
            
            try:
                raw_tx = signed_approve.raw_transaction
            except AttributeError:
                raw_tx = signed_approve.rawTransaction
            
            tx_hash = self.web3_connection.eth.send_raw_transaction(raw_tx)
            receipt = self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt['status'] != 1:
                raise ValueError("Token approval failed")

            print(Fore.GREEN + "Token approval successful")

            # Execute swap transaction
            swap_tx = router.functions.swapExactTokensForETH(
                amount_in_wei,
                min_tokens_out,
                [token_address, self.get_weth_address(params['chain'])],
                self.AGENT_WALLET['public_key'],
                deadline
            ).build_transaction({
                'from': self.AGENT_WALLET['public_key'],
                'gas': 250000,
                'gasPrice': self.get_gas_price(),
                'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                'chainId': self.web3_connection.eth.chain_id
            })

            # Sign and send swap transaction
            signed_tx = self.web3_connection.eth.account.sign_transaction(
                swap_tx,
                private_key=self.AGENT_WALLET['private_key']
            )
            
            try:
                raw_tx = signed_tx.raw_transaction
            except AttributeError:
                raw_tx = signed_tx.rawTransaction
            
            tx_hash = self.web3_connection.eth.send_raw_transaction(raw_tx)
            receipt = self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)

            if receipt['status'] == 1:
                success_message = (
                    f"\nSold {price_quote['amount_in_formatted']} {params['token']} "
                    f"for {price_quote['amount_out_formatted']} {params['using_token']} "
                    f"at rate 1 {params['token']} = {price_quote['exchange_rate']} {params['using_token']} "
                    f"via UniswapV2 pool"
                )
                print(Fore.GREEN + success_message)
                print(f"View on explorer: {self.CHAIN_INFO[params['chain']]['explorer_url']}/tx/{self.web3_connection.to_hex(tx_hash)}")
            else:
                raise ValueError("Swap transaction failed!")

        except Exception as e:
            raise ValueError(f"Sell transaction failed: {str(e)}")

    def get_token_price(self, token1, token2, chain):
        """Get token price from DEX"""
        try:
            router = self.get_dex_router(chain)
            amount_in = Web3.to_wei(1, 'ether')  # Price for 1 token

            # Get price path
            path = [
                self.TOKENS[token1][chain] if token1 != self.CHAIN_INFO[chain]['symbol'] 
                else self.get_weth_address(chain),
                self.TOKENS[token2][chain] if token2 != self.CHAIN_INFO[chain]['symbol']
                else self.get_weth_address(chain)
            ]

            # Get amounts out
            amounts_out = router.functions.getAmountsOut(amount_in, path).call()
            price = amounts_out[1] / amounts_out[0]

            return {
                'price': price,
                'path': path
            }

        except Exception as e:
            raise ValueError(f"Failed to get token price: {str(e)}")

    def get_dex_router(self, chain):
        """Get DEX router contract based on chain with specific configurations"""
        # Router configurations
        ROUTER_CONFIGS = {
            'Base': {
                'address': '0x327Df1E6de05895d2ab08513aaDD9313Fe505d86',  # BaseSwap
                'name': 'BaseSwap',
                'factory': '0xFDa619b6d20975be80A10332cD39b9a4b0FAa8BB'
            },
            'Ethereum': {
                'address': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',  # Uniswap V2
                'name': 'Uniswap V2',
                'factory': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
            },
            'Polygon': {
                'address': '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff',  # QuickSwap
                'name': 'QuickSwap',
                'factory': '0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32'
            }
        }

        config = ROUTER_CONFIGS.get(chain)
        if not config:
            raise ValueError(f"No DEX configuration for chain {chain}")

        router = self.web3_connection.eth.contract(
            address=Web3.to_checksum_address(config['address']),
            abi=ROUTER_ABI
        )

        # Verify router is operational
        try:
            factory_address = router.functions.factory().call()
            if factory_address.lower() != config['factory'].lower():
                raise ValueError(f"Router factory mismatch on {chain}")
        except Exception as e:
            raise ValueError(f"Router verification failed on {chain}: {str(e)}")

        return router

    def get_token_contract(self, token, chain):
        """Get token contract instance"""
        if token == self.CHAIN_INFO[chain]['symbol']:
            return None  # Native token

        token_address = self.TOKENS.get(token, {}).get(chain)
        if not token_address:
            raise ValueError(f"Token {token} not supported on {chain}")

        return self.web3_connection.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=TOKEN_ABI
        )

    def get_weth_address(self, chain):
        """Get wrapped native token address for the chain"""
        WETH_ADDRESSES = {
            'Base': '0x4200000000000000000000000000000000000006',
            'Ethereum': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
            'Polygon': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
        }

        weth_address = WETH_ADDRESSES.get(chain)
        if not weth_address:
            raise ValueError(f"No WETH address configured for chain {chain}")

        return Web3.to_checksum_address(weth_address)

    def handle_0x_command(self, command, agent_voice_active=False, voice_mode_active=False, speak_response=None):
        """Main handler for all /0x commands"""
        try:
            if not command:
                raise ValueError("Empty command received")
            
            parts = command.lower().split()
            if len(parts) < 2:
                raise ValueError("Invalid command format")
            
            subcommand = parts[1]
            args = ' '.join(parts[2:]) if len(parts) > 2 else ""

            # Existing transaction commands
            if subcommand in ["buy", "sell"]:
                params = self.parse_transaction_intent(command)
                if not params:
                    raise ValueError("Could not understand transaction intent")

                params = self.validate_and_complete_transaction(params)
                price_data = self.get_best_price(params)
                
                if price_data:
                    preview_text = self.format_transaction_preview(params, price_data)
                    print(preview_text)

                    if self.confirm_transaction():
                        if subcommand == "buy":
                            self.execute_buy(params)
                        else:
                            self.execute_sell(params)

            elif subcommand == "send":
                self.handle_send_command(command, agent_voice_active, voice_mode_active, speak_response)
            elif subcommand == "receive":
                self.handle_receive_command()
            elif subcommand == "gas":
                if not args:
                    raise ValueError("Gas level not specified. Use: /0x gas <low|medium|high>")
                self.handle_gas_command(command)
                
            # New configuration commands
            elif subcommand == "new":
                if len(parts) < 3:
                    raise ValueError("Use: /0x new chain|token")
                if parts[2] == "chain":
                    self.add_chain_interactive()
                elif parts[2] == "token":
                    self.add_token_interactive()
                else:
                    raise ValueError("Use: /0x new chain|token")
                
            elif subcommand == "forget":
                if len(parts) < 4:
                    raise ValueError("Use: /0x forget chain|token <name>")
                
                target_type = parts[2]
                target_name = ' '.join(parts[3:])  # Join remaining parts for multi-word names
                
                if target_type == "chain":
                    self.forget_chain(target_name)
                elif target_type == "token":
                    self.forget_token(target_name)
                else:
                    raise ValueError("Use: /0x forget chain|token <name>")
            else:
                raise ValueError("Invalid command. Use /0x followed by: buy, sell, send, gas, receive, new, or forget")

        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(Fore.RED + error_message)
            if agent_voice_active or voice_mode_active and speak_response:
                speak_response(error_message)

    def get_token_usd_price(self, token_symbol, chain):
        """Get token price in USD using price feeds"""
        try:
            # Use CoinGecko API for price data
            token_id = self.get_coingecko_id(token_symbol, chain)
            response = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price",
                params={
                    'ids': token_id,
                    'vs_currencies': 'usd'
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if token_id in data and 'usd' in data[token_id]:
                    return float(data[token_id]['usd'])
            
            # Fallback to default price if API fails
            print(f"Warning: Could not get USD price for {token_symbol}, using fallback price")
            return self.get_fallback_price(token_symbol)

        except Exception as e:
            print(f"Warning: Failed to get USD price for {token_symbol}: {str(e)}")
            return self.get_fallback_price(token_symbol)

    def get_fallback_price(self, token_symbol):
        """Fallback prices when API fails"""
        FALLBACK_PRICES = {
            'ETH': 2000.0,
            'DEGEN': 0.01,
            # Add more fallback prices as needed
        }
        return FALLBACK_PRICES.get(token_symbol.upper(), 0.0)

    def execute_buy(self, params):
        """Execute a buy transaction with additional validation"""
        try:
            if not self.connect_to_chain(params['chain']):
                raise ValueError(f"Failed to connect to {params['chain']}")

            # Get price quote first
            price_quote = self.get_best_price(params)
            
            token_address = Web3.to_checksum_address(self.TOKENS[params['token']][params['chain']])
            using_token_address = (self.get_weth_address(params['chain']) 
                                 if params['using_token'] == self.CHAIN_INFO[params['chain']]['symbol']
                                 else Web3.to_checksum_address(self.TOKENS[params['using_token']][params['chain']]))
            
            router = self.get_dex_router(params['chain'])
            
            # Calculate slippage and deadline
            slippage = 0.005  # 0.5% slippage tolerance
            amount_out_min = int(price_quote['amount_out'] * (1 - slippage))
            deadline = int(time.time()) + 300  # 5 minutes

            if params['using_token'] == self.CHAIN_INFO[params['chain']]['symbol']:
                # Check ETH balance
                balance = self.web3_connection.eth.get_balance(self.AGENT_WALLET['public_key'])
                if balance < price_quote['amount_in']:
                    raise ValueError(f"Insufficient ETH balance. Need {Web3.from_wei(price_quote['amount_in'], 'ether')} ETH")

                # Execute ETH swap
                swap_tx = router.functions.swapExactETHForTokens(
                    amount_out_min,  # minimum amount of tokens to receive
                    [using_token_address, token_address],  # path
                    self.AGENT_WALLET['public_key'],  # recipient
                    deadline
                ).build_transaction({
                    'from': self.AGENT_WALLET['public_key'],
                    'value': price_quote['amount_in'],  # amount of ETH to send
                    'gas': 250000,
                    'gasPrice': self.get_gas_price(),
                    'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                    'chainId': self.web3_connection.eth.chain_id
                })

            else:
                # Handle ERC20 token
                token_contract = self.web3_connection.eth.contract(
                    address=using_token_address,
                    abi=TOKEN_ABI
                )
                
                # Check token balance
                balance = token_contract.functions.balanceOf(self.AGENT_WALLET['public_key']).call()
                if balance < price_quote['amount_in']:
                    raise ValueError(f"Insufficient {params['using_token']} balance")

                # Approve tokens if needed
                allowance = token_contract.functions.allowance(
                    self.AGENT_WALLET['public_key'],
                    router.address
                ).call()
                
                if allowance < price_quote['amount_in']:
                    approve_tx = token_contract.functions.approve(
                        router.address,
                        price_quote['amount_in']
                    ).build_transaction({
                        'from': self.AGENT_WALLET['public_key'],
                        'gas': 100000,
                        'gasPrice': self.get_gas_price(),
                        'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                        'chainId': self.web3_connection.eth.chain_id
                    })
                    
                    signed_tx = self.web3_connection.eth.account.sign_transaction(
                        approve_tx,
                        private_key=self.AGENT_WALLET['private_key']
                    )
                    tx_hash = self.web3_connection.eth.send_raw_transaction(signed_tx.raw_transaction)
                    self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)

                # Execute token swap
                swap_tx = router.functions.swapExactTokensForTokens(
                    price_quote['amount_in'],  # amount of tokens to send
                    amount_out_min,  # minimum amount of tokens to receive
                    [using_token_address, token_address],  # path
                    self.AGENT_WALLET['public_key'],  # recipient
                    deadline
                ).build_transaction({
                    'from': self.AGENT_WALLET['public_key'],
                    'gas': 250000,
                    'gasPrice': self.get_gas_price(),
                    'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                    'chainId': self.web3_connection.eth.chain_id
                })

            # Sign and send transaction
            signed_tx = self.web3_connection.eth.account.sign_transaction(
                swap_tx,
                private_key=self.AGENT_WALLET['private_key']
            )
            tx_hash = self.web3_connection.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)

            if receipt['status'] == 1:
                success_message = (
                    f"\nBought {price_quote['amount_out_formatted']} {params['token']} "
                    f"using {price_quote['amount_in_formatted']} {params['using_token']} "
                    f"at rate 1 {params['using_token']} = {1/price_quote['exchange_rate']:.8f} {params['token']} "
                    f"via UniswapV2 pool"
                )
                print(Fore.GREEN + success_message)
                print(f"View on explorer: {self.CHAIN_INFO[params['chain']]['explorer_url']}/tx/{self.web3_connection.to_hex(tx_hash)}")
            else:
                raise ValueError("Swap transaction failed!")

        except Exception as e:
            raise ValueError(f"Buy transaction failed: {str(e)}")

    def approve_token_spending(self, token_address, spender_address, amount):
        """Approve token spending for a specific contract"""
        try:
            token_contract = self.web3_connection.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=TOKEN_ABI
            )
            
            # Check current allowance
            current_allowance = token_contract.functions.allowance(
                self.AGENT_WALLET['public_key'],
                spender_address
            ).call()
            
            if current_allowance < amount:
                # Prepare approval transaction
                approve_tx = token_contract.functions.approve(
                    spender_address,
                    amount
                ).build_transaction({
                    'from': self.AGENT_WALLET['public_key'],
                    'gas': 100000,
                    'gasPrice': self.get_gas_price(),
                    'nonce': self.web3_connection.eth.get_transaction_count(self.AGENT_WALLET['public_key']),
                    'chainId': self.web3_connection.eth.chain_id
                })
                
                # Sign and send approval
                signed_approve = self.web3_connection.eth.account.sign_transaction(
                    approve_tx,
                    private_key=self.AGENT_WALLET['private_key']
                )
                
                # Send the raw transaction
                tx_hash = self.web3_connection.eth.send_raw_transaction(signed_approve.rawTransaction)
                
                # Wait for approval to be mined
                receipt = self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)
                if receipt['status'] != 1:
                    raise ValueError("Token approval failed")
                
                print(Fore.GREEN + "Token approval successful")
                
        except Exception as e:
            raise ValueError(f"Failed to approve token spending: {str(e)}")

    def ensure_checksum_address(self, address):
        """Ensure an address is in checksum format"""
        try:
            if not address:
                raise ValueError("Empty address provided")
            return Web3.to_checksum_address(address.lower())
        except Exception as e:
            raise ValueError(f"Invalid address format: {address}")

    def get_coingecko_id(self, token_symbol, chain):
        """Map token symbols to CoinGecko IDs"""
        COINGECKO_IDS = {
            'ETH': 'ethereum',
            'DEGEN': 'degen',
            'USDC': 'usd-coin',
            # Add more mappings as needed
        }
        return COINGECKO_IDS.get(token_symbol.upper(), token_symbol.lower())

    def add_token_interactive(self):
        """Interactive token addition with validation and file update"""
        print(Fore.YELLOW + "\nAdding new token configuration:")
        
        try:
            token_name = input("Token name: ").strip().capitalize()
            chain_name = input("Chain name: ").strip().capitalize()
            
            if chain_name not in self.CHAIN_INFO:
                raise ValueError(f"Chain {chain_name} not supported!")

            contract_address = input("Contract address: ").strip()
            contract_address = Web3.to_checksum_address(contract_address)
            
            # Update runtime dictionary
            if token_name not in self.TOKENS:
                self.TOKENS[token_name] = {}
            self.TOKENS[token_name][chain_name] = contract_address

            # Update Python file
            current_file = os.path.abspath(__file__)
            with open(current_file, 'r', encoding='utf-8') as f:
                content = f.readlines()

            # Find TOKENS dictionary
            start_index = None
            end_index = None
            brace_count = 0
            in_tokens = False

            for i, line in enumerate(content):
                if line.strip().startswith('TOKENS = {'):
                    start_index = i
                    in_tokens = True
                    brace_count = 1
                    continue
                
                if in_tokens:
                    if '{' in line:
                        brace_count += 1
                    if '}' in line:
                        brace_count -= 1
                    if brace_count == 0:
                        end_index = i + 1
                        break

            if start_index is None or end_index is None:
                raise ValueError("TOKENS dictionary not found in file")

            # Check if there are existing entries
            has_entries = False
            for i in range(start_index + 1, end_index - 1):
                if "': {" in content[i]:
                    has_entries = True
                    break

            # Create new token entry
            new_token_lines = []
            if has_entries:
                # If there are existing entries, add comma to the previous entry if needed
                prev_line = content[end_index - 2].rstrip()
                if not prev_line.endswith(','):
                    content[end_index - 2] = prev_line + ',\n'
            
            new_token_lines.extend([
                f"    '{token_name}': {{\n",
                f"        '{chain_name}': '{contract_address}',\n",
                "    }"  # No comma here - will be added by next entry if needed
            ])

            # Insert new token before the closing brace of TOKENS
            content.insert(end_index - 1, '\n'.join(new_token_lines) + '\n')

            with open(current_file, 'w', encoding='utf-8') as f:
                f.writelines(content)

            print(Fore.GREEN + f"\nToken {token_name} added successfully on {chain_name}!")

        except Exception as e:
            raise ValueError(f"Failed to add token: {str(e)}")

    def forget_token(self, token_name):
        """Remove token configuration"""
        try:
            token_name = token_name.strip().capitalize()
            if token_name not in self.TOKENS:
                raise ValueError(f"Token {token_name} not found")

            # Remove from runtime dictionary
            del self.TOKENS[token_name]

            # Update Python file
            current_file = os.path.abspath(__file__)
            with open(current_file, 'r', encoding='utf-8') as f:
                content = f.readlines()

            # Find token entry
            start_index = None
            end_index = None
            token_found = False
            brace_count = 0

            for i, line in enumerate(content):
                if f"'{token_name}'" in line and "': {" in line:
                    start_index = i
                    token_found = True
                    brace_count = 1
                    continue
                
                if token_found:
                    if '{' in line:
                        brace_count += 1
                    if '}' in line:
                        brace_count -= 1
                    if brace_count == 0:
                        end_index = i + 1
                        break

            if start_index is None or end_index is None:
                raise ValueError(f"Token {token_name} entry not found in file")

            # Check if this is the last entry
            is_last_entry = True
            for i in range(end_index, len(content)):
                if "': {" in content[i]:
                    is_last_entry = False
                    break

            # If it's not the last entry, keep the comma from the current entry
            # If it is the last entry, remove the comma from the previous entry
            if is_last_entry and start_index > 0:
                # Find previous entry's closing brace
                for i in range(start_index - 1, -1, -1):
                    if content[i].strip() == '},':
                        content[i] = content[i].replace('},', '}')
                        break

            # Remove the token entry
            del content[start_index:end_index]

            with open(current_file, 'w', encoding='utf-8') as f:
                f.writelines(content)

            print(Fore.GREEN + f"Token {token_name} removed successfully")

        except Exception as e:
            raise ValueError(f"Failed to remove token: {str(e)}")

    def add_chain_interactive(self):
        """Interactive chain addition with validation"""
        print(Fore.YELLOW + "\nAdding new chain configuration:")
        
        try:
            chain_name = input("Chain name: ").strip().capitalize()
            if chain_name in self.CHAIN_INFO:
                raise ValueError(f"Chain {chain_name} already exists!")

            chain_id = int(input("Chain ID: ").strip())
            rpc_url = input("RPC URL: ").strip()
            symbol = input("Native token symbol: ").strip().upper()
            explorer_url = input("Block explorer URL: ").strip()

            # Test connection
            web3 = Web3(Web3.HTTPProvider(rpc_url))
            if not web3.is_connected():
                raise ValueError("Unable to connect to RPC URL")

            # Update runtime dictionary
            self.CHAIN_INFO[chain_name] = {
                'chain_id': chain_id,
                'rpc_url': rpc_url,
                'symbol': symbol,
                'decimals': 18,
                'explorer_url': explorer_url
            }

            # Update Python file
            current_file = os.path.abspath(__file__)
            with open(current_file, 'r', encoding='utf-8') as f:
                content = f.readlines()

            # Find CHAIN_INFO dictionary
            start_index = None
            end_index = None
            brace_count = 0
            in_chain_info = False

            for i, line in enumerate(content):
                if line.strip().startswith('CHAIN_INFO = {'):
                    start_index = i
                    in_chain_info = True
                    brace_count = 1
                    continue
                
                if in_chain_info:
                    if '{' in line:
                        brace_count += 1
                    if '}' in line:
                        brace_count -= 1
                    if brace_count == 0:
                        end_index = i + 1
                        break

            if start_index is None or end_index is None:
                raise ValueError("CHAIN_INFO dictionary not found in file")

            # Check if there are existing entries
            has_entries = False
            for i in range(start_index + 1, end_index - 1):
                if "': {" in content[i]:
                    has_entries = True
                    break

            # Create new chain entry
            new_chain_lines = []
            if has_entries:
                # If there are existing entries, add comma to the previous entry if needed
                prev_line = content[end_index - 2].rstrip()
                if not prev_line.endswith(','):
                    content[end_index - 2] = prev_line + ',\n'
            
            new_chain_lines.extend([
                f"    '{chain_name}': {{",
                f"        'chain_id': {chain_id},",
                f"        'rpc_url': '{rpc_url}',",
                f"        'symbol': '{symbol}',",
                "        'decimals': 18,",
                f"        'explorer_url': '{explorer_url}'",
                "    }"  # No comma here - will be added by next entry if needed
            ])

            # Insert new chain before the closing brace
            content.insert(end_index - 1, '\n'.join(new_chain_lines) + '\n')

            with open(current_file, 'w', encoding='utf-8') as f:
                f.writelines(content)

            print(Fore.GREEN + f"\nChain {chain_name} added successfully!")

        except Exception as e:
            raise ValueError(f"Failed to add chain: {str(e)}")

    def forget_chain(self, chain_name):
        """Remove chain configuration"""
        try:
            chain_name = chain_name.strip().capitalize()
            if chain_name not in self.CHAIN_INFO:
                raise ValueError(f"Chain {chain_name} not found")

            # Check if chain is in use by any tokens
            for token, chains in self.TOKENS.items():
                if chain_name in chains:
                    raise ValueError(f"Cannot remove chain {chain_name} as it is used by token {token}")

            # Remove from runtime dictionary
            del self.CHAIN_INFO[chain_name]

            # Save to temporary JSON for persistence until code is updated
            self.save_chain_config()

            # Update the Python file
            self._update_python_file_chain_removal(chain_name)

            print(Fore.GREEN + f"Chain {chain_name} removed successfully")

        except Exception as e:
            raise ValueError(f"Failed to remove chain: {str(e)}")

    def get_price(self, token_name, chain_name, amount, using_token=None):
        """Get price for token swap"""
        try:
            if not self.web3_connection or not self.web3_connection.is_connected():
                raise ConnectionError("No active web3 connection")

            # Get token addresses
            if token_name not in self.TOKENS and token_name != self.CHAIN_INFO[chain_name]['symbol']:
                raise ValueError(f"Token {token_name} not supported")

            if using_token and using_token not in self.TOKENS and using_token != self.CHAIN_INFO[chain_name]['symbol']:
                raise ValueError(f"Token {using_token} not supported")

            # Get token contract addresses
            token_address = None
            if token_name in self.TOKENS:
                if chain_name not in self.TOKENS[token_name]:
                    raise ValueError(f"Token {token_name} not supported on {chain_name}")
                token_address = self.TOKENS[token_name][chain_name]

            using_token_address = None
            if using_token in self.TOKENS:
                if chain_name not in self.TOKENS[using_token]:
                    raise ValueError(f"Token {using_token} not supported on {chain_name}")
                using_token_address = self.TOKENS[using_token][chain_name]

            # Create the path for the swap
            path = []
            if token_address:
                path.append(token_address)
            if using_token_address:
                path.append(using_token_address)

            # Get the router contract
            router_address = Web3.to_checksum_address("0x327Df1E6de05895d2ab08513aaDD9313Fe505d86")
            router_contract = self.web3_connection.eth.contract(
                address=router_address,
                abi=ROUTER_ABI
            )

            # Calculate the price
            if path:
                amount_in_wei = self.web3_connection.to_wei(amount, 'ether')
                amounts = router_contract.functions.getAmountsOut(
                    amount_in_wei,
                    path
                ).call()
                return self.web3_connection.from_wei(amounts[-1], 'ether')
            
            return amount

        except Exception as e:
            raise ValueError(f"Failed to get price: {str(e)}")

    def handle_buy_command(self, command):
        """Handle the buy command"""
        global CHAIN_INFO, TOKENS
        try:
            # Parse the command
            params = self.parse_transaction_intent(command)
            if not params or params['action'] != 'buy':
                raise ValueError("Invalid buy command")

            # Get required parameters
            token_name = params['token']
            chain_name = params['chain']
            amount = params['amount']
            using_token = params['using_token']

            if not all([token_name, chain_name, amount, using_token]):
                raise ValueError("Missing required parameters")

            # Connect to chain first
            if not self.connect_to_chain(chain_name):
                raise ConnectionError(f"Failed to connect to {chain_name}")

            # Get price quote
            price = self.get_price(token_name, chain_name, amount, using_token)
            print(f"Price quote: {price} {using_token}")

        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")

    def handle_sell_command(self, command):
        """Handle the sell command"""
        try:
            # Parse the command
            params = self.parse_transaction_intent(command)
            if not params or params['action'] != 'sell':
                raise ValueError("Invalid sell command")

            # Get required parameters and continue with similar updates
            # ... (implement similar to handle_buy_command)

        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}")

    def _update_python_file_chain_removal(self, chain_name):
        """Remove chain entry from Python file"""
        try:
            current_file = os.path.abspath(__file__)
            with open(current_file, 'r', encoding='utf-8') as f:
                content = f.readlines()

            # Find CHAIN_INFO dictionary
            start_index = None
            end_index = None
            chain_found = False
            brace_count = 0

            for i, line in enumerate(content):
                if line.strip().startswith('CHAIN_INFO = {'):
                    start_index = i
                    continue
                
                if start_index is not None:
                    if f"'{chain_name}': {{" in line:
                        chain_start = i
                        chain_found = True
                        brace_count = 1
                        continue
                    
                    if chain_found:
                        if '{' in line:
                            brace_count += 1
                        if '}' in line:
                            brace_count -= 1
                        if brace_count == 0:
                            chain_end = i + 1
                            break

            if not chain_found:
                raise ValueError(f"Chain {chain_name} entry not found in file")

            # Check if this is the last entry
            is_last_entry = True
            for i in range(chain_end, len(content)):
                if "': {" in content[i]:
                    is_last_entry = False
                    break

            # If it's not the last entry, keep the comma from the current entry
            # If it is the last entry, remove the comma from the previous entry
            if is_last_entry and chain_start > 0:
                # Find previous entry's closing brace
                for i in range(chain_start - 1, -1, -1):
                    if content[i].strip() == '},':
                        content[i] = content[i].replace('},', '}')
                        break

            # Remove the chain entry
            del content[chain_start:chain_end]

            with open(current_file, 'w', encoding='utf-8') as f:
                f.writelines(content)

        except Exception as e:
            raise ValueError(f"Failed to update Python file: {str(e)}")

# Test loop
def main():
    """Main test loop for the Web3 transaction functionality."""
    print(Fore.LIGHTCYAN_EX + "\n" + "═" * 80)
    print(Fore.LIGHTGREEN_EX + """
    ╔═══════════════════════════════════════════╗
    ║      Web3 Transaction Test Interface      ║
    ╚═══════════════════════════════════════════╝
    """)
    print(Fore.LIGHTCYAN_EX + "═" * 80)
    print(Fore.LIGHTYELLOW_EX + "\nAvailable commands:")
    print("  /0x buy <amount> <token> using <token> on <chain>")
    print("  /0x sell <amount> <token> for <token> on <chain>")
    print("  /0x send <chain> <token> <amount> to <recipient>")
    print("  /0x gas <low|medium|high>")
    print("  /0x receive")
    print("\nConfiguration commands:")
    print("  /0x new chain")
    print("  /0x new token")
    print("  /0x forget chain <name>")
    print("  /0x forget token <name>")
    print(Fore.LIGHTCYAN_EX + "═" * 80)

    # Initialize Web3Handler with test user data
    test_users = {
        'Ross': {
            'full_name': 'Ross Peili',
            'call_name': 'Ross',
            'public0x': '0x89A7f83Db9C1919B89370182002ffE5dfFc03e21'
        }
    }
    
    handler = Web3Handler(test_users)
    
    while True:
        try:
            command = input(f"\n{Fore.GREEN}Enter command: {Style.RESET_ALL}")
            
            if command.lower() in ['exit', 'quit', 'q']:
                print(f"{Fore.LIGHTGREEN_EX}[SYSTEM] Exiting Web3 Transaction Interface...{Style.RESET_ALL}")
                break
                
            if not command.strip():
                continue
            
            if command.startswith('/0x'):
                handler.handle_0x_command(command, False, False, None)
            else:
                print(Fore.RED + "Invalid command. Use /0x followed by: buy, sell, send, gas, or receive")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTGREEN_EX}[SYSTEM] Exiting Web3 Transaction Interface...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":

    main()
