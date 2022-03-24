from web3 import Web3
from os.path import exists as file_exists
from hashlib import sha256
from web3.middleware import geth_poa_middleware
import json


with open('networks.json', 'r') as config:
	    json_load = json.load(config)

# Web3 provider configuration
provider = Web3.HTTPProvider(json_load['rpc_node'])
w3 = Web3(provider)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

print("Welcome dear user \n")


menu_options = {
    1: 'Create Account',
    2: 'Send transaction',
    3: 'Get balance',
    4: 'Networks',
    5: 'Export passphrase',
    6: 'Restore wallet',
    7: 'Change password',
    8: 'Exit'
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

#it will create account and store encrypted private and public keys

def create_account():
    global account
    account = w3.eth.account.create();
    with open('config.json', 'r+') as config:
        data = json.load(config)
        data["privatekey"] = account.privateKey.hex()
        data["address"] = account.address
        config.seek(0)
        config.write(json.dumps(data))
        config.truncate()
    print("your account has been created \n")

# it will make a transaction and sign it with private key    

def send_transaction():
    with open('config.json', 'r') as config:
        json_load = json.load(config)
    nonce = w3.eth.getTransactionCount(json_load['address'])

    tx = {
        'nonce': nonce,
        'to': input("Enter recipient address: "),
        'value': w3.toWei(1, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    }


    signed_tx = w3.eth.account.sign_transaction(tx,json_load['privatekey'])


    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    print("Congratulation! your transaction was successful \n TX Hash is : "+ w3.toHex(tx_hash))

def export():
    with open('config.json', 'r') as config:
	    json_load = json.load(config)
    print("Your privatekey is: "+json_load['privatekey'])
    print("Your address is: "+json_load['address'])
     
def get_balance():
    with open('config.json', 'r') as config:
	    json_load = json.load(config)
    print(" \n Your balance is: " + str(w3.eth.get_balance(json_load['address'])) +" CET \n")

def networks():

    with open('networks.json', 'r+') as config:
        data = json.load(config)
        print("Current RPC node is: " + data["rpc_node"])
        data["rpc_node"] = input("Enter node RPC url")

def change_password():
    with open('config.json', 'r+') as config:
        data = json.load(config)
        password = sha256(input("Enter your new password: ").encode('utf-8')).hexdigest()
        data["password"] = password
        config.seek(0)
        config.write(json.dumps(data))
        config.truncate()
    print("\nYour password changed secessfully :) \n")

     
           
if ( file_exists('networks.json') and file_exists('config.json') == True ):
    with open('config.json', 'r+') as config:
        data = json.load(config)
        n = sha256(input("Enter your password: ").encode('utf-8')).hexdigest()
        if ( data["password"] == n ) :
            pass
        else:
            print("Wrong password!")
            exit()
else:
    create_account()



if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('\n Enter your choice: '))
        except:
            print('\nWrong input. Please enter a number ...')

        if option == 1:
           create_account()
        elif option == 2:
            send_transaction()
        elif option == 3:
            get_balance()
        elif option == 4:
            networks()
        elif option == 5:
            export()
        elif option == 6:
            restore()
        elif option == 7:
            change_password()
        elif option == 8:
            print('Thank you because of choosing NeuWallet')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')



