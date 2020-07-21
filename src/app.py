from flask import (
    Flask,
    render_template,
    json,
    request,
    redirect,
    url_for,
    make_response,
)
import os
from web3 import Web3
from time import sleep
from .encryption_decryption import encryptedMessage, decryptedMessage


app = Flask(__name__)
priv_key = os.getenv("PRIV_KEY")
infura_uri = os.getenv("INFURA_API")
web3 = Web3(Web3.HTTPProvider(infura_uri))
with open("../build/contracts/Inbox.json", "r") as f:
    data = json.load(f)
    abi = data["abi"]
    contract_address = data["networks"]["3"]["address"]
contract = web3.eth.contract(address=contract_address, abi=abi)
default_account = web3.eth.account.privateKeyToAccount(priv_key)


@app.route("/", methods=["GET"])
def index():
    message = getMessage()
    return render_template(
        "index.html", account=str(default_account.address), message=message
    )


@app.route("/set/message", methods=["POST"])
def setMessage():
    if request.method == "POST":
        new_message = request.form["new_message"]
        nonce = web3.eth.getTransactionCount(str(default_account.address))
        transaction = contract.functions.SetMessage(str(new_message)).buildTransaction(
            {
                "gas": 210000,
                "gasPrice": web3.eth.gasPrice,
                "from": str(default_account.address),
                "nonce": nonce,
            }
        )
        signed_txn = web3.eth.account.signTransaction(transaction, private_key=priv_key)
        tx_id = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(tx_id.hex())
    return redirect(url_for("index"))


def getMessage():
    message = contract.functions.GetMessage().call()
    return message