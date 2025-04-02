這是一個用來架設Discord Bot的程式，我自己也是用這個。

使用Discord裡的Slash，也就是用/取代一些像是!、#之類的，而且在對話框打上「/」會有彈出選單，看你的伺服器有幾個Bot有這功能就會有多少個，可參考下圖。

![image](https://github.com/user-attachments/assets/f41802e6-8760-4813-bb43-d8afeb9a0cab)

=================我是分隔線=================

根目錄下，會有二個資料夾及二個檔案。(目前啦)

main.py為主程式，會抓取.env裡的Token，去啟動Discord Bot。

以及認程式的主人id，可以執行 /同步，也就是更新指令的功能(意思在不關閉程式下更新程式後讓他同步)。

再來就是利用cogs去呼叫功能模組，如下。

![image](https://github.com/user-attachments/assets/b574b563-450c-4389-8288-e5b1997e0f02)

另外一個是.env，這個很重要，要把你Discord Bot的Token放在這裡。

還有架這隻Discord Bot的主人。

=================我是分隔線=================

再來介紹功能選項，之後還有可能會再新增，但不確定。

#Choose = 🎲 多選一

主要是用來給有選擇障礙的人使用，指令為/選擇

輸入會先有倒數3秒的特效，特效效果是放在choose_countdown.json上，可以自己找AI生成，貼給他後說不滿意請他更新一批，只要重複這個動作，大概你想要有上萬種倒數特效也不是問題，但你的.json可能會很肥？

![image](https://github.com/user-attachments/assets/2ebdb7ab-bbc3-4a5f-acd5-9c1ab05eabea)

選擇完的效果是這樣。

![image](https://github.com/user-attachments/assets/4530f56a-f962-4646-91b9-b296955c3857)

讓命運的齒輪轉動吧！ 上下的框是放在choose_countdown.json，跟上面一樣，貼幾個叫AI生成就好。

會有跑出你輸入要選擇的東西，也方便給自己看一下剛剛KEY了什麼選項。

結果出爐的下方是放在choose_answer.json下，這類的檔案都可以請AI無限生成，你開心的話。

另外說明一下，有各1%的機會，會中【全選】跟【全不選】的低機率，所以你在查看choose_answer.json時，會有三個message。

分別為1_percent_1 (全選)、1_percent_2 (全不選)、以及98_percent(選其一)。

這邊的.json我都只留五個選項給下載的用戶，你可以拿去餵給AI請他生成就好。

=================我是分隔線=================

#🧹 清理訊息

簡單來說，就是可以透過/清除 1~100，去刪除該頻道內的訊息。

![image](https://github.com/user-attachments/assets/aeeba670-53a0-4d13-a17e-234d131a7443)

雖然訊息只有發送指令的人才能看得到，但為了美觀，所以我一樣在完成後，有請AI幫我隨機送出刪除成功的話。

不過因為也不太常用這種功能，所以我就懶得做.json來存放，裡面就放了五個提醒，隨機抽一個這樣。

![image](https://github.com/user-attachments/assets/0a00a31d-35fc-493f-8a9c-5d3612743fb3)

如果你很常用，也希望有不一樣的效果，請跟AI說，我要把執行刪除訊息後的提示功能以.json來存放，並請他以這5個為範本去生成更多。

建議在這邊可以先跟AI說檔名，如果是我的會取名為clear_answer.json。

會這麼取名只是因為想讓以後對檔案的時候方便可以跟cogs對。

=================我是分隔線=================



