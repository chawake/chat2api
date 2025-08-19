
# CHAT2API (English)

🤖 A simple ChatGPT-to-API proxy

🌟 Use free, unlimited `GPT-3.5` without an account

💥 Supports AccessToken login; supports `O3-mini/high`, `O1/mini/Pro`, `GPT-4/4o/mini`, `GPTs`

🔍 Response format fully matches the official API; compatible with almost all clients

👮 Works with the user management panel [Chat-Share](https://github.com/h88782481/Chat-Share). Before using it, configure environment variables in advance (set `ENABLE_GATEWAY=True`, `AUTO_SEED=False`).

## Community

[https://t.me/chat2api](https://t.me/chat2api)

Please read the repository docs before asking questions, especially the FAQ.

When asking questions, please provide:

1. Startup logs screenshot (mask sensitive info, including env vars and versions)
2. Error logs (mask sensitive info)
3. HTTP status code and response body from the API

## Features

### Latest version is stored in `version.txt`

### Reverse API Features

> - [x] Streaming and non-streaming
> - [x] Account-free GPT-3.5 chat
> - [x] GPT-3.5 model chat (if the provided model name does not contain `gpt-4`, it defaults to GPT-3.5, i.e. `text-davinci-002-render-sha`)
> - [x] GPT-4 series chat (use a model name containing: `gpt-4`, `gpt-4o`, `gpt-4o-mini`, `gpt-4-mobile` to use the corresponding model; AccessToken required)
> - [x] O1 series chat (use a model name containing `o1-preview`, `o1-mini`; AccessToken required)
> - [x] GPT-4 image generation, code, and web browsing
> - [x] GPTs supported (model name: `gpt-4-gizmo-g-*`)
> - [x] Team Plus accounts supported (requires team account id)
> - [x] Upload images and files (API-compatible formats; supports URL and base64)
> - [x] Can serve as a gateway with distributed deployment
> - [x] Multi-account round-robin; supports both `AccessToken` and `RefreshToken`
> - [x] Retry on request failure and automatically round-robin to the next token
> - [x] Tokens management: upload and clear
> - [x] Scheduled `AccessToken` refresh via `RefreshToken` / On every startup, a non-forced refresh of all tokens; every 4 days at 3 AM, forced refresh all.
> - [x] File download supported (requires history enabled)
> - [x] Supports reasoning traces for models like `O3-mini/high`, `O1/mini/Pro`

### Official-site Mirror Features

> - [x] Supports native official mirror
> - [x] Backend account pool random selection; `Seed` sets a random account
> - [x] Login directly with `RefreshToken` or `AccessToken`
> - [x] Supports `O3-mini/high`, `O1/mini/Pro`, `GPT-4/4o/mini`
> - [x] Sensitive endpoints disabled; some settings endpoints disabled
> - [x] `/login` page; after logout, auto-redirect to login
> - [x] `/?token=xxx` direct login, where `xxx` is `RefreshToken`, `AccessToken`, or `SeedToken` (random seed)
> - [x] Session isolation per different SeedToken
> - [x] Supports `GPTs` store
> - [x] Supports official unique features like `DeepResearch`, `Canvas`
> - [x] Supports switching languages

> TODO
> - [ ] None for now, PRs/issues are welcome

## Reverse API

Fully `OpenAI`-compatible API. Supports `AccessToken` or `RefreshToken`. Usable models: GPT-4, GPT-4o, GPT-4o-Mini, GPTs, O1-Pro, O1, O1-Mini, O3-Mini, O3-Mini-High:

```bash
curl --location 'http://127.0.0.1:5005/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{Token}}' \
--data '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "stream": true
   }'
```

Pass your account `AccessToken` or `RefreshToken` as `{{ Token }}`.
You can also pass the value you configured in the environment variable `AUTHORIZATION`; it will randomly choose a backend account.

If you have a team account, pass `ChatGPT-Account-ID` to use the Team workspace:

- Method 1:
  Put `ChatGPT-Account-ID` in the request headers.

- Method 2:
  `Authorization: Bearer <AccessToken or RefreshToken>,<ChatGPT-Account-ID>`

If `AUTHORIZATION` is set, you can use its value as `{{ Token }}` to enable multi-token round-robin.

> - Get `AccessToken`: log in to ChatGPT officially, then open https://chatgpt.com/api/auth/session and copy the `accessToken` value.
> - Get `RefreshToken`: not provided here.
> - Account-free GPT-3.5 does not require any token.

## Token Management

1. Configure env var `AUTHORIZATION` as an “authorization code”, then run the program.
2. Visit `/tokens` or `/{api_prefix}/tokens` to view the number of existing tokens, upload new ones, or clear tokens.
3. When requesting, pass the authorization code you set in `AUTHORIZATION` to use the round-robin tokens.

![tokens.png](docs/tokens.png)

## Official-site Mirror

1. Set env var `ENABLE_GATEWAY=true`, then run the program. Note: after enabling, others can access your gateway by domain directly.
2. Upload `RefreshToken` or `AccessToken` on the Tokens management page.
3. Visit `/login` to open the login page.

![login.png](docs/login.png)

4. Use the native official mirror page.

![chatgpt.png](docs/chatgpt.png)

## Environment Variables

Each variable has a default. If you’re unsure about meanings, do not set them (and do not pass empty strings). Strings do not need quotes.

| Category | Name               | Example                                                       | Default                 | Description |
|---------|--------------------|---------------------------------------------------------------|-------------------------|-------------|
| Security | API_PREFIX        | `your_prefix`                                                | `None`                  | API prefix password. If unset, it’s easy to be accessed. When set, you must call `/your_prefix/v1/chat/completions`. |
|         | AUTHORIZATION      | `your_first_authorization`,<br/>`your_second_authorization`  | `[]`                    | Your self-defined authorization code(s) for multi-account token round-robin, comma-separated. |
|         | AUTH_KEY           | `your_auth_key`                                              | `None`                  | Set this if your private gateway requires an `auth_key` header. |
| Request | CHATGPT_BASE_URL   | `https://chatgpt.com`                                        | `https://chatgpt.com`   | ChatGPT gateway address. Changes the target site; multiple URLs comma-separated. |
|         | PROXY_URL          | `http://ip:port`,<br/>`http://username:password@ip:port`     | `[]`                    | Global proxy URL. Used when 403 occurs. Multiple proxies comma-separated. |
|         | EXPORT_PROXY_URL   | `http://ip:port` or<br/>`http://username:password@ip:port`   | `None`                  | Egress proxy to avoid leaking source IP when requesting images/files. |
| Features | HISTORY_DISABLED  | `true`                                                       | `true`                  | Whether to avoid saving chat history and returning conversation_id. |
|         | POW_DIFFICULTY     | `00003a`                                                     | `00003a`                | Proof-of-work difficulty target. Don’t change if unsure. |
|         | RETRY_TIMES        | `3`                                                          | `3`                     | Retry count on errors; with `AUTHORIZATION` it will auto random/round-robin next account. |
|         | CONVERSATION_ONLY  | `false`                                                      | `false`                 | Use the conversation endpoint directly. Enable only if your gateway can auto-solve POW. |
|         | ENABLE_LIMIT       | `true`                                                       | `true`                  | When enabled, avoids trying to bypass official rate limits to reduce risk of account bans. |
|         | UPLOAD_BY_URL      | `false`                                                      | `false`                 | When enabled, chat by `URL + space + text`; automatically fetches URL content and uploads. Multiple URLs separated by spaces. |
|         | SCHEDULED_REFRESH  | `false`                                                      | `false`                 | Whether to refresh `AccessToken` on a schedule. On startup, all tokens non-forced refresh once; every 4 days at 3 AM, forced refresh all. |
|         | RANDOM_TOKEN       | `true`                                                       | `true`                  | Randomly choose a backend token. When disabled, round-robin in order. |
| Gateway | ENABLE_GATEWAY     | `false`                                                      | `false`                 | Enable gateway mode to use the mirror site (will be publicly accessible). |
|         | AUTO_SEED          | `false`                                                      | `true`                  | Enable random account (seed) mode. If disabled, you must integrate your own interface to manage tokens. |

## Deployment

### Zeabur

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/6HEGIZ?referralCode=LanQian528)

### Direct

```bash
git clone https://github.com/LanQian528/chat2api
cd chat2api
pip install -r requirements.txt
python app.py
```

### Docker

You need Docker and Docker Compose.

```bash
docker run -d \
  --name chat2api \
  -p 5005:5005 \
  lanqian528/chat2api:latest
```

### (Recommended, works with PLUS account) Docker Compose

Create a new directory (e.g. chat2api) and enter it:

```bash
mkdir chat2api
cd chat2api
```

Download `docker-compose-warp.yml` from the repo into this directory:

```bash
wget https://raw.githubusercontent.com/LanQian528/chat2api/main/docker-compose-warp.yml
```

Modify environment variables in `docker-compose-warp.yml`, then run:

```bash
docker-compose up -d
```

## FAQ

> - Error codes:
>   - `401`: Your current IP does not support account-free login. Try changing IP, set a proxy in env var `PROXY_URL`, or your authentication failed.
>   - `403`: Check logs for details.
>   - `429`: Your IP exceeded the per-hour request limit. Try later or change IP.
>   - `500`: Internal server error.
>   - `502`: Bad gateway or network unavailable. Try a different network.

> - Known notes:
>   - Many Japanese IPs do not support account-free login. For GPT-3.5 no-auth, US IPs are recommended.
>   - 99% of accounts support free `GPT-4o`, but availability depends on region; Japan and Singapore IPs are often enabled.

> - What is the `AUTHORIZATION` environment variable?
>   - It’s a custom auth code you set for chat2api. After setting, you can use the saved token pool via round-robin by passing it as an `APIKEY`.
> - How to get `AccessToken`?
>   - Log into ChatGPT officially, then open https://chatgpt.com/api/auth/session and copy the `accessToken` value.

## License

MIT License

---

# CHAT2API

🤖 一个简单的 ChatGPT TO API 代理

🌟 无需账号即可使用免费、无限的 `GPT-3.5`

💥 支持 AccessToken 使用账号，支持 `O3-mini/high`、`O1/mini/Pro`、`GPT-4/4o/mini`、`GPTs`

🔍 回复格式与真实 API 完全一致，适配几乎所有客户端

👮 配套用户管理端[Chat-Share](https://github.com/h88782481/Chat-Share)使用前需提前配置好环境变量（ENABLE_GATEWAY设置为True，AUTO_SEED设---

置为False）


## 交流群

[https://t.me/chat2api](https://t.me/chat2api)

要提问请先阅读完仓库文档，尤其是常见问题部分。

提问时请提供：

1. 启动日志截图（敏感信息打码，包括环境变量和版本号）
2. 报错的日志信息（敏感信息打码）
3. 接口返回的状态码和响应体

## 功能

### 最新版本号存于 `version.txt`

### 逆向API 功能
> - [x] 流式、非流式传输
> - [x] 免登录 GPT-3.5 对话
> - [x] GPT-3.5 模型对话（传入模型名不包含 gpt-4，则默认使用 gpt-3.5，也就是 text-davinci-002-render-sha）
> - [x] GPT-4 系列模型对话（传入模型名包含: gpt-4，gpt-4o，gpt-4o-mini，gpt-4-moblie, gpt-5 即可使用对应模型，需传入 AccessToken）
> - [x] O1 系列模型对话（传入模型名包含 o1-preview，o1-mini 即可使用对应模型，需传入 AccessToken）
> - [x] GPT-4 模型画图、代码、联网
> - [x] 支持 GPTs（传入模型名：gpt-4-gizmo-g-*）
> - [x] 支持 Team Plus 账号（需传入 team account id）
> - [x] 上传图片、文件（格式为 API 对应格式，支持 URL 和 base64）
> - [x] 可作为网关使用，可多机分布部署
> - [x] 多账号轮询，同时支持 `AccessToken` 和 `RefreshToken`
> - [x] 请求失败重试，自动轮询下一个 Token
> - [x] Tokens 管理，支持上传、清除
> - [x] 定时使用 `RefreshToken` 刷新 `AccessToken` / 每次启动将会全部非强制刷新一次，每4天晚上3点全部强制刷新一次。
> - [x] 支持文件下载，需要开启历史记录
> - [x] 支持 `O3-mini/high`、`O1/mini/Pro` 等模型推理过程输出

### 官网镜像 功能
> - [x] 支持官网原生镜像
> - [x] 后台账号池随机抽取，`Seed` 设置随机账号
> - [x] 输入 `RefreshToken` 或 `AccessToken` 直接登录使用
> - [x] 支持 `O3-mini/high`、`O1/mini/Pro`、`GPT-4/4o/mini`
> - [x] 敏感信息接口禁用、部分设置接口禁用
> - [x] /login 登录页面，注销后自动跳转到登录页面
> - [x] /?token=xxx 直接登录, xxx 为 `RefreshToken` 或 `AccessToken` 或 `SeedToken` (随机种子)
> - [x] 支持不同 SeedToken 会话隔离
> - [x] 支持 `GPTs` 商店
> - [x] 支持 `DeepReaserch`、`Canvas` 等官网独有功能
> - [x] 支持切换各国语言


> TODO
> - [ ] 暂无，欢迎提 `issue`

## 逆向API

完全 `OpenAI` 格式的 API ，支持传入 `AccessToken` 或 `RefreshToken`，可用 GPT-4, GPT-4o, GPT-4o-Mini, GPTs, O1-Pro, O1, O1-Mini, O3-Mini, O3-Mini-High：

```bash
curl --location 'http://127.0.0.1:5005/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{Token}}' \
--data '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "stream": true
   }'
```

将你账号的 `AccessToken` 或 `RefreshToken` 作为 `{{ Token }}` 传入。
也可填写你设置的环境变量 `Authorization` 的值, 将会随机选择后台账号

如果有team账号，可以传入 `ChatGPT-Account-ID`，使用 Team 工作区：

- 传入方式一：
`headers` 中传入 `ChatGPT-Account-ID`值

- 传入方式二：
`Authorization: Bearer <AccessToken 或 RefreshToken>,<ChatGPT-Account-ID>`

如果设置了 `AUTHORIZATION` 环境变量，可以将设置的值作为 `{{ Token }}` 传入进行多 Tokens 轮询。

> - `AccessToken` 获取: chatgpt官网登录后，再打开 [https://chatgpt.com/api/auth/session](https://chatgpt.com/api/auth/session) 获取 `accessToken` 这个值。
> - `RefreshToken` 获取: 此处不提供获取方法。
> - 免登录 gpt-3.5 无需传入 Token。

## Tokens 管理

1. 配置环境变量 `AUTHORIZATION` 作为 `授权码` ，然后运行程序。

2. 访问 `/tokens` 或者 `/{api_prefix}/tokens` 可以查看现有 Tokens 数量，也可以上传新的 Tokens ，或者清空 Tokens。

3. 请求时传入 `AUTHORIZATION` 中配置的 `授权码` 即可使用轮询的Tokens进行对话

![tokens.png](docs/tokens.png)

## 官网原生镜像

1. 配置环境变量 `ENABLE_GATEWAY` 为 `true`，然后运行程序, 注意开启后别人也可以直接通过域名访问你的网关。

2. 在 Tokens 管理页面上传 `RefreshToken` 或 `AccessToken`

3. 访问 `/login` 到登录页面

![login.png](docs/login.png)

4. 进入官网原生镜像页面使用

![chatgpt.png](docs/chatgpt.png)

## 环境变量

每个环境变量都有默认值，如果不懂环境变量的含义，请不要设置，更不要传空值，字符串无需引号。

| 分类   | 变量名               | 示例值                                                         | 默认值                   | 描述                                                           |
|------|-------------------|-------------------------------------------------------------|-----------------------|--------------------------------------------------------------|
| 安全相关 | API_PREFIX        | `your_prefix`                                               | `None`                | API 前缀密码，不设置容易被人访问，设置后需请求 `/your_prefix/v1/chat/completions` |
|      | AUTHORIZATION     | `your_first_authorization`,<br/>`your_second_authorization` | `[]`                  | 你自己为使用多账号轮询 Tokens 设置的授权码，英文逗号分隔                             |
|      | AUTH_KEY          | `your_auth_key`                                             | `None`                | 私人网关需要加`auth_key`请求头才设置该项                                    |
| 请求相关 | CHATGPT_BASE_URL  | `https://chatgpt.com`                                       | `https://chatgpt.com` | ChatGPT 网关地址，设置后会改变请求的网站，多个网关用逗号分隔                           |
|      | PROXY_URL         | `http://ip:port`,<br/>`http://username:password@ip:port`    | `[]`                  | 全局代理 URL，出 403 时启用，多个代理用逗号分隔                                 |
|      | EXPORT_PROXY_URL  | `http://ip:port`或<br/>`http://username:password@ip:port`    | `None`                | 出口代理 URL，防止请求图片和文件时泄漏源站 ip                                   |
| 功能相关 | HISTORY_DISABLED  | `true`                                                      | `true`                | 是否不保存聊天记录并返回 conversation_id                                 |
|      | POW_DIFFICULTY    | `00003a`                                                    | `00003a`              | 要解决的工作量证明难度，不懂别设置                                            |
|      | RETRY_TIMES       | `3`                                                         | `3`                   | 出错重试次数，使用 `AUTHORIZATION` 会自动随机/轮询下一个账号                      |
|      | CONVERSATION_ONLY | `false`                                                     | `false`               | 是否直接使用对话接口，如果你用的网关支持自动解决 `POW` 才启用                           |
|      | ENABLE_LIMIT      | `true`                                                      | `true`                | 开启后不尝试突破官方次数限制，尽可能防止封号                                       |
|      | UPLOAD_BY_URL     | `false`                                                     | `false`               | 开启后按照 `URL+空格+正文` 进行对话，自动解析 URL 内容并上传，多个 URL 用空格分隔           |
|      | SCHEDULED_REFRESH | `false`                                                     | `false`               | 是否定时刷新 `AccessToken` ，开启后每次启动程序将会全部非强制刷新一次，每4天晚上3点全部强制刷新一次。  |
|      | RANDOM_TOKEN      | `true`                                                      | `true`                | 是否随机选取后台 `Token` ，开启后随机后台账号，关闭后为顺序轮询                         |
| 网关功能 | ENABLE_GATEWAY    | `false`                                                     | `false`               | 是否启用网关模式，开启后可以使用镜像站，但也将会不设防                                  |
|      | AUTO_SEED          | `false`                                                     | `true`               | 是否启用随机账号模式，默认启用，输入`seed`后随机匹配后台`Token`。关闭之后需要手动对接接口，来进行`Token`管控。    |

## 部署

### Zeabur 部署

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/6HEGIZ?referralCode=LanQian528)

### 直接部署

```bash
git clone https://github.com/LanQian528/chat2api
cd chat2api
pip install -r requirements.txt
python app.py
```

### Docker 部署

您需要安装 Docker 和 Docker Compose。

```bash
docker run -d \
  --name chat2api \
  -p 5005:5005 \
  lanqian528/chat2api:latest
```

### (推荐，可用 PLUS 账号) Docker Compose 部署

创建一个新的目录，例如 chat2api，并进入该目录：

```bash
mkdir chat2api
cd chat2api
```

在此目录中下载库中的 docker-compose.yml 文件：

```bash
wget https://raw.githubusercontent.com/LanQian528/chat2api/main/docker-compose-warp.yml
```

修改 docker-compose-warp.yml 文件中的环境变量，保存后：

```bash
docker-compose up -d
```


## 常见问题

> - 错误代码：
>   - `401`：当前 IP 不支持免登录，请尝试更换 IP 地址，或者在环境变量 `PROXY_URL` 中设置代理，或者你的身份验证失败。
>   - `403`：请在日志中查看具体报错信息。
>   - `429`：当前 IP 请求1小时内请求超过限制，请稍后再试，或更换 IP。
>   - `500`：服务器内部错误，请求失败。
>   - `502`：服务器网关错误，或网络不可用，请尝试更换网络环境。

> - 已知情况：
>   - 日本 IP 很多不支持免登，免登 GPT-3.5 建议使用美国 IP。
>   - 99%的账号都支持免费 `GPT-4o` ，但根据 IP 地区开启，目前日本和新加坡 IP 已知开启概率较大。

> - 环境变量 `AUTHORIZATION` 是什么？
>   - 是一个自己给 chat2api 设置的一个身份验证，设置后才可使用已保存的 Tokens 轮询，请求时当作 `APIKEY` 传入。
> - AccessToken 如何获取？
>   - chatgpt官网登录后，再打开 [https://chatgpt.com/api/auth/session](https://chatgpt.com/api/auth/session) 获取 `accessToken` 这个值。


## License

MIT License
