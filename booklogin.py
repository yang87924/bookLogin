import platform
from time import sleep
from DrissionPage import ChromiumPage, ChromiumOptions
from dotenv import load_dotenv
import os
import ddddocr
import pytesseract
from PIL import Image
# 從 .env 文件加載環境變量
load_dotenv()

# 從環境變量中獲取用戶名和密碼
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# 根據操作系統設置 Chromium 選項
if platform.system().lower() == "darwin":
    co = ChromiumOptions().set_paths(browser_path=r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
else:
    co = ChromiumOptions().set_paths(browser_path=r'/opt/google/chrome/google-chrome')  # Linux 系統路徑
    co.incognito(True)  # 匿名模式 //無痕模式
    co.headless(True)  # 無頭模式 //無GUI
    co.set_argument('--no-sandbox')  # 無沙盒模式
    co.auto_port()
 
# 有GUI
page = ChromiumPage()
# 沒有GUI
# page = ChromiumPage(co)
# 跳轉到登錄頁面
page.get('https://web.pcc.gov.tw/pis/')
# 等待頁面加載完成
page.wait.load_start()

print('username'+username)
print('password'+password)
# 輸入用戶名和密碼
page.ele('#orgUserId').input("123456")
page.ele('#orgPassword').input("654321")

# sleep(1000)  # 等待 1 秒後重試
# # 輸入用戶名和密碼
# page.ele('#login_id').input(username)
# page.ele('#login_pswd').input(password)
# # 檢查驗證碼圖片是否存在
captcha_div = page.ele('.imgVerify')
imgs = captcha_div.ele('#commonUtil_imgVerify_imgDiv')
# for i in range(10):
if imgs:
    captcha_img = imgs.ele('#orgImageVerification')
    if captcha_img:
        img_bytes = captcha_img.src()
        ocr = ddddocr.DdddOcr(show_ad=False)
        yzm = ocr.classification(img_bytes)
        page.ele('#orgImageVerifyCode').input(yzm)
        print('驗證碼'+yzm)
        # logout_button = page.ele('x://button[@class="button04" and contains(., "登入")]').click()
    else:
        print('驗證碼圖片未找到')
else:
    print('驗證碼容器未找到')
sleep(1000)  # 等待 1 秒後重試


# <div class="imgVerify" style="display: inline-flex;align-items: center">
# 				<div style="max-width:100px;width:85px;height: 40px; color: red; display: inline-flex;align-items: center;justify-content: center;margin-right:10px;" id="commonUtil_imgVerify_imgDiv">
# 					<img alt="驗證碼文字圖片" style="max-width:85px" id="orgImageVerification" name="orgImageVerification" src="https://web.pcc.gov.tw/ccs/img?token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ3cnUwU0h5cVl5NkhqWEFveXNySFhodXRKeUtsVHlBeiIsImV4cCI6MTcyNDU5NzEzM30.rp1XHOzWRDMfpSPSZLP87InX2d28zcjOOnbIjVfQmAb8AeuYVkKfpMphX5musKngq1HnpxUlYZxiA4KAHAbJmQ">
# 				</div>
# 				<input type="text" class="form-control" size="4" maxlength="4" style="width:58px; display: inline-block; float: left; margin-left: 10px" id="orgImageVerifyCode" name="orgImageVerifyCode" aria-label="imageVerifyCode">
# 				<input type="hidden" id="imageVerifyToken" name="imageVerifyToken">						
# 				<div style="font-size:0px">
# 					<a href="#" style="line-height: inherit;display: inline-block;" id="reloadBut" onclick="event.preventDefault();">
# 						<img src="https://web.pcc.gov.tw/ccs/dist/assets/images/soundPlay/refresh.png" id="reloadButImg" alt="重新產生驗證碼" title="重新產生驗證碼" style="width:30px">					
# 					</a>
# 					<noscript>Script未啟用, 部分功能將無法使用</noscript> 
# 					<a href="#" style="line-height: inherit;display: inline-block;" id="playVoiceBut" onclick="event.preventDefault();">
# 						<img src="https://web.pcc.gov.tw/ccs/dist/assets/images/soundPlay/play.png" id="playVoiceButImg" alt="驗證碼語音播放" title="驗證碼語音播放" style="width:30px">						
# 					</a>
# 					<span id="commonUtil_imgVerify_soundSpan"></span>					
# 					<span id="commonUtil_imgVerify_message" class="red"> 
# 					</span>	
# 				</div>			
# 			</div>

# -----------------------------------
# <div class="imgVerify" style="display: inline-flex;align-items: center">
# 				<div style="max-width:100px;width:85px;height: 40px; color: red; display: inline-flex;align-items: center;justify-content: center;margin-right:10px;" id="commonUtil_imgVerify_imgDiv">
# 					<img alt="驗證碼文字圖片" style="max-width:85px" id="suppImageVerification" name="suppImageVerification" src="https://web.pcc.gov.tw/ccs/img?token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ3cnUwU0h5cVpTZE9TdDBFaTc4eVkvOG9lRVJZK011USIsImV4cCI6MTcyNDU5NzEzM30.ITkXycZ9Ct_0IJegY5Tl6ZS4KG-Umh_Zm9sIGtpuEmz2pqGz1hfr7p66TMOXz5VJzrjVTyuqcVONAINCa0zO5Q">
# 				</div>
# 				<input type="text" class="form-control" size="4" maxlength="4" style="width:58px; display: inline-block; float: left; margin-left: 10px" id="suppImageVerifyCode" name="suppImageVerifyCode" aria-label="imageVerifyCode">
# 				<input type="hidden" id="imageVerifyToken" name="imageVerifyToken">						
# 				<div style="font-size:0px">
# 					<a href="#" style="line-height: inherit;display: inline-block;" id="reloadBut" onclick="event.preventDefault();">
# 						<img src="https://web.pcc.gov.tw/ccs/dist/assets/images/soundPlay/refresh.png" id="reloadButImg" alt="重新產生驗證碼" title="重新產生驗證碼" style="width:30px">					
# 					</a>
# 					<noscript>Script未啟用, 部分功能將無法使用</noscript> 
# 					<a href="#" style="line-height: inherit;display: inline-block;" id="playVoiceBut" onclick="event.preventDefault();">
# 						<img src="https://web.pcc.gov.tw/ccs/dist/assets/images/soundPlay/play.png" id="playVoiceButImg" alt="驗證碼語音播放" title="驗證碼語音播放" style="width:30px">						
# 					</a>
# 					<span id="commonUtil_imgVerify_soundSpan"></span>					
# 					<span id="commonUtil_imgVerify_message" class="red"> 
# 					</span>	
# 				</div>			
# 			</div>