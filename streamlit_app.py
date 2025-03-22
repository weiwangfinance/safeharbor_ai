import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 SafeHarbor AI ")
st.write(
    "Welcome to **SafeHarbor AI**, your trusted companion in the fight against financial fraud and investment scams! In today's fast-paced digital world, staying vigilant against deceptive schemes is more important than ever. FraudShield AI leverages cutting-edge artificial intelligence to empower individuals with the knowledge and tools to protect their finances and make informed decisions."
    """
    \n **What Does FraudShield AI Do?**
- **Financial Fraud Detection:** The chatbot helps you identify red flags in financial offers, investment opportunities, and transactions. Whether it's phishing, Ponzi schemes, or cryptocurrency scams, FraudShield AI is here to guide you.
- **Education on Financial Safety:** Learn essential skills to safeguard your money, understand common fraud tactics, and build financial literacy to make smarter decisions.
- **Real-Time Consultation:** Have doubts about a suspicious email, call, or investment pitch? FraudShield AI provides instant advice and actionable insights.
- **Scam Awareness Updates:** Stay up-to-date with the latest trends in financial fraud and scams, so you're always prepared.

 **Why Choose FraudShield AI?**
- **Accessible and Reliable:** Available 24/7, FraudShield AI is your go-to resource for combating financial fraud and gaining confidence in managing your finances.
- **Empowering You:** By educating and assisting you, the chatbot ensures you're not only protected but also equipped to prevent fraud on your own.

Join the movement to protect yourself and others from financial fraud. With FraudShield AI, you're in control of your financial future. Let's build a safer and smarter financial world together!
"""
)






# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    #client = OpenAI(api_key=openai_api_key)
    client = OpenAI(
        base_url="wss://spark-api.xf-yun.com/v1.1/chat",
        api_key="46909103&MTU1YWQ5MGFkNzhkYTBmM2NjNzMyYTBj&e8583878e386f949c0776808a7160823", 
    )


    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )



completion = client.chat.completions.create(
    model="generalv3.5",  # e.g. gpt-35-instant
    max_tokens=6000,
    messages=[
        {
            "role": "system",
            "content":  "你是一个非常棒的Wrapper代码生成Agent，通过跟用户不断对话，理解用户需求并按照既定范式完成插件wrapper代码编写。",
            "role": "user",
            "content":"\nWrapper代码用于把如模型推理，三方API 包装成符合ASE协议规范的的服务。\n\nWrapper的既定范式如下:\n```\n### start 以下是导入必要的工具包代码区块\nimport json\nimport os.path\n\nfrom aiges.core.types import *\n\ntry:\n    from aiges_embed import ResponseData, Response, DataListNode, DataListCls, SessionCreateResponse  # c++\nexcept:\n    from aiges.dto import Response, ResponseData, DataListNode, DataListCls, SessionCreateResponse\n\nfrom aiges.sdk import WrapperBase, \\\n    ImageBodyField, \\\n    StringBodyField, StringParamField\nfrom aiges.utils.log import log, getFileLogger\n### end 以下是导入必要的工具包代码区块\n\n### start 下面是引用你的推理代码区块\nfrom  inference import Engine\n\n### end\n\n### start 下面是设置服务的请求和响应字段代码区块\n# 定义服务的请求参数\nclass UserRequest(object):\n    input1 = ImageBodyField(key=\"img\", path=\"test_data/0.png\") # 代表服务需要输入一个 key为 img的图片字段，该字段需要传递图片的二进制bytes. input1为固定格式命名，如果有多个输入，则以input1, input2,input3... 分别命名\n\n\n# 定义模型的输出参数\nclass UserResponse(object):\n    accept1 = StringBodyField(key=\"result\") # 代表服务需要输出一个 key为 result，该字段需类型是一个String类型. accept1，如果有多个输出，则以accept1, accept2, accept3... 分别命名\n\n### end\n\n\n\n### 下面以mnist手写体模型推理插件为例\n\n### start 推理的核心区块是实现如下Wrapper类以及其方法，\n# wrapper类必须继承WrapperBase\nclass Wrapper(WrapperBase):\n    serviceId = \"mnist\" # 服务英文名，由用户输入，默认可以为 default\n    version = \"v1\" # 版本号固定为v1\n    call_type = 1 # 调用类型固定为1\n    requestCls = UserRequest() # 这里引用了上述定义的 UserRequest类并实例化为requestCls\n    responseCls = UserResponse() # 这里引用了上述定义的UserResponse并实例化为responseCls\n    model = None\n\n    def __init__(self, *args, **kwargs):\n        super().__init__(*args, **kwargs)\n        self.transform = None\n        self.device = None\n        self.filelogger = None\n\n    def wrapperInit(self, config: {}) -> int:\n        log.info(\"Initializing ...\")\n        self.filelogger = getFileLogger()\n        self.engine = Engine(config) # 实例化用户实现的inference.py中的 Engine类\n        return 0\n\n    def wrapperLoadRes(self, reqData: DataListCls, resId: int) -> int:\n        # 该方法用于加载个性化资源，默认无需实现\n        return 0\n\n    def wrapperUnloadRes(self, resId: int) -> int:\n        # 该方法用于卸载个性化资源，默认无需实现\n        return 0\n\n    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag: str = \"\", persId: int = 0) -> Response:\n        # 非流式推理接口，会把reqData数据转换送入到 engine的 infer方法中\n        # 使用Response封装result\n        res = Response()\n        ctrl = params.get(\"ctrl\", \"default\")\n        self.filelogger.info(\"got reqdata , %s\" % reqData.list)\n        imagebytes = reqData.get(\"img\").data\n        img = Image.open(io.BytesIO(imagebytes)) # 对于图片数据，需要使用Image.open转成内存bytes流\n        try:\n            result = self.engine.infer(img) # 该方法需要根据self.engine.infer方法返回修改\n            log.info(\"infer result ###:%d\" % int(result))\n            # 如下结构用用户定义，这里mnist服务返回一个 json，包含 result 和msg\n            text_json = {\n                \"result\": int(result),\n                \"msg\": \"result is: %d\" % int(result)\n            }\n            accept1Data = ResponseData() # responseCls 中只有一个数据段accept1，所以只需要实例化一个ResponseData\n            accept1Data.key = \"result\" # 由于上述响应类responseCls 设置的key为 result\n            accept1Data.setDataType(DataText) # 响应是是StringBody 需要设置为 DataText\n            accept1Data.status = Once # 非流式设置为Once\n            accept1Data.setData(json.dumps(text_json).encode(\"utf-8\")) # 把text_json转换为 str 放入响应数据中\n            res.list = [accept1Data] # 将accept1Data 放入res响应类中\n        except Exception as e:\n            log.error(e)\n            # 错误逻辑处理\n            return res.response_err(100)\n        return res\n\n    def wrapperFini(cls) -> int:\n        return 0\n\n    def wrapperError(cls, ret: int) -> str:\n        if ret == 100:\n            return \"wrapper exec exception here...\"\n        return \"\"\n    def wrapperCreate(cls, params: {}, sid: str, persId: int = 0) -> SessionCreateResponse:\n        print(params)\n        i = random.randint(1,30000)\n        print(sid)\n        return f\"hd-test-{i}\"\n    '''\n        此函数保留测试用，不可删除\n    '''\n\n    def wrapperTestFunc(cls, data: [], respData: []):\n        pass\n\n### end\n\n\n```\n\n现在Wrapper的引入的inference.py代码如下:\n\n```python\nimport os\n\nimport torch\nimport torch.nn as nn\nimport torch.nn.functional as F\nfrom torchvision import transforms\n\nclass Net(nn.Module):\n    def __init__(self):\n        super(Net, self).__init__()\n        self.conv1 = nn.Conv2d(1, 32, 3, 1)\n        self.conv2 = nn.Conv2d(32, 64, 3, 1)\n        self.dropout1 = nn.Dropout(0.25)\n        self.dropout2 = nn.Dropout(0.5)\n        self.fc1 = nn.Linear(9216, 128)\n        self.fc2 = nn.Linear(128, 10)\n\n    def forward(self, x):\n        x = self.conv1(x)\n        x = F.relu(x)\n        x = self.conv2(x)\n        x = F.relu(x)\n        x = F.max_pool2d(x, 2)\n        x = self.dropout1(x)\n        x = torch.flatten(x, 1)\n        x = self.fc1(x)\n        x = F.relu(x)\n        x = self.dropout2(x)\n        x = self.fc2(x)\n        output = F.log_softmax(x, dim=1)\n        return output\n\n## 推理引擎类,由用户实现\nclass Engine():\n    def __init__(self,config):\n        self.config = config\n        self.device = \"cpu\"\n        self.model = Net().to(self.device)\n        ptfile = os.path.join(os.path.dirname(__file__), \"train\", \"mnist_cnn.pt\")\n        self.model.load_state_dict(torch.load(ptfile))  # 根据模型结构，调用存储的模型参数\n        self.model.eval()\n        self.transform = transforms.Compose([\n            transforms.Grayscale(num_output_channels=1),\n            transforms.Resize([28, 28]),\n            transforms.ToTensor(),\n            transforms.Normalize((0.1307,), (0.3081,))\n        ])\n\n    def infer(self, config, data):\n        img = self.transform(data).unsqueeze(0)\n        img.to(self.device)\n        result = self.model(img).argmax()\n        return result\n\n```\n\n\n请根据上述规范代码中注释部分和如下用户的需求调整并生成新的wrapper.py，注意inference.py 不需要合入wrapper.py.代码必须符合python规范\n\n用户需求如下:\n帮我根据inference.py中的推理实现调整下 wrapper.py中调用 infer方法部分",
        },
    ],

)
print(completion.model_dump()["choices"][0]["message"]["content"])

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

