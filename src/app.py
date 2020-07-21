from flask import Flask,render_template,json,request,redirect,url_for,make_response
import os
from web3 import Web3
from time import sleep
from .encryption_decryption import encryptedMessage,decryptedMessage


infura_uri = os.getenv("INFURA_API")
app = Flask(__name__)
web3 = web3 = Web3(Web3.HTTPProvider(infura_uri))
priv_key = os.getenv('PRIV_KEY')
with open('../build/contracts/Inbox.json','r') as f:
    data = json.load(f)
    abi = data['abi']
    contract_address = data['networks']['3']['address']
contract = web3.eth.contract(address=contract_address,abi=abi)
default_account = web3.eth.account.privateKeyToAccount(priv_key)
# web3.eth.defaultAccount = str(default_account.address)

@app.route('/')
def index():
    status = web3.net.version
    print(status)
    account = web3.eth.account.privateKeyToAccount(priv_key)
    message = getMessage()
    return render_template("index.html",account=account.address,message=message)

@app.route('/waiting/tx',methods=['POST','GET'])
def waitingTx():
    message_data = request.form['new_message']
    return render_template('waiting.html',data=data)

@app.route('/set/message',methods=['POST'])
def setMessage():
    if request.method == 'POST':
        
        new_message = request.form['new_message']
        # new_message = request.get_data()
        nonce = web3.eth.getTransactionCount(str(default_account.address))
        transaction = contract.functions.SetMessage(str(new_message)).buildTransaction({
            'gas':4000000,
            'gasPrice':web3.toWei('87','gwei'),
            'from':str(default_account.address),
            'nonce':nonce
        })
        signed_txn = web3.eth.account.signTransaction(transaction,private_key=priv_key)
        data = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(data)
    # sleep(3)
    return redirect(url_for('index'))
    # return make_response("Sukses create tx",200)


def getMessage():
    message = contract.functions.GetMessage().call()
    return message
