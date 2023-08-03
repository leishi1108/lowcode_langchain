include "base.thrift"

struct ChatCompletionRequest {
    1: string model,
    2: list<map<string, string>> messages,
    3: optional double temperature,
    255: optional base.Base Base
}

struct LangChainRequest {
    1: string model,
    2: string task,
    3: string query,
    4: optional map<string, string> context,
    5: optional list<string> vectorstrores,
    6: optional list<string> docs,
    7: optional double temperature,
    255: optional base.Base Base,
}


struct ChatCompletionResponse {
    1: string id,
    2: string object,
    3: string json,
    255: base.BaseResp BaseResp,
}

struct LangChainResponse {
    1: string id,
    2: string object,
    3: string json,
    255: base.BaseResp BaseResp,
}


service AIProxyService {
    ChatCompletionResponse ChatCompletionCreate(1: ChatCompletionRequest req),
    LangChainResponse LangChainCreate(1: LangChainRequest req),
    string Ping()
}
