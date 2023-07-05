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
    intake_permit?: number;
    offtake_permit?: number;
    translocation_destination?: string;
    note?: string;
}

export interface UploadSpeciesDetailInterface {
    taxon_id: number;
    taxon_name?: string;
    common_name?: string;
    year: number;
    property_id: number;
    month: number;
    month_name?: string;
    annual_population: AnnualPopulationInterface;
    intake_population: AnnualPopulationPerActivityInterface;
    offtake_population: AnnualPopulationPerActivityInterface;
}


const getDefaultAnnualPopulation = ():AnnualPopulationInterface => {
    return {
        present: true,
        total: 0,
        adult_male: 0,
        adult_female: 0,
        sub_adult_male: 0,
        sub_adult_female: 0,
        juvenile_male: 0,
        juvenile_female: 0,
        group: 0,
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

const getDefaultAnnualPopulationPerActivity = ():AnnualPopulationPerActivityInterface => {
    return {
        activity_type_id: 0,
        total: 0,
        adult_male: 0,
        adult_female: 0,
        juvenile_male: 0,
        juvenile_female: 0,
        founder_population: false,
        reintroduction_source: '',
    }
}

export const getDefaultUploadSpeciesDetail = (propertyId: number):UploadSpeciesDetailInterface => {
    let _currentDate = new Date()
    return {
        taxon_id: 0,
        taxon_name: '',
        common_name: '',
        year: _currentDate.getFullYear(),
        month: _currentDate.getMonth() + 1,
        property_id: propertyId,
        annual_population: getDefaultAnnualPopulation(),
        intake_population: getDefaultAnnualPopulationPerActivity(),
        offtake_population: getDefaultAnnualPopulationPerActivity()
    }
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
