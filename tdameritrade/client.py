import os
import pandas as pd
from .session import TDASession
from .urls import ACCOUNTS, INSTRUMENTS, QUOTES, SEARCH, HISTORY, OPTIONCHAIN, MOVERS
from .exceptions import handle_error_response
import requests

def response_is_valid(resp):
    valid_codes = [200, 201]
    return resp.status_code in valid_codes


class TDClient(object):
    def __init__(self, consumer_id=None, refresh_token=None, access_token=None, accountIds=None):
        self._token = access_token or os.environ['ACCESS_TOKEN']
        self.refresh_token = refresh_token
        self.accountIds = accountIds or []
        self.consumer_id = consumer_id
        self.session = TDASession()
        if self._token:
            self.session.set_token(self._token)

    def _headers(self):
        return {'Authorization': 'Bearer ' + self._token}

    def get_token(self, *args, **kwargs):
        data = {'client_id': self.consumer_id + '@AMER.OAUTHAP',
                'grant_type': 'refresh_token',
                # 'access_type': 'offline',
                'refresh_token': self.refresh_token,
                }
        resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token', 
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data=data,verify=True)

    
        if resp.status_code == 401:
            raise('The Credentials you passed through are invalid.')
        elif resp.status_code == 400:
            raise('Validation was unsuccessful.')
        elif resp.status_code == 500:
            raise('The TD Server is experiencing an error, please try again later.')
        elif resp.status_code == 403:
            raise("You don't have access to this resource, cannot authenticate.")
        elif resp.status_code == 503:
            raise("The TD Server can't respond, please try again later.")

        body = resp.json()
        self._token = body['access_token']
        self.session = TDASession()
        self.session.set_token(self._token)

        path = "/Users/chenxinma/Documents/projects/td/token/"
        # path = "/home/ubuntu/td/token/"
        text_file = open(path + "access_token.txt", "w")
        text_file.write(self._token)
        text_file.close()

        if 'refresh_token' in body:
            text_file = open(path + "refresh_token.txt", "w")
            text_file.write(body['refresh_token'])
            text_file.close()

        # print(resp.json())




    def _request(self, method, params=None, *args, **kwargs):
        resp = self.session.request('GET', method, params=params, *args, **kwargs)

        if (resp.status_code == 401):
            self.get_token()
            resp = self.session.request('GET', method, 
                                    headers=self._headers(),
                                    params=params)
            # print(resp)
            return resp
        if not response_is_valid(resp):
            handle_error_response(resp)

        return resp

    # TODO: output results to self.accountIds
    def accounts(self, positions=False, orders=False):
        ret = {}

        if positions or orders:
            fields = '?fields='
            if positions:
                fields += 'positions'
                if orders:
                    fields += ',orders'
            elif orders:
                fields += 'orders'
        else:
            fields = ''

        if self.accountIds:
            for acc in self.accountIds:
                resp = self._request(ACCOUNTS + str(acc) + fields, headers=self._headers())
                ret[acc] = resp.json()

        else:
            resp = self._request(ACCOUNTS + fields, headers=self._headers())
            for account in resp.json():
                ret[account['securitiesAccount']['accountId']] = account

        return ret

    def accountsDF(self):
        return pd.json_normalize(self.accounts())

    def transactions(self, acc=None, type=None, symbol=None, start_date=None, end_date=None):
        if acc is None:
            acc = self.accounts
        transactions = ACCOUNTS + str(acc) + "/transactions"
        resp = self._request(transactions,
                             headers=self._headers(),
                             params={
                                 'type': type,
                                 'symbol': symbol,
                                 'startDate': start_date,
                                 'endDate': end_date
                             }).json()

        return resp

    def transactionsDF(self, acc, **kwargs):
        return pd.json_normalize(self.transactions(acc, kwargs))

    def search(self, symbol, projection='symbol-search'):
        resp = self._request(SEARCH,
                             headers=self._headers(),
                             params={'symbol': symbol,
                                     'projection': projection}).json()
        return resp

    def searchDF(self, symbol, projection='symbol-search'):
        ret = []
        dat = self.search(symbol, projection)
        for symbol in dat:
            ret.append(dat[symbol])
        return pd.DataFrame(ret)

    def fundamental(self, symbol):
        return self.search(symbol, 'fundamental')

    def fundamentalDF(self, symbol):
        return self.searchDF(symbol, 'fundamental')

    def instrument(self, cusip):
        resp = self._request(INSTRUMENTS + str(cusip),
                             headers=self._headers()).json()
        return resp

    def instrumentDF(self, cusip):
        return pd.DataFrame(self.instrument(cusip))

    def quote(self, symbol):
        resp = self._request(QUOTES,
                             headers=self._headers(),
                             params={'symbol': symbol.upper()}).json()
        return resp

    def quoteDF(self, symbol):
        x = self.quote(symbol)
        return pd.DataFrame(x).T.reset_index(drop=True)

    def history(self, symbol, **kwargs):
        resp = self._request(HISTORY % symbol,
                             headers=self._headers(),
                             params=kwargs).json()
        return resp

    def historyDF(self, symbol, **kwargs):
        x = self.history(symbol, **kwargs)
        df = pd.DataFrame(x['candles'])
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        except: 
            return None
        return df

    def options(self, symbol):
        resp = self._request(OPTIONCHAIN,
                             headers=self._headers(),
                             params={'symbol': symbol.upper()}).json()
        return resp

    def optionsDF(self, symbol):
        ret = []
        dat = self.options(symbol)
        for date in dat['callExpDateMap']:
            for strike in dat['callExpDateMap'][date]:
                ret.extend(dat['callExpDateMap'][date][strike])
        for date in dat['putExpDateMap']:
            for strike in dat['putExpDateMap'][date]:
                ret.extend(dat['putExpDateMap'][date][strike])

        df = pd.DataFrame(ret)
        if 'tradeTimeInLong' not in df.columns:
            return None
            
        for col in ('tradeTimeInLong', 'quoteTimeInLong', 'expirationDate', 'lastTradingDay'):
        # for col in ['expirationDate']:
            df[col] = pd.to_datetime(df[col], unit='ms')
        return df

    def movers(self, index, direction='up', change_type='percent'):
        resp = self._request(MOVERS % index,
                             headers=self._headers(),
                             params={'direction': direction,
                                     'change_type': change_type}).json()
        return resp

    def saved_orders(self, account_id, json_order):
        saved_orders = ACCOUNTS + account_id + "/savedorders"
        resp = self._request(saved_orders,
                             headers=self._headers(),
                             json=json_order).json()
        return resp

    def orders(self, account_id, json_order):
        orders = ACCOUNTS + account_id + "/orders"
        resp = self._request(orders,
                             headers=self._headers(),
                             json=json_order
                             ).json()
        return resp
