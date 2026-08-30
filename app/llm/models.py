from dataclasses import dataclass
from app.config.settings import Settings

@dataclass(frozen=True)
class GPTModelConfig:
    name: str
    reasoning_effort: str


def get_gpt_model_config(settings: Settings) -> GPTModelConfig:
    """ Build GPT configuration from application settings """
    return GPTModelConfig(
        name = settings.openai_model,
        reasoning_effort= settings.openai_reasoning_effort
    )