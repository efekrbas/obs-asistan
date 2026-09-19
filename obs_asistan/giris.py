"""
Selenium ile OBS'ye giriş ve çerez kaydetme
"""

import os
import pickle
import time
import getpass
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class OBSGiris:
    """OBS'ye Selenium ile giriş yapan sınıf"""

    def __init__(self, obs_url=None, cookie_file="obs_cookies.pkl"):
        self.obs_url = obs_url or "https://obs.bilecik.edu.tr/"
        self.cookie_file = cookie_file

    def interaktif_giris(self):
        """Kullanıcıdan bilgileri alıp giriş yapar"""
        print(f"{Fore.CYAN}🔐 OBS Giriş{Style.RESET_ALL}\n")
        kullanici = input("Kullanıcı Adı: ").strip()
        sifre = getpass.getpass("Şifre: ")

        if not kullanici or not sifre:
            print(f"{Fore.RED}❌ Kullanıcı adı ve şifre gerekli!{Style.RESET_ALL}")
            return False

        return self.giris_yap(kullanici, sifre)

    def giris_yap(self, kullanici, sifre):
        """Selenium ile giriş yapar ve çerezleri kaydeder"""
        print(f"\n{Fore.YELLOW}🌐 Chrome başlatılıyor...{Style.RESET_ALL}")

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        try:
            print(f"{Fore.YELLOW}📡 OBS'ye bağlanılıyor...{Style.RESET_ALL}")
            driver.get(self.obs_url)

            wait = WebDriverWait(driver, 20)

            print(f"{Fore.YELLOW}✍️ Bilgiler giriliyor...{Style.RESET_ALL}")
            username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            username.send_keys(kullanici)

            password = driver.find_element(By.NAME, "password")
            password.send_keys(sifre)

            time.sleep(2)

            print(f"{Fore.YELLOW}🔓 Giriş yapılıyor...{Style.RESET_ALL}")
            login_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Giriş Yap']"))
            )
            login_btn.click()

            wait.until(EC.url_contains("ogrencianasayfa"))
            time.sleep(3)

            cookies = driver.get_cookies()
            with open(self.cookie_file, "wb") as f:
                pickle.dump(cookies, f)

            print(f"\n{Fore.GREEN}✅ Giriş başarılı!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ {len(cookies)} çerez kaydedildi.{Style.RESET_ALL}")
            return True

        except Exception as e:
            print(f"\n{Fore.RED}❌ Giriş başarısız: {e}{Style.RESET_ALL}")
            return False

        finally:
            driver.quit()
