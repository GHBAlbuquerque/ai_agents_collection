from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field

class CharacterLoreCreationRequest(BaseModel):
    character_name: Optional[str] = Field(default=None, description="Character Name (Optional)")
    character_class: str = Field(..., description="Character Class (Required)")
    gender: str = Field(..., description="Gender (Required)")
    birth_location: Optional[str] = Field(default=None, description="Birth Location (Optional)")
    character_age: Optional[int] = Field(default=None, description="Character Age (Optional)")
    character_alignment: Optional[str] = Field(default=None, description="Character Alignment (Optional)")
    description: Optional[str] = Field(default=None, description="Brief Description (Optional)")


class CharacterLoreCreationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(default="", description="Character Name")
    character_class: str = Field(default="", alias="class", description="Character Class")
    gender: str = Field(default="", description="Gender")
    place_of_birth: str = Field(default="", description="Place of Birth")
    role: str = Field(default="", description="Character Role")
    description: str = Field(default="", description="Detailed Description")
    act_1: str = Field(default="", description="Act I Lore")
    act_2: str = Field(default="", description="Act II Lore")
    act_3: str = Field(default="", description="Act III Lore")
    act_4: str = Field(default="", description="Act IV Lore")
    metadata: str = Field(default="", description="Metadata")

    def get(self, key: str, default: Any = "") -> Any:
        if key == "class":
            return self.character_class
        return getattr(self, key, default)

    def __getitem__(self, key: str) -> Any:
        if key == "class":
            return self.character_class
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)