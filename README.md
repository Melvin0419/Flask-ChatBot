# Flask ChatBot 
用 Flask 架構伺服器，串接 Open AI 的 Assistant API 來實作一個即時聊天機器人，並使用 PostgreSQL 來儲存聊天紀錄。
## 頁面介紹
* **登入頁面**
  
   一個簡單的登入頁面，使用者輸入名稱即可登入。再次造訪時輸入相同的名稱即可接續先前的聊天
  
  <img src=https://github.com/user-attachments/assets/c8908bb3-4387-40f4-b354-298f3e6e3eca width="70%"/>

  
* **聊天頁面**

   主要聊天的頁面，使用者可以用打字或是使用語音錄製的方式送出訊息，不論何種方式皆會將訊息顯示在視窗上，略等片刻就可以得到模型的回覆

  <img src=https://github.com/user-attachments/assets/6efe4fe6-4c7e-466f-9e7a-b09532768226 width="70%"/>

  (2021/12/28)新增語句建議功能，滑鼠點擊自己送出的訊息，即可得到針對這則訊息的改正版本，模型會列出改正的地方以及修正的原因。
  
  <img src=https://github.com/user-attachments/assets/4847d569-3765-47bd-a15e-c0780836d1fc width="70%"/>

## 使用介紹
1. 下載整個專案並依照`requirements.txt`安裝package
2. 到 OpenAI 的網站申請 API_KEY
3. 安裝 PostgreSQL，開好資料庫，並設定使用者密碼
4. 將必要的資訊(`API_KEY`,`SECRET_KEY`等)儲存在`.env`裡面，程式才能正常讀取

功能展示的YT影片:
https://youtu.be/7E9tVvf4nyM


