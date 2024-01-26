import json
import requests

def mod_load_config(mod_config_path = "mod-config.json") -> dict:
    if mod_config_path is None:
        mod_config_path = "mod-config.json"
    try:
       mod_config = json.load(open(mod_config_path))
       print(mod_config)
    except Exception as e:
        raise Exception(f"error loading mod config file {mod_config_path} {e}")
    return {
       k : mod_config[k] if k in mod_config else ""
       for k in ["tg_token", "chat_id", 
                 "wallet_dir", "oracle_user", "oracle_password", "dsn", "wallet_location", "wallet_password", "table_name"]
    }

def load_user_info(user: str, api_keys_path="api-keys.json") -> dict:
    if api_keys_path is None:
        api_keys_path = "api-keys.json"
    try:
        api_keys = json.load(open(api_keys_path))
    except Exception as e:
        raise Exception(f"error loading api keys file {api_keys_path} {e}")
    if user not in api_keys:
        raise Exception(f"user {user} not found in {api_keys_path}")
    return {
        k: api_keys[user][k] if k in api_keys[user] else ""
        for k in ["exchange", "key", "secret", "passphrase"]
    }

def send_msg(msg,token,chat_id):
    r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={"chat_id": chat_id, "text": msg})
    print(r.json())

# print(mod_load_config())
# send_msg(mod_load_config(),(mod_load_config()["tg_token"]),(mod_load_config()["chat_id"]))
{
       "tg_token": "1582443382:AAGZHjDtgK5R1hNdcWXviBjQ1ihXaoIW4FE",
        "chat_id": "-911547716",
        "wallet_dir": "wallet",
        "oracle_user": "ADMIN",
        "oracle_password": "3FhlI7gg99qOZl4i",
        "dsn": "a247k8swn2929rtw_low",
        "wallet_location": "wallet",
        "wallet_password": "3FhlI7gg99qOZl4i",
        "table_name": "binancefutures2309"
    }