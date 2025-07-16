from pydantic import BaseModel, Field
from typing import List


class AQIInputItem(BaseModel):
    NO2_Mean: float = Field(..., alias="NO2 Mean")
    O3_Mean: float = Field(..., alias="O3 Mean")
    SO2_Mean: float = Field(..., alias="SO2 Mean")
    CO_Mean: float = Field(..., alias="CO Mean")
    SO2_Mean_Imputed: float = Field(..., alias="SO2_Mean_Imputed")
    CO_Mean_Imputed: float = Field(..., alias="CO_Mean_Imputed")
    NO2_to_SO2: float
    CO_to_SO2: float
    O3_to_CO: float
    NO2_Mean_roll_3: float = Field(..., alias="NO2 Mean_roll_3")
    O3_Mean_roll_3: float = Field(..., alias="O3 Mean_roll_3")
    SO2_Mean_roll_3: float = Field(..., alias="SO2 Mean_roll_3")
    CO_Mean_roll_3: float = Field(..., alias="CO Mean_roll_3")
    year: int
    month: int
    is_weekend: int

    class Config:
        allow_population_by_field_name = True


class AQIRequest(BaseModel):
    data: List[AQIInputItem]
