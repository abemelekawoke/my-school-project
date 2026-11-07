from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

# Password is Pa$$w0rd -> URL-encoded as Pa%24%24w0rd
ROUTER_URL = "http://admin:Pa$$w0rd@192.168.8.1/"


def send_sms_hilink(phone_number: str, message: str):
    """Returns (success: bool, error_message: str)."""
    try:
        with Connection(ROUTER_URL) as connection:
            client = Client(connection)
            result = client.sms.send_sms([phone_number], message)
            if result == "OK":
                return True, ""
            return False, f"Router returned: {result}"
    except Exception as e:
        return False, str(e)