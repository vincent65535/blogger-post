# Blogger Post

CLI tool to publish Markdown/HTML posts to Blogger via Google API.

## 前置需求

- Python 3.8+
- Google Blogger API 憑證 (`credentials.json`)

## 安裝

安裝後可直接使用 `blogger-post` 指令。

### 直接執行

```bash
pip install -r requirements.txt
python main.py ...
```

## OAuth2 設定

1. 前往 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. 啟用 Blogger API
3. 建立 OAuth2 用戶端憑證 → 選擇「桌面應用程式」→ 下載 JSON
4. 將下載的檔案更名為 `credentials.json`，放在執行目錄

第一次執行會自動開啟瀏覽器進行 OAuth2 授權，完成後產生 `token.json`，之後不需重複授權。

## 使用方式

```bash
# 從 Markdown 檔案發布
blogger-post --file article.md
blogger-post --title "文章標題" --file article.md --blog-id YOUR_BLOG_ID

# 直接指定 HTML 內容
blogger-post --title "Hello" --content "<p>World</p>" --blog-id YOUR_BLOG_ID

# 存為草稿
blogger-post --title "Draft" --file post.md --blog-id YOUR_BLOG_ID --draft

# 加上標籤
blogger-post --title "Tech Post" --content "<p>content</p>" --blog-id YOUR_BLOG_ID --labels "python,blogger,api"

# 顯示版本
blogger-post --version
```

## Markdown 語法高亮

程式碼區塊會自動套用 Pygments 的 Monokai 暗色主題 CSS，內嵌在 HTML 中直接發布。

## 打包成獨立執行檔

### Windows

```cmd
pip install pyinstaller
pyinstaller --onefile --name blogger-post main.py
```

產出 `dist/blogger-post.exe`，將 `credentials.json` 放在同目錄即可執行。

### Linux

```bash
pip install pyinstaller
pyinstaller --onefile --name blogger-post main.py
```

產出 `dist/blogger-post`。

> 注意：打包後首次執行仍需要網路連線進行 OAuth2 授權。

## 專案結構

```
blogger_post/
├── main.py          # CLI 入口
├── oauth.py         # OAuth2 憑證管理
├── blogger.py       # Blogger API 封裝
├── md_utils.py      # Markdown 轉 HTML (含 syntax highlight CSS)
├── pyproject.toml   # 專案設定與 entry point
├── config.json      # BLOG ID 設定檔
└── requirements.txt # pip 依賴
```

## 依賴

- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- markdown
