# Savicoin OpenAPI Documentation

## 项目介绍

这是Savicoin交易所的现货交易API官方文档和示例代码仓库，旨在帮助开发者快速理解和集成我们的交易API。通过此SDK，您可以轻松接入Savicoin交易平台，实现数字货币的现货交易、行情查询、账户管理等功能。

## 项目结构

```
openapi-spot-docs/
├── docs/                 # API文档目录
│   └── api_reference.md  # API接口参考文档
├── sample/               # 示例代码
│   ├── java/             # Java语言示例
│   │   ├── src/          # 源代码
│   │   │   └── main/
│   │   │       ├── java/com/example/openapi/
│   │   │       │   ├── client/     # API客户端
│   │   │       │   ├── model/      # 数据模型
│   │   │       │   └── utils/      # 工具类
│   │   │       └── resources/      # 配置文件
│   │   └── pom.xml       # Maven配置文件
│   ├── python/           # Python语言示例（待补充）
└── README.md             # 项目说明文档
```

## 主要功能

- **市场数据查询**：获取交易对、深度、K线、ticker等行情信息
- **交易操作**：下单、撤单、查询订单状态等
- **账户管理**：查询账户资产、交易历史等
- **WebSocket接口**：实时订阅市场数据和账户变动

## 快速开始

### Java SDK使用

1. **添加依赖**

   将示例代码中的`pom.xml`依赖添加到您的项目中

2. **创建API客户端**

   ```java
   // 初始化客户端（公共API无需认证）
   ApiClient publicClient = new ApiClient("https://open.icsotic.com");
   
   // 初始化客户端（私有API需要认证）
   ApiClient privateClient = new ApiClient(
       "https://open.icsotic.com",
       "your-access-key", 
       "your-secret-key"
   );
   ```

3. **调用API**

   ```java
   // 查询市场深度（公共API）
   TreeMap<String, String> params = new TreeMap<>();
   params.put("symbol", "BTC_USDT");
   params.put("limit", "10");
   
   String marketDepth = publicClient.sendGetRequest("/market/depth", params, false);
   ```

## 认证方式

API请求需要使用AccessKey和SecretKey进行签名认证，详细认证流程请参考API文档。

## 联系我们

如有任何问题或建议，请通过以下方式联系我们：

- 官方网站：https://savicoin.com/
