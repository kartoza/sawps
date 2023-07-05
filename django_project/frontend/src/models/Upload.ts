export enum UploadMode {
    None = 'none',
    SelectProperty = 'SelectProperty',
    CreateNew = 'CreateNew',
    PropertySelected = 'PropertySelected'
}

export interface UploadSpeciesDetailInterface {
    taxon_id: number;
    taxon_name?: string;
    common_name?: string;
    year: number;
    property_id: number;
    month: number;
}

export interface AnnualPopulationInterface {
    present: boolean;
    total: number;
    adult_male?: number;
    adult_female?: number;
    sub_adult_male?: number;
    sub_adult_female?: number;
    juvenile_male?: number;
    juvenile_female?: number;
    group?: number;
    open_close: boolean;
    area_available_to_species: number;
    count_method_id: number;
    count_method_name?: string;
    survey_method_id: number;
    survey_method_name?: string;
    sampling_effort: number;
    sampling_size_unit_id: number;
    sampling_size_unit_name?: string;
    area_covered: number;
    note?: string;
}


export interface AnnualPopulationPerActivityInterface {
    activity_type_id: number;
    activity_type_name?: string;
    total: number;
    adult_male?: number;
    adult_female?: number;
    juvenile_male?: number;
    juvenile_female?: number;
    founder_population?: boolean;
    reintroduction_source?: string;
    intake_permit?: number;
    offtake_permit?: number;
    translocation_destinataion?: string;
    note?: string;
}
