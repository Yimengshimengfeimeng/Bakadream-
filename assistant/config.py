from pathlib import Path
from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings,SettingsConfigDict
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_WORKSPACE_DIR = PROJECT_ROOT / "sandbox"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = PROJECT_ROOT /".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
        case_sensitive = False
    )
    llm_base_url: str = ""
    llm_api_key: str = ""
    llm_model: str = ""
    llm_temperature: float = 0.0
    llm_timeout: float = 60.0
    #应用
    app_name: str = "Bakadream的小助手"
    data_dir: Path = DEFAULT_DATA_DIR
    workspace_dir: Path = DEFAULT_WORKSPACE_DIR
    @field_validator("llm_base_url")
    @classmethod
    def _normalize_base_url(cls,url: str) -> str:
        return url.strip().rstrip("/")
    @property
    def masked_api_key(self) -> str:
        key = self.llm_api_key.strip()
        if not key:
            return "未设置密钥"
        if len(key)<= 10:
            return key[0]+"*"*(len(key)-1)
        return f"{key[:6]}...{key[-4:]}"
    @property
    def masked_base_url(self) -> str:
        base_url = self.llm_base_url.strip()
        if not base_url:
            return "未设置供应商网址"
        return base_url[8:-3]
    def require_llm_config(self) -> str:
        key = self.llm_api_key.strip()
        base_url = self.llm_base_url.strip()
        model = self.llm_model.strip()
        if not key :
            raise RuntimeError(
                "LLM_API_KEY 未配置。\n"
                f"  1) 复制模板：Copy-Item .env.example .env   （在 {PROJECT_ROOT}）\n"
                "  2) 打开 .env 填入 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL"
            )
        if not base_url :
            raise RuntimeError(
                "LLM_BASE_URL 未配置。\n"
                f"  1) 复制模板：Copy-Item .env.example .env   （在 {PROJECT_ROOT}）\n"
                "  2) 打开 .env 填入 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL"
            )
        if base_url[:8] != "https://":
            raise RuntimeError(
                "LLM_BASE_URL 格式错误。\n"
                f"  1) 复制模板：Copy-Item .env.example .env   （在 {PROJECT_ROOT}）\n"
                "  2) 打开 .env 填入 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL"
            )
        if not model : 
            raise RuntimeError(
                "LLM_MODEL 未配置。\n"
                f"  1) 复制模板：Copy-Item .env.example .env   （在 {PROJECT_ROOT}）\n"
                "  2) 打开 .env 填入 LLM_API_KEY / LLM_BASE_URL / LLM_MODEL"
            )
        return key

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
