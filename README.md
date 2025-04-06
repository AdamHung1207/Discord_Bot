2025/04/06更新。

不一定會放上來，有點懶。

在經過一整天的努力，再把cogs給瘦身，拆分成cogs只接收指令，service是負責做邏輯運算。

main.py也拆分成config.py以及utils.py，也稍微瘦身一下，如下圖。

![image](https://github.com/user-attachments/assets/1ccceadb-fdb8-4a20-8771-d52ea37a3f11)

現在的終端機畫面輸出如下。

![image](https://github.com/user-attachments/assets/9e91a66e-361e-4658-a86f-dfcdaa079117)

=================我是分隔線=================

2025/04/05更新。

差別在main.py分出config.py及utils.py，把main.py再瘦身一點。

為了方便自己重灌，也生成了目前需要的套件快速安裝清單，requirements.txt，這下載後用cmd到指定的資料夾後執行即可。

另外也把塔羅牌的倒數功能給加上去了。

![image](https://github.com/user-attachments/assets/bb4c6be8-5e50-47b5-bb7d-550aff6dc5b9)

=================我是分隔線=================

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

會這麼做的原因主要是，原本是把token跟owner id都寫在main.py裡，但每次貼給AI就會說這很機密，然後就自動幫你碼掉。

為了省事，不要在自己複製貼上，就依照AI提示弄了一個.env來存放，這.env也可以用來存放API，我之前有加前FinMine API，就是台股的。

但功能一直做不起來就先放棄了，目前這個待AI幫我寫出來後我再看要不要更新上來。

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

#🍀 今日運勢

再來是我每天都會玩一下的/運勢。

一樣，有加入倒數效果，放在lucky_countdown.json下，想要更多請AI幫忙生成。

![image](https://github.com/user-attachments/assets/01eb05b5-ceda-42b7-bdb4-b99b49d463b7)

然後倒數完出來的效果就是這樣。

![image](https://github.com/user-attachments/assets/fa31bc22-36c6-4cf1-b86d-080353a0e5f8)

首先，有在lucky_cogs.py上，固定每個ID在每一天，在台灣時間晚上11:59前怎麼測，都是一樣的輸出結果，

我設定了有"大吉", "中吉", "小吉", "吉", "半吉", "末吉", "末小吉","凶", "小凶", "半凶", "末凶", "大凶"這些運勢，會佔98%的機率出現。

另外還有"超吉","吉娃娃"，各佔1%，為特殊彩蛋。

幸運數字我就設定只有0~9，你要是開心可以把9改成10000000000000000000000000都不是問題，前提你想要？

再來解說.json吧。

lucky_Anime.json，是用來做結尾，來一句動漫的經典台詞。

lucky_color.json，是用來抽幸運顏色。

lucky_fortunes.json，是用來抽上面說的各種運勢，然後運勢後面會有小說明。

lucky_suggestions.json，是用來給小建議的，讓各位即使抽到大凶也能逢凶化吉，如果真的有用的話？

一樣都可以請AI幫忙生成，不用太擔心！一個AI生成不夠好，別忘了還有好多個AI。

=================我是分隔線=================

#🖼️ 圖片統整 

/查圖這個功能主要是用來對應/哲哲。

因為zhezhe_cogs.py有23張圖片，但快捷顯示只有10張，為了讓自己知道並清楚有上傳什麼哲哲金句，所以就做了一個查圖，會顯示目前對應/哲哲的關鍵字。

![image](https://github.com/user-attachments/assets/fb93530e-f0b5-4592-9fca-8809ba47dac9)

=================我是分隔線=================

#🔄 手動同步

就AI寫在裡面的，然後我就把他獨立出來做成cogs，以節省main.py的空間。

這部份功能用的機率不高，就沒什麼做美化了。

![image](https://github.com/user-attachments/assets/b68cc793-dc4c-4e2b-87da-e7ff9c20de02)

=================我是分隔線=================

#🎴 塔羅牌

為了這個我也是搞了超久的.json，但因為牽扯到我的圖床，所以我只能提供範本，你們再自己玩吧。

目前還只有抽單張的功能，所以就自己心裡想一個問題，然後送出去，看這張牌的解釋是什麼吧。

取名邏輯也很簡單，就是tarot.big/small.json。

為什麼有二個，因為塔羅牌就分大/小阿爾克那，我就照著分出來，未來可能打算進化升級這一塊，但目前還沒有想法，所以就先這樣，停在這裡不動工了。

參考下圖，會有中英文卡名，正逆位的單詞和解釋，以及附上基本牌義，真有想建立的網路上有資料都可以搜得到，再不行請AI幫你生成都很簡單。

![image](https://github.com/user-attachments/assets/0ac52b9b-14dc-4833-98eb-1b528ccfa719)

=================我是分隔線=================

#😂 哲哲梗圖

這個就是學MYGO BOT來的。

可以發送哲哲金句，玩法差不多類似。

可以有關鍵字查詢。

![image](https://github.com/user-attachments/assets/e2c58088-c01a-430f-8968-bfacdedca15d)

選擇後就變成。

![image](https://github.com/user-attachments/assets/2e22fe0f-92a4-4553-9b9f-d107843b2d04)

所以才有搭配上面的查圖，可以用來知道目前有什麼圖片，不喜歡的就改一下就可以變其它梗圖了。

更早期還有結合梗圖倉庫隨機發送，但發現一般般就拔掉，才自己做這個出來了。

=================我是分隔線=================

會不會再更新未知中！！！！！
