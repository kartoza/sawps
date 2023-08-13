export enum UploadMode {
    None = 'none',
    SelectProperty = 'SelectProperty',
    CreateNew = 'CreateNew',
    PropertySelected = 'PropertySelected'
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
    open_close_id: number;
    open_close_name?: string;
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
    permit?: number;
    translocation_destination?: string;
    note?: string;
    id?: number;
}

export interface UploadSpeciesDetailInterface {
    taxon_id: number;
    taxon_name?: string;
    common_name?: string;
    year: number;
    property_id: number;
    month_name?: string;
    annual_population: AnnualPopulationInterface;
    intake_populations: AnnualPopulationPerActivityInterface[];
    offtake_populations: AnnualPopulationPerActivityInterface[];
}

export interface TaxonMetadata {
    id: number;
    common_name_varbatim: string;
    scientific_name: string
}

export interface CommonUploadMetadata {
    id: number;
    name: string;
}

export interface AnnualPopulationValidation {
    open_close_id?: boolean;
    area_available_to_species?: boolean;
    count_method_id?: boolean;
    survey_method_id?: boolean;
    sampling_effort?: boolean;
    sampling_size_unit_id?: boolean;
    area_covered?: boolean;
}

export interface AnnualPopulationPerActivityValidation {
    activity_type_id?: boolean;
    permit?: boolean;
    reintroduction_source?: boolean;
    translocation_destination?: boolean;
}

export interface UploadSpeciesDetailValidation {
    taxon_id?: boolean;
    year?: boolean;
    annual_population?: AnnualPopulationValidation;
    intake_population?: AnnualPopulationPerActivityValidation;
    offtake_population?: AnnualPopulationPerActivityValidation;
}

/* Create Default Data Functions */
const getDefaultAnnualPopulation = ():AnnualPopulationInterface => {
    return {
        present: true,
        total: 0,
        open_close_id: 0,
        area_available_to_species: 0,
        count_method_id: 0,
        survey_method_id: 0,
        sampling_effort: 0,
        sampling_size_unit_id: 0,
        area_covered: 0,
        note: ''
    }
}

export const getDefaultAnnualPopulationPerActivity = ():AnnualPopulationPerActivityInterface => {
    return {
        activity_type_id: 0,
        adult_male: 0,
        adult_female: 0,
        juvenile_male: 0,
        juvenile_female: 0,
        total: 0,
        founder_population: false,
        reintroduction_source: '',
        translocation_destination: '',
        note: '',
        permit: 0,
        id: -1
    }
}

export const getDefaultUploadSpeciesDetail = (propertyId: number):UploadSpeciesDetailInterface => {
    let _currentDate = new Date()
    return {
        taxon_id: 0,
        taxon_name: '',
        common_name: ' ',
        year: _currentDate.getFullYear(),
        property_id: propertyId,
        annual_population: getDefaultAnnualPopulation(),
        intake_populations: [],
        offtake_populations: []
    }
}

export const FIELD_COUNTER = [
    'adult_male', 'adult_female',
    'sub_adult_male', 'sub_adult_female',
    'juvenile_male', 'juvenile_female'
]

export const OTHER_NUMBER_FIELDS = [
    'group', 'sampling_effort', 'area_available_to_species',
    'area_covered', 'permit'
]
