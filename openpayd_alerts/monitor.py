import requests, sys, time, datetime
import pandas as pd

sys.path.append('/home/ubuntu/openpayd_alerts/config/')
import confi

def get_currency(row):
    return row['amount']['currency']
def get_value(row):
    return row['amount']['value']

dfInit = pd.read_csv('/home/ubuntu/openpayd_alerts/newest.csv')

while True:
    url = " https://secure-mt.openpayd.com/api/oauth/token?grant_type=client_credentials"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "authorization": "Basic dGVsZWdyYW1hbGVydHM6TiFqIyVNNDVVbQ=="
    }

    response = requests.post(url, headers=headers).json()

    url = f"https://secure-mt.openpayd.com/api/transactions"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-account-holder-id": response['accountHolderId'],
        "Authorization": f"Bearer {response['access_token']}"
    }
    response = requests.get(url, headers=headers).json()

    df = pd.DataFrame(response['content'])
    df = df[df['type'] == 'PAYIN']
    df['currency'] = df.apply(get_currency, axis=1)
    df['value'] = df.apply(get_value, axis=1)
    df = df[['createdDate', 'source', 'currency', 'value']]
    try:
        dfInit['currency'] = dfInit.apply(get_currency, axis=1)
        dfInit['value'] = dfInit.apply(get_value, axis=1)
        dfInit = dfInit[['createdDate', 'source', 'currency', 'value']]
    except Exception as e:
        print(f"There was an error with the dfInit formatting\nError: {e}")
        requests.get(f"https://api.telegram.org/bot{confi.telegram_error_token}/sendMessage?chat_id={confi.telegram_error_id}&text=Error formatting dfInit: {e}")
    print(df)
    print(dfInit)
    try:
        dfCon = pd.concat([dfInit, df]).drop_duplicates(keep=False)
        print('there where differences')
        dfCon = dfCon.to_dict(orient='records')
        if len(dfCon) != 0:
            for i in dfCon:
                requests.get(f"https://api.telegram.org/bot{confi.telegram_token}/sendMessage?chat_id={confi.telegram_id}&text=New transaction Currency: {i['currency']}\nValue: {i['value']}\nDate/Time: {i['createdDate']}\nSource: {i['source']}")
    except Exception as e:
        print(f"They were the same or there was an error.\nError: {e}")
        requests.get(f"https://api.telegram.org/bot{confi.telegram_error_token}/sendMessage?chat_id={confi.telegram_error_id}&text=Error concating dataframes: {e}")
    #requests.get(f"https://api.telegram.org/bot{confi.telegram_token}/sendMessage?chat_id={confi.telegram_id}&text={df}")
    dfInit = df
    #dfInit = dfInit[['createdDate', 'amount', 'source']]
    df.to_csv('/home/ubuntu/openpayd_alerts/newest.csv') #server code
    #df.to_csv('newest.csv') #local code
    startSleep = time.time()
    print(f"Starting to sleep for 2 minutes.\nStarting at: {datetime.datetime.fromtimestamp(startSleep).strftime('%H:%M:%S')}\nFinishing at: {datetime.datetime.fromtimestamp(startSleep+120).strftime('%H:%M:%S')}")
    time.sleep(60*confi.sleepTime)
