from transaction import txns,chain

def makeBlock(txns,chain):
    parentBlock = chain[-1]
    parentHash  = parentBlock[u'hash']
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
    txnCount    = len(txns)
    blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,
                     u'txnCount':len(txns),'txns':txns}
    blockHash = hashMe( blockContents )
    block = {u'hash':blockHash,u'contents':blockContents}
    
    return block

blockSizeLimit = 5  # Arbitrary number of transactions per block- 
               #  this is chosen by the block miner, and can vary between blocks!

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)
    
    ## Gather a set of valid transactions for inclusion
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isValidTxn(newTxn,state) # This will return False if txn is invalid
        
        if validTxn:           # If we got a valid state, not 'False'
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue  # This was an invalid transaction; ignore it and move on
        
    ## Make a block
    myBlock = makeBlock(txnList,chain)
    chain.append(myBlock)    

chain[0]

{'contents': {'blockNumber': 0,
  'parentHash': None,
  'txnCount': 1,
  'txns': [{'Alice': 50, 'Bob': 50}]},
 'hash': '7c88a4312054f89a2b73b04989cd9b9e1ae437e1048f89fbb4e18a08479de507'}

chain[1]

{'contents': {'blockNumber': 1,
  'parentHash': '7c88a4312054f89a2b73b04989cd9b9e1ae437e1048f89fbb4e18a08479de507',
  'txnCount': 5,
  'txns': [{'Alice': 3, 'Bob': -3},
   {'Alice': -1, 'Bob': 1},
   {'Alice': 3, 'Bob': -3},
   {'Alice': -2, 'Bob': 2},
   {'Alice': 3, 'Bob': -3}]},
 'hash': '7a91fc8206c5351293fd11200b33b7192e87fad6545504068a51aba868bc6f72'}


{'Alice': 72, 'Bob': 28}
