var Inbox = artifacts.require("Inbox");

contract('Inbox', function(accounts){
    var contractInstance;

    it('Cek Initial Message', function(){
        return Inbox.deployed().then(function(instance){
            contractInstance = instance;
            // console.log(contractInstance.address);
            return contractInstance.message.call();
        }).then(function(message){
            assert.equal(message,'Hai Ini Initial Message');
        });
    });

    it("Set new message",function(){
        return Inbox.deployed().then(function(instance){
            contractInstance = instance;
            return contractInstance.SetMessage("Hai ini pesan kedua",{from:accounts[0]});
        }).then(function(){
            return contractInstance.GetMessage();
        }).then(function(data){
            assert.equal(data,"Hai ini pesan kedua");
            // console.log(data);
        });
    });
});