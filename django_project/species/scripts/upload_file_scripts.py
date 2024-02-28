PROPERTY = "Property_code"
SCIENTIFIC_NAME = "Scientific_name"
COMMON_NAME = "Common_name_verbatim"
OPEN_SYS = "open/closed_system"
PRESENCE = "presence/absence"
YEAR = "Year_of_estimate"
COUNT_TOTAL = "COUNT_TOTAL"
COUNT_ADULT_TOTAL = "COUNT_adult_TOTAL"
COUNT_ADULT_MALES = "Count_adult_males"
COUNT_ADULT_FEMALES = "Count_adult_females"
COUNT_SUBADULT_TOTAL = "COUNT_subadult_TOTAL"
COUNT_SUBADULT_MALE = "Count_subadult_male"
COUNT_SUBADULT_FEMALE = "Count_subadult_female"
COUNT_JUVENILE_TOTAL = "COUNT_Juvenile_TOTAL"
COUNT_JUVENILE_MALES = "Count_Juvenile_males"
COUNT_JUVENILE_FEMALES = "Count_Juvenile_females"
GROUP = "No. subpopulations / groups"
AREA = "Area_available_to_population_(total enclosure area)_ha"
POPULATION_STATUS = "Population_status"
POPULATION_ESTIMATE_CATEGORY = "Population_estimate_category"
IF_OTHER_POPULATION = "If_other_(population_estimate_category)_please explain"
SURVEY_METHOD = "Survey_method"
IF_OTHER_SURVEY = "If_other_(survey_method)_please explain"
SAMPLING_EFFORT = "Sampling_effort_coverage"
POPULATION_ESTIMATE_CERTAINTY = "Population_estimate_certainty"
UPPER = "Upper_confidence_limits_for_population_estimate"
LOWER = "Lower_confidence_limits_for_population_estimate"
CERTAINTY_OF_POPULATION = "Certainity_of_population_bounds"
INTRODUCTION_TOTAL = "(Re)Introduction_TOTAL"
INTRODUCTION_TOTAL_MALES = "(Re)Introduction_adult_males"
INTRODUCTION_TOTAL_FEMALES = "(Re)Introduction_adult_females"
INTRODUCTION_MALE_JUV = "(Re)Introduction_male_juveniles"
INTRODUCTION_FEMALE_JUV = "(Re)Introduction_female_juveniles"
FOUNDER_POPULATION = "Founder_population"
INTRODUCTION_SOURCE = "(Re)Introduction_source"
INTRODUCTION_PERMIT_NUMBER = "(Re)Introduction_permit_number"
OFFTAKE_TOTAL = "Offtake_TOTAL"
TRANS_OFFTAKE_TOTAL = "Translocation_(Offtake)_total"
TRANS_OFFTAKE_ADULTE_MALES = "Translocation_Offtake_adult_males"
TRANS_OFFTAKE_ADULTE_FEMALES = "Translocation_Offtake_adult_females"
TRANS_OFFTAKE_MALE_JUV = "Translocation_Offtake_male_juveniles"
TRANS_OFFTAKE_FEMALE_JUV = "Translocation_Offtake_female_juveniles"
TRANS_DESTINATION = "Translocation_destination"
TRANS_OFFTAKE_PERMIT_NUMBER = "Translocation_Offtake_Permit_number"
PLANNED_HUNT_TOTAL = "Planned_Hunt/Cull_TOTAL"
PLANNED_HUNT_OFFTAKE_ADULT_MALES = "Planned hunt/culling_Offtake_adult_males"
PLANNED_HUNT_OFFTAKE_ADULT_FAMALES = \
    "Planned hunt/culling_Offtake_adult_females"
PLANNED_HUNT_OFFTAKE_MALE_JUV = \
    "Planned hunt/culling_Offtake_male_juveniles"
PLANNED_HUNT_OFFTAKE_FEMALE_JUV = \
    "Planned hunt/culling_Offtake_female_juveniles"
PLANNED_HUNT_PERMIT_NUMBER = "Planned hunt/culling_Permit_number"
PLANNED_EUTH_TOTAL = "Planned euthanasia/DCA_TOTAL"
PLANNED_EUTH_OFFTAKE_ADULT_MALES = "Planned euthanasia_Offtake_adult_males"
PLANNED_EUTH_OFFTAKE_ADULT_FAMALES = "Planned euthanasia_Offtake_adult_females"
PLANNED_EUTH_OFFTAKE_MALE_JUV = "Planned euthanasia_Offtake_male_juveniles"
PLANNED_EUTH_OFFTAKE_FEMALE_JUV = "Planned euthanasia_Offtake_female_juveniles"
PLANNED_EUTH_PERMIT_NUMBER = "Planned euthanasia_Permit_number"
UNPLANNED_HUNT_TOTAL = "Unplanned/illegal hunting_TOTAL"
UNPLANNED_HUNT_OFFTAKE_ADULT_MALES = \
    "Unplanned/illegal hunting_Offtake_adult_males"
UNPLANNED_HUNT_OFFTAKE_ADULT_FAMALES = \
    "Unplanned/illegal hunting_Offtake_adult_females"
UNPLANNED_HUNT_OFFTAKE_MALE_JUV = \
    "Unplanned/illegal hunting_Offtake_male_juveniles"
UNPLANNED_HUNT_OFFTAKE_FEMALE_JUV = \
    "Unplanned/illegal hunting_Offtake_female_juveniles"

# ACTIVITY TYPES
ACTIVITY_TRANSLOCATION_INTAKE = 'Translocation (Intake)'
ACTIVITY_TRANSLOCATION_OFFTAKE = 'Translocation (Offtake)'
ACTIVITY_PLANNED_HUNT_CULL = 'Planned Hunt/Cull'
ACTIVITY_PLANNED_EUTH_DCA = 'Planned Euthanasia/DCA'
ACTIVITY_UNPLANNED_ILLEGAL_HUNTING = 'Unplanned/Illegal Hunting'

COMPULSORY_FIELDS = [
    PROPERTY,
    SCIENTIFIC_NAME,
    COMMON_NAME,
    OPEN_SYS,
    PRESENCE,
    YEAR,
    COUNT_TOTAL,
    AREA,
    POPULATION_ESTIMATE_CATEGORY,
    POPULATION_ESTIMATE_CERTAINTY,
]

SHEET_TITLE = "Dataset pilot"
IF_OTHER_POPULATION_VAL = "Other (please describe how the population " \
                          "size estimate was determined)"
IF_OTHER_SURVEY_VAL = "Other - please explain"

PRESENCE_VALUE_MAPPING = {
    'Present': True,
    'Absent': False
}
