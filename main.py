import json
import random
from web3 import Web3

ABI = json.load(open('abi/omnisea_root.json'))
PRIVATE_KEYS = 'files/private_keys.txt'
PROXIES = 'files/proxies.txt'
ROOT_CONTRACT_ADDRESS = Web3.to_checksum_address('0xAF8000CEc22904C8E3FBDD0bbd6e459bA4D95ac0')
OMNISEA_NFT_ADDRESS = '0xC8651B7698988badB162584a61118cEe967bE4b9'
RPC = 'https://mainnet.base.org'


print('Получаю приватники')
with open(PRIVATE_KEYS, 'r') as f:
    private_keys = f.read().splitlines()
random.shuffle(private_keys)

print('Получаю прокси\n')
with open(PROXIES, 'r') as f:
    proxies = [{'proxies': {'http': f'http://{proxy}', 'https': f'http://{proxy}'}} for proxy in f.read().splitlines()]
random.shuffle(proxies)

queue = list(zip(private_keys, proxies))

for private_key, proxies in queue:
    web3 = Web3(Web3.HTTPProvider(endpoint_uri=RPC, request_kwargs=proxies))
    account = web3.eth.account.from_key(private_key)
    address = account.address
    contract = web3.eth.contract(address=ROOT_CONTRACT_ADDRESS, abi=ABI)

    mint = 0
    _params = (OMNISEA_NFT_ADDRESS, 1, [], 1)
    bytes32Array = []

    tx_params = {
        "chainId": web3.eth.chain_id,
        "from": address,
        "gasPrice": web3.eth.gas_price,
        "nonce": web3.eth.get_transaction_count(address)
    }
    transaction = contract.functions.mint(0.00025, ('0xC8651B7698988badB162584a61118cEe967bE4b9', 1, '[]', 1)).build_transaction(tx_params)
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    txn = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"Транзакция: https://basescan.org/tx/{txn.hex()}")

