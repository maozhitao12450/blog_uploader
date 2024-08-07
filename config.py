import json
import os

class Config:
    def __init__(self):
        # 读取config.json
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            
            self.UEESHOP_URL = config.get("UEESHOP_URL")
            if self.UEESHOP_URL is None or len(self.UEESHOP_URL) == 0:
                self.UEESHOP_URL = os.getenv("UEESHOP_URL")
            if self.UEESHOP_URL is None or len(self.UEESHOP_URL) == 0:
                raise Exception("UEESHOP_URL is not set")


            self.UEESHOP_LOGIN_USER = config.get("UEESHOP_LOGIN_USER")
            if self.UEESHOP_LOGIN_USER is None or len(self.UEESHOP_LOGIN_USER) == 0:
                self.UEESHOP_LOGIN_USER = os.getenv("UEESHOP_LOGIN_USER")
            if self.UEESHOP_LOGIN_USER is None or len(self.UEESHOP_LOGIN_USER) == 0:
                raise Exception("UEESHOP_LOGIN_USER is not set")


            self.UEESHOP_LOGIN_PASSWORD = config.get("UEESHOP_LOGIN_PASSWORD")
            if self.UEESHOP_LOGIN_PASSWORD is None or len(self.UEESHOP_LOGIN_PASSWORD) == 0:
                self.UEESHOP_LOGIN_PASSWORD = os.getenv("UEESHOP_LOGIN_PASSWORD")
            if self.UEESHOP_LOGIN_PASSWORD is None or len(self.UEESHOP_LOGIN_PASSWORD) == 0:
                raise Exception("UEESHOP_LOGIN_PASSWORD is not set")


            self.BLOG_GENERATE_API_KEY = config.get("BLOG_GENERATE_API_KEY")
            if self.BLOG_GENERATE_API_KEY is None or len(self.BLOG_GENERATE_API_KEY) == 0:
                self.BLOG_GENERATE_API_KEY = os.getenv("BLOG_GENERATE_API_KEY")
            if self.BLOG_GENERATE_API_KEY is None or len(self.BLOG_GENERATE_API_KEY) == 0:
                self.BLOG_GENERATE_API_KEY = "ollama"
            if self.BLOG_GENERATE_API_KEY is None or len(self.BLOG_GENERATE_API_KEY) == 0:
                raise Exception("BLOG_GENERATE_API_KEY is not set")
            self.BLOG_GENERATE_API_BASE = config.get("BLOG_GENERATE_API_BASE")
            if self.BLOG_GENERATE_API_BASE is None or len(self.BLOG_GENERATE_API_BASE) == 0:
                self.BLOG_GENERATE_API_BASE = os.getenv("BLOG_GENERATE_API_BASE")
            if self.BLOG_GENERATE_API_BASE is None or len(self.BLOG_GENERATE_API_BASE) == 0:
                self.BLOG_GENERATE_API_BASE = "http://localhost:11434/v1"
            if self.BLOG_GENERATE_API_BASE is None or len(self.BLOG_GENERATE_API_BASE) == 0:
                raise Exception("BLOG_GENERATE_API_BASE is not set")
            self.BLOG_GENERATE_API_MODEL = config.get("BLOG_GENERATE_API_MODEL")
            if self.BLOG_GENERATE_API_MODEL is None or len(self.BLOG_GENERATE_API_MODEL) == 0:
                self.BLOG_GENERATE_API_MODEL = os.getenv("BLOG_GENERATE_API_MODEL")
            if self.BLOG_GENERATE_API_MODEL is None or len(self.BLOG_GENERATE_API_MODEL) == 0:
                self.BLOG_GENERATE_API_MODEL = "gemma2:latest"
            if self.BLOG_GENERATE_API_MODEL is None or len(self.BLOG_GENERATE_API_MODEL) == 0:
                raise Exception("BLOG_GENERATE_API_MODEL is not set")
            
            self.SEO_GENERATE_API_KEY = config.get("SEO_GENERATE_API_KEY")
            if self.SEO_GENERATE_API_KEY is None or len(self.SEO_GENERATE_API_KEY) == 0:
                self.SEO_GENERATE_API_KEY = os.getenv("SEO_GENERATE_API_KEY")
            if self.SEO_GENERATE_API_KEY is None or len(self.SEO_GENERATE_API_KEY) == 0:
                self.SEO_GENERATE_API_KEY = "ollama"
            if self.SEO_GENERATE_API_KEY is None or len(self.SEO_GENERATE_API_KEY) == 0:
                raise Exception("SEO_GENERATE_API_KEY is not set")
            self.SEO_GENERATE_API_BASE = config.get("SEO_GENERATE_API_BASE")
            if self.SEO_GENERATE_API_BASE is None or len(self.SEO_GENERATE_API_BASE) == 0:
                self.SEO_GENERATE_API_BASE = os.getenv("SEO_GENERATE_API_BASE")
            if self.SEO_GENERATE_API_BASE is None or len(self.SEO_GENERATE_API_BASE) == 0:
                self.SEO_GENERATE_API_BASE = "http://localhost:11434/v1"
            if self.SEO_GENERATE_API_BASE is None or len(self.SEO_GENERATE_API_BASE) == 0:
                raise Exception("SEO_GENERATE_API_BASE is not set")
            self.SEO_GENERATE_API_MODEL = config.get("SEO_GENERATE_API_MODEL")
            if self.SEO_GENERATE_API_MODEL is None or len(self.SEO_GENERATE_API_MODEL) == 0:
                self.SEO_GENERATE_API_MODEL = os.getenv("SEO_GENERATE_API_MODEL")
            if self.SEO_GENERATE_API_MODEL is None or len(self.SEO_GENERATE_API_MODEL) == 0:
                self.SEO_GENERATE_API_MODEL = "gemma2:latest"
            if self.SEO_GENERATE_API_MODEL is None or len(self.SEO_GENERATE_API_MODEL) == 0:
                raise Exception("SEO_GENERATE_API_MODEL is not set")
          
if __name__ == "__main__":
    config = Config()
    print(json.dumps(config.__dict__, indent=4))

            