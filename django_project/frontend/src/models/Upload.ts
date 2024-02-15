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
    adult_total?: number;
    sub_adult_total?: number;
    juvenile_total?: number;
    group?: number;
    area_available_to_species: number;
    survey_method_id: number;
    survey_method_name?: string;
    note?: string;
    population_estimate_certainty: number;
    upper_confidence_level?: number;
    lower_confidence_level?: number;
    certainty_of_bounds?: number;
    sampling_effort_coverage_id?: number;
    sampling_effort_coverage_name?: string;
    population_status_id?: number;
    population_status_name?: string;
    population_estimate_category_id: number;
    population_estimate_category_name?: string;
    population_estimate_category_other?: string;
    survey_method_other?: string;
    population_estimate_certainty_name?: string;
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
    id?: number;
    taxon_id: number;
    taxon_name?: string;
    common_name?: string;
    year: number;
    property_id: number;
    month_name?: string;
    annual_population: AnnualPopulationInterface;
    intake_populations: AnnualPopulationPerActivityInterface[];
    offtake_populations: AnnualPopulationPerActivityInterface[];
    confirm_overwrite?: boolean;
}

export interface TaxonMetadata {
    id: number;
    common_name_verbatim: string;
    scientific_name: string
}

export interface CommonUploadMetadata {
    id: number;
    name: string;
}

export interface AnnualPopulationValidation {
    area_available_to_species?: boolean;
    survey_method_id?: boolean;
    population_estimate_certainty?: boolean;
    population_estimate_category_id?: boolean;
    population_estimate_category_other?: boolean;
    survey_method_other?: boolean;
}

export interface AnnualPopulationPerActivityValidation {
    activity_type_id?: boolean;
    permit?: boolean;
    reintroduction_source?: boolean;
    translocation_destination?: boolean;
}

export interface AnnualPopulationPerActivityErrorMessage {
    activity_type_id?: string;
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
        adult_male: 0,
        adult_female: 0,
        sub_adult_male: 0,
        sub_adult_female: 0,
        juvenile_male: 0,
        juvenile_female: 0,
        adult_total: 0,
        sub_adult_total: 0,
        juvenile_total: 0,
        area_available_to_species: 0,
        survey_method_id: 0,
        note: '',
        population_estimate_certainty: 0,
        population_estimate_category_id: 0,
        population_estimate_certainty_name: '',
        survey_method_other: ''
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

const copyAnnualPopulation = (data: AnnualPopulationInterface):AnnualPopulationInterface => {
    // replace null with 0 or empty string
    return {
        present: data.present,
        total: data.total,
        adult_male: data.adult_male != null ? data.adult_male : 0,
        adult_female: data.adult_female != null ? data.adult_female : 0,
        sub_adult_male: data.sub_adult_male != null ? data.sub_adult_male : 0,
        sub_adult_female: data.sub_adult_female != null ? data.sub_adult_female : 0,
        juvenile_male: data.juvenile_male != null ? data.juvenile_male : 0,
        juvenile_female: data.juvenile_female != null ? data.juvenile_female : 0,
        adult_total: data.adult_total != null ? data.adult_total : 0,
        sub_adult_total: data.sub_adult_total != null ? data.sub_adult_total : 0,
        juvenile_total: data.juvenile_total != null ? data.juvenile_total : 0,
        area_available_to_species: data.area_available_to_species,
        survey_method_id: data.survey_method_id != null ? data.survey_method_id : 0,
        survey_method_name: data.survey_method_name != null ? data.survey_method_name : '',
        survey_method_other: data.survey_method_other != null ? data.survey_method_other : '',
        note: data.note != null ? data.note : '',
        population_estimate_certainty: data.population_estimate_certainty != null ? data.population_estimate_certainty : 0,
        population_estimate_certainty_name: data.population_estimate_category_name != null ? data.population_estimate_category_name : '',
        population_estimate_category_id: data.population_estimate_category_id != null ? data.population_estimate_category_id : 0,
        population_estimate_category_name: data.population_estimate_category_name != null ? data.population_estimate_category_name : '',
        population_estimate_category_other: data.population_estimate_category_other != null ? data.population_estimate_category_other : '',
        sampling_effort_coverage_id: data.sampling_effort_coverage_id != null ? data.sampling_effort_coverage_id : 0,
        sampling_effort_coverage_name: data.sampling_effort_coverage_name != null ? data.sampling_effort_coverage_name : '',
        population_status_id: data.population_status_id != null ? data.population_status_id : 0,
        population_status_name: data.population_status_name != null ? data.population_status_name : '',
        certainty_of_bounds: data.certainty_of_bounds,
        upper_confidence_level: data.upper_confidence_level,
        lower_confidence_level: data.lower_confidence_level,
        group: data.group
    }
}

const copyActivityPopulation = (dataList: AnnualPopulationPerActivityInterface[]):AnnualPopulationPerActivityInterface[] => {
    let _results:AnnualPopulationPerActivityInterface[] = []
    dataList.forEach((data) => {
        _results.push({
            id: data.id,
            activity_type_id: data.activity_type_id,
            activity_type_name: data.activity_type_name,
            adult_male: data.adult_male != null ? data.adult_male : 0,
            adult_female: data.adult_female != null ? data.adult_female : 0,
            juvenile_male: data.juvenile_male != null ? data.juvenile_male : 0,
            juvenile_female: data.juvenile_female != null ? data.juvenile_female : 0,
            total: data.total,
            founder_population: data.founder_population != null ? data.founder_population : false,
            reintroduction_source: data.reintroduction_source != null ? data.reintroduction_source : '',
            translocation_destination: data.translocation_destination != null ? data.translocation_destination : '',
            note: data.note != null ? data.note : '',
            permit: data.permit != null ? data.permit : 0,
        })
    })
    return _results
}


export const getDefaultUploadSpeciesDetail = (propertyId: number, initialData?: UploadSpeciesDetailInterface):UploadSpeciesDetailInterface => {
    if (initialData) {
        let _cpData = {
            taxon_id: initialData.taxon_id,
            taxon_name: initialData.taxon_name,
            common_name: initialData.common_name,
            year: initialData.year,
            property_id: propertyId,
            annual_population: copyAnnualPopulation(initialData.annual_population),
            intake_populations: copyActivityPopulation(initialData.intake_populations),
            offtake_populations: copyActivityPopulation(initialData.offtake_populations),
            id: initialData.id
        }
        return _cpData
    }
    let _currentDate = new Date()
    return {
        taxon_id: 0,
        taxon_name: '',
        common_name: ' ',
        year: _currentDate.getFullYear(),
        property_id: propertyId,
        annual_population: getDefaultAnnualPopulation(),
        intake_populations: [],
        offtake_populations: [],
        id: 0
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


export const SUBPOPULATION_FIELD_MAP: { [key: string]: 'adult_total' | 'sub_adult_total' | 'juvenile_total' } = {
    'adult_male': 'adult_total',
    'adult_female': 'adult_total',
    'sub_adult_male': 'sub_adult_total',
    'sub_adult_female': 'sub_adult_total',
    'juvenile_male': 'juvenile_total',
    'juvenile_female': 'juvenile_total'
}

export const SUBPOPULATION_FIELD_KEYS: { [key: string]: string[] } = {
    'adult_total': ['adult_male', 'adult_female'],
    'sub_adult_total': ['sub_adult_male', 'sub_adult_female'],
    'juvenile_total': ['juvenile_male', 'juvenile_female']
}
