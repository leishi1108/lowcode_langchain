import logging
import thriftpy2
from thriftpy2.rpc import make_client
ai_proxy_thrift = thriftpy2.load("ai_proxy/idl/ai_proxy.thrift", module_name="ai_proxy_thrift")
base_thrift = thriftpy2.load("ai_proxy/idl/base.thrift", module_name="ai_proxy_thrift")

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == '__main__':

    client = make_client(ai_proxy_thrift.AIProxyService, host='localhost', port=6668, timeout=30000)

    print(client.Ping())

    chat_request = ai_proxy_thrift.ChatCompletionRequest(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "can you tell me who are you and who's your father"}
        ],
        temperature=0.001,
        Base=ai_proxy_thrift.base.Base(Caller="shilei")
    )
    chat_res = client.ChatCompletionCreate(chat_request)

    print(f"chat_request: {chat_request}\n")
    print(f"chat_res: {chat_res}\n\n")

    tabledesc = """
        # Employee-雇员(id, name, department_id, local_city-居住城市, city-办公城市, birth_date, gender, hire_date-入职日期)
        # Department-部门(id, name, address-办公地址, tel-联系电话)
        # Salary_Payments-薪酬支出(id, employee_id, amount, tax, date)
        # Sales-销售(id, employee_id, product_id, state-状态 0:进行中、1:完成、2:取消, amount-销量, date)
        # Product-产品(id, name, price, category)
        """

    text = "列出办公地址在北京的月平均薪酬最高的5个雇员及其销售量最大的产品名称"

    langchain_request = ai_proxy_thrift.LangChainRequest(
        model="gpt-3.5-turbo",
        task="text-to-sql",
        query=text,
        context = {"tabledesc": tabledesc},
        Base=ai_proxy_thrift.base.Base(Caller="shilei")
    )
    langchain_res = client.LangChainCreate(langchain_request)

    print(f"langchain_request: {langchain_request}\n")
    print(f"langchain_res: {langchain_res}\n\n")
