import os
import sys
import logging
import json
import multiprocessing
import argparse
import time
import thriftpy2
from thriftpy2.rpc import make_server

from thriftpy2.protocol import (
    TBinaryProtocolFactory,
    TCompactProtocolFactory
)

from thriftpy2.transport import (
    TBufferedTransportFactory,
    TFramedTransportFactory,
    TServerSocket,
    TSSLServerSocket,
    TSocket,
    TSSLSocket,
)

from utils.langchain_util import LangChainClient
from utils.openai_util import get_completion

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_path = os.path.abspath(os.path.dirname(__file__))
logger.info(f"file_path {file_path}")
root_path = os.path.abspath(os.path.join(file_path, '../'))
logger.info(f"root_path {root_path}")
sys.path.insert(0, root_path)

ai_proxy_thrift = thriftpy2.load(f"{root_path}/ai_proxy/idl/ai_proxy.thrift", module_name="ai_proxy_thrift")

class Handler(object):

    def Ping(self):
        return "Pong"

    def LangChainCreate(self, req):
        model_name = req.model
        task = req.task
        query = req.query
        context = req.context
        temperature = req.temperature

        logger.info(f"model_name {model_name}")
        logger.info(f"task {task}")
        logger.info(f"query {query}")
        logger.info(f"context {context}")
        logger.info(f"temperature {temperature}")

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
                id='-1',
                object=output,
                json=json.dumps({}),
                BaseResp=ai_proxy_thrift.base.BaseResp(
                    StatusMessage=f"Success",
                    StatusCode=0
                )
            )
        else:
            resp = ai_proxy_thrift.LangChainResponse(
                BaseResp=ai_proxy_thrift.base.BaseResp(
                    StatusMessage=f"not support {task} task",
                    StatusCode=1
                )
            )

        return resp

    def ChatCompletionCreate(self, req):
        logger.info(f"req {req}")

        model = req.model
        messages = req.messages
        temperature = req.temperature

        logger.info(f"model {model}")
        logger.info(f"messages {messages}")
        logger.info(f"temperature {temperature}")

        # model="gpt-35-turbo",
        # messages=[
        #     {"role": "system", "content": "You are a helpful assistant."},
        #     {"role": "user", "content": "can you tell me who are you and who's your father"}
        # ]
        # temperature=0.01

        output = get_completion(messages=messages, model=model, temperature=temperature)
        resp = ai_proxy_thrift.ChatCompletionResponse(
            id='-1',
            object=output,
            json=json.dumps({}),
            BaseResp=ai_proxy_thrift.base.BaseResp(
                StatusMessage=f"Success",
                StatusCode=0
            )
        )
        return resp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=str, required=True, help="port")
    args = parser.parse_args()
    port = int(args.port)
    multiprocessing.set_start_method('fork')

    # make_server(service, handler,
    #             host="localhost", port=9090, unix_socket=None,
    #             proto_factory=TBinaryProtocolFactory(),
    #             trans_factory=TBufferedTransportFactory(),
    #             client_timeout=3000, certfile=None):

    # TBinaryProtocolFactory v.s. TCompactProtocolFactory
    # TBufferedTransportFactory v.s. TFramedTransportFactory
    # server = make_server(ai_proxy_thrift.AIProxyService, Handler(), '127.0.0.1', port)

    server = make_server(service=ai_proxy_thrift.AIProxyService,
                         handler=Handler(),
                         host='localhost',
                         port=port,
                         # proto_factory=TCompactProtocolFactory(),
                         proto_factory=TBinaryProtocolFactory(),
                         # trans_factory=TFramedTransportFactory(),
                         trans_factory=TBufferedTransportFactory(),
                         client_timeout=30000
                         )
    server.serve()

    logger.info(f"start serving")


    # handle = Handler()
    #
    # chat_request = ai_proxy_thrift.ChatCompletionRequest(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "can you tell me who are you and who's your father"}
    #     ],
    #     temperature=0.001,
    #     Base=ai_proxy_thrift.base.Base(Caller="shilei")
    # )
    #
    # output = handle.ChatCompletionCreate(chat_request)
    # print(output)
