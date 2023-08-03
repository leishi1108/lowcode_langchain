import logging
import thriftpy2
from thriftpy2.rpc import make_client
ai_proxy_thrift = thriftpy2.load("ai_proxy/idl/ai_proxy.thrift", module_name="ai_proxy_thrift")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == '__main__':

    client = make_client(ai_proxy_thrift.AIProxyService, host='localhost', port=6668, timeout=30000)

    print(client.Ping())

    chat_request = ai_proxy_thrift.ChatCompletionRequest(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "can you tell me who are you and who's your father"}
        ]
    )
    chat_res = client.ChatCompletionCreate(chat_request)
    print(f"chat_res: {chat_res}")


    
