from rx import Observable
import sys
sys.path.append('.')
import asyncio
import os
from deriv_api import DerivAPI
import websockets
from time import gmtime, strftime

app_id = 1089
api_token = os.getenv('DERIV_TOKEN', 'mU4knUW75QRtaLJ')
async def connect():
    url = f'wss://frontend.binaryws.com/websockets/v3?l=EN&app_id={app_id}'
    connection = await websockets.connect(url)
    return connection

async def open_position(symbol: str, stake: float, trade_option: str, expiration: int):
    
    """Function to open a position.
    Args:
        symbol (string)
        stake (float)
        trade_option: Type of the operation buy/sell (call or put)
    """
    # create your own websocket connection and pass it as argument to DerivAPI
    api = DerivAPI(app_id=app_id)

    print("After Before Auth: ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))    
    # Authorize
    authorize = await api.authorize(api_token)
    print("After Authorization: ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    symbol_code = None 
    if symbol == "Volatility 10 Index":
        symbol_code = "R_10"
    elif symbol == "Volatility 25 Index":
        symbol_code = "R_25"
    elif symbol == "Volatility 50 Index":
        symbol_code = "R_50"
    elif symbol == "Volatility 75 Index":
        symbol_code = "R_75"
    elif symbol == "Volatility 100 Index":
        symbol_code = "R_100"
    
    #(1s)
    elif symbol == "Volatility 10 (1s) Index":
        symbol_code = "1HZ10V"
    elif symbol == "Volatility 25 (1s) Index":
        symbol_code = "1HZ25V"
    elif symbol == "Volatility 50 (1s) Index":
        symbol_code = "1HZ50V"
    elif symbol == "Volatility 75 (1s) Index":
        symbol_code = "1HZ75V"
    elif symbol == "Volatility 100 (1s) Index":
        symbol_code = "1HZ100V"
    
    #Jumps    
    elif symbol == "Jump 10 Index":
        symbol_code = "JD10"
    elif symbol == "Jump 25 Index":
        symbol_code = "JD25"
    elif symbol == "Jump 50 Index":
        symbol_code = "JD50"
    elif symbol == "Jump 75 Index":
        symbol_code = "JD75"
    elif symbol == "Jump 100 Index":
        symbol_code = "JD100"

    # Get proposal
    proposal = await api.proposal({"proposal": 1, "amount": stake, "barrier": "+0.1", "basis": "stake",
                                   "contract_type": "CALL" if trade_option == "buy" else "PUT", "currency": "USD", "duration": expiration, "duration_unit": "s",
                                   "symbol": symbol_code
                                   })
    print("After Proposal: ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    # Place order  
    response = await api.buy({"buy": proposal.get('proposal').get('id'), "price": stake}) 
    print(symbol," Purchased: ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))  

    closed_order = False
    while closed_order == False:
        # Subscribe to contract
        poc = await api.proposal_open_contract(
        {"proposal_open_contract": 1, "contract_id": response.get('buy').get('contract_id')})
        status = poc.get('proposal_open_contract').get('is_sold')
        profit = poc.get('proposal_open_contract').get('profit')     
        print("Position Closed :",profit) if status == 1 else print("Running with profit of:",profit)
        if status == 1:          
            closed_order = True
            break
        await asyncio.sleep(3)
def thread_orders(stop_event, data,trading_data):
    """Function executed by a thread. It checks if the conditions to open orders
    are okay.
    Args:
        stop_event (thread.Event): Event to stop the thread.
        data (dict): Dictionary with trade option and the symbol.
        trading_data (dict): Dictionary with the stake and expiration time for trade.
    """
    current_asset = ""
    while data["symbol"] == "" and data["trade_option"] == "":
        pass

    print("[INFO]\tOrders running")
    
    while not stop_event.is_set():
        if data["trade_option"] != "":
            asyncio.run(open_position(data["symbol"],trading_data["stake"],data["trade_option"],trading_data["expiration"]))
            data["trade_option"] = ""
    

            
