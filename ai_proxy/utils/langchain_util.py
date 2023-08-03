from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain, SimpleSequentialChain


llm = OpenAI(temperature=0.0001, model_name="gpt-3.5-turbo-0613", openai_api_key="sk-ilvleyujXnlgzMV8K66dssh2y3BZFt5QGe+kbferrPMNAQAA", openai_api_base="https://api.app4gpt.com/v1")

OPENAI_API_KEY="sk-ilvleyujXnlgzMV8K66dssh2y3BZFt5QGe+kbferrPMNAQAA"
OPENAI_API_BASE="https://api.app4gpt.com/v1"
class LangChainClient(object):

    def __init__(self, model_name="gpt-3.5-turbo-0613", temperature=0,
                 openai_api_base=OPENAI_API_BASE, openai_api_key=OPENAI_API_KEY):

        self.api_base = openai_api_base
        self.api_key = openai_api_key
        self.llm = OpenAI(temperature=temperature, model_name=model_name,
                          openai_api_key=openai_api_key,
                          openai_api_base=openai_api_base)


    def text_to_sql(self, text, tabledesc):
        sql_template = """现在你是一个数据分析师,SQL大神,请根据用户提供的表的信息，以及用户的需求，写出简洁的效率最高的SQL,
        并且要求输出的SQL以#开头,以#结尾，样例如下：
        #SELECT * FROM table#
        #SELECT COUNT(*) FROM table#
        #WITH table AS (), SELECT * FROM table#

        % 表信息如下
        {tabledesc}

        % 用户需求
        {sqltext}
        """

        sql_prompt_template = PromptTemplate(input_variables=["tabledesc", "sqltext"], template=sql_template)
        sql_chain = LLMChain(llm=llm, prompt=sql_prompt_template, output_key="sql_output")
        overall_chain = SequentialChain(chains=[sql_chain], input_variables=["tabledesc", "sqltext"],
                                        output_variables=["sql_output"], verbose=True)

        output = overall_chain({"tabledesc": tabledesc, "sqltext": text})
        for k, v in output.items():
            print(f"{k}\n{v}")

        sql_output = output["sql_output"].strip('#')

        return sql_output



    def text_to_code(self):
        pass


if __name__ == '__main__':

    tabledesc = """
    # Employee-雇员(id, name, department_id, local_city-居住城市, city-办公城市, birth_date, gender, hire_date-入职日期)
    # Department-部门(id, name, address-办公地址, tel-联系电话)
    # Salary_Payments-薪酬支出(id, employee_id, amount, tax, date)
    # Sales-销售(id, employee_id, product_id, state-状态 0:进行中、1:完成、2:取消, amount-销量, date)
    # Product-产品(id, name, price, category)
    """

    text = "列出办公地址在北京的月平均薪酬最高的5个雇员及其销售量最大的产品名称"

    client = LangChainClient()
    sql = client.text_to_sql(text=text, tabledesc=tabledesc)
    print(f"sql:\n${sql}")
