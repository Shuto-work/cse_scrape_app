import secrets
cookie_key = secrets.token_hex(16)  # 32文字の16進数文字列
print(cookie_key)  # この値をconfig.yamlファイルにコピーします
