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
    co.incognito()  # 匿名模式
    co.headless()  # 無頭模式
    co.set_argument('--no-sandbox')  # 無沙盒模式
    co.auto_port()

# 有GUI
page = ChromiumPage()
# 沒有GUI
page = ChromiumPage(co)
# 跳轉到登錄頁面
page.get('https://cart.books.com.tw/member/login?loc=customer_003&url=https%3A%2F%2Fwww.books.com.tw%2F')
print('username'+username)
print('password'+password)
# 輸入用戶名和密碼
page.ele('#login_id').input("")
page.ele('#login_pswd').input("")
# 輸入用戶名和密碼
page.ele('#login_id').input(username)
page.ele('#login_pswd').input(password)
# 檢查驗證碼圖片是否存在
captcha_div = page.ele('#captcha_img')
# for i in range(10):
if captcha_div:
    captcha_img = captcha_div.ele('tag:img')
    if captcha_img:
        img_bytes = captcha_img.src()
        ocr = ddddocr.DdddOcr(show_ad=False)
        yzm = ocr.classification(img_bytes)
        # result = pytesseract.image_to_string(img_bytes)

        print('驗證碼'+yzm)
        page.ele('#captcha').input(yzm)
        # logout_button = page.ele('x://button[@class="button04" and contains(., "登入")]').click()

    else:
        print('驗證碼圖片未找到')
else:
    print('驗證碼容器未找到')
# books_login
# captcha_warn