
import os

file_path = 'chatgpt/ChatService.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_method = """
    async def get_conversation(self, conversation_id):
        url = f'{self.base_url}/conversation/{conversation_id}'
        headers = self.base_headers.copy()
        try:
            r = await self.s.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                return r.json()
            else:
                return None
        except Exception:
            return None
"""

if "def get_conversation(self, conversation_id):" not in content:
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(new_method)
    print("Successfully appended get_conversation method")
else:
    print("Method already exists")
