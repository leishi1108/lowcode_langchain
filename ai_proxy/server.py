import logging
import json
import multiprocessing
import argparse
import time
import thriftpy2

from thriftpy2.rpc import make_server
from utils.langchain_util import LangChainClient
from utils.openai_util import get_completion

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ai_proxy_thrift = thriftpy2.load("ai_proxy/idl/ai_proxy.thrift", module_name="ai_proxy_thrift")


class Handler(object):

    def Ping(self):
        return "Pong"

    def ChatCompletionCreate(self, req):
        model = req.model
        messages = req.messages
        temperature = req.temperature

        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "can you tell me who are you and who's your father"}
        ]
        temperature=0.01
        output = get_completion(messages=messages, model=model, temperature=temperature)
        resp = ai_proxy_thrift.ChatCompletionResponse(
            id=-1,
            object=output,
            json={},
            BaseResp=ai_proxy_thrift.BaseResp(
                StatusMessage=f"Success",
                StatusCode=0
            )
        )
        return resp


    def LangChainCreate(self, req):
        model_name = req.model
        task = req.task
        query = req.query
        context = req.context
        temperature = req.temperature


        client = LangChainClient(model_name=model_name, temperature=temperature)
        if task == "text-to-sql":
            if "tabledesc" not in context:
                return ai_proxy_thrift.LangChainResponse(
                    BaseResp=ai_proxy_thrift.BaseResp(
                        StatusMessage=f"tabledesc not in context",
                        StatusCode=1
                    )
                )

            tabledesc = context["tabledesc"]
            output = client.text_to_sql(query, tabledesc)

            resp = ai_proxy_thrift.LangChainResponse(
                id=-1,
                object=output,
                json={},
                BaseResp=ai_proxy_thrift.BaseResp(
                    StatusMessage=f"Success",
                    StatusCode=0
                )
            )
        else:
            resp = ai_proxy_thrift.LangChainResponse(
                BaseResp=ai_proxy_thrift.BaseResp(
                    StatusMessage=f"not support {task} task",
                    StatusCode=1
                )
            )

        return resp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=str, required=True, help="port")
    args = parser.parse_args()
    port = int(args.port)
    multiprocessing.set_start_method('fork')
    server = make_server(ai_proxy_thrift.AIProxyService, Handler(), '127.0.0.1', port)
    server.serve()

    logger.info(f"start serving")
