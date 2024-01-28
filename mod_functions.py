import json
import requests

def mod_load_config() -> dict:
    mod_config_path = "mod-config.json"
    try:
       mod_config = json.load(open(mod_config_path))
       print(mod_config)
    except Exception as e:
        raise Exception(f"error loading mod config file {mod_config_path} {e}")
    return {
       k : mod_config[k] if k in mod_config else ""
       for k in ["tg_token", "chat_id", 
                 "wallet_dir", "oracle_user", 
                 "oracle_password", 
                 "dsn", "wallet_location", 
                 "wallet_password", "table_name"]
    }

def send_msg(msg,token,chat_id):
    r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={"chat_id": chat_id, "text": msg})
    print(r.json())

if __name__ == "__main__":
    config = mod_load_config()
    send_msg("load config successed!",config["tg_token"],config["chat_id"])
