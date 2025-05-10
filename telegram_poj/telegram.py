import asyncio
from telethon import TelegramClient, events,utils,types
import requests
from telethon.hints import TotalList

# Telegram API 配置
api_id = 29909382             # 替换为你的 API ID
api_hash = 'b14527b65c5c2ebe2054ff14573b18c5'  # 替换为你的 API Hash

# 监听的群组 ID 或 @用户名
target_chat = '@SHANGHAIXIAOGAODUAN'  # 例如 -1001234567890 或 'mygroupname'

# 关键词设置（忽略大小写）
KEYWORDS = ['优惠', '秒杀', '开源', '招聘','PP']

# 你的服务器接口地址
MY_SERVER_URL = 'https://v.codelin.vip/api'


# 转发到你自己的服务器
def send_to_server(msg):
    # print(f"转发到服务器：{msg}")
    # r = requests.post(MY_SERVER_URL, json={'msg': msg})
    # print(f"转发到服务器：{r.status_code}")
    with open("history.txt","a+",encoding="utf-8") as f:
        f.write(msg)

# 创建 Telegram 客户端i
client = TelegramClient('telegram_assit', api_id, api_hash,proxy=(("socks5", '127.0.0.1', 7890)))

async def get_history(limit=100):  # 默认获取最近 100 条消息
    try:
        entity = await client.get_entity(target_chat)  # 获取群组实体
        messages:TotalList = await client.get_messages(entity, limit=limit)
        for message in messages:
            message:types.Message
            message_content = ""
            if message.text:
                message_content += message.text
            if message.media:
                try:
                    if isinstance(message.media, types.MessageMediaPhoto):
                        # 获取图片链接
                        photo_url = utils.get_input_photo(message.media)
                        message_content += f"\n[图片] {photo_url}"
                    elif isinstance(message.media, types.MessageMediaDocument):
                        # 获取文件链接 (适用于视频, GIF 等)
                        file_url = utils.get_input_document(message.media.document)
                        message_content += f"\n[文件] {file_url}"
                    else:
                        message_content += f"\n[多媒体] 未知类型：{type(message.media)}"
                except Exception as e:
                    print(f"获取多媒体链接失败: {e}")
                    message_content += f"\n[多媒体] (获取链接失败: {e})"

            if message_content and any(keyword.lower() in message_content.lower() for keyword in KEYWORDS):
                print(f"匹配到历史消息：{message_content[:50]}...")
                send_to_server(message_content)
    except Exception as e:
        print(f"获取历史消息时出错：{e}")


@client.on(events.NewMessage(chats=target_chat))
async def handler(event):
    message_content = ""
    if event.message.text:
        message_content += event.message.text
    if event.message.media:
        try:
            if isinstance(event.message.media, types.MessageMediaPhoto):
                # 获取图片链接
                photo_url = utils.get_input_photo(event.message.media)
                message_content += f"\n[图片] {photo_url}"
            elif isinstance(event.message.media, types.MessageMediaDocument):
                # 获取文件链接 (适用于视频, GIF 等)
                file_url = utils.get_input_document(event.message.media.document)
                message_content += f"\n[文件] {file_url}"
            else:
                message_content += "\n[多媒体] (无法获取链接)"
        except Exception as e:
            print(f"获取多媒体链接失败: {e}")
            message_content += f"\n[多媒体] (获取链接失败: {e})"

    if message_content and any(keyword.lower() in message_content.lower() for keyword in KEYWORDS):
        print(f"匹配到关键词消息：{message_content[:50]}...")
        send_to_server(message_content)

async def main():
    await client.start()
    print("监听中... Ctrl+C 可退出")
    await get_history()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
    # s = socks.socksocket()
    # s.set_proxy(socks.SOCKS5, "127.0.0.1", 7890)  # 改成你本地代理
    # try:
    #     s.connect(("149.154.167.50", 443))  # Telegram 的一个官方 IP
    #     print("✅ 代理可用，连接成功")
    # except Exception as e:
    #     print("❌ 代理不可用:", e)