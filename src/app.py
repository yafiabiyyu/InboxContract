from flask import Flask,render_template,json,request,redirect,url_for
import os
from web3 import Web3
from time import sleep


gnache_uri = os.getenv("GNACHE_URI")
app = Flask(__name__)
web3 = web3 = Web3(Web3.HTTPProvider(gnache_uri))
priv_key = os.getenv('PRIV_KEY')
with open('../build/contracts/Inbox.json','r') as f:
    data = json.load(f)
    abi = data['abi']
    contract_address = data['networks']['5777']['address']
contract = web3.eth.contract(address=contract_address,abi=abi)
default_account = web3.eth.account.privateKeyToAccount(priv_key)
web3.eth.defaultAccount = str(default_account.address)

@app.route('/')
def index():
    status = web3.isConnected()
    account = web3.eth.account.privateKeyToAccount(priv_key)
    message = getMessage()
    return render_template("index.html",account=account.address,message=message)


@app.route('/set/message',methods=['POST'])
def setMessage():
    if request.method == 'POST':
        new_message = request.form['new_message']
        tx_hash = contract.functions.SetMessage(str(new_message)).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_hash)
    # sleep(3)
    return redirect(url_for('index'))


def getMessage():
    message = contract.functions.GetMessage().call()
    return message
