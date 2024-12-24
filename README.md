# Flask ChatBot 
用 Flask 串接 Open AI 的 Assistant API，實作一個自己的聊天機器人，並使用 PostgreSQL 來儲存聊天紀錄。
## 頁面介紹
* **登入頁面**
  
   一個簡單的登入頁面，使用者輸入名稱即可登入。再次造訪時輸入相同的名稱即可接續先前的聊天
  
* **聊天頁面**

   主要聊天的頁面，使用者可以用打字或是使用語音錄製的方式送出訊息，不論何種方式皆會將訊息顯示在視窗上，略等片刻就可以得到模型的回覆


## 使用介紹
1. 下載專案及安裝package
2. 到OpenAI的網站申請API_KEY
3. 安裝PostgreSQL，開好資料庫，並設定使用者密碼
4. 將必要的資訊(API_KEY,SECRET_KEY等)儲存在.env檔裡面，程式才能正常讀取

下方有功能展示的YT影片
https://youtu.be/7E9tVvf4nyM


