MINING_REWARD = 10
genesis_block = {'previous_hash': '',
                 'index': 0,
                 'transactions': []
                 }
blockchain = [genesis_block]
open_transactions = []
owner = 'Wale'
participants = {'Wale'}


def previous_blockchain():
    ''' Returns either the last transaction amount listed in the blockchain,
    or None if the chain is empty.
    '''
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(receiver, sender=owner, amount=1.0):
    """ Adds the current customer transaction value to the blockchain list.
    Args:
    :sender: The sender of the coins. Default = Owner of the app.
    :receiver: The receiver of the coins.
    :amount: The amount of coins being sent, (default=1.0)
    """
    transaction = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(receiver)
        return True
    return False


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participants):
    '''This function returns the balance in the owner's wallet.
     The difference between amount received and amount sent is computed and returned.
     Args:
     :participants: global variable. Set of all people involved in transactions
     with the owner, including the owner.
    '''
    # Two list comprehensions as one. Pretty neat:
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participants] for block in blockchain]
    # keeping track of any transaction pending verification which the sender may have sent
    open_tx_sender = [tx['amount']
                      for tx in open_transactions
                      if tx['sender'] == participants]
    # Compiling a list containig all transactions sent by the swender, approved or otherwise
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['receiver'] == participants] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    balance = (amount_received - amount_sent)
    return balance


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print(hashed_block)

    # Using list compehensions for the list converison 
    # instead of a for loop

    # for key in last_block:
    #     value = last_block[key]
    #     hashed_block = hashed_block + str(value)
    reward_transaction = {
        'sender': 'MINING',
        'receiver': owner,
        'amount': MINING_REWARD
    }
    # Adding the reward to the system by creating a 
    # copy that will be managd locally:
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': copied_transactions}
    blockchain.append(block)
    return True


def get_user_choice():
    """ Returns the action choice input by the customer. 
    """
    user_input = input('Your choice: ')
    return user_input


def get_transaction_value():
    """ Returns the transaction value input of the customer. 
    """
    tx_receipient = input('Enter the address of the recepient: ')
    tx_amount = float(input('Your current transaction amount please: '))
    return (tx_receipient, tx_amount)


def print_blockchain_elements():
    '''Output the blockchain list to the console'''
    for block in blockchain:
        print('State of the blockchain: ')
        print(block)
    else:
        print('-' * 25)


def verify_chain():
    '''Verifies that the blockchain has not been manipulated'''
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue  # this is cos we do not want to verify the genesis block yet
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    return False


def check_validity():
    '''This checks if all transactions are valid. 
    Returns bool.
    '''
    return all([verify_transaction(tx) for tx in open_transactions])


while_waiting_for_input = True
while while_waiting_for_input:
    print('Please select action:')
    print('Select 1 to add a new transaction value')
    print('Select 2 to create a new block.')
    print('Select 3 to see blockchain elements.')
    print('Select 4 to see output participants.')
    print('h: manipulate elements.')
    print('Enter q to Quit')

    user_choice = get_user_choice()
    if user_choice == '1':
        # Get next value of the customer's input.
        tx_data = get_transaction_value()
        recipient, amount = tx_data  # This is an example of tuple unpacking

        # Add transaction amount to the blockchain
        if add_transaction(recipient, amount=amount):
            print('Transaction added succesfully')
        else:
            print('Transaction failed')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {'previous_hash': '',
                             'index': 0,
                             'transactions': [{}]
                             }
    elif user_choice == 'q':
        while_waiting_for_input = False  # Alternative to using 'break'
    elif not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # break out of the loop
        break
    else:
        print('Invalid choice. Please select a choice in the list.')
    print(get_balance('Wale'))

print('Done!')
